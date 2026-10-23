import json
import re
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / 'docs/pufferfish-catalog.json').read_text(encoding='utf-8-sig'))
name_rows = json.loads((root / 'Languages/pufferfish.zh-CN.json').read_text(encoding='utf-8'))
text_rows = json.loads((root / 'Languages/pufferfish-text.zh-CN.json').read_text(encoding='utf-8'))
names = {(x['category'], x['name']) for x in name_rows}
texts = {(x['category'], x['name']) for x in text_rows}
compact_texts = {(category, re.sub(r'\s+', '', text)) for category, text in texts}
missing = []
for rows in (name_rows, text_rows):
    keys = [(x['category'], x['name']) for x in rows]
    if len(keys) != len(set(keys)):
        raise SystemExit('Duplicate Pufferfish dictionary keys')
for tool in catalog['tools'] + catalog.get('users', []):
    for key, collection in [(('Pufferfish', tool['name']), names), (('description', tool['description']), texts)]:
        if key not in collection:
            missing.append(key)
    for port in tool['inputs'] + tool['outputs']:
        if ('port-name', port['name']) not in names:
            missing.append(('port-name', port['name']))
        if ('port-description', port['description']) not in texts:
            missing.append(('port-description', port['description']))
for tool in catalog['failures']:
    if ('Pufferfish', tool['constructor'][0]) not in names:
        missing.append(('Pufferfish', tool['constructor'][0]))
    if ('description', tool['constructor'][2]) not in texts:
        missing.append(('description', tool['constructor'][2]))
for method in catalog['method_text']:
    for port in method.get('ports', []):
        if ('port-name', port['name']) not in names:
            missing.append(('port-name', port['name']))
        if ('port-description', re.sub(r'\s+', '', port['description'])) not in compact_texts:
            missing.append(('port-description', port['description']))
    if method['method'] == 'SolveInstance':
        for text in method['strings']:
            if ('runtime', text) not in texts:
                missing.append(('runtime', text))
report = {
    'assembly': catalog['assembly'],
    'version': catalog['version'],
    'extracted_components': len(catalog['tools']),
    'offline_instantiation_failures': catalog['failures'],
    'component_types': len(catalog['tools']) + len(catalog['failures']),
    'subd_user_objects': len(catalog.get('users', [])),
    'unique_translations': dict(Counter(x['category'] for x in name_rows + text_rows)),
    'missing': sorted(set(missing)),
    'scope': 'Static component and SubD user-object metadata plus IL text coverage; GUI behavior not verified'
}
(root / 'docs/pufferfish-coverage.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k not in {'offline_instantiation_failures', 'scope'}}, ensure_ascii=False))
if missing:
    raise SystemExit('Pufferfish translation coverage is incomplete')
