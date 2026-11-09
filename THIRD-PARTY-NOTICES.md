# Third-party notices

MultilingualGH — Copyright (c) 2020 Victor Lin — MIT License.

Source: https://github.com/lin-ycv/MultilingualGH

The bundled Chinese dictionary is derived from upstream Languages/繁體中文.json. Script conversion uses the Windows LCMapStringEx Simplified Chinese conversion; duplicate keys retain the first upstream entry. Common terminology has local corrections. This is not a fully reviewed translation.

The GH_AssemblyPriority / CanvasCreated / MainMenuStrip loading pattern in src/Plugin.cs is adapted from upstream src/MultilingualGH/Menu.cs. The language entry schema and category-before-generic lookup are adapted from Translation.cs. Upstream annotation groups, drawing routines and dependencies are not shipped as binaries.

The upstream MIT license is included in LICENSE-MultilingualGH.txt in the distribution and upstream/LICENSE in the source tree. This license permits redistribution and modification subject to retaining its notice. Attribution metadata in the dictionary is retained.

Pufferfish 3.0 — Michael Pryor (ekimroyrp). The offline bundle includes the original `Pufferfish3-0.gha` and ten original WIP SubD user objects; these files are not modified. The distributor confirmed having authorization to redistribute these files in this bundle. That confirmation does not grant recipients any additional redistribution rights or place Pufferfish under the MultilingualGH MIT license. The author's installation notes are preserved as `Pufferfish/AUTHOR-NOTES.txt`.

Pufferfish Chinese dictionaries and runtime adapters are part of this localization project. No Rhino program files, Grasshopper SDK binaries, Eto binaries, or Raven binaries are redistributed. The installer compiles against the recipient's own Rhino 8 installation without network access. Existing project licensing restrictions still apply.

RichedGraphMapper — Daniel Gonzalez Abalde (DanielAbalde), source: https://github.com/DanielAbalde/RichedGraphMapper, GPL-3.0-or-later. This localization bundle supplies a separate display-text dictionary and a runtime UI adapter for an already installed RichedGraphMapper. It does not redistribute or incorporate the plugin's binary, graph algorithms, icons, or source code. The separate Rhino 8 adaptation and installer retain the original author's notice, GPL license, and corresponding source in their own repository: https://github.com/khaoyu93-del/Rhino-grasshopper-Riched-Graph-Mapper-NEW-8-. These projects' licenses are not interchangeable.
