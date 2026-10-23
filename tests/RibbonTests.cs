using System;
using System.Reflection;
using System.Runtime.Serialization;
using Grasshopper.GUI.Ribbon;
using GrasshopperChinese;

class RibbonTests
{
    static void Equal(string expected, string actual)
    { if (expected != actual) throw new Exception("Expected " + expected + ", got " + actual); }
    static int Main()
    {
        try
        {
            // Use real SDK objects without launching a Rhino application or triggering native services.
            var tab = (GH_RibbonTab)FormatterServices.GetUninitializedObject(typeof(GH_RibbonTab));
            foreach (var name in new[] { "m_nameFull", "m_nameShort", "m_nameSymbol" })
                typeof(GH_RibbonTab).GetField(name, BindingFlags.Instance | BindingFlags.NonPublic).SetValue(tab, name == "m_nameSymbol" ? "P" : "Params");
            var panel = (GH_RibbonPanel)FormatterServices.GetUninitializedObject(typeof(GH_RibbonPanel));
            panel.Name = "Geometry";
            var adapter = new RibbonTranslator();
            adapter.ApplyTab(tab, true, false);
            adapter.ApplyPanel(panel, "Params", true, false);
            Equal("参数", tab.NameFull); Equal("参数", tab.NameShort); Equal("几何", panel.Name);
            adapter.ApplyTab(tab, true, true);
            adapter.ApplyPanel(panel, "Params", true, true);
            Equal("参数 · Params", tab.NameFull); Equal("几何 · Geometry", panel.Name);
            adapter.ApplyTab(tab, true, true); adapter.ApplyPanel(panel, "Params", true, true);
            Equal("参数 · Params", tab.NameFull); Equal("几何 · Geometry", panel.Name);
            adapter.ApplyTab(tab, false, false);
            adapter.ApplyPanel(panel, "Params", false, false);
            Equal("Params", tab.NameFull); Equal("Params", tab.NameShort); Equal("P", tab.NameSymbol); Equal("Geometry", panel.Name);
            var thirdParty = (GH_RibbonPanel)FormatterServices.GetUninitializedObject(typeof(GH_RibbonPanel));
            thirdParty.Name = "Geometry";
            adapter.ApplyPanel(thirdParty, "UnknownPlugin", true, false);
            Equal("Geometry", thirdParty.Name);
            Equal("基本类型", RibbonTranslator.Translate("Primitive", false));
            Equal("输入", RibbonTranslator.Translate("Input", false));
            Equal("工具", RibbonTranslator.Translate("Util", false));
            Equal("标注", RibbonTranslator.Translate("Annotations", false));
            Equal("内容", RibbonTranslator.Translate("Content", false));
            Equal("制图", RibbonTranslator.Translate("Drafting", false));
            Equal("视口", RibbonTranslator.Translate("Viewports", false));
            Equal("标注", RibbonTranslator.Translate("Dimensions", false));
            Equal("渐变", RibbonTranslator.Translate("Gradients", false));
            var kangarooTab = (GH_RibbonTab)FormatterServices.GetUninitializedObject(typeof(GH_RibbonTab));
            foreach (var name in new[] { "m_nameFull", "m_nameShort", "m_nameSymbol" })
                typeof(GH_RibbonTab).GetField(name, BindingFlags.Instance | BindingFlags.NonPublic).SetValue(kangarooTab, name == "m_nameSymbol" ? "K" : "Kangaroo2");
            var kangarooPanel = (GH_RibbonPanel)FormatterServices.GetUninitializedObject(typeof(GH_RibbonPanel));
            kangarooPanel.Name = "Goals-Lin";
            adapter.ApplyTab(kangarooTab, true, false);
            adapter.ApplyPanel(kangarooPanel, "Kangaroo2", true, false);
            Equal("袋鼠2", kangarooTab.NameFull); Equal("目标·长度与直线", kangarooPanel.Name);
            adapter.ApplyTab(kangarooTab, false, false);
            adapter.ApplyPanel(kangarooPanel, "Kangaroo2", false, false);
            Equal("Kangaroo2", kangarooTab.NameFull); Equal("Goals-Lin", kangarooPanel.Name);
            var pufferfishTab = (GH_RibbonTab)FormatterServices.GetUninitializedObject(typeof(GH_RibbonTab));
            foreach (var name in new[] { "m_nameFull", "m_nameShort", "m_nameSymbol" })
                typeof(GH_RibbonTab).GetField(name, BindingFlags.Instance | BindingFlags.NonPublic).SetValue(pufferfishTab, name == "m_nameSymbol" ? "P" : "Pufferfish");
            var pufferfishPanel = (GH_RibbonPanel)FormatterServices.GetUninitializedObject(typeof(GH_RibbonPanel));
            pufferfishPanel.Name = "Twisted Box";
            adapter.ApplyTab(pufferfishTab, true, false);
            adapter.ApplyPanel(pufferfishPanel, "Pufferfish", true, false);
            Equal("河豚", pufferfishTab.NameFull); Equal("扭曲盒", pufferfishPanel.Name);
            adapter.ApplyTab(pufferfishTab, false, false);
            adapter.ApplyPanel(pufferfishPanel, "Pufferfish", false, false);
            Equal("Pufferfish", pufferfishTab.NameFull); Equal("Twisted Box", pufferfishPanel.Name);
            Equal("公鸡", RibbonTranslator.Translate("公鸡", false));
            Console.WriteLine("PASS real SDK ribbon names: Chinese, bilingual, repeated updates, exact restoration, unknown-plugin isolation");
            return 0;
        }
        catch (Exception e) { Console.WriteLine("FAIL " + e); return 1; }
    }
}
