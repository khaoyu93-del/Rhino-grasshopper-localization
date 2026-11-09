using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using System.Windows.Forms;
using Grasshopper.GUI;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Graphs;
using Grasshopper.GUI.Ribbon;
using GrasshopperChinese;

public static class RichGraphMapperTests
{
    static readonly BindingFlags Static = BindingFlags.Static | BindingFlags.NonPublic | BindingFlags.Public;
    static readonly BindingFlags Instance = BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public;
    static Type runtime;
    static object Call(string name, params object[] args) { return runtime.GetMethod(name, Static).Invoke(null, args); }
    static void Equal(object expected, object actual)
    {
        if (!object.Equals(expected, actual)) throw new Exception("Expected " + expected + ", got " + actual);
    }
    static void Mode(bool enabled, bool bilingual)
    {
        runtime.GetField("Enabled", Static).SetValue(null, enabled);
        runtime.GetField("Bilingual", Static).SetValue(null, bilingual);
    }
    static void Restore(List<TextScope> scopes)
    {
        for (int i = scopes.Count - 1; i >= 0; i--) scopes[i].Dispose();
    }
    static string Label(string english, string category, bool enabled, bool bilingual)
    { return (string)Call("RichLabel", english, category, enabled, bilingual); }

    public static void Run(string root)
    {
        var assembly = typeof(Catalog).Assembly;
        runtime = assembly.GetType("GrasshopperChinese.Runtime");
        foreach (var pair in new[] { new[] { "catalog", "zh-CN.json" }, new[] { "toolText", "tool-text.zh-CN.json" }, new[] { "pufferfishNames", "pufferfish.zh-CN.json" }, new[] { "pufferfishText", "pufferfish-text.zh-CN.json" }, new[] { "richText", "richedgraphmapper.zh-CN.json" } })
            runtime.GetField(pair[0], Static).SetValue(null, Catalog.Parse(File.ReadAllText(Path.Combine(root, "Languages", pair[1]))));
        Mode(true, false);
        Equal(new Version(0, 3, 1, 0), assembly.GetName().Version);
        Equal("0.3.1.0", System.Diagnostics.FileVersionInfo.GetVersionInfo(assembly.Location).FileVersion);
        string usage = (string)Call("UsageText");
        Equal(true, usage.Contains("0.3.1"));
        Equal(false, usage.Contains("预览版"));
        Equal(true, usage.Contains("刷新组件目录"));
        Equal(true, usage.Contains("导出组件及缺译清单"));
        Equal(true, usage.Contains("JSON"));
        Equal(true, usage.Contains("翻译字段为空"));
        Console.WriteLine("PASS 0.3.1 assembly/file versions and usage/export explanations");
        var startupParameters = (GH_RibbonTab)FormatterServices.GetUninitializedObject(typeof(GH_RibbonTab));
        foreach (string name in new[] { "m_nameFull", "m_nameShort", "m_nameSymbol" })
            typeof(GH_RibbonTab).GetField(name, Instance).SetValue(startupParameters, "Params");
        var startupPanel = (GH_RibbonPanel)FormatterServices.GetUninitializedObject(typeof(GH_RibbonPanel));
        var startupItems = new List<GH_RibbonItem>();
        typeof(GH_RibbonPanel).GetField("m_items", Instance).SetValue(startupPanel, startupItems);
        typeof(GH_RibbonTab).GetField("m_panels", Instance).SetValue(startupParameters, new List<GH_RibbonPanel> { startupPanel });
        var startupTabs = new List<GH_RibbonTab> { startupParameters };
        Equal(null, Call("StartupTab", startupTabs, true));
        startupItems.Add((GH_RibbonItem)FormatterServices.GetUninitializedObject(typeof(GH_RibbonItem)));
        Equal(startupParameters, Call("StartupTab", startupTabs, true));
        Equal(null, Call("StartupTab", startupTabs, false));
        ((RibbonTranslator)runtime.GetField("ribbonTranslator", Static).GetValue(null)).ApplyTab(startupParameters, true, false);
        Equal(startupParameters, Call("StartupTab", startupTabs, true));
        Equal(null, Call("StartupTab", startupTabs, false));
        Console.WriteLine("PASS startup waits for populated Params, recognizes translated tabs, and does not force later selection");
        Console.WriteLine("Full Ribbon layout needs Rhino-host user acceptance; this test does not construct that UI.");
        Equal("增强图形映射器", Label("Rich Graph Mapper", "component", true, false));
        Equal("源区间 · Source", Label("Source", "port-name", true, true));
        Equal("Source", Label("Source", "port-name", false, false));
        Equal("Unknown", Label("Unknown", "component", true, false));
        Equal("Arc", Label("Arc", "component", true, false));
        Equal(false, NativeTools.Contains("RichedGraphMapper"));

        var richAssembly = AppDomain.CurrentDomain.GetAssemblies().Single(a => a.GetName().Name == "RichedGraphMapper");
        var componentType = richAssembly.GetType("RichedGraphMapper.RichGraphMapper");
        var component = (IGH_Component)Activator.CreateInstance(componentType);
        var recordType = assembly.GetType("GrasshopperChinese.OriginalDescription");
        var proxyType = typeof(IGH_ObjectProxy).Assembly.GetType("Grasshopper.Kernel.GH_CompiledObjectProxy");
        var proxy = (IGH_ObjectProxy)FormatterServices.GetUninitializedObject(proxyType);
        proxyType.GetField("m_id", Instance).SetValue(proxy, component.ComponentGuid);
        proxyType.GetField("m_type", Instance).SetValue(proxy, componentType);
        proxyType.GetField("m_description", Instance).SetValue(proxy, new GH_InstanceDescription(component.Name, component.NickName, component.Description, component.Category));
        Call("CollectProxy", proxy);
        var records = (IDictionary)runtime.GetField("originals", Static).GetValue(null);
        var record = records[component.ComponentGuid];
        Equal("RichedGraphMapper", recordType.GetField("AssemblyName", Instance).GetValue(record));
        var unrelated = (IGH_ObjectProxy)FormatterServices.GetUninitializedObject(proxyType);
        var unrelatedId = Guid.NewGuid();
        proxyType.GetField("m_id", Instance).SetValue(unrelated, unrelatedId);
        proxyType.GetField("m_type", Instance).SetValue(unrelated, typeof(RichGraphMapperTests));
        proxyType.GetField("m_description", Instance).SetValue(unrelated, new GH_InstanceDescription("Rich Graph Mapper", "Rich Graph", component.Description, component.Category));
        Call("CollectProxy", unrelated);
        Equal(false, records.Contains(unrelatedId));
        Console.WriteLine("PASS loaded assembly proxy collection and unknown-plugin isolation");
        Equal(true, Call("IsRich", component));
        Equal("增强图形映射器", Call("ComponentName", record));
        Equal("表示数值映射函数。", Call("ComponentDescription", record));
        var scopes = new List<TextScope>();
        try
        {
            Call("AddRichDisplayScopes", component, scopes);
            Equal("增强图形", component.NickName);
            Equal("表示数值映射函数。", component.Description);
            Equal("数值", component.Params.Input[0].Name);
            Equal("值", component.Params.Input[0].NickName);
            Equal("源区间", component.Params.Input[1].Name);
            Equal("源", component.Params.Input[1].NickName);
            Equal("目标", component.Params.Input[2].NickName);
            Equal("输出数值。", component.Params.Output[0].Description);
        }
        finally { Restore(scopes); }
        Equal("Rich Graph", component.NickName);
        Equal("Values", component.Params.Input[0].Name);
        Equal("V", component.Params.Input[0].NickName);
        Equal("Input values", component.Params.Input[0].Description);
        component.NickName = "用户曲线";
        component.Params.Input[0].NickName = "用户数值";
        scopes = new List<TextScope>();
        try { Call("AddRichDisplayScopes", component, scopes); Equal("用户曲线", component.NickName); Equal("用户数值", component.Params.Input[0].NickName); }
        finally { Restore(scopes); }
        Equal("用户曲线", component.NickName);
        Equal("用户数值", component.Params.Input[0].NickName);
        var attributesType = componentType.GetNestedType("RichGraphMapperAttributes");
        var attributes = (IGH_Attributes)FormatterServices.GetUninitializedObject(attributesType);
        component.Attributes = attributes;
        Call("Adapt", component);
        Equal(attributes, component.Attributes);
        Console.WriteLine("PASS component and ports, custom nicknames, scope restoration and custom attributes retained");

        var tooltip = (GH_TooltipDisplayEventArgs)FormatterServices.GetUninitializedObject(typeof(GH_TooltipDisplayEventArgs));
        tooltip.Title = "Values (V) as list";
        tooltip.Text = "Input values";
        tooltip.Description = "Source domain";
        Call("TranslateRichTooltip", tooltip);
        Equal("数值 (V)（列表）", tooltip.Title);
        Equal("输入数值。", tooltip.Text);
        Equal("源区间。", tooltip.Description);
        Mode(true, true);
        tooltip.Title = "Target (T) as tree"; tooltip.Text = "Target domain";
        Call("TranslateRichTooltip", tooltip);
        Equal("目标区间 · Target (T) as tree", tooltip.Title);
        Equal("目标区间。 · Target domain", tooltip.Text);
        Mode(true, false);

        string[] names = { "Sigmoid", "Polyline", "Interpolated", "Bezier2", "Arc" };
        string[] translations = { "S形曲线", "折线", "插值曲线", "双贝塞尔曲线", "弧形曲线" };
        string[] ids = { "d221fdb4-a2a5-4861-a206-f7ac8f91f9cb", "e4f68fba-e0ba-4bbb-98aa-96ecb7db5d4e", "19f04c28-60bd-4807-9308-c961b1233cea", "34afa8f2-fee6-4e3b-82da-b980ffeb87aa", "c5363e79-994b-4030-8e69-02cd00bf5982" };
        using (var menu = new ContextMenuStrip())
        {
            for (int i = 0; i < names.Length; i++)
            {
                var item = new ToolStripMenuItem(names[i]) { Tag = new Guid(ids[i]) };
                menu.Items.Add(item);
                Equal(translations[i], Call("RichMenuLabel", item, item.Text, true, false, null));
                Equal(names[i], Call("RichMenuLabel", item, item.Text, false, false, null));
                Equal(new Guid(ids[i]), item.Tag);
            }
            var unknown = new ToolStripMenuItem("Arc") { Tag = Guid.NewGuid() };
            Equal("Arc", Call("RichMenuLabel", unknown, unknown.Text, true, false, null));
            foreach (string name in new[] { "Polyline", "Interpolated" })
                for (int n = 3; n <= 10; n++)
                {
                    var item = new ToolStripMenuItem(name + " " + n + " points") { Tag = n };
                    menu.Items.Add(item);
                    Equal((name == "Polyline" ? "折线" : "插值曲线") + " " + n + " 点", Call("RichMenuLabel", item, item.Text, true, false, record));
                }
            var graphTypes = new ToolStripMenuItem("Graph types"); menu.Items.Add(graphTypes);
            var remap = new ToolStripMenuItem("Remap") { ToolTipText = "Remap output values to target domain" }; menu.Items.Add(remap);
            Call("CaptureMenusForDescription", menu.Items, component.ComponentGuid, record);
            Call("TranslateMenus");
            Equal("图形类型", graphTypes.Text);
            Equal("重映射", remap.Text);
            Equal("将输出数值重映射到目标区间。", remap.ToolTipText);
            Mode(true, true); Call("TranslateMenus"); Equal("重映射 · Remap", remap.Text);
            Call("TranslateMenus"); Equal("重映射 · Remap", remap.Text);
            Mode(false, false); Call("TranslateMenus"); Equal("Remap", remap.Text); Equal("Remap output values to target domain", remap.ToolTipText);
        }
        Mode(true, false);
        Console.WriteLine("PASS canvas tooltip, five graph GUID menus, 3-10 points, bilingual and English restoration");

        using (var form = new GH_GraphEditor())
        {
            var graph = (IGH_Graph)FormatterServices.GetUninitializedObject(richAssembly.GetType("RichedGraphMapper.SigmoidGraph"));
            typeof(GH_GraphEditor).GetField("m_graph", Instance).SetValue(form, new GH_GraphContainer(graph));
            var x0 = (GH_DigitScroller)typeof(GH_GraphEditor).GetField("_numX0", Instance).GetValue(form);
            var ok = (Button)typeof(GH_GraphEditor).GetField("_btnOK", Instance).GetValue(form);
            var propertyGrid = (PropertyGrid)typeof(GH_GraphEditor).GetField("_propGraph", Instance).GetValue(form);
            x0.Value = 12.5m;
            string inputText = x0.Text;
            object selected = propertyGrid.SelectedObject;
            Equal(true, Call("PrepareGraphEditor", form));
            Equal("图形编辑器", form.Text); Equal("确定", ok.Text); Equal("源区间下限", x0.Prefix);
            Equal(12.5m, x0.Value); Equal(inputText, x0.Text); Equal(selected, propertyGrid.SelectedObject);
            Mode(true, true); Call("PrepareGraphEditor", form); Equal("确定 · OK", ok.Text);
            Call("PrepareGraphEditor", form); Equal("确定 · OK", ok.Text);
            Mode(false, false); Call("PrepareGraphEditor", form);
            Equal("Graph Editor", form.Text); Equal("OK", ok.Text); Equal("X [0]", x0.Prefix); Equal(12.5m, x0.Value);
        }
        Mode(true, false);
        Console.WriteLine("PASS unshown graph editor captions, numeric inputs untouched and language restoration");
        Console.WriteLine("Offline checks only; Rhino UI, graph editing and GH/GHX round trips remain user acceptance.");
    }
}
