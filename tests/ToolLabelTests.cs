using System;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Runtime.Serialization;
using System.Collections;
using System.Windows.Forms;
using Grasshopper.GUI.Ribbon;
using Grasshopper.GUI;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Parameters;
using GrasshopperChinese;

class ToolLabelTests
{
    static void Equal(string expected, string actual) { if (expected != actual) throw new Exception("Expected " + expected + ", got " + actual); }
    static int Main()
    {
        try
        {
            var assembly = typeof(NativeTools).Assembly;
            var runtime = assembly.GetType("GrasshopperChinese.Runtime");
            var flags = BindingFlags.Static | BindingFlags.NonPublic;
            var c = Catalog.Parse("[{\"name\":\"Circle\",\"category\":\"Params\",\"translation\":\"圆\"}]");
            runtime.GetField("catalog", flags).SetValue(null, c);
            runtime.GetField("Enabled", flags).SetValue(null, true);
            runtime.GetField("Bilingual", flags).SetValue(null, false);
            var circle = new Param_Circle();
            var proxy = (IGH_ObjectProxy)FormatterServices.GetUninitializedObject(typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy"));
            typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy").GetField("m_id", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(proxy, circle.ComponentGuid);
            var recordType = assembly.GetType("GrasshopperChinese.OriginalDescription");
            var record = Activator.CreateInstance(recordType, true);
            foreach (var pair in new[] { new[] { "Name", "Circle" }, new[] { "Nickname", circle.NickName }, new[] { "Category", "Params" } })
                recordType.GetField(pair[0], BindingFlags.Instance | BindingFlags.NonPublic).SetValue(record, pair[1]);
            ((IDictionary)runtime.GetField("originals", flags).GetValue(null)).Add(circle.ComponentGuid, record);
            using (new TextScope(() => circle.Name, value => circle.Name = value, "圆")) Equal("圆", circle.Name);
            Equal("Circle", circle.Name);
            var menuLabel = runtime.GetMethod("MenuLabel", flags);
            var toolbarLabel = runtime.GetMethod("ToolbarLabel", flags);
            Equal(null, (string)toolbarLabel.Invoke(null, new object[] { null, true, false }));
            Equal("", (string)toolbarLabel.Invoke(null, new object[] { "", true, false }));
            Equal("以线框模式预览几何对象", (string)toolbarLabel.Invoke(null, new object[] { "Draw wireframe preview geometry", true, false }));
            Equal("Draw wireframe preview geometry", (string)toolbarLabel.Invoke(null, new object[] { "Draw wireframe preview geometry", false, false }));
            Equal("打开 gh 或 ghx 文件", (string)toolbarLabel.Invoke(null, new object[] { "Open a gh or ghx file", true, false }));
            Equal("保存当前文件", (string)toolbarLabel.Invoke(null, new object[] { "Save the current file", true, false }));
            Equal("保存当前文件 · Save the current file", (string)toolbarLabel.Invoke(null, new object[] { "Save the current file", true, true }));
            var canvasLabel = runtime.GetMethod("CanvasLabel", flags);
            Equal("指南针", (string)canvasLabel.Invoke(null, new object[] { "Compass", true, false }));
            Equal("快速定位画布中的对象", (string)canvasLabel.Invoke(null, new object[] { "Find your way home", true, false }));
            Equal("开启预览", (string)canvasLabel.Invoke(null, new object[] { "Enable Preview", true, false }));
            Equal("开启全部所选对象的预览", (string)canvasLabel.Invoke(null, new object[] { "Enable preview for all selected objects", true, false }));
            Equal("禁用求解器", (string)canvasLabel.Invoke(null, new object[] { "Disable Solver", true, false }));
            Equal("启用求解器", (string)canvasLabel.Invoke(null, new object[] { "Enable Solver", true, false }));
            Equal("在文档中查找组件和参数", (string)canvasLabel.Invoke(null, new object[] { "Search the document for components and parameters", true, false }));
            Equal("指南针 · Compass", (string)canvasLabel.Invoke(null, new object[] { "Compass", true, true }));
            Equal("Compass", (string)canvasLabel.Invoke(null, new object[] { "Compass", false, false }));
            Equal("Third party tooltip", (string)canvasLabel.Invoke(null, new object[] { "Third party tooltip", true, false }));
            var tutorialLabel = runtime.GetMethod("TutorialLabel", flags);
            Equal("Grasshopper 入门…", (string)tutorialLabel.Invoke(null, new object[] { "Getting started with Grasshopper…", true, false }));
            Equal("01 基础输入与数学", (string)tutorialLabel.Invoke(null, new object[] { "01 Simple Input and Maths", true, false }));
            Equal("01 Simple Input and Maths", (string)tutorialLabel.Invoke(null, new object[] { "01 Simple Input and Maths", false, false }));
            using (var tutorialForm = new Form())
            {
                tutorialForm.Text = "Getting started with Grasshopper…";
                var tutorialCard = new Label { Text = "01 Simple Input and Maths" };
                tutorialForm.Controls.Add(tutorialCard);
                runtime.GetMethod("PrepareTutorial", flags).Invoke(null, new object[] { tutorialForm });
                Equal("Grasshopper 入门…", tutorialForm.Text);
                Equal("01 基础输入与数学", tutorialCard.Text);
                runtime.GetField("Enabled", flags).SetValue(null, false);
                runtime.GetMethod("PrepareTutorial", flags).Invoke(null, new object[] { tutorialForm });
                Equal("Getting started with Grasshopper…", tutorialForm.Text);
                Equal("01 Simple Input and Maths", tutorialCard.Text);
                runtime.GetField("Enabled", flags).SetValue(null, true);
            }
            var ravenLabel = runtime.GetMethod("RavenLabel", flags);
            Equal("Raven 区域编辑器", (string)ravenLabel.Invoke(null, new object[] { "Raven Zones Editor", true, false }));
            Equal("跨文档搜索组。", (string)ravenLabel.Invoke(null, new object[] { "Search groups across your documents.", true, false }));
            Equal("Raven 搜索 · Raven Search", (string)ravenLabel.Invoke(null, new object[] { "Raven Search", true, true }));
            Equal("Raven Search", (string)ravenLabel.Invoke(null, new object[] { "Raven Search", false, false }));
            Equal("解锁此工作区中的全部对象（3）", (string)ravenLabel.Invoke(null, new object[] { "Unlock all in this workspace (3)", true, false }));
            Equal("保护来源：My group", (string)ravenLabel.Invoke(null, new object[] { "Protected by My group", true, false }));
            Equal("My group", (string)ravenLabel.Invoke(null, new object[] { "My group", true, false }));
            var propertyType = assembly.GetType("GrasshopperChinese.RavenTextProperty");
            var property = Activator.CreateInstance(propertyType, true);
            string searchLockText = "Lock";
            propertyType.GetField("Get", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(property, new Func<string>(() => searchLockText));
            propertyType.GetField("Set", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(property, new Action<string>(value => searchLockText = value));
            var applyRavenText = runtime.GetMethod("ApplyRavenText", flags);
            applyRavenText.Invoke(null, new object[] { property });
            Equal("锁定", searchLockText);
            applyRavenText.Invoke(null, new object[] { property });
            Equal("锁定", searchLockText);
            searchLockText = "Remove own locks";
            applyRavenText.Invoke(null, new object[] { property });
            Equal("移除自身锁定", searchLockText);
            runtime.GetField("Bilingual", flags).SetValue(null, true);
            applyRavenText.Invoke(null, new object[] { property });
            Equal("移除自身锁定 · Remove own locks", searchLockText);
            runtime.GetField("Enabled", flags).SetValue(null, false);
            applyRavenText.Invoke(null, new object[] { property });
            Equal("Remove own locks", searchLockText);
            runtime.GetField("Enabled", flags).SetValue(null, true);
            runtime.GetField("Bilingual", flags).SetValue(null, false);
            Equal("最近文件", (string)menuLabel.Invoke(null, new object[] { "Recent Files", true, false }));
            Equal("导出快速图像...", (string)menuLabel.Invoke(null, new object[] { "Export Quick Image...", true, false }));
            Equal("开启预览", (string)menuLabel.Invoke(null, new object[] { "Preview On", true, false }));
            Equal("视图 (&V)", (string)menuLabel.Invoke(null, new object[] { "&View", true, false }));
            Equal("视图 · View", (string)menuLabel.Invoke(null, new object[] { "View", true, true }));
            Equal("Preview On", (string)menuLabel.Invoke(null, new object[] { "Preview On", false, false }));
            Equal("Raven V2", (string)menuLabel.Invoke(null, new object[] { "Raven V2", true, false }));
            Equal("隐藏指南针", (string)menuLabel.Invoke(null, new object[] { "Hide Compass", true, false }));
            Equal("绘制对象气泡", (string)menuLabel.Invoke(null, new object[] { "Draw object bubbles", true, false }));
            Equal("仅绘制所选对象", (string)menuLabel.Invoke(null, new object[] { "Only draw selected objects", true, false }));
            Equal("Hide Compass", (string)menuLabel.Invoke(null, new object[] { "Hide Compass", false, false }));
            Equal("隐藏指南针 · Hide Compass", (string)menuLabel.Invoke(null, new object[] { "Hide Compass", true, true }));
            var isCompassPopup = runtime.GetMethod("IsCompassPopup", flags);
            var isRavenPopup = runtime.GetMethod("IsRavenPopup", flags);
            using (var ravenPopup = new ToolStripDropDownMenu())
            {
                ravenPopup.Items.Add("Lock selection from Raven");
                ravenPopup.Items.Add("Remove own Raven locks");
                Equal("True", isRavenPopup.Invoke(null, new object[] { ravenPopup.Items }).ToString());
                runtime.GetMethod("CaptureRavenMenus", flags).Invoke(null, new object[] { ravenPopup.Items });
                runtime.GetMethod("TranslateRavenMenus", flags).Invoke(null, null);
                Equal("锁定所选对象，防止 Raven 修改", ravenPopup.Items[0].Text);
                Equal("移除对象自身的 Raven 锁定", ravenPopup.Items[1].Text);
                ravenPopup.Items.Add("Allow Raven to reference outputs");
                runtime.GetMethod("CaptureRavenMenus", flags).Invoke(null, new object[] { ravenPopup.Items });
                runtime.GetMethod("TranslateRavenMenus", flags).Invoke(null, null);
                Equal("允许 Raven 引用输出", ravenPopup.Items[2].Text);
                ravenPopup.Items.Add("Unlock all in this workspace (2)");
                runtime.GetMethod("CaptureRavenMenus", flags).Invoke(null, new object[] { ravenPopup.Items });
                runtime.GetMethod("TranslateRavenMenus", flags).Invoke(null, null);
                Equal("解锁此工作区中的全部对象（2）", ravenPopup.Items[3].Text);
                ravenPopup.Items[3].Text = "Unlock all in this workspace (4)";
                runtime.GetMethod("TranslateRavenMenus", flags).Invoke(null, null);
                Equal("解锁此工作区中的全部对象（4）", ravenPopup.Items[3].Text);
                runtime.GetField("Enabled", flags).SetValue(null, false);
                runtime.GetMethod("TranslateRavenMenus", flags).Invoke(null, null);
                Equal("Lock selection from Raven", ravenPopup.Items[0].Text);
                runtime.GetField("Enabled", flags).SetValue(null, true);
            }
            using (var compassPopup = new ToolStripDropDownMenu())
            {
                compassPopup.Items.Add("Hide Compass");
                compassPopup.Items.Add("Draw object bubbles");
                compassPopup.Items.Add("Only draw selected objects");
                Equal("True", isCompassPopup.Invoke(null, new object[] { compassPopup.Items }).ToString());
                if (compassPopup.Visible) throw new Exception("Popup unexpectedly visible");
                runtime.GetMethod("PreparePopup", flags).Invoke(null, new object[] { compassPopup });
                Equal("隐藏指南针", compassPopup.Items[0].Text);
                if (compassPopup.Visible) throw new Exception("Translation showed popup");
                compassPopup.Items[0].Text = "隐藏指南针";
                compassPopup.Items[1].Text = "绘制对象气泡";
                compassPopup.Items[2].Text = "仅绘制所选对象";
                Equal("True", isCompassPopup.Invoke(null, new object[] { compassPopup.Items }).ToString());
                compassPopup.Items.Clear();
                compassPopup.Items.Add("Hide Compass");
                compassPopup.Items.Add("Raven V2");
                Equal("False", isCompassPopup.Invoke(null, new object[] { compassPopup.Items }).ToString());
            }
            using (var beforeShowPopup = new ToolStripDropDownMenu())
            {
                beforeShowPopup.Items.Add("Hide Compass");
                beforeShowPopup.Items.Add("Draw object bubbles");
                beforeShowPopup.Items.Add("Only draw selected objects");
                var messageType = assembly.GetType("GrasshopperChinese.Runtime+WindowMessageData");
                var message = Activator.CreateInstance(messageType);
                messageType.GetField("Message", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(message, (uint)0x18);
                messageType.GetField("WParam", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(message, new IntPtr(1));
                messageType.GetField("Handle", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(message, beforeShowPopup.Handle);
                var pointer = System.Runtime.InteropServices.Marshal.AllocHGlobal(System.Runtime.InteropServices.Marshal.SizeOf(messageType));
                try
                {
                    System.Runtime.InteropServices.Marshal.StructureToPtr(message, pointer, false);
                    runtime.GetMethod("WindowMessage", flags).Invoke(null, new object[] { 0, IntPtr.Zero, pointer });
                    Equal("隐藏指南针", beforeShowPopup.Items[0].Text);
                    Equal("False", beforeShowPopup.Visible.ToString());
                }
                finally { System.Runtime.InteropServices.Marshal.FreeHGlobal(pointer); }
            }
            runtime.GetField("catalog", flags).SetValue(null, Catalog.Parse("[{\"name\":\"Geometry\",\"category\":\"port-name\",\"translation\":\"几何\"}]"));
            Equal("输入：几何", (string)menuLabel.Invoke(null, new object[] { "Input: Geometry", true, false }));
            Equal("Input: Geometry", (string)menuLabel.Invoke(null, new object[] { "Input: Geometry", false, false }));
            Equal("管理几何集合", (string)menuLabel.Invoke(null, new object[] { "Manage Geometry collection", true, false }));
            Equal("Manage Geometry collection", (string)menuLabel.Invoke(null, new object[] { "Manage Geometry collection", false, false }));
            Equal("查看整个文档", (string)menuLabel.Invoke(null, new object[] { "View entire document", true, false }));
            Equal("聚焦左上角", (string)menuLabel.Invoke(null, new object[] { "Focus on Upper Left", true, false }));
            runtime.GetField("catalog", flags).SetValue(null, c);
            foreach (var pair in new[] { new[] { "Paste In Place", "原位粘贴" }, new[] { "Put To Back", "置于底层" },
                new[] { "Disable Meshing", "禁用网格划分" }, new[] { "Clear Exceptions", "清除异常" },
                new[] { "Download SDK Help...", "下载 SDK 帮助..." } })
                Equal(pair[1], (string)menuLabel.Invoke(null, new object[] { pair[0], true, false }));
            var isCanvasPopup = runtime.GetMethod("IsCanvasPopup", flags);
            using (var popup = new ToolStripDropDownMenu())
            {
                popup.Items.Add("Preview On"); popup.Items.Add("Preview Off"); popup.Items.Add("Lock Solver");
                Equal("True", isCanvasPopup.Invoke(null, new object[] { popup.Items }).ToString());
                popup.Items[0].Text = "开启预览";
                popup.Items[1].Text = "关闭预览";
                popup.Items[2].Text = "锁定求解器";
                Equal("True", isCanvasPopup.Invoke(null, new object[] { popup.Items }).ToString());
                popup.Items.Clear(); popup.Items.Add("Preview On"); popup.Items.Add("Raven V2");
                Equal("False", isCanvasPopup.Invoke(null, new object[] { popup.Items }).ToString());
            }
            var languagePath = Path.Combine(Environment.GetEnvironmentVariable("GRASSHOPPER_CHINESE_TEST_ROOT"), "Languages");
            var names = Catalog.Parse(File.ReadAllText(Path.Combine(languagePath, "zh-CN.json")));
            var descriptions = Catalog.Parse(File.ReadAllText(Path.Combine(languagePath, "tool-text.zh-CN.json")));
            runtime.GetField("catalog", flags).SetValue(null, names);
            Equal("设置一个圆", (string)menuLabel.Invoke(null, new object[] { "Set one Circle", true, false }));
            Equal("设置多个圆", (string)menuLabel.Invoke(null, new object[] { "Set Multiple Circles", true, false }));
            Equal("Set one Circle", (string)menuLabel.Invoke(null, new object[] { "Set one Circle", false, false }));
            Equal("聚焦左上角", (string)menuLabel.Invoke(null, new object[] { "Focus on Upper Left", true, false }));
            runtime.GetField("toolText", flags).SetValue(null, descriptions);
            runtime.GetField("Enabled", flags).SetValue(null, true);
            runtime.GetField("Bilingual", flags).SetValue(null, false);
            var portName = runtime.GetMethod("PortName", flags);
            var portDescription = runtime.GetMethod("PortDescription", flags);
            Equal("几何", (string)portName.Invoke(null, new object[] { "Geometry" }));
            Equal("待变换的基础几何对象。", (string)portDescription.Invoke(null, new object[] { "Base geometry" }));
            runtime.GetField("Bilingual", flags).SetValue(null, false);
            var point = new Param_Point();
            if (point.NickName != "Pt") throw new Exception("Point default nickname changed");
            point.CreateAttributes();
            if (point.Attributes.GetType().FullName != "Grasshopper.Kernel.Parameters.Param_PointAttributes") throw new Exception("Point native attributes changed");
            Equal("点", names.Find(point.Name, point.Category));
            Equal("点", DisplayText.Nickname(point.NickName, "Pt", names.Find(point.Name, point.Category)));
            Equal("自定义点", DisplayText.Nickname("自定义点", "Pt", "点"));
            using (new TextScope(() => point.NickName, value => point.NickName = value, DisplayText.Nickname(point.NickName, "Pt", "点")))
                Equal("点", point.NickName);
            Equal("Pt", point.NickName);
            var pointProxy = (IGH_ObjectProxy)FormatterServices.GetUninitializedObject(typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy"));
            typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy").GetField("m_id", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(pointProxy, point.ComponentGuid);
            typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy").GetField("m_description", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(pointProxy, new GH_InstanceDescription(point.Name, point.NickName, point.Description, point.Category));
            var pointRecord = Activator.CreateInstance(recordType, true);
            foreach (var pair in new[] { new[] { "Name", point.Name }, new[] { "Nickname", point.NickName }, new[] { "Category", point.Category }, new[] { "Description", point.Description } })
                recordType.GetField(pair[0], BindingFlags.Instance | BindingFlags.NonPublic).SetValue(pointRecord, pair[1]);
            ((IDictionary)runtime.GetField("originals", flags).GetValue(null)).Add(point.ComponentGuid, pointRecord);
            var translateProxyTooltip = runtime.GetMethod("TranslateProxyTooltip", flags);
            var canvasTipArgs = (GH_TooltipDisplayEventArgs)Activator.CreateInstance(typeof(GH_TooltipDisplayEventArgs), BindingFlags.Instance | BindingFlags.NonPublic, null, new object[] { new Grasshopper.GUI.Canvas.GH_Canvas(), Point.Empty }, null);
            var translateCanvasTooltip = runtime.GetMethod("TranslateCanvasTooltip", flags);
            canvasTipArgs.Title = "Compass";
            canvasTipArgs.Text = "Find your way home";
            translateCanvasTooltip.Invoke(null, new object[] { null, canvasTipArgs });
            Equal("指南针", canvasTipArgs.Title);
            Equal("快速定位画布中的对象", canvasTipArgs.Text);
            canvasTipArgs.Title = "Raven Zones Editor";
            canvasTipArgs.Text = "Draw and edit Raven's zones. Right-click a workspace padlock to unlock its contents.";
            translateCanvasTooltip.Invoke(null, new object[] { null, canvasTipArgs });
            Equal("Raven 区域编辑器", canvasTipArgs.Title);
            Equal("绘制和编辑 Raven 区域。右键单击工作区挂锁可解锁其内容。", canvasTipArgs.Text);
            canvasTipArgs.Title = "Raven Search";
            canvasTipArgs.Text = "Search groups across your documents.";
            translateCanvasTooltip.Invoke(null, new object[] { null, canvasTipArgs });
            Equal("Raven 搜索", canvasTipArgs.Title);
            Equal("跨文档搜索组。", canvasTipArgs.Text);
            var radialType = typeof(Grasshopper.GUI.Canvas.GH_Canvas).Assembly.GetType("Grasshopper.GUI.Canvas.Interaction.GH_RadialMenuInteraction");
            var buttonType = radialType.GetNestedType("WheelButtons", BindingFlags.Public | BindingFlags.NonPublic);
            var radial = FormatterServices.GetUninitializedObject(radialType);
            radialType.BaseType.GetField("m_canvas", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(radial, canvasTipArgs.Control);
            radialType.GetField("_allowObjectButtons", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(radial, true);
            radialType.GetField("_allowDocumentButtons", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(radial, true);
            radialType.GetField("_inner", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(radial, 25);
            radialType.GetField("_outer", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(radial, 75);
            var buttonArea = radialType.GetMethod("ButtonArea", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
            var setupRadialTooltip = radialType.GetMethod("SetupTooltip", BindingFlags.Instance | BindingFlags.Public);
            foreach (var button in Enum.GetNames(buttonType))
            {
                if (button == "None" || button == "Solver") continue;
                var area = (Rectangle)buttonArea.Invoke(radial, new object[] { Enum.Parse(buttonType, button) });
                var location = new PointF(area.Left + area.Width / 2, area.Top + area.Height / 2);
                var canvas = (Grasshopper.GUI.Canvas.GH_Canvas)canvasTipArgs.Control;
                canvasTipArgs.Title = "";
                canvasTipArgs.Text = "";
                setupRadialTooltip.Invoke(radial, new object[] { canvas.Viewport.UnprojectPoint(location), canvasTipArgs });
                var title = canvasTipArgs.Title;
                var body = canvasTipArgs.Text;
                if (string.IsNullOrEmpty(title) || string.IsNullOrEmpty(body)) throw new Exception("Empty radial tooltip: " + button);
                translateCanvasTooltip.Invoke(null, new object[] { null, canvasTipArgs });
                if (canvasTipArgs.Title == title || canvasTipArgs.Text == body) throw new Exception("Untranslated radial tooltip: " + button);
            }
            canvasTipArgs.Title = "Enable Preview";
            canvasTipArgs.Text = "Enable preview for all selected objects";
            translateCanvasTooltip.Invoke(null, new object[] { null, canvasTipArgs });
            Equal("开启预览", canvasTipArgs.Title);
            Equal("开启全部所选对象的预览", canvasTipArgs.Text);
            canvasTipArgs.Title = "Disable Solver";
            canvasTipArgs.Text = "Disable the global Grasshopper solver";
            translateCanvasTooltip.Invoke(null, new object[] { null, canvasTipArgs });
            Equal("禁用求解器", canvasTipArgs.Title);
            Equal("禁用 Grasshopper 全局求解器", canvasTipArgs.Text);
            runtime.GetField("Bilingual", flags).SetValue(null, true);
            canvasTipArgs.Title = "Compass";
            canvasTipArgs.Text = "Find your way home";
            translateCanvasTooltip.Invoke(null, new object[] { null, canvasTipArgs });
            Equal("指南针 · Compass", canvasTipArgs.Title);
            Equal("快速定位画布中的对象 · Find your way home", canvasTipArgs.Text);
            runtime.GetField("Enabled", flags).SetValue(null, false);
            canvasTipArgs.Title = "Compass";
            canvasTipArgs.Text = "Find your way home";
            translateCanvasTooltip.Invoke(null, new object[] { null, canvasTipArgs });
            Equal("Compass", canvasTipArgs.Title);
            Equal("Find your way home", canvasTipArgs.Text);
            runtime.GetField("Bilingual", flags).SetValue(null, false);
            runtime.GetField("Enabled", flags).SetValue(null, true);
            var tooltipArgs = (GH_TooltipDisplayEventArgs)Activator.CreateInstance(typeof(GH_TooltipDisplayEventArgs), BindingFlags.Instance | BindingFlags.NonPublic, null, new object[] { new Panel(), Point.Empty }, null);
            tooltipArgs.Title = point.Name;
            tooltipArgs.Text = point.Description;
            translateProxyTooltip.Invoke(null, new object[] { pointProxy, tooltipArgs });
            Equal("点", tooltipArgs.Title);
            Equal("存储一组点数据。", tooltipArgs.Text);
            pointProxy.Desc.Name = "点";
            pointProxy.Desc.Description = "存储一组点数据。";
            tooltipArgs.Title = point.Name;
            tooltipArgs.Text = point.Description;
            translateProxyTooltip.Invoke(null, new object[] { pointProxy, tooltipArgs });
            Equal("点", tooltipArgs.Title);
            Equal("存储一组点数据。", tooltipArgs.Text);
            runtime.GetField("Bilingual", flags).SetValue(null, true);
            tooltipArgs.Title = pointProxy.Desc.Name;
            tooltipArgs.Text = pointProxy.Desc.Description;
            translateProxyTooltip.Invoke(null, new object[] { pointProxy, tooltipArgs });
            Equal("点 · Point", tooltipArgs.Title);
            Equal("存储一组点数据。 · " + point.Description, tooltipArgs.Text);
            runtime.GetField("Enabled", flags).SetValue(null, false);
            tooltipArgs.Title = point.Name;
            tooltipArgs.Text = point.Description;
            translateProxyTooltip.Invoke(null, new object[] { pointProxy, tooltipArgs });
            Equal(point.Name, tooltipArgs.Title);
            Equal(point.Description, tooltipArgs.Text);
            runtime.GetField("Enabled", flags).SetValue(null, true);
            tooltipArgs.Title = point.Name;
            tooltipArgs.Text = point.Description;
            var unrelatedProxy = (IGH_ObjectProxy)FormatterServices.GetUninitializedObject(typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy"));
            typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy").GetField("m_id", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(unrelatedProxy, Guid.NewGuid());
            translateProxyTooltip.Invoke(null, new object[] { unrelatedProxy, tooltipArgs });
            Equal(point.Name, tooltipArgs.Title);
            Equal(point.Description, tooltipArgs.Text);
            runtime.GetField("Bilingual", flags).SetValue(null, false);
            var dropdownProxy = (IGH_ObjectProxy)FormatterServices.GetUninitializedObject(typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy"));
            typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy").GetField("m_id", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(dropdownProxy, point.ComponentGuid);
            typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy").GetField("m_description", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(dropdownProxy, new GH_InstanceDescription(point.Name, point.NickName, point.Description, point.Category));
            var dropdownLabel = new GH_Label { Tag = dropdownProxy, Text = "  " + point.Name };
            var updateDropdownLabel = runtime.GetMethod("UpdateDropdownLabel", flags);
            updateDropdownLabel.Invoke(null, new object[] { dropdownLabel });
            Equal("  点", dropdownLabel.Text);
            Equal("存储一组点数据。", dropdownProxy.Desc.Description);
            updateDropdownLabel.Invoke(null, new object[] { dropdownLabel });
            Equal("  点", dropdownLabel.Text);
            runtime.GetField("Bilingual", flags).SetValue(null, true);
            updateDropdownLabel.Invoke(null, new object[] { dropdownLabel });
            Equal("  点 · Point", dropdownLabel.Text);
            Equal("存储一组点数据。 · " + point.Description, dropdownProxy.Desc.Description);
            runtime.GetField("Enabled", flags).SetValue(null, false);
            updateDropdownLabel.Invoke(null, new object[] { dropdownLabel });
            Equal("  Point", dropdownLabel.Text);
            Equal(point.Description, dropdownProxy.Desc.Description);
            runtime.GetField("Enabled", flags).SetValue(null, true);
            runtime.GetField("Bilingual", flags).SetValue(null, false);
            var panelProxy = (IGH_ObjectProxy)FormatterServices.GetUninitializedObject(typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy"));
            typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy").GetField("m_id", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(panelProxy, point.ComponentGuid);
            typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy").GetField("m_description", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(panelProxy, new GH_InstanceDescription(point.Name, point.NickName, point.Description, point.Category));
            var ribbonPanel = new GH_RibbonPanel();
            if (!ribbonPanel.AddItem(new GH_RibbonItem(panelProxy))) throw new Exception("Could not add native proxy to ribbon panel");
            var updateRibbonPanel = runtime.GetMethod("UpdateRibbonPanel", flags);
            updateRibbonPanel.Invoke(null, new object[] { ribbonPanel });
            Equal("点", panelProxy.Desc.Name);
            Equal("存储一组点数据。", panelProxy.Desc.Description);
            var restartedProxy = (IGH_ObjectProxy)FormatterServices.GetUninitializedObject(typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy"));
            typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy").GetField("m_id", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(restartedProxy, point.ComponentGuid);
            typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy").GetField("m_description", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(restartedProxy, new GH_InstanceDescription(point.Name, point.NickName, point.Description, point.Category));
            var restartedPanel = new GH_RibbonPanel();
            if (!restartedPanel.AddItem(new GH_RibbonItem(restartedProxy))) throw new Exception("Could not add rebuilt proxy to ribbon panel");
            updateRibbonPanel.Invoke(null, new object[] { restartedPanel });
            Equal("点", restartedProxy.Desc.Name);
            Equal("存储一组点数据。", restartedProxy.Desc.Description);
            var prebuiltDropdownLabel = new GH_Label { Tag = panelProxy, Text = "  " + panelProxy.Desc.Name };
            Equal("  点", prebuiltDropdownLabel.Text);
            runtime.GetField("Bilingual", flags).SetValue(null, true);
            updateRibbonPanel.Invoke(null, new object[] { ribbonPanel });
            Equal("点 · Point", panelProxy.Desc.Name);
            Equal("存储一组点数据。 · " + point.Description, panelProxy.Desc.Description);
            runtime.GetField("Enabled", flags).SetValue(null, false);
            updateRibbonPanel.Invoke(null, new object[] { ribbonPanel });
            Equal(point.Name, panelProxy.Desc.Name);
            Equal(point.Description, panelProxy.Desc.Description);
            runtime.GetField("Enabled", flags).SetValue(null, true);
            runtime.GetField("Bilingual", flags).SetValue(null, false);
            using (var dropdown = new GH_RibbonDropdown())
            using (var content = new Panel())
            {
                dropdown.Controls.Add(content);
                typeof(GH_RibbonDropdown).GetField("_pnlContent", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(dropdown, content);
                content.Controls.Add(dropdownLabel);
                dropdownProxy.Desc.Name = point.Name;
                dropdownProxy.Desc.Description = point.Description;
                dropdownLabel.Text = "  " + point.Name;
                runtime.GetMethod("UpdateDropdown", flags).Invoke(null, new object[] { dropdown });
                Equal("  点", dropdownLabel.Text);
                Equal("存储一组点数据。", dropdownProxy.Desc.Description);
            }
            var otherLabel = new GH_Label { Tag = unrelatedProxy, Text = "  Point" };
            updateDropdownLabel.Invoke(null, new object[] { otherLabel });
            Equal("  Point", otherLabel.Text);
            var menuKeys = runtime.GetField("menuText", flags).GetValue(null) as IDictionary;
            if (menuKeys == null || menuKeys.Count < 100) throw new Exception("Menu dictionary did not initialize");
            var moveAssembly = Assembly.LoadFrom(@"C:\Program Files\Rhino 8\Plug-ins\Grasshopper\Components\XformComponents.gha");
            var move = (GH_Component)Activator.CreateInstance(moveAssembly.GetType("LinearXForms.Component_Move"));
            var moveRecord = Activator.CreateInstance(recordType, true);
            foreach (var pair in new[] { new[] { "Name", move.Name }, new[] { "Nickname", move.NickName }, new[] { "Category", move.Category } })
                recordType.GetField(pair[0], BindingFlags.Instance | BindingFlags.NonPublic).SetValue(moveRecord, pair[1]);
            ((IDictionary)runtime.GetField("originals", flags).GetValue(null)).Add(move.ComponentGuid, moveRecord);
            var attributeType = assembly.GetType("GrasshopperChinese.ChineseAttributes");
            var attributes = Activator.CreateInstance(attributeType, BindingFlags.Instance | BindingFlags.NonPublic, null, new object[] { move }, null);
            var withText = attributeType.GetMethod("WithTranslatedText", BindingFlags.Instance | BindingFlags.NonPublic);
            var input = move.Params.Input[0];
            var originalName = input.Name;
            var originalDescription = input.Description;
            withText.Invoke(attributes, new object[] { new Action(delegate {
                Equal("几何", input.Name);
                Equal("待变换的基础几何对象。", input.Description);
            }) });
            Equal(originalName, input.Name);
            Equal(originalDescription, input.Description);
            try
            {
                withText.Invoke(attributes, new object[] { new Action(delegate {
                    Equal("几何", input.Name);
                    throw new InvalidOperationException("render failed");
                }) });
                throw new Exception("Render exception was swallowed");
            }
            catch (TargetInvocationException e)
            {
                if (!(e.InnerException is InvalidOperationException)) throw;
            }
            Equal(originalName, input.Name);
            Equal(originalDescription, input.Description);
            runtime.GetField("Enabled", flags).SetValue(null, false);
            withText.Invoke(attributes, new object[] { new Action(delegate {
                Equal(originalName, input.Name);
                Equal(originalDescription, input.Description);
            }) });
            runtime.GetField("Enabled", flags).SetValue(null, true);
            var noTitle = Catalog.Parse("[{\"name\":\"Geometry\",\"category\":\"port-name\",\"translation\":\"几何\"}]");
            runtime.GetField("catalog", flags).SetValue(null, noTitle);
            withText.Invoke(attributes, new object[] { new Action(delegate {
                Equal("Move", move.Name);
                Equal("几何", input.Name);
            }) });
            Equal(originalName, input.Name);
            Equal(originalDescription, input.Description);
            runtime.GetField("catalog", flags).SetValue(null, names);
            runtime.GetField("pufferfishNames", flags).SetValue(null, Catalog.Parse(File.ReadAllText(Path.Combine(languagePath, "pufferfish.zh-CN.json"))));
            runtime.GetField("pufferfishText", flags).SetValue(null, Catalog.Parse(File.ReadAllText(Path.Combine(languagePath, "pufferfish-text.zh-CN.json"))));
            var pufferfishPath = Environment.GetEnvironmentVariable("GRASSHOPPER_CHINESE_PUFFERFISH_TEST_PATH") ?? Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), @"McNeel\Rhinoceros\packages\8.0\Pufferfish\3.0.0\Pufferfish3-0.gha");
            var pufferfishAssembly = Assembly.LoadFrom(pufferfishPath);
            var fish = (GH_Component)Activator.CreateInstance(pufferfishAssembly.GetType("Pufferfish.Components.Components_Curve._6_Curve.MirrorCutCurve"));
            var fishRecord = Activator.CreateInstance(recordType, true);
            foreach (var pair in new[] { new[] { "Name", fish.Name }, new[] { "Nickname", fish.NickName }, new[] { "Category", fish.Category }, new[] { "Description", fish.Description }, new[] { "AssemblyName", "Pufferfish" } })
                recordType.GetField(pair[0], BindingFlags.Instance | BindingFlags.NonPublic).SetValue(fishRecord, pair[1]);
            ((IDictionary)runtime.GetField("originals", flags).GetValue(null)).Add(fish.ComponentGuid, fishRecord);
            var fishAttributesType = assembly.GetType("GrasshopperChinese.ChineseAttributes");
            var fishAttributes = Activator.CreateInstance(fishAttributesType, BindingFlags.Instance | BindingFlags.NonPublic, null, new object[] { fish }, null);
            var fishWithText = fishAttributesType.GetMethod("WithTranslatedText", BindingFlags.Instance | BindingFlags.NonPublic);
            var fishOriginalName = fish.Name;
            var fishOriginalDescription = fish.Description;
            var fishPortName = fish.Params.Input[1].Name;
            var fishPortDescription = fish.Params.Input[1].Description;
            fishWithText.Invoke(fishAttributes, new object[] { new Action(delegate {
                Equal("镜像裁剪曲线", fish.Name);
                Equal("镜像平面", fish.Params.Input[1].Name);
                Equal("镜像平面", fish.Params.Input[1].NickName);
                Equal("曲线裁剪后保留侧所用的镜像平面。", fish.Params.Input[1].Description);
                if (fish.Description == fishOriginalDescription) throw new Exception("Pufferfish component description not translated");
            }) });
            Equal(fishOriginalName, fish.Name);
            Equal(fishOriginalDescription, fish.Description);
            Equal(fishPortName, fish.Params.Input[1].Name);
            Equal("MP", fish.Params.Input[1].NickName);
            Equal(fishPortDescription, fish.Params.Input[1].Description);
            runtime.GetField("Bilingual", flags).SetValue(null, true);
            fishWithText.Invoke(fishAttributes, new object[] { new Action(delegate {
                Equal("镜像裁剪曲线 · Mirror Cut Curve", fish.Name);
            }) });
            Equal(fishOriginalName, fish.Name);
            fish.NickName = "我的镜像";
            fishWithText.Invoke(fishAttributes, new object[] { new Action(delegate { Equal("我的镜像", fish.NickName); }) });
            Equal("我的镜像", fish.NickName);
            runtime.GetField("Enabled", flags).SetValue(null, false);
            fishWithText.Invoke(fishAttributes, new object[] { new Action(delegate {
                Equal(fishOriginalName, fish.Name);
                Equal(fishPortName, fish.Params.Input[1].Name);
            }) });
            runtime.GetField("Enabled", flags).SetValue(null, true);
            runtime.GetField("Bilingual", flags).SetValue(null, false);
            var fishTip = (GH_TooltipDisplayEventArgs)Activator.CreateInstance(typeof(GH_TooltipDisplayEventArgs), BindingFlags.Instance | BindingFlags.NonPublic, null, new object[] { new Panel(), Point.Empty }, null);
            fishTip.Title = fishPortName;
            fishTip.Description = fishPortDescription;
            runtime.GetMethod("TranslatePufferfishTooltip", flags).Invoke(null, new object[] { fishTip });
            Equal("镜像平面", fishTip.Title);
            Equal("曲线裁剪后保留侧所用的镜像平面。", fishTip.Description);
            fishTip.Title = "Mirror Plane (MP) as list";
            runtime.GetMethod("TranslatePufferfishTooltip", flags).Invoke(null, new object[] { fishTip });
            Equal("镜像平面 (MP)（列表）", fishTip.Title);
            fishTip.Title = "Warning";
            fishTip.Text = "Area cannot be less than or equal to zero";
            runtime.GetMethod("TranslatePufferfishTooltip", flags).Invoke(null, new object[] { fishTip });
            Equal("面积必须大于零。", fishTip.Text);
            var fishMenuLabel = runtime.GetMethod("MenuLabelForObject", flags);
            Equal("输入：镜像平面", (string)fishMenuLabel.Invoke(null, new object[] { "Input: Mirror Plane", true, false, fish.ComponentGuid }));
            Equal("Input: Mirror Plane", (string)fishMenuLabel.Invoke(null, new object[] { "Input: Mirror Plane", false, false, fish.ComponentGuid }));
            Equal("1. 面积必须大于零。", (string)fishMenuLabel.Invoke(null, new object[] { "1. Area cannot be less than or equal to zero", true, false, fish.ComponentGuid }));
            runtime.GetMethod("ComponentLibraryLoaded", flags).Invoke(null, new object[] { null, null });
            Equal("True", runtime.GetField("proxiesChanged", flags).GetValue(null).ToString());
            runtime.GetField("proxiesChanged", flags).SetValue(null, false);
            var subdProxyType = typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_UserObjectProxy");
            var subdFolder = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), @"McNeel\Rhinoceros\packages\8.0\Pufferfish\3.0.0\Pufferfish WIP SubD Components");
            foreach (var subdFile in Directory.GetFiles(subdFolder, "*.ghuser"))
            {
                var user = new GH_UserObject(subdFile);
                user.ReadFromFile();
                var subdProxy = (IGH_ObjectProxy)FormatterServices.GetUninitializedObject(subdProxyType);
                subdProxyType.GetField("m_id", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(subdProxy, user.Guid);
                subdProxyType.GetField("m_description", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(subdProxy, new GH_InstanceDescription(user.Description));
                runtime.GetMethod("CollectProxy", flags).Invoke(null, new object[] { subdProxy });
                runtime.GetMethod("ApplyProxyDescription", flags).Invoke(null, new object[] { subdProxy });
                if (subdProxy.Desc.Name == user.Description.Name) throw new Exception("SubD user name not translated: " + user.Description.Name);
                if (subdProxy.Desc.Description == user.Description.Description) throw new Exception("SubD user description not translated");
                var clusterType = typeof(GH_Component).Assembly.GetType("Grasshopper.Kernel.Special.GH_Cluster");
                var cluster = (GH_Component)FormatterServices.GetUninitializedObject(clusterType);
                cluster.Name = user.Description.Name;
                cluster.NickName = "自定义细分曲面";
                cluster.Description = user.Description.Description;
                cluster.Category = "Pufferfish";
                cluster.SubCategory = "SubD";
                var lookupArgs = new object[] { cluster, null, null };
                Equal("True", runtime.GetMethod("Lookup", flags).Invoke(null, lookupArgs).ToString());
                Equal(user.Description.NickName, (string)lookupArgs[2]);
                Equal("自定义细分曲面", cluster.NickName);
                Equal("True", runtime.GetMethod("IsPufferfish", flags).Invoke(null, new object[] { cluster }).ToString());
            }
            var fishPack = Catalog.Parse(File.ReadAllText(Path.Combine(languagePath, "pufferfish-text.zh-CN.json")));
            Equal("角度不为零时，依据曲线角度精度（度）划分网格面，替代 {v} 分割参数，以适应曲率变化。仅当挤出方向为曲线时有效。", fishPack.Find("If Angle is not 0.0, extrusion direction curves mesh face divisions are defined by angle accuracy in degrees instead of the {v} parameters if a curve is used for the extrusion direction\r\n\r\n(useful for conforming mesh face divisions to the curvature of the extrusion direction curve)", "port-description"));
            Console.WriteLine("PASS SubD user proxies/clusters, tutorial text, before-show message translation, Pufferfish restoration");
            Console.WriteLine("PASS native dropdown, toolbar, Compass popup, radial buttons, Raven tooltip/dynamic menus/text, Pt nickname, bilingual/disabled modes");
            return 0;
        }
        catch (Exception e) { Console.WriteLine(e); return 1; }
    }
}
