# Grasshopper 简体中文界面 0.3.1 + 河豚 3.0 离线安装包

当前成果适用于 **Windows Rhino 8 / Grasshopper 1**。离线包包含汉化源码、五份词库、Pufferfish 3.0 原插件及 10 个 WIP SubD 用户对象；不包含 Rhino、Grasshopper SDK、Raven 或 RichedGraphMapper 插件本体。第五份词库为已安装的 RichedGraphMapper 提供定向中文显示适配。

## 下载与最简安装

- [0.3.1 独立映射器分类汉化更新包](downloads/GrasshopperChinese-0.3.1-Rhino8-Pufferfish3-RichedGraphMapper-tab-offline-setup.zip)
- [独立分类汉化包的 SHA-256 校验值](downloads/GrasshopperChinese-0.3.1-Rhino8-Pufferfish3-RichedGraphMapper-tab-offline-setup.zip.sha256)
- [此前 0.3.1 更新包（历史记录）](downloads/GrasshopperChinese-0.3.1-Rhino8-Pufferfish3-RichedGraphMapper-offline-setup.zip)
- [此前 Rich Graph Mapper 汉化整合包（历史记录）](downloads/GrasshopperChinese-Rhino8-Pufferfish3-RichedGraphMapper-offline-setup.zip)
- [此前四词库版本（历史记录）](downloads/GrasshopperChinese-Rhino8-Pufferfish3-offline-setup.zip)

1. 目标电脑先安装 Rhino 8 和 Windows .NET Framework 4.8 或更高版本。**不用联网、不用 Python、不用管理员权限。**
2. 保存工作，关闭全部 Rhino 窗口。
3. 完整解压 ZIP 到普通文件夹，不要在压缩包内部运行。
4. 双击 **`Setup.exe`**，点击“安装 / 更新”，看到“安装完成”后关闭窗口。
5. 启动 Rhino 8，输入 `Grasshopper`。检查“中文界面”菜单、河豚分类和细分曲面分组。

安装器会校验全部包文件、自动查找 Rhino 8，并直接调用 Windows 编译工具，使用目标电脑自带的 SDK 离线编译汉化插件。因此不会直接把本机 8.2 二进制当作通用版本安装。非默认路径可在安装窗口点击“选择 Rhino 8…”指定安装目录，无需输入命令。

**新版安装器不调用 PowerShell，不执行 `.ps1` 或 `.cmd`，也不修改系统执行策略。** 它是正常的 Windows .NET Framework 应用程序。安装程序尚未数字签名；公司应用控制、SmartScreen、杀毒软件或权限限制仍可能阻止运行，此时请由管理员核验并批准，不要关闭安全软件或绕过强制策略。

## 自动备份与重复插件

- 汉化安装到 `%APPDATA%\Grasshopper\Libraries\GrasshopperChinese`。
- 未安装河豚时，将原插件安装到 `Libraries\PufferfishChineseBundle`；10 个 SubD 用户对象安装到 `%APPDATA%\Grasshopper\UserObjects\PufferfishChineseBundle`。
- 已有与包内完全相同的河豚原文件时保留原位置，不重复复制。发现多个版本、不同内容或同名修改版时会停止，**不会擅自删除原插件**。
- 同名 SubD 用户对象会同时检查 UserObjects 与 Rhino 8 Packages；相同则复用，不同则停止，防止覆盖个人修改。0.3.1 更新会备份并移出此前本安装器新增、未修改且与外部原对象相同的重复副本；缺失的本包副本不再复制，外部原对象保留，卸载也不重新制造重复。
- 替换前备份旧文件；安装记录及备份在 `%LOCALAPPDATA%\GrasshopperChinese\OfflineInstaller`，不位于 Grasshopper 插件扫描目录。
- 安装前先编译，编译不兼容时不会替换旧插件。复制失败时回滚此次替换。
- 请保留安装器给出的备份目录，不要删除安装记录后再要求自动恢复旧版。

## 卸载与回退

关闭全部 Rhino 窗口，双击 **`Setup.exe`** 并点击“卸载并恢复旧版”。卸载器依据本包安装记录恢复被替换的旧文件，删除本包新增且未被修改的文件；不会删除原先安装的河豚、用户设置、个人修改或备份。原脚本版的安装记录也可读取。

安装后手动修改过的文件会保留并给出提示，不能保证自动完成卸载。无安装记录时停止，不会按文件名盲删。旧版若从其他途径安装，请自行用备份回退；也可在“中文界面”中取消“启用界面汉化”临时恢复英文。

## 中文界面菜单说明

- **刷新组件目录**：重新收集当前已加载且受支持的组件，再应用现有离线词库。适用于新组件加载后的显示刷新；不下载词库、不在线翻译，也不自动生成未知插件译文。
- **导出组件及缺译清单**：选择位置后保存一份 JSON，包含组件 GUID、分类、英文名称/说明、输入输出端口、匹配译文和实例化错误。翻译字段为空表示未匹配，`Error` 表示提取实例失败。这个文件用于整理补译，不会自动翻译、改写 GH 文档或拆成两个导出文件。
- **使用说明**：显示版本 `0.3.1`、上述操作解释和当前词库数量；当前版本说明不再标注“预览版”。首次有效功能区初始化一次选择“参数”，分类和分组完成重排；之后切换分类、语言或刷新目录不强制跳回参数栏。不同分类的图标行数本来不同，未固定窗口或功能区像素高度。

