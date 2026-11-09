// UI entry point adapted from MultilingualGH Menu.cs (MIT, Victor Lin).
using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using Grasshopper;
using Grasshopper.GUI;
using Grasshopper.GUI.Canvas;
using Grasshopper.GUI.Ribbon;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Attributes;

[assembly: AssemblyTitle("GrasshopperChinese")]
[assembly: AssemblyVersion("0.3.1.0")]
[assembly: AssemblyFileVersion("0.3.1.0")]

namespace GrasshopperChinese
{
    public sealed class PluginInfo : GH_AssemblyInfo
    {
        public override string Name { get { return "GrasshopperChinese"; } }
        public override string Description { get { return "Grasshopper 简体中文界面 0.3.1"; } }
        public override Guid Id { get { return new Guid("531059ef-a238-48c3-ac68-6827ab8fd66f"); } }
        public override string AuthorName { get { return "GrasshopperChinese contributors"; } }
        public override string AuthorContact { get { return ""; } }
        public override Bitmap Icon { get { return null; } }
    }

    public sealed class Loader : GH_AssemblyPriority
    {
        public override GH_LoadingInstruction PriorityLoad()
        {
            if (Rhino.RhinoApp.ExeVersion != 8) return GH_LoadingInstruction.Abort;
            try { Runtime.Prepare(); }
            catch (Exception ex) { Runtime.Log(ex); return GH_LoadingInstruction.Abort; }
            Instances.CanvasCreated += Runtime.Attach;
            if (Instances.ActiveCanvas != null) Runtime.Attach(Instances.ActiveCanvas);
            return GH_LoadingInstruction.Proceed;
        }
    }

    internal sealed class OriginalDescription
    {
        internal IGH_ObjectProxy Proxy;
        internal string Name, Nickname, Category, Description, AssemblyName;
    }

    internal sealed class RavenTextProperty
    {
        internal Func<string> Get;
        internal Action<string> Set;
        internal string Original, Desired;
    }

