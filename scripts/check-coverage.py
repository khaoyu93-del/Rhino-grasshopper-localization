import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / 'docs/native-catalog.json').read_text(encoding='utf-8-sig'))
tools = catalog['tools']
names = {(r.get('category', ''), r['name']) for r in json.loads((root / 'Languages/zh-CN.json').read_text(encoding='utf-8'))}
texts = {(r.get('category', ''), r['name']) for r in json.loads((root / 'Languages/tool-text.zh-CN.json').read_text(encoding='utf-8'))}
missing_names = []
missing_descriptions = []
missing_port_names = []
missing_port_descriptions = []
for tool in tools:
    if (tool['category'], tool['name']) not in names and ('', tool['name']) not in names:
        missing_names.append({'guid': tool['guid'], 'name': tool['name'], 'category': tool['category'], 'assembly': tool['assembly']})
    if ('description', tool['description']) not in texts:
        missing_descriptions.append({'guid': tool['guid'], 'name': tool['name'], 'description': tool['description']})
    for direction in ('inputs', 'outputs'):
        for port in tool[direction]:
            if ('port-name', port['name']) not in names and ('', port['name']) not in names:
                missing_port_names.append({'guid': tool['guid'], 'direction': direction, 'name': port['name']})
            if ('port-description', port['description']) not in texts:
                missing_port_descriptions.append({'guid': tool['guid'], 'direction': direction, 'description': port['description']})

report = {
    'scope': 'Static Rhino SDK export; compare loaded native proxies inside Rhino for complete coverage',
    'sdk': catalog['sdk'],
    'extracted_tools': len(tools),
    'assemblies': dict(Counter(tool['assembly'] for tool in tools)),
    'export_failures': catalog['failures'],
    'assembly_failures': catalog.get('assembly_failures', []),
    'missing_tool_names': missing_names,
    'missing_tool_descriptions': missing_descriptions,
    'missing_port_names': missing_port_names,
    'missing_port_descriptions': missing_port_descriptions,
    'missing_unique_tool_descriptions': len({item['description'] for item in missing_descriptions}),
    'missing_unique_port_names': len({item['name'] for item in missing_port_names}),
    'missing_unique_port_descriptions': len({item['description'] for item in missing_port_descriptions}),
}
(root / 'docs/coverage.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({key: len(value) if isinstance(value, list) else value for key, value in report.items() if key != 'assemblies'}, ensure_ascii=False))
