# Rhino 8 / Grasshopper 1 简体中文界面实践记录

本仓库记录使用 [GrasshopperChinese](https://github.com/xiaofeng-1011/GrasshopperChinese) 在 Windows Rhino 8 中进行界面汉化的安装、版本适配与验证方法。**本仓库不是该插件的发行仓库**；下载、更新、许可与问题反馈请以原项目为准。

## 适用范围与现状

- 原项目当前提供 `0.3.0-preview`：可翻译部分 Grasshopper 原生菜单、分类、工具名称、画布标题及说明，支持中文、中英对照和关闭汉化；尚未覆盖全部工具及第三方插件。
- 官方预览安装包按 Rhino SDK `8.31.26126.13431` 编译。本机验证环境为 Windows、Rhino / Grasshopper `8.2.23346.13001`；为避免跨版本加载问题，使用原项目源码在本机 SDK 下重新编译了 `.gha`。
- 已验证 Rhino 进程加载了 `GrasshopperChinese.gha`，Grasshopper 菜单出现“中文界面”，并可读到中文“文件”菜单；未出现插件错误日志。**尚未完成**组件搜索、拖放、求解、存档往返及不同运行时的完整图形界面验收，不应把菜单出现视为全面兼容。

## 安装原项目预览版

1. 从[原项目的下载与安装说明](https://github.com/xiaofeng-1011/GrasshopperChinese#下载与安装)获取 **Windows 安装包**（不是源码包），完整解压，并核对原项目提供的 SHA-256。
2. 关闭所有 Rhino 窗口。在解压目录运行 `Install.cmd`。安装脚本将文件复制到 `%APPDATA%\Grasshopper\Libraries\GrasshopperChinese`，不修改 Rhino 程序目录，也不需要管理员权限。
3. 启动 Rhino 8，运行 `Grasshopper`。在“中文界面”菜单中勾选“启用界面汉化”，按需勾选“中英对照”。如果没有看到文字标题，在 Grasshopper 的“显示”菜单中关闭“显示图标”。
4. 同一 `Libraries` 目录中不要同时留有独立的 `GrasshopperChinese.gha` 和子目录内的 `GrasshopperChinese.gha`：这可能导致重复加载。旧文件需先确认来源并备份，再移出 `Libraries`；词库 `Languages\*.json` 必须与正在加载的 `.gha` 放在同一目录下的 `Languages` 子目录。

## Rhino 8.2 的本机适配记录

预览包中的 `.gha` 引用 RhinoCommon 和 Grasshopper `8.31.26126.13431`；将相同发行版本的源码与本机 `8.2.23346.13001` SDK 编译后，引用版本变为 `8.2.23346.13001`，Grasshopper 中能显示中文菜单。**其他 Rhino 8 版本需在各自环境下验证，不保证同样结果。**

如遇旧版 Rhino 无法加载预编译插件，可在装有该版本 Rhino 8 的 Windows 机器上：

1. 从[原项目](https://github.com/xiaofeng-1011/GrasshopperChinese)下载同一版本的 **源码压缩包** 并完整解压。先关闭 Rhino。确认原项目的 `scripts/build.ps1` 所引用的 SDK 路径与你安装的 Rhino 一致。
2. 在源码根目录执行 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\build.ps1 -RhinoRoot "C:\Program Files\Rhino 8"`（如果安装在别处，替换为实际路径）。构建需要 Windows 自带的 .NET Framework C# 编译器，输出位于 `build\GrasshopperChinese\GrasshopperChinese.gha`。
3. 将安装目录内原有的 `GrasshopperChinese.gha` **备份至 `Libraries` 目录之外**，再用本机构建的 `.gha` 替换它。保留安装包原有的 `Languages` 目录，避免出现两份可加载的 `.gha`。
4. 启动 Rhino，运行 `Grasshopper`，确认“中文界面”菜单和已翻译的原生菜单出现；再用自己的 GH 文件测试搜索、拖放、运算、保存重开和第三方插件。

此次操作还发现：如果 `Libraries` 根目录已有独立 `.gha` 但没有相邻词库，插件读取 `Languages\zh-CN.json` 和 `Languages\tool-text.zh-CN.json` 时无法正常初始化。修复时先将孤立文件备份并移出扫描目录，然后按原项目安装完整文件；不要只复制单个 `.gha`。

## 回退与许可

要临时恢复英文，取消勾选“中文界面 → 启用界面汉化”。要卸载，关闭 Rhino 后运行安装包的 `Uninstall.cmd`；如果此前在 `Libraries` 根目录单独放过 `.gha`，也需自行核对并移出该文件。卸载脚本仅处理其安装子目录中的已知文件，不会删除本记录中建议保存的备份。

原项目的上游 MultilingualGH 资源有 MIT 许可，但原项目 README 说明其**新增代码尚未指定统一开源许可证**。因此此处仅保留操作记录与来源链接，不重新发布其源码、汉化词库或插件二进制。使用与再分发请遵循原项目的许可说明。