    internal static class Runtime
    {
        internal static bool Enabled = true;
        internal static bool Bilingual;
        static Catalog catalog;
        static Catalog toolText;
        static Catalog pufferfishNames;
        static Catalog pufferfishText;
        static Catalog richText;
        static readonly Dictionary<Guid, string> richGraphs = new Dictionary<Guid, string>
        {
            { new Guid("d221fdb4-a2a5-4861-a206-f7ac8f91f9cb"), "Sigmoid" },
            { new Guid("e4f68fba-e0ba-4bbb-98aa-96ecb7db5d4e"), "Polyline" },
            { new Guid("19f04c28-60bd-4807-9308-c961b1233cea"), "Interpolated" },
            { new Guid("34afa8f2-fee6-4e3b-82da-b980ffeb87aa"), "Bezier2" },
            { new Guid("c5363e79-994b-4030-8e69-02cd00bf5982"), "Arc" }
        };
        static readonly Dictionary<Form, List<RavenTextProperty>> richEditorForms = new Dictionary<Form, List<RavenTextProperty>>();
        static readonly Dictionary<ToolStripItem, string> richMenuTooltips = new Dictionary<ToolStripItem, string>();
        static readonly Dictionary<Guid, OriginalDescription> originals = new Dictionary<Guid, OriginalDescription>();
        static readonly Dictionary<string, string> pufferfishUserNicknames = new Dictionary<string, string>(StringComparer.Ordinal)
        {
            { "Average SubD", "AvrSubD" }, { "Weighted Average SubD", "WavSubD" },
            { "Mirror Cut SubD", "MirCutSubD" }, { "Tween Two SubDs", "Twn2SubDs" },
            { "Tween Consecutive SubDs", "TwnConSubDs" }, { "Tween Through SubDs", "TwnThruSubDs" },
            { "Twisted Box SubD", "TBoxSubD" }, { "Twisted Box Two SubDs", "TBox2SubDs" },
            { "Twisted Box Consecutive SubDs", "TBoxConSubDs" }, { "Twisted Box Through SubDs", "TBoxThruSubDs" }
        };
        static readonly ConditionalWeakTable<IGH_DocumentObject, OriginalDescription> userDescriptions = new ConditionalWeakTable<IGH_DocumentObject, OriginalDescription>();
        static readonly Dictionary<Form, Dictionary<Control, string>> tutorialForms = new Dictionary<Form, Dictionary<Control, string>>();
        static readonly HashSet<ToolStripDropDown> preparedMenus = new HashSet<ToolStripDropDown>();
        static bool preparingWindow;
        static WindowHook windowHook;
        static IntPtr windowHookHandle;
        static bool prepared;
        static readonly Dictionary<ToolStripItem, string> menuOriginals = new Dictionary<ToolStripItem, string>();
        static readonly Dictionary<ToolStripItem, OriginalDescription> menuDescriptions = new Dictionary<ToolStripItem, OriginalDescription>();
        static readonly Dictionary<ToolStripItem, Guid> menuOwners = new Dictionary<ToolStripItem, Guid>();
        static readonly HashSet<ContextMenuStrip> canvasMenus = new HashSet<ContextMenuStrip>();
        static readonly HashSet<ToolStripDropDown> canvasPopups = new HashSet<ToolStripDropDown>();
        static readonly HashSet<ToolStripDropDown> widgetPopups = new HashSet<ToolStripDropDown>();
        static readonly HashSet<ToolStripDropDown> ravenPopups = new HashSet<ToolStripDropDown>();
        static readonly Dictionary<Eto.Forms.Window, List<RavenTextProperty>> ravenSearchWindows = new Dictionary<Eto.Forms.Window, List<RavenTextProperty>>();
        static readonly Dictionary<ToolStripItem, List<RavenTextProperty>> ravenMenuProperties = new Dictionary<ToolStripItem, List<RavenTextProperty>>();
        static IGH_DocumentObject contextObject;
        static GH_Canvas menuCanvas;
        static Guid menuObjectGuid;
        static readonly FieldInfo canvasTooltip = typeof(GH_Canvas).GetField("_Tooltip", BindingFlags.Instance | BindingFlags.NonPublic);
        static readonly Type userObjectProxy = typeof(GH_Canvas).Assembly.GetType("Grasshopper.Kernel.GH_UserObjectProxy");
        static readonly Type pointAttributes = typeof(GH_Canvas).Assembly.GetType("Grasshopper.Kernel.Parameters.Param_PointAttributes");
        static readonly Type graphEditorType = typeof(GH_Canvas).Assembly.GetType("Grasshopper.GUI.GH_GraphEditor");
        static readonly PropertyInfo graphEditorGraph = graphEditorType == null ? null : graphEditorType.GetProperty("Graph", BindingFlags.Instance | BindingFlags.Public);
        static readonly PropertyInfo ribbonTooltip = typeof(GH_Ribbon).GetProperty("GH_Tooltip", BindingFlags.Instance | BindingFlags.NonPublic);
        static GH_TooltipComponent subscribedRibbonTooltip;
        static readonly Dictionary<ToolStripItem, string> toolbarOriginals = new Dictionary<ToolStripItem, string>();
        static readonly Dictionary<ToolStripItem, string> toolbarDesired = new Dictionary<ToolStripItem, string>();
        static readonly Dictionary<ToolStripItem, string> toolbarNames = new Dictionary<ToolStripItem, string>();
        static readonly HashSet<ToolStripDropDownItem> observedToolbarMenus = new HashSet<ToolStripDropDownItem>();
        static GH_Toolstrip canvasToolbar;
        static readonly HashSet<GH_Canvas> canvases = new HashSet<GH_Canvas>();
        static readonly Dictionary<GH_Canvas, List<TextScope>> paintScopes = new Dictionary<GH_Canvas, List<TextScope>>();
        static readonly Dictionary<GH_Canvas, GH_TooltipComponent> canvasTooltips = new Dictionary<GH_Canvas, GH_TooltipComponent>();
        static readonly GH_SettingsServer settings = new GH_SettingsServer("GrasshopperChinese", true);
        static Timer setupTimer;
        static Timer ribbonTimer;
        static readonly RibbonTranslator ribbonTranslator = new RibbonTranslator();
        static readonly HashSet<GH_RibbonDropdown> observedDropdowns = new HashSet<GH_RibbonDropdown>();
        static readonly FieldInfo dropdownContent = typeof(GH_RibbonDropdown).GetField("_pnlContent", BindingFlags.Instance | BindingFlags.NonPublic);
        static GH_Ribbon ribbon;
        static GH_Ribbon layoutRibbon;
        static bool ribbonLayoutDirty = true;
        static bool startupTabPending = true;
        static int ribbonStructure = -1;
        static Size ribbonLayoutSize;
        static string ribbonLayoutError;
        static GH_DocumentEditor editor;
        static ToolStripMenuItem enabledItem, bilingualItem;
        static bool initialized;
        static bool proxiesChanged;
        static GH_ComponentServer componentServer;
        static readonly string folder = Path.GetDirectoryName(typeof(Runtime).Assembly.Location);
        static readonly Dictionary<string, string> tutorialText = new Dictionary<string, string>(StringComparer.Ordinal)
        {
            { "Getting started with Grasshopper…", "Grasshopper 入门…" },
            { "All these files are available from the Help menu as well.", "这些教程文件也可以从“帮助”菜单打开。" },
            { "Show the tutorial browser when Grasshopper starts.", "启动 Grasshopper 时显示教程浏览器。" },
            { "01 Simple Input and Maths", "01 基础输入与数学" },
            { "02 Interpolating Values", "02 数值插值" },
            { "03 Wires and Conversions", "03 连线与类型转换" },
            { "04 Polynomial Graphing with Derivatives", "04 多项式图形与导数" },
            { "05 Measure and Display Values", "05 测量与显示数值" },
            { "06 Adaptive Pattern within Shape", "06 形状内自适应图案" },
            { "07 Column Arcade", "07 柱廊" }
        };
        static readonly Dictionary<string, string> ravenText = new Dictionary<string, string>(StringComparer.Ordinal)
        {
            { "Raven Zones Editor", "Raven 区域编辑器" },
            { "Draw and edit Raven's zones. Right-click a workspace padlock to unlock its contents.", "绘制和编辑 Raven 区域。右键单击工作区挂锁可解锁其内容。" },
            { "Raven Search", "Raven 搜索" },
            { "Search groups across your documents.", "跨文档搜索组。" },
            { "Hide Raven Zones Editor", "隐藏 Raven 区域编辑器" },
            { "Hide Raven Search", "隐藏 Raven 搜索" },
            { "Select components or groups to lock", "选择需要锁定的组件或组" },
            { "Lock selection from Raven", "锁定所选对象，防止 Raven 修改" },
            { "Remove own Raven locks", "移除对象自身的 Raven 锁定" },
            { "Protect values, code, wiring and positions. Grasshopper continues to compute. Group and area locks still apply.", "保护数值、代码、连线和位置。Grasshopper 仍会计算，组和区域的锁定继续生效。" },
            { "Allow Raven to reference outputs", "允许 Raven 引用输出" },
            { "Turning this off prevents new references. Existing connections keep working.", "关闭后阻止新建引用，现有连接继续有效。" },
            { "Remove contained component, group and area locks. Keep the workspace boundary and locks extending outside it. Undo restores all removed locks.", "移除工作区内的组件、组和区域锁定，保留工作区边界及延伸至外部的锁定。撤销可恢复移除的锁定。" },
            { "Search groups and doors…", "搜索组和入口/出口…" },
            { "Back (Alt+Left)", "后退（Alt+左箭头）" },
            { "Forward (Alt+Right)", "前进（Alt+右箭头）" },
            { "Lock", "锁定" }, { "Unlock", "解锁" },
            { "Protect this item from Raven edits. Computing and referencing outputs remain available.", "防止 Raven 修改此对象，仍允许计算和引用输出。" },
            { "Remove own locks", "移除自身锁定" },
            { "Select an item in an open document.", "在已打开的文档中选择一个对象。" },
            { "Preview only · this document is not open.", "仅预览 · 此文档尚未打开。" },
            { "Preview only · this item is no longer on the canvas.", "仅预览 · 此对象已不在画布上。" }
        };
        static readonly Dictionary<string, string> canvasText = new Dictionary<string, string>(StringComparer.Ordinal)
        {
            { "Compass", "指南针" },
            { "Find your way home", "快速定位画布中的对象" },
            { "Align", "对齐" },
            { "Mr. Sparkle", "辅助对齐画布对象" },
            { "Markov", "马尔可夫" },
            { "What's next?", "推荐下一步组件" },
            { "Profiler", "性能分析器" },
            { "Chop-chop!", "查看组件运行耗时" },
            { "Double click to switch metrics.", "双击切换统计指标。" },
            { "Message Balloons", "消息气泡" },
            { "Whaddup?", "查看画布提示消息" },
            { "Enable Preview", "开启预览" },
            { "Enable preview for all selected objects", "开启全部所选对象的预览" },
            { "Disable Preview", "关闭预览" },
            { "Disable preview for all selected objects", "关闭全部所选对象的预览" },
            { "Enable", "启用" },
            { "Enable all selected objects", "启用全部所选对象" },
            { "Disable", "禁用" },
            { "Disable all selected objects", "禁用全部所选对象" },
            { "Bake", "烘焙" },
            { "Bake geometry in all selected objects", "烘焙全部所选对象中的几何对象" },
            { "Zoom", "缩放" },
            { "Zoom to preview geometry of all selected objects", "缩放至全部所选对象的预览几何" },
            { "Group", "编组" },
            { "Create a group containing all selected objects", "将全部所选对象创建为一个组" },
            { "Cluster", "群集" },
            { "Convert all selected objects into a cluster", "将全部所选对象转换为群集" },
            { "Find", "查找" },
            { "Search the document for components and parameters", "在文档中查找组件和参数" },
            { "Navigate", "导航" },
            { "Navigate the document using a scaled down map", "通过缩略图导航文档" },
            { "Disable Solver", "禁用求解器" },
            { "Disable the global Grasshopper solver", "禁用 Grasshopper 全局求解器" },
            { "Enable Solver", "启用求解器" },
            { "Enable the global Grasshopper solver", "启用 Grasshopper 全局求解器" },
            { "Recompute", "重新计算" },
            { "Force all objects in the document to recompute", "强制重新计算文档中的全部对象" },
            { "Preferences", "首选项" },
            { "Show the Grasshopper preferences window", "显示 Grasshopper 首选项窗口" },
            { "Cluster Document", "群集文档" },
            { "Solution Aborted", "求解已中止" },
            { "You are currently editing a cluster document. " + Environment.NewLine + "Click here for some cluster related tools.", "正在编辑群集文档。点击此处查看群集工具。" },
            { "The most recent solution was aborted. " + Environment.NewLine + "This warning will disappear once a solution completes.", "最近一次求解已中止；下次求解完成后，此警告将消失。" }
        };
        static readonly Dictionary<string, string> toolbarText = new Dictionary<string, string>(StringComparer.Ordinal)
        {
            { "Open a gh or ghx file", "打开 gh 或 ghx 文件" },
            { "Save the current file", "保存当前文件" },
            { "View all selected objects", "查看全部选中对象" },
            { "View upper left corner of document", "查看文档左上角" },
            { "View upper right corner of document", "查看文档右上角" },
            { "View lower left corner of document", "查看文档左下角" },
            { "View lower right corner of document", "查看文档右下角" },
            { "Add named view…", "添加命名视图…" },
            { "Create a new sketch object", "创建草图对象" },
            { "Use the Rhino document meshing settings", "使用 Rhino 文档网格设置" },
            { "Use custom mesh quality", "使用自定义网格质量" },
            { "Modify the custom mesh quality", "修改自定义网格质量" },
            { "Press ESCAPE to remove any existing boundary.", "按 Esc 移除现有边界。" },
            { "When checked, points and curves will be drawn slightly closer than they actually are", "启用后，点和曲线会绘制得比实际位置略近。" },
            { "Open", "打开" }, { "Save", "保存" },
            { "Sketch", "草图" }, { "Add View", "添加视图" },
            { "Preview Mesh Quality", "预览网格质量" },
            { "Selected", "仅选中" }, { "Boundary", "边界" },
            { "Shaded", "着色" }, { "Wireframe", "线框" },
            { "Draw a preview boundary on the canvas to exclude objects." + Environment.NewLine + "Press ESCAPE to remove any existing boundary.", "在画布上绘制预览边界以排除对象。按 Esc 移除现有边界。" },
            { "View entire document", "查看整个文档" },
            { "Zoom factor", "缩放比例" },
            { "Zoom Selected", "缩放至所选对象" },
            { "Preview Off", "关闭预览" },
            { "Focus on All objects", "聚焦全部对象" },
            { "Focus on Upper Left", "聚焦左上角" },
            { "Focus on Upper Right", "聚焦右上角" },
            { "Focus on Lower Left", "聚焦左下角" },
            { "Focus on Lower Right", "聚焦右下角" },
            { "Focus on the selected preview geometry", "聚焦所选预览几何" },
            { "Zoom on Preview", "缩放至预览几何" },
            { "Draw wireframe preview geometry", "以线框模式预览几何对象" },
            { "Draw shaded preview geometry", "以着色模式预览几何对象" },
            { "Don't draw any preview geometry", "不绘制预览几何对象" },
            { "Only draw preview geometry for selected objects", "仅绘制所选对象的预览几何" },
            { "Disable preview geometry for all selected objects", "关闭全部所选对象的预览" },
            { "Enable preview geometry for all selected objects", "开启全部所选对象的预览" },
            { "Toggle preview geometry visibility for all selected objects", "切换全部所选对象的预览可见性" },
            { "Do not compute preview meshes", "不计算预览网格" },
            { "Fast and coarse preview meshing", "快速粗略的预览网格" },
            { "Slow and smooth preview meshing", "缓慢平滑的预览网格" },
            { "Document preview settings…", "文档预览设置…" },
            { "Draw a new preview boundary", "绘制新的预览边界" },
            { "Draw a preview boundary on the canvas to exclude objects.", "在画布上绘制预览边界以排除对象。" },
            { "Set the size (in model units) of preview planes", "以模型单位设置预览平面的尺寸" },
            { "Set the style of preview points", "设置预览点的样式" },
            { "Show or hide mesh edges in the preview", "在预览中显示或隐藏网格边线" },
            { "Show the preview settings for the current document", "显示当前文档的预览设置" },
            { "Bump Preview", "增强预览" },
            { "Focus Upper-Left", "聚焦左上角" }, { "Focus Upper-Right", "聚焦右上角" },
            { "Focus Lower-Left", "聚焦左下角" }, { "Focus Lower-Right", "聚焦右下角" }
        };
        static readonly Dictionary<string, string> menuText = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
        {
            { "File", "文件" }, { "Edit", "编辑" }, { "View", "视图" }, { "Display", "显示" },
            { "Solution", "求解" }, { "Help", "帮助" }, { "New Document", "新建文档" },
            { "New", "新建" }, { "Open Document", "打开文档" }, { "Open", "打开" },
            { "Save Document", "保存文档" }, { "Save", "保存" }, { "Save As", "另存为" },
            { "Save Document As", "文档另存为" }, { "Close", "关闭" }, { "Close Document", "关闭文档" },
            { "Undo", "撤销" }, { "Redo", "重做" }, { "Cut", "剪切" }, { "Copy", "复制" },
            { "Paste", "粘贴" }, { "Delete", "删除" }, { "Select All", "全选" },
            { "Preferences", "首选项" }, { "Special Folders", "特殊文件夹" },
            { "Components Folder", "组件文件夹" }, { "Settings Folder", "设置文件夹" },
            { "User Object Folder", "用户对象文件夹" }, { "Export", "导出" },
            { "Preview", "预览" }, { "Draw Icons", "显示图标" }, { "Draw Full Names", "显示完整名称" },
            { "Enable Solver", "启用求解器" }, { "Recompute", "重新计算" },
            { "Disable Preview", "禁用预览" }, { "Wireframe Preview", "线框预览" },
            { "Shaded Preview", "着色预览" }, { "Preview Selected Only", "仅预览所选对象" },
            { "Zoom", "缩放" }, { "Zoom Extents", "缩放至全部对象" }, { "Zoom Selected", "缩放至所选对象" },
            { "View entire document", "查看整个文档" },
            { "Focus on All objects", "聚焦全部对象" },
            { "Focus on Upper Left", "聚焦左上角" }, { "Focus on Upper Right", "聚焦右上角" },
            { "Focus on Lower Left", "聚焦左下角" }, { "Focus on Lower Right", "聚焦右下角" },
            { "Zoom on Preview", "缩放至预览几何" },
            { "Focus on the selected preview geometry", "聚焦所选预览几何" },
            { "No Named Views", "没有命名视图" }, { "Add named view", "添加命名视图" },
            { "Group", "编组" }, { "Ungroup", "取消编组" }, { "Bake", "烘焙" },
            { "About", "关于" }, { "About Grasshopper", "关于 Grasshopper" },
            { "Recent Files", "最近文件" }, { "Save Backup", "保存备份" },
            { "Export Quick Image", "导出快速图像" }, { "Export Hi-Res Image", "导出高分辨率图像" },
            { "Document Properties", "文档属性" }, { "Create User Object", "创建用户对象" },
            { "Insert Cluster Into File", "将群集保存到文件" }, { "Show In Folder", "在文件夹中显示" },
            { "Remote Control Panel", "远程控制面板" }, { "Ribbon Tab Icons", "功能区标签图标" },
            { "Canvas Toolbar", "画布工具栏" }, { "Component Tabs", "组件标签" },
            { "Panel Separators", "面板分隔线" }, { "Obscure Components", "隐藏组件" },
            { "Data Viewer", "数据查看器" }, { "Store Current View", "保存当前视图" },
            { "Restore Named View", "恢复命名视图" }, { "Canvas redraw speed", "画布重绘速度" },
            { "Document Info", "文档信息" }, { "Preview On", "开启预览" },
            { "Preview Off", "关闭预览" }, { "Enable", "启用" }, { "Disable", "禁用" },
            { "Cluster", "群集" }, { "Lock Solver", "锁定求解器" },
            { "Navigate", "导航" }, { "Find", "查找" },
            { "Paste In Place", "原位粘贴" }, { "Paste In Center", "居中粘贴" },
            { "Deselect All", "取消全选" }, { "Invert Selection", "反选" },
            { "Modify Selection", "修改选择集" }, { "Arrange", "排列" },
            { "Put To Back", "置于底层" }, { "Bring To Front", "置于顶层" },
            { "Move Backwards", "后移一层" }, { "Move Forwards", "前移一层" },
            { "Align Selection", "对齐所选对象" }, { "Grow Selection", "扩展选择集" },
            { "Grow Upstream", "向上游扩展" }, { "Grow Downstream", "向下游扩展" },
            { "Shift Upstream", "选择上游" }, { "Shift Downstream", "选择下游" },
            { "Create", "创建" }, { "Draw Fancy Wires", "绘制美化连线" },
            { "Preview Mesh Settings", "预览网格设置" }, { "No Preview", "关闭预览" },
            { "Preview Boundary", "预览边界" }, { "Selected Only Preview", "仅预览所选对象" },
            { "Preview Settings", "预览设置" }, { "Preview Point Flavour", "预览点样式" },
            { "Preview Plane Size", "预览平面大小" }, { "Preview Mesh Edges", "预览网格边线" },
            { "Gumballs", "操作轴" }, { "Canvas Widgets", "画布小部件" },
            { "Clear", "清除" }, { "Disable Solver", "禁用求解器" },
            { "Clear Exceptions", "清除异常" }, { "Upgrade Components", "升级组件" },
            { "Bake Selected", "烘焙所选对象" }, { "Save State", "保存状态" },
            { "Restore State", "恢复状态" }, { "Delete State", "删除状态" },
            { "Preview Selected On", "开启所选对象预览" }, { "Preview Selected Off", "关闭所选对象预览" },
            { "Toggle Preview", "切换预览" }, { "Enable Selected", "启用所选对象" },
            { "Disable Selected", "禁用所选对象" }, { "Toggle Enable Selected", "切换所选对象启用状态" },
            { "Tutorial Files", "教程文件" }, { "Grasshopper Support", "Grasshopper 技术支持" },
            { "Online Reference", "在线参考" }, { "Export Help", "导出帮助" },
            { "Download SDK Help", "下载 SDK 帮助" },
            { "Disable Meshing", "禁用网格划分" }, { "Low Quality", "低质量" },
            { "High Quality", "高质量" }, { "Document Quality", "文档质量" },
            { "Custom Quality", "自定义质量" }, { "Edit Custom Quality", "编辑自定义质量" },
            { "Dot", "圆点" }, { "Point", "点" }, { "Cross", "十字" },
            { "Compass", "指南针" }, { "Align", "对齐" }, { "Markov", "马尔可夫" },
            { "Hide Compass", "隐藏指南针" },
            { "Draw object bubbles", "绘制对象气泡" },
            { "Only draw selected objects", "仅绘制所选对象" },
            { "Profiler", "性能分析器" }, { "Message Balloons", "消息气泡" },
            { "Help…", "帮助…" },
            { "Bake Geometry", "烘焙几何" },
            { "Enabled", "已启用" }, { "Locked", "已锁定" },
            { "Wire Display", "连线显示" }, { "Default", "默认" },
            { "Hidden", "隐藏" }, { "Faint", "浅色" },
            { "Flatten", "展平" }, { "Graft", "嫁接" }, { "Simplify", "简化" },
            { "Reverse", "反转" }, { "Reparameterize", "重新参数化" },
            { "Item Access", "单项访问" }, { "List Access", "列表访问" },
            { "Tree Access", "数据树访问" }, { "Input Manager", "输入管理器" },
            { "Output Manager", "输出管理器" }, { "Variable Parameters", "可变参数" },
            { "Disconnect", "断开连接" }, { "Disconnect All", "断开全部连接" },
            { "Disconnect Selected", "断开所选连接" }, { "Internalise data", "内化数据" },
            { "Expression Editor", "表达式编辑器" }, { "Type hint", "类型提示" },
            { "Runtime errors", "运行时错误" }, { "Runtime warnings", "运行时警告" },
            { "Runtime remarks", "运行时提示" }, { "Open Cluster", "打开群集" },
            { "Publish To Remote Panel", "发布到远程面板" },
            { "Input:", "输入：" }, { "Output:", "输出：" },
            { "Set As Default", "设为默认" }, { "Settings", "设置" },
            { "Shortest list", "最短列表" }, { "Cross reference", "交叉引用" },
            { "Principal", "主参数" }, { "Manage {0} collection", "管理{0}集合" },
            { "Add to group", "添加到组" }, { "Remove from group", "从组中移除" },
            { "Align Left", "左对齐" }, { "Align Center", "居中对齐" },
            { "Align Right", "右对齐" }, { "Animate", "制作动画" },
            { "Automatic Domain", "自动区间" }, { "By Display", "按显示属性" },
            { "By Layer", "按图层" }, { "By Material", "按材质" },
            { "By Parent", "按父对象" }, { "Clear values", "清空数值" },
            { "Copy All Content", "复制全部内容" }, { "Copy Data Only", "仅复制数据" },
            { "Create Flatten Mapping", "创建展平映射" }, { "Create Graft Mapping", "创建嫁接映射" },
            { "Create Null Mapping", "创建原样映射" }, { "Create Renumber Mapping", "创建重新编号映射" },
            { "Create Reverse Mapping", "创建反转映射" }, { "Create Trim Mapping", "创建修剪映射" },
            { "Delete Geometry", "删除几何" }, { "Draw Indices", "绘制索引" },
            { "Draw Paths", "绘制路径" }, { "Draw Tag", "绘制标签" },
            { "Draw Tree", "绘制数据树" }, { "Edit Notes", "编辑注释" },
            { "Edit Snapping", "编辑捕捉设置" }, { "Expression", "表达式" },
            { "Flip", "翻转" }, { "Floating point", "浮点数" },
            { "Go to", "跳转到" }, { "Group by Layer", "按图层编组" },
            { "Group by Type", "按类型编组" }, { "Include Hidden Objects", "包含隐藏对象" },
            { "Include Locked Objects", "包含锁定对象" }, { "Integers", "整数" },
            { "Invert", "取反" }, { "Layer Filter", "图层筛选器" },
            { "Load from Rhino", "从 Rhino 加载" }, { "Load Geometry", "加载几何" },
            { "Maintain References", "保持引用" }, { "Manual", "手动" },
            { "Mapping Editor", "映射编辑器" }, { "Match Method", "匹配方式" },
            { "Meshes", "网格" }, { "Multiline Data", "多行数据" },
            { "Name Filter", "名称筛选器" }, { "Never", "从不" },
            { "No updates", "不更新" }, { "None", "无" },
            { "Normal state", "正常状态" }, { "Open the mapping editor", "打开映射编辑器" },
            { "Parallel computing", "并行计算" }, { "Presets", "预设" },
            { "Record Data", "记录数据" }, { "Record Limit", "记录上限" },
            { "Remove Target", "移除目标" },
            { "Select many existing files", "选择多个现有文件" },
            { "Select one existing file", "选择一个现有文件" },
            { "Set Culture", "设置区域文化" }, { "Set Default Culture", "设置默认区域文化" },
            { "Set Invariant Culture", "设置固定区域文化" },
            { "Set Mesh Options", "设置网格选项" },
            { "Sort Ascending", "升序排列" }, { "Sort Descending", "降序排列" },
            { "Starts With", "以指定文本开头" }, { "Ends With", "以指定文本结尾" },
            { "Synchronize", "同步" }, { "Unitize", "单位化" },
            { "Update", "更新" }, { "User Text", "用户文本" },
            { "Value Cycle", "循环取值" }, { "Value Sequence", "数值序列" },
            { "Wildcards", "通配符" }, { "Wrap Items", "循环列表项" },
            { "Add Current Gradient", "添加当前渐变" },
            { "Adjust Defaults", "调整默认设置" },
            { "Make Colour Default", "设为默认颜色" },
            { "Make Font Default", "设为默认字体" },
            { "Make Font Global", "将字体应用到所有面板" },
            { "Smooth (25 ms.)", "平滑（25 毫秒）" },
            { "Jagged (100 ms.)", "阶梯（100 毫秒）" },
            { "Slow (1 s.)", "缓慢（1 秒）" },
            { "Excruciating (10 s.)", "极慢（10 秒）" },
            { "New layer filters", "新建图层筛选器" },
            { "Output data will be structured based on this parameter.", "按此参数组织输出数据。" },
            { "Output data will be structured using standard logic.", "按标准规则组织输出数据。" },
            { "The Default Culture of Rhino and Grasshopper is US-English.", "Rhino 和 Grasshopper 的默认区域文化为美国英语。" },
            { "The Invariant Culture is based on English but has no specific location.", "固定区域文化基于英语，但不对应特定地区。" },
            { "Updates can only be triggered manually.", "只能手动触发更新。" },
            { "Extract parameter", "提取参数" }, { "List", "列表" },
            { "Negate", "取反" }, { "Degrees", "角度制" },
            { "Further errors not shown", "还有错误未显示" },
            { "Further warnings not shown", "还有警告未显示" },
            { "Further remarks not shown", "还有提示未显示" },
            { "VariableParameterZuiMessage", "可变参数" },
            { "Flatten all data in this parameter into a single list", "将此参数中的全部数据展平为一个列表" },
            { "Graft all data in this parameter", "嫁接此参数中的全部数据" },
            { "Reverse the order of all lists in this parameter", "反转此参数中所有列表的顺序" },
            { "Unitize all vectors in this parameter", "将此参数中的全部向量单位化" },
            { "All incoming wires are drawn as faint lines", "将所有输入连线绘制为浅色线条" },
            { "All incoming wires are not drawn unless selected", "仅选中时绘制输入连线" },
            { "Change this input into a principal parameter.", "将此输入改为主参数。" },
            { "Change this input into a regular parameter.", "将此输入改为普通参数。" },
            { "Make volatile data permanent and disconnect all sources", "将临时数据内化并断开所有来源" },
            { "Click to copy error text to clipboard.", "点击复制错误信息。" },
            { "Click to copy warning text to clipboard.", "点击复制警告信息。" },
            { "Click to copy remark text to clipboard.", "点击复制提示信息。" }
        };

