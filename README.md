# Grasshopper 1 简体中文界面：Rhino 8.2 适配包

本仓库提供 [GrasshopperChinese](https://github.com/xiaofeng-1011/GrasshopperChinese) `0.3.0-preview` 在 **Windows Rhino 8 / Grasshopper 1 `8.2.23346.13001`** 上的本机编译安装包及操作记录。原项目的预编译插件引用 SDK `8.31.26126.13431`；本包使用同一版本的源码重新编译，使 `.gha` 引用本机的 `8.2.23346.13001` SDK。它不是 Rhino 官方汉化包，也不保证适用其他 Rhino 版本。

## 下载与校验

- [Rhino 8.2 汉化安装包（ZIP）](downloads/GrasshopperChinese-0.3.0-preview-rhino8.2-win.zip)
- [安装包 SHA-256 校验值](downloads/GrasshopperChinese-0.3.0-preview-rhino8.2-win.zip.sha256)

先下载完整 ZIP 与 `.sha256`，不要只下载 `.gha`。在 PowerShell 中进入下载目录，执行：

```powershell
(Get-FileHash -Algorithm SHA256 .\GrasshopperChinese-0.3.0-preview-rhino8.2-win.zip).Hash.ToLowerInvariant()
Get-Content .\GrasshopperChinese-0.3.0-preview-rhino8.2-win.zip.sha256
```

两行输出的 64 位十六进制哈希应一致；不一致时停止安装并重新下载。ZIP 内含 `Install.cmd` / `Install.ps1`、`Uninstall.cmd` / `Uninstall.ps1`，以及 `GrasshopperChinese` 子目录中的插件、两个词库、说明和上游版权声明。无需管理员权限，不包含 Rhino 程序文件。

## 安装步骤

1. 在 Rhino 的“帮助 → 关于”确认版本。**本包只针对 Rhino / Grasshopper `8.2.23346.13001` 构建和初步验证**。若版本不同，请使用[原项目安装包](https://github.com/xiaofeng-1011/GrasshopperChinese)，或参照下方“其他 Rhino 8 版本”一节用本机 SDK 编译。不要把这个 `.gha` 当作通用 Rhino 8 插件。
2. 关闭**全部** Rhino / Grasshopper 窗口。完整解压 ZIP 到一个普通文件夹，保持 `Install.cmd` 和 `GrasshopperChinese` 文件夹的相对位置，不要从 ZIP 压缩包内部直接运行脚本。
3. 在文件管理器地址栏输入 `%APPDATA%\Grasshopper\Libraries`。检查有无 `GrasshopperChinese.gha`（根目录中的独立旧文件）以及 `GrasshopperChinese` 文件夹。如有现存文件，先备份到 **`Libraries` 外**：旧版本或个人修改不应被无提示覆盖；单独的 `.gha` 留在根目录还可能导致重复加载。不要删除其他插件或用户文件。
4. 双击解压目录中的 `Install.cmd`，按提示运行。脚本在 Rhino 关闭时复制插件及词库到 `%APPDATA%\Grasshopper\Libraries\GrasshopperChinese`，并对已复制文件解除 Windows 下载标记。执行后确认该目录内有 `GrasshopperChinese.gha` 和 `Languages\zh-CN.json`、`Languages\tool-text.zh-CN.json`；`Libraries` 根目录不应再有第二份同名 `.gha`。
5. 启动 Rhino 8，在命令行输入 `Grasshopper`。Grasshopper 的菜单栏应有“中文界面”；菜单中勾选“启用界面汉化”，按需要勾选“中英对照”。如果组件只显示图标，在 Grasshopper 的“显示 / Display”菜单中关闭“显示图标 / Draw Icons”以查看文字名称。

安装脚本会覆盖**安装子目录中同名的文件**，不自动备份旧版本，也不会处理 `Libraries` 根目录中的独立 `.gha`。安装前的备份和旧文件排查不可省略。不要修改 Rhino 的 `Program Files` 安装目录。

## 安装后的验证与已知限制

本机已确认 Rhino 进程加载 `GrasshopperChinese.gha`、Grasshopper 出现“中文界面”菜单，且“文件”菜单显示中文；当时未发现插件错误日志。建议用**副本**而非唯一的正式项目文件继续测试：

1. 展开原生分类并放置 Move、Circle 等常用组件，检查名称、图标/文字模式及工具提示；第三方插件可能保持英文。
2. 测试画布搜索中文和英文、连线与求解结果、复制粘贴、撤销重做。
3. 修改组件自定义昵称，切换中文/中英/关闭汉化，确认自定义昵称不丢失；保存 GH 与 GHX 文件，关闭后重新打开并比较组件、连线和结果。
4. 如加载失败，检查 `Libraries` 中是否存在重复插件、词库是否与 `.gha` 相邻，以及 `%LOCALAPPDATA%\GrasshopperChinese\errors.log`（仅在插件写入异常时才会出现）。

**尚未完成**上述搜索、拖放、求解、存档往返、不同 .NET 运行时及高清屏幕的完整图形界面验收。原项目仍是 `0.3.0-preview`：并非所有原生工具和说明都已翻译，输入输出参数、右键菜单、动态报错和部分特殊控件仍可能是英文；不支持 Rhino 7 或 macOS。中文模式下英文搜索还可能受 Grasshopper 搜索缓存影响。

## 暂停、卸载与回退

- 临时关闭：在“中文界面”菜单取消勾选“启用界面汉化”，无需删文件。
- 卸载：关闭全部 Rhino 窗口，再运行本包的 `Uninstall.cmd`。它只删除安装子目录中列出的插件、词库和随包文件，保留设置和用户自行添加的文件，可能留下空目录；**不会**删除 `Libraries` 根目录中曾经单独安装的 `.gha`。
- 回退旧版：关闭 Rhino，按需要运行卸载脚本，再将你在第 3 步备份的旧版本**及其对应词库**恢复到原位置。恢复前确认 `Libraries` 中只有一份可加载的 `GrasshopperChinese.gha`。如果没有旧版备份，直接卸载后重启 Rhino 即可恢复原生英文界面。

## 其他 Rhino 8 版本：本机重新编译

不同版本的 SDK 可能不兼容，不建议直接复用本包的 `.gha`。如果需要适配自己的 Rhino 8 版本，从[原项目](https://github.com/xiaofeng-1011/GrasshopperChinese)取得同版本源码包并完整解压，在已安装目标 Rhino 的 Windows 机器上关闭 Rhino，从源码根目录执行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\build.ps1 -RhinoRoot "C:\Program Files\Rhino 8"
```

安装路径不同则调整 `-RhinoRoot`。构建需要 Windows 自带的 .NET Framework C# 编译器；成功后会生成 `build\GrasshopperChinese\GrasshopperChinese.gha`。备份并替换安装子目录中的 `.gha`，**保留与源码版本匹配的 `Languages` 词库**，重新启动 Rhino 并完成上面的验证步骤。本包未包含原项目源码；构建或进一步修改应从原项目获取源码和许可信息。

## 来源与许可

插件、词库和安装脚本来自 [xiaofeng-1011/GrasshopperChinese](https://github.com/xiaofeng-1011/GrasshopperChinese) `0.3.0-preview`，本包仅将插件针对 Rhino 8.2 SDK 重新编译。发布者已确认拥有本次再分发授权；原项目 README 指出新增代码尚未指定统一开源许可证，本仓库**不宣称这些新增代码采用 MIT 许可，也不授予额外的修改或再分发许可**。其中复用的 MultilingualGH 部分遵循 Victor Lin 的 MIT 许可，原版权声明及第三方告知保留在 ZIP 内。其他版本、源码及后续更新请以原项目的许可和说明为准。