## 汉化范围与限制

- 已匹配原生组件、Kangaroo2、河豚分类、下拉项、组件名称/说明、端口名称/说明和标准右键项。
- 河豚静态词库包含 611 个组件类型和 10 个 WIP SubD 用户对象的元数据、模式说明及已提取的运行提示。静态导出有 13 个类型依赖 Rhino 原生状态，无法离线完整实例化；详细范围见源码仓库的 `docs/pufferfish-coverage.json`。
- 补译指南针右键、中键圆盘及启动教程浏览器文字。右键菜单在原生窗口显示消息处理前翻译；保留菜单操作，仍需在目标电脑验收实际效果。
- Raven 2.0.20 的左侧搜索/锁定界面有定向适配；**离线包不包含 Raven**，未安装 Raven 的电脑不需要它。
- RichedGraphMapper 的“增强图形映射器”、输入输出区间与数值、右键图形类型及固定编辑器文字使用专属词库；保留自定义曲线编辑属性，翻译不改其图形算法或组件 GUID。先安装 [独立 Rhino 8 适配版](https://github.com/khaoyu93-del/Rhino-grasshopper-Riched-Graph-Mapper-NEW-8-)，再更新汉化包。本包不重复安装或改写 RichedGraphMapper 本体。
- 更新映射器独立栏安装程序后，组件在“参数、数学、曲线……”顶部分类行**最右端的 图形映射器 → 映射** 独立分类，不属于参数页内部。旧映射器版本仍位于数学工具分组，仅更新汉化包不能移动旧插件分类。新建后右键选择“图形类型”，例如“插值曲线 → 5 点”，再拖动控制点；默认空白不代表加载失败。
- Rich 图形编辑器目前翻译标题、确定/取消按钮及四个区间标签；属性表细项、曲线模型内部名称和撤销历史不改写。自绘组件本身没有标题栏，不额外添加标题；中文端口仍使用原组件布局，实际显示宽度、交互及存档效果需用户验收。
- 画布汉化以显示层为主，绘制后恢复原始字段，保留自定义昵称。但搜索、拖放、求解、存档往返和全部自定义控件不能仅靠离线测试保证正确。
- 新 `.gha` 加载后自动刷新已支持的词库，**不会为任意未知插件自动生成译文**，也不使用在线翻译。
- 原作者注明 SubD 为 Rhino 7 专用的 WIP 用户对象；本包提供原文件和中文显示适配，Rhino 8 中的全部求解功能仍需用户验证。

**已在本机 Rhino/Grasshopper `8.2.23346.13001` 多轮使用并由用户阶段性验收。其他 Rhino 8 小版本仅提供本机 SDK 编译机制，并未逐版本验收。** 插件内部仍依赖部分 Rhino 8 UI 结构，编译通过不代表每个界面都兼容。不支持 Rhino 7、macOS 或缺少 SDK 的电脑。

建议在副本文件中验收：河豚常用组件与 SubD、右键首次显示、教程启动页、中文/双语/英文切换、自定义昵称、保存关闭再打开。加载失败时检查重复 `.gha`、五份词库是否与插件相邻，以及 `%LOCALAPPDATA%\GrasshopperChinese\errors.log`。

## 离线包内容和完整性

ZIP 内有 `Setup.exe`、`package-manifest.json`、`src`、`Languages`、`GrasshopperChinese`、`Pufferfish` 与版权说明，不包含安装用 PowerShell 脚本。预编译 `.gha` 仅为本机参考，安装器实际使用目标电脑 SDK 编译。

`package-manifest.json` 校验文件是否完整，不是数字签名。ZIP 的 `.sha256` 用于核对传输是否损坏，也不能证明来源可信；只使用来自可信发布者的包。

源码开发的构建命令仍是 `scripts/build.ps1`；制作离线包使用 `scripts/package-offline.ps1`。用户安装不需要这些开发脚本、测试工具或 Python。旧 `0.3.0-preview-rhino8.2-win.zip` 保留作历史记录，不含当前成果。

## 来源与许可

本项目参考 [GrasshopperChinese](https://github.com/xiaofeng-1011/GrasshopperChinese) `0.3.0-preview`，复用的 MultilingualGH 资源遵守 Victor Lin 的 MIT 许可，见 `LICENSE-MultilingualGH.txt` 和 `THIRD-PARTY-NOTICES.md`。

河豚 3.0 作者为 Michael Pryor（ekimroyrp）。发布者已确认取得本包的再分发授权；原插件和 SubD 文件未修改，作者安装说明保留在 `Pufferfish/AUTHOR-NOTES.txt`。此授权确认不向收件人授予额外再分发权，也不表示河豚适用 MIT 许可。

原汉化项目的新增代码尚未指定统一开源许可证，本仓库不宣称全部代码采用 MIT，也不授予额外修改或再分发许可。不得将 Rhino 程序、SDK、Raven 或个人文件混入离线包。没有额外要求时不上传 GitHub、不提交代码、不替换历史 ZIP。