        internal static void Log(Exception exception)
        {
            try
            {
                string path = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "GrasshopperChinese");
                Directory.CreateDirectory(path);
                File.AppendAllText(Path.Combine(path, "errors.log"), DateTime.UtcNow.ToString("o") + " " + exception + Environment.NewLine);
            }
            catch { System.Diagnostics.Debug.WriteLine(exception); }
        }

        static void CaptureContextObject(GH_Canvas canvas, MouseEventArgs args)
        {
            if (args.Button != MouseButtons.Right) return;
            menuCanvas = canvas;
            menuObjectGuid = Guid.Empty;
            contextObject = null;
            if (canvas.Document == null) return;
            var point = canvas.Viewport.UnprojectPoint(new PointF(args.X, args.Y));
            var attributes = canvas.Document.FindAttribute(point, false);
            var owner = attributes == null ? null : attributes.GetTopLevel.DocObject;
            OriginalDescription original;
            if (owner != null && OriginalForObject(owner, out original))
            {
                contextObject = owner;
                menuObjectGuid = original.Proxy == null ? owner.ComponentGuid : original.Proxy.Guid;
            }
        }

        internal static void Attach(GH_Canvas canvas)
        {
            if (!canvases.Add(canvas)) { StartInitialization(canvas); return; }
            canvas.DocumentChanged += delegate { Observe(canvas); };
            canvas.ContextMenuStripChanged += delegate { ObserveCanvasMenu(canvas); };
            canvas.MouseUp += delegate(object sender, MouseEventArgs args)
            {
                CaptureContextObject(canvas, args);
                ObserveCanvasPopup();
                ObserveRavenSearch();
            };
            canvas.MouseDown += delegate(object sender, MouseEventArgs args) { CaptureContextObject(canvas, args); ObserveCanvasPopup(); ObserveRavenSearch(); };
            ObserveCanvasMenu(canvas);
            canvas.CanvasPrePaintObjects += BeginDisplayNames;
            canvas.CanvasPaintEnd += EndDisplayNames;
            ObserveCanvasTooltip(canvas);
            canvas.Disposed += delegate { EndDisplayNames(canvas); ForgetCanvasTooltip(canvas); canvases.Remove(canvas); if (menuCanvas == canvas) { menuCanvas = null; menuObjectGuid = Guid.Empty; contextObject = null; } };
            StartInitialization(canvas);
        }

        static void StartInitialization(GH_Canvas canvas)
        {
            if (setupTimer != null || initialized) { if (initialized) Observe(canvas); return; }
            setupTimer = new Timer { Interval = 250 };
            setupTimer.Tick += delegate
            {
                if (Instances.DocumentEditor == null || Instances.DocumentEditor.IsDisposed) return;
                setupTimer.Stop();
                setupTimer.Dispose();
                setupTimer = null;
                try { Initialize(); }
                catch (Exception ex) { Enabled = false; Log(ex); MessageBox.Show("中文界面加载失败，已保留英文界面。\n" + ex.Message, "Grasshopper 中文界面"); }
            };
            setupTimer.Start();
        }

        internal static void Prepare()
        {
            if (prepared) return;
            catalog = Catalog.Parse(File.ReadAllText(Path.Combine(folder, "Languages", "zh-CN.json")));
            toolText = Catalog.Parse(File.ReadAllText(Path.Combine(folder, "Languages", "tool-text.zh-CN.json")));
            pufferfishNames = Catalog.Parse(File.ReadAllText(Path.Combine(folder, "Languages", "pufferfish.zh-CN.json")));
            pufferfishText = Catalog.Parse(File.ReadAllText(Path.Combine(folder, "Languages", "pufferfish-text.zh-CN.json")));
            richText = Catalog.Parse(File.ReadAllText(Path.Combine(folder, "Languages", "richedgraphmapper.zh-CN.json")));
            Enabled = settings.GetValue("Enabled", true);
            Bilingual = settings.GetValue("Bilingual", false);
            windowHook = WindowMessage;
            windowHookHandle = SetWindowsHookEx(4, windowHook, IntPtr.Zero, GetCurrentThreadId());
            if (windowHookHandle == IntPtr.Zero) throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
            prepared = true;
        }

        static void Initialize()
        {
            Prepare();
            if (windowHookHandle == IntPtr.Zero)
            {
                windowHookHandle = SetWindowsHookEx(4, windowHook, IntPtr.Zero, GetCurrentThreadId());
                if (windowHookHandle == IntPtr.Zero) throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
            }
            editor = Instances.DocumentEditor;
            var root = new ToolStripMenuItem("中文界面") { Name = "GrasshopperChineseMenu" };
            enabledItem = new ToolStripMenuItem("启用界面汉化") { Checked = Enabled, CheckOnClick = true };
            bilingualItem = new ToolStripMenuItem("中英对照") { Checked = Bilingual, CheckOnClick = true };
            enabledItem.Click += delegate { Enabled = enabledItem.Checked; Update(); };
            bilingualItem.Click += delegate { Bilingual = bilingualItem.Checked; Update(); };
            root.DropDownItems.Add(enabledItem);
            root.DropDownItems.Add(bilingualItem);
            root.DropDownItems.Add("刷新组件目录", null, delegate { CollectProxies(); Update(); });
            root.DropDownItems.Add("导出组件及缺译清单", null, delegate { ExportCatalog(); });
            root.DropDownItems.Add(new ToolStripSeparator());
            root.DropDownItems.Add("使用说明", null, delegate
            {
                MessageBox.Show(UsageText(), "Grasshopper 中文界面 0.3.1", MessageBoxButtons.OK, MessageBoxIcon.Information);
            });
            editor.MainMenuStrip.Items.Add(root);
            componentServer = Instances.ComponentServer;
            componentServer.GHAFileLoaded += ComponentLibraryLoaded;
            CollectProxies();
            CaptureMenus(editor.MainMenuStrip.Items);
            CaptureToolbar();
            initialized = true;
            Update();
            ribbonTimer = new Timer { Interval = 300 };
            ribbonTimer.Tick += delegate { if (proxiesChanged) { proxiesChanged = false; CollectProxies(); Update(); } RefreshRibbon(); ObserveCanvasTooltips(); CaptureToolbar(); ObserveDropdowns(); RefreshCanvasMenus(); ObserveMenuPopups(); ObserveRavenSearch(); };
            ribbonTimer.Start();
            editor.Disposed += delegate
            {
                if (ribbonTimer != null) { ribbonTimer.Stop(); ribbonTimer.Dispose(); ribbonTimer = null; }
                if (componentServer != null) componentServer.GHAFileLoaded -= ComponentLibraryLoaded;
                if (windowHookHandle != IntPtr.Zero) { UnhookWindowsHookEx(windowHookHandle); windowHookHandle = IntPtr.Zero; }
                if (subscribedRibbonTooltip != null) subscribedRibbonTooltip.PopulateTooltip -= TranslateRibbonTooltip;
                subscribedRibbonTooltip = null;
                foreach (var canvas in canvases) EndDisplayNames(canvas);
                ribbon = null; layoutRibbon = null; editor = null; componentServer = null;
                ribbonLayoutDirty = true; startupTabPending = true; ribbonStructure = -1;
                ribbonLayoutError = null; initialized = false; proxiesChanged = false;
            };
        }

        static void ComponentLibraryLoaded(object sender, GH_GHALoadingEventArgs args)
        { proxiesChanged = true; ribbonLayoutDirty = true; }

        static void CollectProxies()
        {
            foreach (IGH_ObjectProxy proxy in Instances.ComponentServer.ObjectProxies) CollectProxy(proxy);
        }

        static void CollectProxy(IGH_ObjectProxy proxy)
        {
            if (proxy == null || originals.ContainsKey(proxy.Guid)) return;
            string assemblyName;
            if (proxy.GetType() == userObjectProxy && IsPufferfishUserDescription(proxy.Desc)) assemblyName = "Pufferfish";
            else
            {
                if (proxy.Type == null) return;
                assemblyName = proxy.Type.Assembly.GetName().Name;
                if (!NativeTools.Contains(assemblyName) && assemblyName != "Pufferfish" && assemblyName != "RichedGraphMapper") return;
            }
            originals.Add(proxy.Guid, new OriginalDescription { Proxy = proxy, Name = proxy.Desc.Name, Nickname = proxy.Desc.NickName, Category = proxy.Desc.Category, Description = proxy.Desc.Description, AssemblyName = assemblyName });
        }

        static bool IsPufferfishUserDescription(IGH_InstanceDescription description)
        {
            return description.Category == "Pufferfish" && description.SubCategory == "SubD" &&
                pufferfishUserNicknames.ContainsKey(description.Name) && pufferfishNames.Find(description.Name, "Pufferfish") != null &&
                pufferfishText.Find(description.Description, "description") != null;
        }

        static bool OriginalForObject(IGH_DocumentObject component, out OriginalDescription original)
        {
            if (userDescriptions.TryGetValue(component, out original)) return true;
            var cluster = component as Grasshopper.Kernel.Special.GH_Cluster;
            if (cluster != null && IsPufferfishUserDescription(component))
            {
                original = new OriginalDescription { Name = component.Name, Nickname = pufferfishUserNicknames[component.Name], Category = component.Category, Description = component.Description, AssemblyName = "Pufferfish" };
                userDescriptions.Add(component, original);
                return true;
            }
            return originals.TryGetValue(component.ComponentGuid, out original);
        }

        static string Format(string chinese, string english) { return Bilingual ? chinese + " · " + english : chinese; }

        static string ComponentName(OriginalDescription original)
        {
            if (original.AssemblyName == "RichedGraphMapper") return richText.Find(original.Name, "component");
            return original.AssemblyName == "Pufferfish" ? pufferfishNames.Find(original.Name, "Pufferfish") : catalog.Find(original.Name, original.Category);
        }

        static string ComponentDescription(OriginalDescription original)
        {
            if (original.AssemblyName == "RichedGraphMapper") return richText.Find(original.Description, "description");
            return original.AssemblyName == "Pufferfish" ? pufferfishText.Find(original.Description, "description") : toolText.Find(original.Description, "description");
        }

        internal static bool IsRich(IGH_DocumentObject component)
        {
            OriginalDescription original;
            return component != null && OriginalForObject(component, out original) && original.AssemblyName == "RichedGraphMapper";
        }

        internal static string RichLabel(string english, string category, bool enabled, bool bilingual)
        {
            if (!enabled || richText == null || string.IsNullOrEmpty(english)) return english;
            var chinese = richText.Find(english, category);
            return chinese == null ? english : bilingual ? chinese + " · " + english : chinese;
        }

        static string RichRuntimeLabel(string english, bool enabled, bool bilingual)
        {
            var translated = RichLabel(english, "runtime", enabled, bilingual);
            if (translated != english || string.IsNullOrEmpty(english) || !enabled || richText == null) return translated;
            int separator = english.IndexOf(". ", StringComparison.Ordinal), number;
            if (separator > 0 && int.TryParse(english.Substring(0, separator), out number))
            {
                var message = english.Substring(separator + 2);
                var chinese = richText.Find(message, "runtime");
                if (chinese != null) return bilingual ? english.Substring(0, separator + 2) + chinese + " · " + english : english.Substring(0, separator + 2) + chinese;
            }
            return english;
        }

        static string RichGraphLabel(string english, bool enabled, bool bilingual)
        {
            var translated = RichLabel(english, "graph-name", enabled, bilingual);
            if (translated != english || !enabled || richText == null || string.IsNullOrEmpty(english)) return translated;
            foreach (var name in new[] { "Interpolated", "Polyline" })
            {
                if (!english.StartsWith(name + " ", StringComparison.Ordinal) || !english.EndsWith(" points", StringComparison.Ordinal)) continue;
                int count;
                if (int.TryParse(english.Substring(name.Length + 1, english.Length - name.Length - 8), out count) && count >= 3 && count <= 10)
                {
                    var chinese = richText.Find(name, "graph-name");
                    if (chinese != null) return bilingual ? chinese + " " + count + " 点 · " + english : chinese + " " + count + " 点";
                }
            }
            return english;
        }

        internal static bool Lookup(IGH_DocumentObject component, out string translated, out string originalNickname)
        {
            translated = null; originalNickname = null;
            OriginalDescription original;
            if (!Enabled || catalog == null || !OriginalForObject(component, out original)) return false;
            var text = ComponentName(original);
            if (text == null) return false;
            translated = Format(text, original.Name); originalNickname = original.Nickname; return true;
        }

        static string ToolbarLabel(string english, bool enabled, bool bilingual)
        {
            if (string.IsNullOrEmpty(english)) return english;
            string chinese;
            if (!enabled || !toolbarText.TryGetValue(english, out chinese)) return english;
            return bilingual ? chinese + " · " + english : chinese;
        }

        static string CanvasLabel(string english, bool enabled, bool bilingual)
        {
            if (string.IsNullOrEmpty(english)) return english;
            string chinese;
            if (!enabled || !canvasText.TryGetValue(english, out chinese)) return english;
            return bilingual ? chinese + " · " + english : chinese;
        }

        static string RavenLabel(string english, bool enabled, bool bilingual)
        {
            if (!enabled || string.IsNullOrEmpty(english)) return english;
            string chinese;
            if (!ravenText.TryGetValue(english, out chinese))
            {
                chinese = null;
                foreach (var pair in new[] {
                    new[] { "Unlock all in this workspace (", "解锁此工作区中的全部对象（", ")", "）" },
                    new[] { "Lock gates (", "锁定入口/出口（", ")", "）" },
                    new[] { "Locked by ", "锁定来源：", "", "" },
                    new[] { "Protected by ", "保护来源：", "", "" }
                })
                {
                    if (english.Length <= pair[0].Length + pair[2].Length ||
                        !english.StartsWith(pair[0], StringComparison.Ordinal) || !english.EndsWith(pair[2], StringComparison.Ordinal)) continue;
                    chinese = pair[1] + english.Substring(pair[0].Length, english.Length - pair[0].Length - pair[2].Length) + pair[3];
                    break;
                }
                if (chinese == null) return english;
            }
            return bilingual ? chinese + " · " + english : chinese;
        }

        static void TranslateCanvasTooltip(object sender, GH_TooltipDisplayEventArgs args)
        {
            if (!Enabled || !args.Valid || !(args.Control is GH_Canvas)) return;
            var canvas = (GH_Canvas)args.Control;
            if (canvas.Document != null)
            {
                var point = canvas.Viewport.UnprojectPoint(new PointF(args.Point.X, args.Point.Y));
                var attributes = canvas.Document.FindAttribute(point, false);
                var owner = attributes == null ? null : attributes.GetTopLevel.DocObject;
                if (owner != null && IsPufferfish(owner))
                {
                    TranslatePufferfishTooltip(args);
                    return;
                }
                if (IsRich(owner))
                {
                    TranslateRichTooltip(args);
                    return;
                }
            }
            if (args.Title == "Raven Zones Editor" || args.Title == "Raven Search")
            {
                args.Title = RavenLabel(args.Title, Enabled, Bilingual);
                args.Text = RavenLabel(args.Text, Enabled, Bilingual);
                args.Description = RavenLabel(args.Description, Enabled, Bilingual);
                return;
            }
            args.Title = CanvasLabel(args.Title, Enabled, Bilingual);
            args.Text = CanvasLabel(args.Text, Enabled, Bilingual);
            args.Description = CanvasLabel(args.Description, Enabled, Bilingual);
        }

        static string PufferfishTooltipTitle(string english)
        {
            string access = "";
            string name = english;
            if (name.EndsWith(" as list", StringComparison.Ordinal)) { access = "（列表）"; name = name.Substring(0, name.Length - 8); }
            else if (name.EndsWith(" as tree", StringComparison.Ordinal)) { access = "（数据树）"; name = name.Substring(0, name.Length - 8); }
            var nickname = "";
            int separator = name.LastIndexOf(" (", StringComparison.Ordinal);
            if (separator >= 0 && name.EndsWith(")", StringComparison.Ordinal)) { nickname = name.Substring(separator); name = name.Substring(0, separator); }
            var translated = pufferfishNames.Find(name, "port-name") ?? pufferfishNames.Find(name, "Pufferfish");
            return translated == null ? name + nickname + access : Bilingual ? translated + " · " + english : translated + nickname + access;
        }

        static string PufferfishTooltipText(string english, string category)
        {
            var translated = pufferfishText.Find(english, category) ?? pufferfishText.Find(english, "description") ?? pufferfishText.Find(english, "runtime");
            if (translated != null) return Format(translated, english);
            if (string.IsNullOrEmpty(english)) return english;
            var lines = english.Replace("\r\n", "\n").Split('\n');
            bool changed = false;
            for (int i = 0; i < lines.Length; i++)
            {
                var original = lines[i].Trim();
                var runtime = pufferfishText.Find(original, "runtime");
                if (runtime == null) continue;
                lines[i] = Format(runtime, original);
                changed = true;
            }
            return changed ? string.Join(Environment.NewLine, lines) : english;
        }

        static void TranslatePufferfishTooltip(GH_TooltipDisplayEventArgs args)
        {
            args.Title = PufferfishTooltipTitle(args.Title);
            args.Text = PufferfishTooltipText(args.Text, "port-description");
            args.Description = PufferfishTooltipText(args.Description, "port-description");
        }

        static string RichTooltipTitle(string english)
        {
            if (string.IsNullOrEmpty(english) || richText == null) return english;
            string access = "", name = english;
            if (name.EndsWith(" as list", StringComparison.Ordinal)) { access = "（列表）"; name = name.Substring(0, name.Length - 8); }
            else if (name.EndsWith(" as tree", StringComparison.Ordinal)) { access = "（数据树）"; name = name.Substring(0, name.Length - 8); }
            string nickname = "";
            int separator = name.LastIndexOf(" (", StringComparison.Ordinal);
            if (separator >= 0 && name.EndsWith(")", StringComparison.Ordinal))
            {
                nickname = name.Substring(separator); name = name.Substring(0, separator);
            }
            var translated = richText.Find(name, "port-name") ?? richText.Find(name, "component");
            if (translated == null) return english;
            return Bilingual ? translated + " · " + english : translated + nickname + access;
        }

        static string RichTooltipText(string english)
        {
            if (string.IsNullOrEmpty(english) || richText == null) return english;
            var translated = richText.Find(english, "port-description") ?? richText.Find(english, "description") ?? richText.Find(english, "runtime") ?? richText.Find(english, "graph-description");
            if (translated != null) return Format(translated, english);
            var lines = english.Replace("\r\n", "\n").Split('\n');
            bool changed = false;
            for (int i = 0; i < lines.Length; i++)
            {
                var original = lines[i].Trim();
                var desired = RichRuntimeLabel(original, Enabled, Bilingual);
                if (desired == original) continue;
                lines[i] = desired; changed = true;
            }
            return changed ? string.Join(Environment.NewLine, lines) : english;
        }

        internal static void TranslateRichTooltip(GH_TooltipDisplayEventArgs args)
        {
            if (!Enabled) return;
            args.Title = RichTooltipTitle(args.Title);
            args.Text = RichTooltipText(args.Text);
            args.Description = RichTooltipText(args.Description);
        }

        static void ObserveCanvasTooltip(GH_Canvas canvas)
        {
            GH_TooltipComponent previous;
            var current = canvasTooltip.GetValue(canvas) as GH_TooltipComponent;
            if (canvasTooltips.TryGetValue(canvas, out previous) && previous == current) return;
            if (previous != null) previous.PopulateTooltip -= TranslateCanvasTooltip;
            canvasTooltips[canvas] = current;
            if (current != null) current.PopulateTooltip += TranslateCanvasTooltip;
        }

        static void ForgetCanvasTooltip(GH_Canvas canvas)
        {
            GH_TooltipComponent previous;
            if (!canvasTooltips.TryGetValue(canvas, out previous)) return;
            if (previous != null) previous.PopulateTooltip -= TranslateCanvasTooltip;
            canvasTooltips.Remove(canvas);
        }

        static void ObserveCanvasTooltips()
        {
            foreach (var canvas in canvases) ObserveCanvasTooltip(canvas);
        }

        static void ApplyRavenText(RavenTextProperty property)
        {
            var current = property.Get();
            if (current != property.Desired) property.Original = current;
            var desired = RavenLabel(property.Original, Enabled, Bilingual);
            property.Desired = desired;
            if (current != desired) property.Set(desired);
        }

        static void CaptureRavenSearchControl(Eto.Forms.Control control, List<RavenTextProperty> properties)
        {
            if (control.ID == "search-query")
            {
                var query = control as Eto.Forms.TextBox;
                if (query != null) properties.Add(new RavenTextProperty { Get = () => query.PlaceholderText, Set = value => query.PlaceholderText = value });
            }
            if (control.ID == "search-lock" || control.ID == "search-back" || control.ID == "search-forward" || control.ID == "search-status")
            {
                var text = control as Eto.Forms.TextControl;
                if (text != null)
                {
                    var property = new RavenTextProperty { Get = () => text.Text, Set = value => text.Text = value };
                    properties.Add(property);
                    ApplyRavenText(property);
                    text.TextChanged += delegate { ApplyRavenText(property); };
                }
                properties.Add(new RavenTextProperty { Get = () => control.ToolTip, Set = value => control.ToolTip = value });
            }
            var container = control as Eto.Forms.Container;
            if (container != null)
                foreach (var child in container.Children) CaptureRavenSearchControl(child, properties);
        }

        static void ObserveRavenSearch()
        {
            var application = Eto.Forms.Application.Instance;
            if (application == null) return;
            foreach (var window in application.Windows)
            {
                List<RavenTextProperty> properties;
                if (!ravenSearchWindows.TryGetValue(window, out properties))
                {
                    if (window.Title != "Raven Search") continue;
                    properties = new List<RavenTextProperty>();
                    properties.Add(new RavenTextProperty { Get = () => window.Title, Set = value => window.Title = value });
                    CaptureRavenSearchControl(window, properties);
                    ravenSearchWindows.Add(window, properties);
                    window.Closed += delegate { ravenSearchWindows.Remove(window); };
                }
                foreach (var property in properties) ApplyRavenText(property);
            }
        }

        static void CaptureRavenMenus(ToolStripItemCollection items)
        {
            foreach (ToolStripItem item in items)
            {
                if (!ravenMenuProperties.ContainsKey(item) &&
                    (RavenLabel(item.Text, true, false) != item.Text || RavenLabel(item.ToolTipText, true, false) != item.ToolTipText))
                {
                    ravenMenuProperties.Add(item, new List<RavenTextProperty> {
                        new RavenTextProperty { Get = () => item.Text, Set = value => item.Text = value },
                        new RavenTextProperty { Get = () => item.ToolTipText, Set = value => item.ToolTipText = value }
                    });
                    item.Disposed += delegate { ravenMenuProperties.Remove(item); };
                    var dropdown = item as ToolStripDropDownItem;
                    if (dropdown != null)
                    {
                        dropdown.DropDownOpening += delegate { CaptureRavenMenus(dropdown.DropDownItems); TranslateRavenMenus(); };
                        dropdown.DropDownOpened += delegate { CaptureRavenMenus(dropdown.DropDownItems); TranslateRavenMenus(); };
                    }
                }
                var child = item as ToolStripDropDownItem;
                if (child != null) CaptureRavenMenus(child.DropDownItems);
            }
        }

        static void TranslateRavenMenus()
        {
            foreach (var pair in ravenMenuProperties)
            {
                if (pair.Key.IsDisposed) continue;
                foreach (var property in pair.Value) ApplyRavenText(property);
            }
        }

        static GH_Toolstrip FindToolbar(Control parent)
        {
            var result = parent as GH_Toolstrip;
            if (result != null) return result;
            foreach (Control child in parent.Controls) { result = FindToolbar(child); if (result != null) return result; }
            return null;
        }

        static void RefreshToolbar()
        {
            if (canvasToolbar == null || canvasToolbar.IsDisposed) canvasToolbar = FindToolbar(editor);
            if (canvasToolbar == null) return;
            foreach (ToolStripItem item in canvasToolbar.Items)
            {
                string english;
                if (!toolbarOriginals.TryGetValue(item, out english)) continue;
                string current = item.ToolTipText;
                string previous;
                if (current != english && (!toolbarDesired.TryGetValue(item, out previous) || current != previous))
                {
                    english = current;
                    toolbarOriginals[item] = current;
                }
                string desired = ToolbarLabel(english, Enabled, Bilingual);
                if (current != desired) item.ToolTipText = desired;
                toolbarDesired[item] = desired;
                string originalName;
                if (toolbarNames.TryGetValue(item, out originalName))
                {
                    var desiredName = ToolbarLabel(originalName, Enabled, Bilingual);
                    if (item.Text != desiredName) item.Text = desiredName;
                }
            }
        }

        static void CaptureToolbar()
        {
            if (canvasToolbar == null || canvasToolbar.IsDisposed) canvasToolbar = FindToolbar(editor);
            if (canvasToolbar == null) return;
            foreach (ToolStripItem item in canvasToolbar.Items)
            {
                if (!toolbarOriginals.ContainsKey(item))
                {
                    toolbarOriginals.Add(item, item.ToolTipText);
                    if (item is ToolStripButton || item is ToolStripSplitButton || item is ToolStripDropDownButton)
                        toolbarNames.Add(item, item.Text);
                    item.Disposed += delegate { toolbarOriginals.Remove(item); toolbarDesired.Remove(item); toolbarNames.Remove(item); };
                }
                var dropdown = item as ToolStripDropDownItem;
                if (dropdown == null || !observedToolbarMenus.Add(dropdown)) continue;
                CaptureMenus(dropdown.DropDownItems);
                dropdown.DropDownOpening += delegate { CaptureMenus(dropdown.DropDownItems); TranslateMenus(); };
                dropdown.DropDownOpened += delegate { CaptureMenus(dropdown.DropDownItems); TranslateMenus(); };
                dropdown.Disposed += delegate { observedToolbarMenus.Remove(dropdown); };
            }
            RefreshToolbar();
        }

        static void ObserveCanvasMenu(GH_Canvas canvas)
        {
            var menu = canvas.ContextMenuStrip;
            if (menu == null || !canvasMenus.Add(menu)) return;
            menu.Opening += delegate { CaptureCanvasMenu(menu, canvas); };
            menu.Opened += delegate { CaptureCanvasMenu(menu, canvas); };
            menu.Disposed += delegate { canvasMenus.Remove(menu); };
        }

        static void CaptureCanvasMenu(ContextMenuStrip menu, GH_Canvas canvas)
        {
            if (IsRavenPopup(menu.Items)) { CaptureRavenMenus(menu.Items); TranslateRavenMenus(); return; }
            CaptureMenusForObject(menu.Items, menuCanvas == canvas ? menuObjectGuid : Guid.Empty);
            TranslateMenus();
        }

        static void RefreshCanvasMenus()
        {
            foreach (var canvas in canvases) ObserveCanvasMenu(canvas);
            ObserveCanvasPopup();
        }

        static void ObserveCanvasPopup()
        {
            EnumThreadWindows(GetCurrentThreadId(), delegate(IntPtr handle, IntPtr unused)
            {
                var popup = Control.FromHandle(handle) as ToolStripDropDownMenu;
                if (popup == null || !popup.Visible) return true;
                if (preparedMenus.Contains(popup)) return true;
                if (IsCanvasPopup(popup.Items) && canvasPopups.Add(popup))
                {
                    CaptureMenus(popup.Items);
                    TranslateMenus();
                    popup.Disposed += delegate { canvasPopups.Remove(popup); };
                }
                else if (IsRavenPopup(popup.Items) || ravenPopups.Contains(popup))
                {
                    if (ravenPopups.Add(popup)) popup.Disposed += delegate { ravenPopups.Remove(popup); };
                    CaptureRavenMenus(popup.Items);
                    TranslateRavenMenus();
                }
                else if (IsCompassPopup(popup.Items) && widgetPopups.Add(popup))
                {
                    CaptureMenus(popup.Items);
                    TranslateMenus();
                    popup.Disposed += delegate { widgetPopups.Remove(popup); };
                }
                return true;
            }, IntPtr.Zero);
        }

        static void ObserveMenuPopups()
        {
            EnumThreadWindows(GetCurrentThreadId(), delegate(IntPtr handle, IntPtr unused)
            {
                var popup = Control.FromHandle(handle) as ToolStripDropDown;
                if (popup == null || !popup.Visible || ravenPopups.Contains(popup) || preparedMenus.Contains(popup)) return true;
                if (popup.OwnerItem != null && menuOriginals.ContainsKey(popup.OwnerItem))
                {
                    CaptureMenusForDescription(popup.Items, menuOwners[popup.OwnerItem], menuDescriptions[popup.OwnerItem]);
                    TranslateMenus();
                }
                else if (popup.OwnerItem == null && IsNativeComponentMenu(popup))
                {
                    CaptureMenusForObject(popup.Items, menuObjectGuid);
                    TranslateMenus();
                }
                return true;
            }, IntPtr.Zero);
        }

        static bool IsNativeComponentMenu(ToolStripDropDown popup)
        {
            return popup.Items.Count > 0 && menuCanvas != null && !menuCanvas.IsDisposed &&
                menuCanvas.Document != null && menuObjectGuid != Guid.Empty &&
                contextObject != null &&
                menuCanvas.RectangleToScreen(menuCanvas.ClientRectangle).Contains(Cursor.Position);
        }

        static bool IsCanvasPopup(ToolStripItemCollection items)
        {
            bool previewOn = false, previewOff = false, lockSolver = false;
            foreach (ToolStripItem item in items)
            {
                previewOn |= item.Text == "Preview On" || item.Text == "开启预览";
                previewOff |= item.Text == "Preview Off" || item.Text == "关闭预览";
                lockSolver |= item.Text == "Lock Solver" || item.Text == "锁定求解器";
            }
            return previewOn && previewOff && lockSolver;
        }

        static bool IsRavenPopup(ToolStripItemCollection items)
        {
            bool lockSelection = false, removeLocks = false, reference = false;
            foreach (ToolStripItem item in items)
            {
                if (ravenMenuProperties.ContainsKey(item)) return true;
                if (item.Text == "Hide Raven Zones Editor" || item.Text == "Hide Raven Search" ||
                    item.Text == "Select components or groups to lock" ||
                    item.Text.StartsWith("Unlock all in this workspace (", StringComparison.Ordinal)) return true;
                lockSelection |= item.Text == "Lock selection from Raven";
                removeLocks |= item.Text == "Remove own Raven locks";
                reference |= item.Text == "Allow Raven to reference outputs";
            }
            return lockSelection && removeLocks || reference && removeLocks;
        }

        static bool IsCompassPopup(ToolStripItemCollection items)
        {
            bool hide = false, bubbles = false, selected = false;
            foreach (ToolStripItem item in items)
            {
                hide |= item.Text == "Hide Compass" || item.Text == "隐藏指南针";
                bubbles |= item.Text == "Draw object bubbles" || item.Text == "绘制对象气泡";
                selected |= item.Text == "Only draw selected objects" || item.Text == "仅绘制所选对象";
            }
            return hide && bubbles && selected;
        }

        delegate IntPtr WindowHook(int code, IntPtr wParam, IntPtr lParam);
        [DllImport("user32.dll", SetLastError = true)]
        static extern IntPtr SetWindowsHookEx(int id, WindowHook callback, IntPtr module, uint thread);
        [DllImport("user32.dll")]
        static extern IntPtr CallNextHookEx(IntPtr hook, int code, IntPtr wParam, IntPtr lParam);
        [DllImport("user32.dll")]
        static extern bool UnhookWindowsHookEx(IntPtr hook);

        [StructLayout(LayoutKind.Sequential)]
        struct WindowMessageData
        {
            internal IntPtr LParam, WParam;
            internal uint Message;
            internal IntPtr Handle;
        }

        static IntPtr WindowMessage(int code, IntPtr wParam, IntPtr lParam)
        {
            if (code >= 0 && !preparingWindow)
            {
                preparingWindow = true;
                try
                {
                    var message = (WindowMessageData)Marshal.PtrToStructure(lParam, typeof(WindowMessageData));
                    if (message.Message == 0x18 && message.WParam != IntPtr.Zero || message.Message == 0x46 || message.Message == 0x47 || message.Message == 0x0F)
                        PrepareWindow(Control.FromHandle(message.Handle));
                }
                catch (Exception ex) { Log(ex); }
                finally { preparingWindow = false; }
            }
            return CallNextHookEx(windowHookHandle, code, wParam, lParam);
        }

        static void PrepareWindow(Control control)
        {
            var popup = control as ToolStripDropDown;
            if (popup != null) { PreparePopup(popup); return; }
            var form = control as Form ?? (control == null ? null : control.FindForm());
            if (form != null && !PrepareGraphEditor(form)) PrepareTutorial(form);
        }

        internal static bool PrepareGraphEditor(Form form)
        {
            var editorType = graphEditorType;
            if (form == null || editorType == null || form.GetType() != editorType) return false;
            var container = graphEditorGraph == null ? null : graphEditorGraph.GetValue(form, null) as Grasshopper.Kernel.Graphs.GH_GraphContainer;
            bool rich = container != null && container.Graph != null && container.Graph.GetType().Assembly.GetName().Name == "RichedGraphMapper" && richGraphs.ContainsKey(container.Graph.GraphTypeID);
            List<RavenTextProperty> properties;
            if (!richEditorForms.TryGetValue(form, out properties))
            {
                if (!rich) return false;
                properties = new List<RavenTextProperty>();
                properties.Add(new RavenTextProperty { Get = () => form.Text, Set = value => form.Text = value });
                foreach (string name in new[] { "_btnOK", "_btnCancel" })
                {
                    var field = editorType.GetField(name, BindingFlags.Instance | BindingFlags.NonPublic);
                    var button = field == null ? null : field.GetValue(form) as Button;
                    if (button != null) properties.Add(new RavenTextProperty { Get = () => button.Text, Set = value => button.Text = value });
                }
                foreach (string name in new[] { "_numX0", "_numX1", "_numY0", "_numY1" })
                {
                    var field = editorType.GetField(name, BindingFlags.Instance | BindingFlags.NonPublic);
                    var scroller = field == null ? null : field.GetValue(form);
                    var prefix = scroller == null ? null : scroller.GetType().GetProperty("Prefix", BindingFlags.Instance | BindingFlags.Public);
                    if (prefix != null && prefix.PropertyType == typeof(string) && prefix.CanRead && prefix.CanWrite)
                        properties.Add(new RavenTextProperty { Get = () => (string)prefix.GetValue(scroller, null), Set = value => prefix.SetValue(scroller, value, null) });
                }
                richEditorForms.Add(form, properties);
                form.Disposed += delegate { richEditorForms.Remove(form); };
            }
            foreach (var property in properties)
            {
                var current = property.Get();
                if (current != property.Desired) property.Original = current;
                string original = property.Original;
                int start = string.IsNullOrEmpty(original) ? 0 : original.Length - original.TrimStart().Length;
                int end = string.IsNullOrEmpty(original) ? 0 : original.Length - original.TrimEnd().Length;
                string text = string.IsNullOrEmpty(original) ? original : original.Trim();
                var desired = RichLabel(text, "editor", rich && Enabled, Bilingual);
                if (desired != text) desired = original.Substring(0, start) + desired + original.Substring(original.Length - end);
                else desired = original;
                property.Desired = desired;
                if (current != desired) property.Set(desired);
            }
            return true;
        }

        static bool PreparePopup(ToolStripDropDown popup)
        {
            if (popup.Items.Count == 0) return false;
            Guid owner = Guid.Empty;
            if (IsRavenPopup(popup.Items))
            {
                CaptureRavenMenus(popup.Items);
                TranslateRavenMenus();
            }
            else
            {
                if (popup.OwnerItem != null && menuOwners.ContainsKey(popup.OwnerItem))
                {
                    owner = menuOwners[popup.OwnerItem];
                    CaptureMenusForDescription(popup.Items, owner, menuDescriptions[popup.OwnerItem]);
                    TranslateMenus();
                }
                else
                {
                    if (IsNativeComponentMenu(popup)) owner = menuObjectGuid;
                    else if (!IsCanvasPopup(popup.Items) && !IsCompassPopup(popup.Items)) return false;
                    CaptureMenusForObject(popup.Items, owner);
                    TranslateMenus();
                }
            }
            if (preparedMenus.Add(popup))
            {
                popup.Opening += delegate { PreparePopup(popup); };
                popup.Disposed += delegate { preparedMenus.Remove(popup); };
            }
            return true;
        }

        static string TutorialLabel(string english, bool enabled, bool bilingual)
        {
            string chinese;
            if (!enabled || english == null || !tutorialText.TryGetValue(english, out chinese)) return english;
            return bilingual ? chinese + " · " + english : chinese;
        }

        static void CaptureTutorialControls(Control control, Dictionary<Control, string> originals)
        {
            if (control is Form || control is Label || control is CheckBox)
                if (!originals.ContainsKey(control)) originals.Add(control, control.Text);
            foreach (Control child in control.Controls) CaptureTutorialControls(child, originals);
        }

        static bool PrepareTutorial(Form form)
        {
            Dictionary<Control, string> originals;
            if (!tutorialForms.TryGetValue(form, out originals))
            {
                if (form.Text != "Getting started with Grasshopper…") return false;
                originals = new Dictionary<Control, string>();
                tutorialForms.Add(form, originals);
                form.Disposed += delegate { tutorialForms.Remove(form); };
            }
            CaptureTutorialControls(form, originals);
            foreach (var pair in originals)
            {
                var translated = TutorialLabel(pair.Value, Enabled, Bilingual);
                if (pair.Key.Text != translated) pair.Key.Text = translated;
            }
            return true;
        }

        delegate bool WindowCallback(IntPtr handle, IntPtr unused);
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        static extern bool EnumThreadWindows(uint threadId, WindowCallback callback, IntPtr unused);
        [System.Runtime.InteropServices.DllImport("kernel32.dll")]
        static extern uint GetCurrentThreadId();

        static string MenuLabel(string english, bool enabled, bool bilingual)
        { return MenuLabelForObject(english, enabled, bilingual, Guid.Empty); }

        static string MenuLabelForObject(string english, bool enabled, bool bilingual, Guid owner)
        {
            OriginalDescription original;
            originals.TryGetValue(owner, out original);
            return MenuLabelForDescription(english, enabled, bilingual, original);
        }

        static string MenuLabelForDescription(string english, bool enabled, bool bilingual, OriginalDescription original)
        {
            if (!enabled) return english;
            if (original != null && original.AssemblyName == "RichedGraphMapper")
            {
                var rich = RichLabel(english, "menu", enabled, bilingual);
                if (rich != english) return rich;
                rich = RichRuntimeLabel(english, enabled, bilingual);
                if (rich != english) return rich;
            }
            Catalog names = original != null && original.AssemblyName == "RichedGraphMapper" ? richText : original != null && original.AssemblyName == "Pufferfish" ? pufferfishNames : catalog;
            if (original != null && names != null)
            {
                var specific = names.Find(english, "port-name");
                if (specific != null) return bilingual ? specific + " · " + english : specific;
                if (original != null && original.AssemblyName == "Pufferfish")
                {
                    var runtime = pufferfishText.Find(english, "runtime");
                    if (runtime == null)
                    {
                        int separator = english.IndexOf(". ", StringComparison.Ordinal);
                        int number;
                        if (separator > 0 && int.TryParse(english.Substring(0, separator), out number))
                        {
                            var message = english.Substring(separator + 2);
                            var translated = pufferfishText.Find(message, "runtime");
                            if (translated != null) runtime = english.Substring(0, separator + 2) + translated;
                        }
                    }
                    if (runtime != null) return bilingual ? runtime + " · " + english : runtime;
                }
            }
            foreach (var prefix in new[] { "Input: ", "Output: " })
            {
                if (!english.StartsWith(prefix, StringComparison.Ordinal)) continue;
                var port = english.Substring(prefix.Length);
                var translated = names == null ? null : names.Find(port, "port-name");
                var label = (prefix == "Input: " ? "输入：" : "输出：") + (translated ?? port);
                return bilingual ? label + " · " + english : label;
            }
            if (english.StartsWith("Set one ", StringComparison.OrdinalIgnoreCase) && english.Length > "Set one ".Length)
            {
                var name = english.Substring("Set one ".Length);
                var translated = names == null ? null : names.Find(name, "port-name");
                var label = "设置一个" + (translated ?? name);
                return bilingual ? label + " · " + english : label;
            }
            if (english.StartsWith("Set Multiple ", StringComparison.OrdinalIgnoreCase) && english.Length > "Set Multiple ".Length)
            {
                var plural = english.Substring("Set Multiple ".Length);
                var name = plural.EndsWith("s", StringComparison.OrdinalIgnoreCase) ? plural.Substring(0, plural.Length - 1) : plural;
                var translated = names == null ? null : names.Find(name, "port-name");
                var label = "设置多个" + (translated ?? plural);
                return bilingual ? label + " · " + english : label;
            }
            string key = english.Replace("&", "").Trim().TrimEnd('.', '…');
            if (key.StartsWith("Manage ", StringComparison.OrdinalIgnoreCase) && key.EndsWith(" collection", StringComparison.OrdinalIgnoreCase))
            {
                var noun = key.Substring(7, key.Length - " collection".Length - 7);
                var translated = names == null ? null : names.Find(noun, "port-name");
                var label = "管理" + (translated ?? noun) + "集合";
                return bilingual ? label + " · " + key : label;
            }
            string chinese;
            if (!menuText.TryGetValue(key, out chinese)) return english;
            int access = english.IndexOf('&');
            string accelerator = access >= 0 && access + 1 < english.Length ? " (&" + english[access + 1] + ")" : "";
            string ellipsis = english.EndsWith("...") ? "..." : english.EndsWith("…") ? "…" : "";
            return (bilingual ? chinese + " · " + key : chinese) + accelerator + ellipsis;
        }

        static bool IsRichGraphTag(object tag)
        {
            if (tag is Guid) return richGraphs.ContainsKey((Guid)tag);
            var proxy = tag as GH_GraphProxy;
            return proxy != null && proxy.Type != null && proxy.Type.Assembly.GetName().Name == "RichedGraphMapper" && richGraphs.ContainsKey(proxy.GUID);
        }

        static bool ContainsRichGraphItems(ToolStripItemCollection items)
        {
            foreach (ToolStripItem item in items)
            {
                if (IsRichGraphTag(item.Tag)) return true;
                var menu = item as ToolStripMenuItem;
                if (menu != null && ContainsRichGraphItems(menu.DropDownItems)) return true;
            }
            return false;
        }

        internal static string RichMenuLabel(ToolStripItem item, string english, bool enabled, bool bilingual, OriginalDescription original)
        {
            if (!enabled || item == null || string.IsNullOrEmpty(english)) return english;
            bool richOwner = original != null && original.AssemblyName == "RichedGraphMapper";
            bool richPointItem = richOwner && item.Tag is int && (int)item.Tag >= 3 && (int)item.Tag <= 10 &&
                (english.StartsWith("Interpolated", StringComparison.Ordinal) || english.StartsWith("Polyline", StringComparison.Ordinal));
            if (richPointItem || IsRichGraphTag(item.Tag))
            {
                var graph = RichGraphLabel(english, enabled, bilingual);
                if (graph != english) return graph;
            }
            var parent = item as ToolStripMenuItem;
            if (parent != null && english == "Graph types" && ContainsRichGraphItems(parent.DropDownItems))
            {
                var translated = RichLabel(english, "menu", enabled, bilingual);
                if (translated != english) return translated;
            }
            return MenuLabelForDescription(english, enabled, bilingual, original);
        }

        static void CaptureMenus(ToolStripItemCollection items)
        { CaptureMenusForObject(items, Guid.Empty); }

        static void CaptureMenusForObject(ToolStripItemCollection items, Guid owner)
        {
            OriginalDescription description;
            if (!originals.TryGetValue(owner, out description) && owner == menuObjectGuid && contextObject != null)
                OriginalForObject(contextObject, out description);
            CaptureMenusForDescription(items, owner, description);
        }

        static void CaptureMenusForDescription(ToolStripItemCollection items, Guid owner, OriginalDescription description)
        {
            foreach (ToolStripItem item in items)
            {
                if (item.Name == "GrasshopperChineseMenu" || ravenMenuProperties.ContainsKey(item)) continue;
                if (!menuOriginals.ContainsKey(item))
                {
                    menuOriginals.Add(item, item.Text);
                    menuOwners.Add(item, owner);
                    menuDescriptions.Add(item, description);
                    if ((description != null && description.AssemblyName == "RichedGraphMapper") || IsRichGraphTag(item.Tag)) richMenuTooltips[item] = item.ToolTipText;
                    item.Disposed += delegate { menuOriginals.Remove(item); menuOwners.Remove(item); menuDescriptions.Remove(item); richMenuTooltips.Remove(item); };
                    var dropdown = item as ToolStripMenuItem;
                    if (dropdown != null)
                    {
                        dropdown.DropDownOpening += delegate { CaptureMenusForDescription(dropdown.DropDownItems, owner, description); TranslateMenus(); };
                        dropdown.DropDownOpened += delegate { CaptureMenusForDescription(dropdown.DropDownItems, owner, description); TranslateMenus(); };
                    }
                }
                var menu = item as ToolStripMenuItem;
                if (menu != null) CaptureMenusForDescription(menu.DropDownItems, owner, description);
            }
        }

        static void TranslateMenus()
        {
            foreach (var pair in menuOriginals)
            {
                if (pair.Key.IsDisposed || ravenMenuProperties.ContainsKey(pair.Key)) continue;
                string desired = RichMenuLabel(pair.Key, pair.Value, Enabled, Bilingual, menuDescriptions[pair.Key]);
                if (pair.Key.Text != desired) pair.Key.Text = desired;
                string tooltip;
                if (richMenuTooltips.TryGetValue(pair.Key, out tooltip))
                {
                    var translated = IsRichGraphTag(pair.Key.Tag) ? RichLabel(tooltip, "graph-description", Enabled, Bilingual) : RichLabel(tooltip, "menu", Enabled, Bilingual);
                    if (pair.Key.ToolTipText != translated) pair.Key.ToolTipText = translated;
                }
            }
        }

        static void Update()
        {
            try
            {
                foreach (var canvas in canvases) EndDisplayNames(canvas);
                GH_Tooltip.Clear();
                CaptureMenus(editor.MainMenuStrip.Items);
                foreach (var original in originals.Values)
                    ApplyProxyDescription(original.Proxy);
                TranslateMenus();
                TranslateRavenMenus();
                foreach (var form in new List<Form>(tutorialForms.Keys)) PrepareTutorial(form);
                foreach (var form in new List<Form>(richEditorForms.Keys)) PrepareGraphEditor(form);
                ObserveRavenSearch();
                CaptureToolbar();
                RefreshToolbar();
                ObserveMenuPopups();
                RefreshRibbon();
                foreach (var dropdown in observedDropdowns) UpdateDropdown(dropdown);
                RefreshCanvasMenus();
                foreach (var canvas in canvases) { Observe(canvas); canvas.Refresh(); }
                editor.Refresh();
                settings.SetValue("Enabled", Enabled);
                settings.SetValue("Bilingual", Bilingual);
                settings.WritePersistentSettings();
            }
            catch (Exception ex) { Log(ex); }
        }

        internal static void AddRichDisplayScopes(IGH_Component component, List<TextScope> scopes)
        {
            if (!Enabled || !IsRich(component) || richText == null) return;
            OriginalDescription original;
            if (!OriginalForObject(component, out original)) return;
            var description = richText.Find(original.Description, "description");
            if (description != null) scopes.Add(new TextScope(() => component.Description, value => component.Description = value, Format(description, original.Description)));
            var nickname = richText.Find(original.Nickname, "nickname");
            if (nickname != null) scopes.Add(new TextScope(() => component.NickName, value => component.NickName = value,
                DisplayText.Nickname(component.NickName, original.Nickname, Format(nickname, original.Nickname))));
            var concrete = component as GH_Component;
            if (concrete != null && concrete.Message == "Remap")
                scopes.Add(new TextScope(() => concrete.Message, value => concrete.Message = value, RichLabel("Remap", "runtime", Enabled, Bilingual)));
            foreach (var ports in new[] { component.Params.Input, component.Params.Output })
            {
                foreach (var port in ports)
                {
                    string name = port.Name, text = port.Description;
                    string defaultNickname = name == "Values" ? "V" : name == "Source" ? "S" : name == "Target" ? "T" : null;
                    var translatedName = richText.Find(name, "port-name");
                    var translatedDescription = richText.Find(text, "port-description");
                    if (translatedName != null) scopes.Add(new TextScope(() => port.Name, value => port.Name = value, Format(translatedName, name)));
                    if (translatedDescription != null) scopes.Add(new TextScope(() => port.Description, value => port.Description = value, Format(translatedDescription, text)));
                    if (defaultNickname != null)
                    {
                        var translatedNickname = richText.Find(defaultNickname, "nickname");
                        if (translatedNickname != null) scopes.Add(new TextScope(() => port.NickName, value => port.NickName = value,
                            DisplayText.Nickname(port.NickName, defaultNickname, Format(translatedNickname, defaultNickname))));
                    }
                }
            }
        }

        static void BeginDisplayNames(GH_Canvas canvas)
        {
            EndDisplayNames(canvas);
            if (!Enabled || canvas.Document == null) return;
            var scopes = new List<TextScope>();
            paintScopes[canvas] = scopes;
            try
            {
                foreach (var obj in canvas.Document.Objects)
                {
                    string text, nick;
                    if (Lookup(obj, out text, out nick))
                    {
                        scopes.Add(new TextScope(() => obj.Name, value => obj.Name = value, text));
                        var parameter = obj as IGH_Param;
                        if (parameter != null && parameter.Attributes != null && parameter.Attributes.GetType() == pointAttributes)
                            scopes.Add(new TextScope(() => parameter.NickName, value => parameter.NickName = value,
                                DisplayText.Nickname(parameter.NickName, nick, text)));
                        if (obj is Grasshopper.Kernel.Special.GH_Cluster && IsPufferfish(obj))
                            scopes.Add(new TextScope(() => obj.NickName, value => obj.NickName = value, DisplayText.Nickname(obj.NickName, nick, text)));
                        var richComponent = obj as IGH_Component;
                        if (richComponent != null) AddRichDisplayScopes(richComponent, scopes);
                    }
                }
            }
            catch (Exception ex) { EndDisplayNames(canvas); Log(ex); }
        }

        static void EndDisplayNames(GH_Canvas canvas)
        {
            List<TextScope> scopes;
            if (!paintScopes.TryGetValue(canvas, out scopes)) return;
            try { for (int i = scopes.Count - 1; i >= 0; i--) scopes[i].Dispose(); }
            finally { paintScopes.Remove(canvas); }
        }

        internal static string PortName(string name)
        { return Enabled && catalog != null ? catalog.Find(name, "port-name") : null; }

        internal static string PortDescription(string description)
        { return Enabled && toolText != null ? toolText.Find(description, "port-description") : null; }

        internal static bool IsPufferfish(IGH_DocumentObject component)
        {
            OriginalDescription original;
            return OriginalForObject(component, out original) && original.AssemblyName == "Pufferfish";
        }

        internal static string ComponentPortName(IGH_Component component, string name)
        {
            if (IsRich(component)) return Enabled && richText != null ? richText.Find(name, "port-name") : null;
            return IsPufferfish(component) ? Enabled ? pufferfishNames.Find(name, "port-name") : null : PortName(name);
        }

        internal static string ComponentPortDescription(IGH_Component component, string description)
        {
            if (IsRich(component)) return Enabled && richText != null ? richText.Find(description, "port-description") : null;
            return IsPufferfish(component) ? Enabled ? pufferfishText.Find(description, "port-description") : null : PortDescription(description);
        }

        internal static string Description(IGH_DocumentObject component)
        {
            OriginalDescription original;
            return Enabled && OriginalForObject(component, out original) ? ComponentDescription(original) : null;
        }

        static void ApplyProxyDescription(IGH_ObjectProxy proxy)
        {
            OriginalDescription original;
            if (proxy == null || !originals.TryGetValue(proxy.Guid, out original)) return;
            var name = Enabled ? ComponentName(original) : null;
            var desiredName = name == null ? original.Name : Format(name, original.Name);
            if (proxy.Desc.Name != desiredName) proxy.Desc.Name = desiredName;
            var description = Enabled ? ComponentDescription(original) : null;
            var desiredDescription = description == null ? original.Description : Format(description, original.Description);
            if (proxy.Desc.Description != desiredDescription) proxy.Desc.Description = desiredDescription;
        }

        static void UpdateDropdownLabel(Control child)
        {
            var label = child as GH_Label;
            var proxy = child.Tag as IGH_ObjectProxy;
            if (label == null || proxy == null || !originals.ContainsKey(proxy.Guid)) return;
            ApplyProxyDescription(proxy);
            var current = label.Text;
            int prefixLength = current.Length - current.TrimStart().Length;
            var desired = current.Substring(0, prefixLength) + proxy.Desc.Name;
            if (current != desired) label.Text = desired;
        }

        static void UpdateDropdown(GH_RibbonDropdown dropdown)
        {
            var content = dropdownContent.GetValue(dropdown) as Control;
            if (content == null) return;
            foreach (Control child in content.Controls) UpdateDropdownLabel(child);
        }

        static void ObserveDropdowns()
        {
            foreach (Form form in Application.OpenForms)
            {
                var dropdown = form as GH_RibbonDropdown;
                if (dropdown == null || !observedDropdowns.Add(dropdown)) continue;
                var content = dropdownContent.GetValue(dropdown) as Control;
                if (content != null) content.ControlAdded += delegate(object sender, ControlEventArgs args) { UpdateDropdownLabel(args.Control); };
                dropdown.Disposed += delegate { observedDropdowns.Remove(dropdown); };
                UpdateDropdown(dropdown);
            }
        }

        internal static string UsageText()
        {
            int count = 0;
            foreach (var pack in new[] { catalog, toolText, pufferfishNames, pufferfishText, richText })
                if (pack != null) count += pack.Count;
            return "Grasshopper 中文界面 0.3.1\n\n" +
                "已匹配原生、袋鼠、河豚和增强图形映射器的显示名称与说明。\n" +
                "关闭“显示 > 显示图标 / Display > Draw Icons”可查看文字标题。\n" +
                "增强图形映射器新建后需右键选择“图形类型”，再拖动控制点。\n" +
                "自定义昵称保留；未知插件及未收录文字可能保持英文。关闭汉化可恢复英文。\n\n" +
                "【刷新组件目录】\n" +
                "重新收集当前已加载且支持的组件，并重新应用现有离线词库。用于新增组件后刷新显示；不会下载词库、在线翻译或自动补译未知插件。\n\n" +
                "【导出组件及缺译清单】\n" +
                "选择保存位置后导出一份 JSON 文件：包含组件 GUID、分类、英文名称与说明、输入输出端口、已匹配译文及实例化错误。翻译字段为空表示未匹配译文；Error 表示提取实例失败，不代表已有译文有误。可用于整理和补充词库，不会自动翻译或修改 GH 文档，也不会分别导出两个文件。\n\n" +
                "词库条目：" + count + "（包含未逐条审核的上游转换译文）。\n" +
                "基于 MultilingualGH 的 MIT 翻译资源与加载入口开发。";
        }

        static void ExportCatalog()
        {
            using (var dialog = new SaveFileDialog { Filter = "JSON|*.json", FileName = "grasshopper-native-coverage.json" })
            {
                if (dialog.ShowDialog() != DialogResult.OK) return;
                var rows = new List<Catalog.ExportEntry>();
                foreach (var original in originals.Values)
                {
                    var row = new Catalog.ExportEntry { Guid = original.Proxy.Guid.ToString(), Name = original.Name, Category = original.Category, Description = original.Description,
                        Translation = ComponentName(original), DescriptionTranslation = ComponentDescription(original) };
                    try
                    {
                        var component = original.Proxy.CreateInstance() as IGH_Component;
                        if (component != null)
                        {
                            foreach (var p in component.Params.Input) row.Inputs.Add(p.Name + " | " + p.Description);
                            foreach (var p in component.Params.Output) row.Outputs.Add(p.Name + " | " + p.Description);
                        }
                    }
                    catch (Exception ex) { row.Error = ex.Message; }
                    rows.Add(row);
                }
                using (var stream = File.Create(dialog.FileName)) new System.Runtime.Serialization.Json.DataContractJsonSerializer(typeof(List<Catalog.ExportEntry>)).WriteObject(stream, rows);
            }
        }

        static GH_Ribbon FindRibbon(Control parent)
        {
            var result = parent as GH_Ribbon;
            if (result != null) return result;
            foreach (Control child in parent.Controls) { result = FindRibbon(child); if (result != null) return result; }
            return null;
        }

        static void TranslateProxyTooltip(IGH_ObjectProxy proxy, GH_TooltipDisplayEventArgs args)
        {
            OriginalDescription original;
            if (!Enabled || catalog == null || toolText == null || proxy == null || !originals.TryGetValue(proxy.Guid, out original)) return;
            var title = ComponentName(original);
            var description = ComponentDescription(original);
            if (title != null && (args.Title == original.Name || args.Title == proxy.Desc.Name))
                args.Title = Format(title, original.Name);
            if (description != null && (args.Text == original.Description || args.Text == proxy.Desc.Description))
                args.Text = Format(description, original.Description);
        }

        static void TranslateRibbonTooltip(object sender, GH_TooltipDisplayEventArgs args)
        {
            if (!Enabled || ribbon == null || args.Control != ribbon || ribbon.ActiveTab == null || !args.Valid) return;
            foreach (var tab in ribbon.Tabs)
            {
                if (!tab.Grip.Contains(args.Point)) continue;
                if (args.Title != tab.NameFull) return;
                int panels = tab.Panels.Count;
                int components = 0;
                foreach (var panel in tab.Panels) components += panel.AllItems.Count;
                args.Text = string.Format("此分类包含 {0} 个分组和 {1} 个组件。", panels, components);
                return;
            }
            foreach (var panel in ribbon.ActiveTab.Panels)
            {
                if (!panel.Visible || !panel.Contains(args.Point)) continue;
                foreach (var item in panel.VisibleItems)
                {
                    if (!item.Visible || !item.Contains(args.Point) || item.Proxy == null) continue;
                    TranslateProxyTooltip(item.Proxy, args);
                    return;
                }
            }
        }

        static void ObserveRibbonTooltip()
        {
            if (ribbonTooltip == null || ribbon == null) return;
            var current = ribbonTooltip.GetValue(ribbon, null) as GH_TooltipComponent;
            if (current == subscribedRibbonTooltip) return;
            if (subscribedRibbonTooltip != null) subscribedRibbonTooltip.PopulateTooltip -= TranslateRibbonTooltip;
            subscribedRibbonTooltip = current;
            if (current != null) current.PopulateTooltip += TranslateRibbonTooltip;
        }

        static void UpdateRibbonPanel(GH_RibbonPanel panel)
        {
            foreach (var item in panel.AllItems)
            {
                CollectProxy(item.Proxy);
                ApplyProxyDescription(item.Proxy);
            }
        }

        internal static GH_RibbonTab StartupTab(IList<GH_RibbonTab> tabs, bool pending)
        {
            if (!pending) return null;
            foreach (var tab in tabs)
            {
                if (ribbonTranslator.OriginalCategory(tab) != "Params") continue;
                foreach (var panel in tab.Panels)
                    if (panel.AllItems.Count != 0) return tab;
            }
            return null;
        }

        internal static bool PrepareRibbonLayout(GH_Ribbon target, bool changed)
        {
            if (target == null || target.IsDisposed) return false;
            if (layoutRibbon != target)
            {
                layoutRibbon = target;
                ribbonLayoutDirty = true; startupTabPending = true; ribbonStructure = -1;
                ribbonLayoutError = null;
            }
            if (changed) ribbonLayoutDirty = true;
            if (target.ClientSize.Width <= 0 || target.ClientSize.Height <= 0 || target.Tabs.Count == 0) return false;
            int structure = target.Tabs.Count;
            foreach (var tab in target.Tabs)
            {
                unchecked { structure = structure * 31 + RuntimeHelpers.GetHashCode(tab); }
                foreach (var panel in tab.Panels)
                {
                    unchecked { structure = (structure * 31 + RuntimeHelpers.GetHashCode(panel)) * 31 + panel.AllItems.Count; }
                }
            }
            if (structure != ribbonStructure || target.ClientSize != ribbonLayoutSize) ribbonLayoutDirty = true;
            if (startupTabPending)
            {
                var parameters = StartupTab(target.Tabs, true);
                if (parameters == null) return false;
                target.ActiveTab = parameters;
                ribbonLayoutDirty = true;
            }
            if (!ribbonLayoutDirty) return false;
            target.LayoutRibbon();
            foreach (var tab in target.Tabs) tab.PerformLayout();
            target.LayoutRibbon();
            target.Invalidate();
            startupTabPending = false; ribbonLayoutDirty = false;
            ribbonStructure = structure; ribbonLayoutSize = target.ClientSize;
            ribbonLayoutError = null;
            return true;
        }

        static void RefreshRibbon()
        {
            try
            {
                if (editor == null || editor.IsDisposed) return;
                if (ribbon == null || ribbon.IsDisposed) ribbon = FindRibbon(editor);
                if (ribbon == null) return;
                ObserveRibbonTooltip();
                var tooltip = ribbonTooltip == null ? null : ribbonTooltip.GetValue(ribbon, null) as GH_TooltipComponent;
                if (tooltip != null && tooltip.Delay != 0) tooltip.Delay = 0;
                bool changed = false;
                foreach (var tab in ribbon.Tabs)
                {
                    var category = ribbonTranslator.OriginalCategory(tab);
                    string before = tab.NameFull;
                    ribbonTranslator.ApplyTab(tab, Enabled, Bilingual);
                    changed |= before != tab.NameFull;
                    foreach (var panel in tab.Panels)
                    {
                        UpdateRibbonPanel(panel);
                        before = panel.Name;
                        ribbonTranslator.ApplyPanel(panel, category, Enabled, Bilingual);
                        changed |= before != panel.Name;
                    }
                }
                if (PrepareRibbonLayout(ribbon, changed)) ribbon.Refresh();
            }
            catch (Exception ex)
            {
                ribbonLayoutDirty = true;
                if (ribbonLayoutError != ex.Message) { ribbonLayoutError = ex.Message; Log(ex); }
            }
        }

        static void Observe(GH_Canvas canvas)
        {
            if (!initialized || canvas.Document == null) return;
            var document = canvas.Document;
            document.SolutionStart -= BeforeSolution;
            document.SolutionStart += BeforeSolution;
            document.ObjectsAdded -= ObjectsAdded;
            document.ObjectsAdded += ObjectsAdded;
            foreach (var obj in document.Objects) Adapt(obj);
        }

        static void BeforeSolution(object sender, GH_SolutionEventArgs args)
        { foreach (var canvas in canvases) EndDisplayNames(canvas); }

        static void ObjectsAdded(object sender, GH_DocObjectEventArgs e)
        { foreach (var obj in e.Objects) Adapt(obj); }

        static void Adapt(IGH_DocumentObject obj)
        {
            var component = obj as GH_Component;
            if (component == null)
            {
                var parameter = obj as IGH_Param;
                if (parameter == null || parameter.Attributes == null) return;
                if (parameter.Attributes is ChineseParameterAttributes || parameter.Attributes.GetType() == pointAttributes) { parameter.Attributes.ExpireLayout(); return; }
                string text, nick;
                if (parameter.Attributes.GetType() != typeof(GH_FloatingParamAttributes) || !Lookup(parameter, out text, out nick)) return;
                var previousParameter = parameter.Attributes;
                parameter.Attributes = new ChineseParameterAttributes(parameter) { Pivot = previousParameter.Pivot, Selected = previousParameter.Selected };
                parameter.Attributes.ExpireLayout();
                return;
            }
            if (component.Attributes is ChineseAttributes) { component.Attributes.ExpireLayout(); return; }
            OriginalDescription original;
            if (!OriginalForObject(component, out original) || component.Attributes == null || component.Attributes.GetType() != typeof(GH_ComponentAttributes)) return;
            var previous = component.Attributes;
            component.Attributes = new ChineseAttributes(component) { Pivot = previous.Pivot, Selected = previous.Selected };
            component.Attributes.ExpireLayout();
        }
    }

    internal sealed class ChineseParameterAttributes : GH_FloatingParamAttributes
    {
        internal ChineseParameterAttributes(IGH_Param owner) : base(owner) { }
        void WithText(Action action)
        {
            string text, nick;
            if (!Runtime.Lookup(Owner, out text, out nick)) { action(); return; }
            using (new TextScope(() => Owner.Name, value => Owner.Name = value, text))
            using (new TextScope(() => Owner.NickName, value => Owner.NickName = value, DisplayText.Nickname(Owner.NickName, nick, text))) action();
        }
        protected override void Layout() { WithText(delegate { base.Layout(); }); }
        protected override void Render(GH_Canvas canvas, Graphics graphics, GH_CanvasChannel channel)
        { WithText(delegate { base.Render(canvas, graphics, channel); }); }
        public override void SetupTooltip(PointF point, GH_TooltipDisplayEventArgs args)
        { WithText(delegate { base.SetupTooltip(point, args); }); }
    }

    // Replaces the standard text rendering itself, not an annotation above it.
    // All persistent component fields are restored before Layout/Render returns.
    internal sealed class ChineseAttributes : GH_ComponentAttributes
    {
        readonly Dictionary<IGH_Param, string> portNicknames = new Dictionary<IGH_Param, string>();
        internal ChineseAttributes(GH_Component owner) : base(owner)
        {
            foreach (var port in owner.Params.Input) portNicknames[port] = port.NickName;
            foreach (var port in owner.Params.Output) portNicknames[port] = port.NickName;
        }
        void WithTranslatedText(Action action)
        {
            string translated, nickname;
            bool hasTitle = Runtime.Lookup(Owner, out translated, out nickname);
            var scopes = new List<TextScope>();
            try
            {
                foreach (var port in Owner.Params.Input) TranslatePort(port, scopes);
                foreach (var port in Owner.Params.Output) TranslatePort(port, scopes);
                var description = Runtime.Description(Owner);
                if (description != null) scopes.Add(new TextScope(() => Owner.Description, value => Owner.Description = value, description));
                if (!hasTitle) { action(); return; }
                using (new TextScope(() => Owner.Name, value => Owner.Name = value, translated))
                using (new TextScope(() => Owner.NickName, value => Owner.NickName = value, DisplayText.Nickname(Owner.NickName, nickname, translated)))
                    action();
            }
            finally { for (int i = scopes.Count - 1; i >= 0; i--) scopes[i].Dispose(); }
        }
        void TranslatePort(IGH_Param port, List<TextScope> scopes)
        {
            var name = Runtime.ComponentPortName(Owner, port.Name);
            var description = Runtime.ComponentPortDescription(Owner, port.Description);
            if (name != null)
            {
                scopes.Add(new TextScope(() => port.Name, value => port.Name = value, name));
                string nickname;
                if (Runtime.IsPufferfish(Owner) && portNicknames.TryGetValue(port, out nickname))
                    scopes.Add(new TextScope(() => port.NickName, value => port.NickName = value, DisplayText.Nickname(port.NickName, nickname, name)));
            }
            if (description != null) scopes.Add(new TextScope(() => port.Description, value => port.Description = value, description));
        }
        protected override void Layout() { WithTranslatedText(delegate { base.Layout(); }); }
        protected override void Render(GH_Canvas canvas, Graphics graphics, GH_CanvasChannel channel)
        { WithTranslatedText(delegate { base.Render(canvas, graphics, channel); }); }
        public override void SetupTooltip(PointF point, GH_TooltipDisplayEventArgs args)
        { WithTranslatedText(delegate { base.SetupTooltip(point, args); }); }
    }
}
