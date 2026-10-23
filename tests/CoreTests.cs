using System;
using GrasshopperChinese;

class CoreTests
{
    static int failures;
    static void Test(string name, Action action)
    {
        try { action(); Console.WriteLine("PASS " + name); }
        catch (Exception e) { failures++; Console.WriteLine("FAIL " + name + ": " + e.Message); }
    }
    static void Equal(string expected, string actual)
    { if (expected != actual) throw new Exception("Expected '" + expected + "', got '" + actual + "'"); }
    static void Throws(Action action)
    { try { action(); } catch (ArgumentException) { return; } throw new Exception("Invalid language pack accepted"); }
    static int Main()
    {
        Test("native assembly identification survives shadow-copy paths", delegate {
            Equal("True", NativeTools.Contains("Grasshopper").ToString());
            Equal("True", NativeTools.Contains("CurveComponents").ToString());
            Equal("True", NativeTools.Contains("GalapagosComponents").ToString());
            Equal("True", NativeTools.Contains("GhPython").ToString());
            var basePath = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "Languages");
            var names = Catalog.Parse(System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "zh-CN.json")));
            var descriptions = Catalog.Parse(System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "tool-text.zh-CN.json")));
            Equal("查询模型图层", names.Find("Query Model Layers", "Rhino"));
            Equal("查询 Rhino 文档中的所有可用图层。", descriptions.Find("Query a Rhino document for all available layers", "description"));
            Equal("正弦", names.Find("Sine", "Maths"));
            Equal("计算角度的正弦值。", descriptions.Find("Compute the sine of a value", "description"));
            Equal("True", NativeTools.Contains("Kangaroo2Component").ToString());
            Equal("求解器", names.Find("Solver", "Kangaroo2"));
            Equal("组合并应用各项目标的主要袋鼠求解器。", descriptions.Find("The main component where Goals are combined and applied", "description"));
            Equal("False", NativeTools.Contains("GHChinese").ToString());
        });
        Test("Params slider name and description match; unknown descriptions fall back", delegate {
            var basePath = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "Languages");
            var c = Catalog.Parse(System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "zh-CN.json")));
            var d = Catalog.Parse(System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "tool-text.zh-CN.json")));
            Equal("数值滑块", c.Find("Number Slider", "Params"));
            Equal("通过滑块设置单个数值。", d.Find("Numeric slider for single values", "description"));
            Equal(null, d.Find("Unknown description", "description"));
        });
        Test("bundled language pack validates and translates common components", delegate {
            var path = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "Languages", "zh-CN.json");
            var c = Catalog.Parse(System.IO.File.ReadAllText(path));
            Equal("移动", c.Find("Move", "Transform"));
            if (c.Count < 600) throw new Exception("Bundled dictionary unexpectedly incomplete");
        });
        Test("port translations use separate keys and preserve unknown text", delegate {
            var basePath = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "Languages");
            var c = Catalog.Parse(System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "zh-CN.json")));
            var d = Catalog.Parse(System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "tool-text.zh-CN.json")));
            Equal("几何", c.Find("Geometry", "port-name"));
            Equal("待变换的基础几何对象。", d.Find("Base geometry", "port-description"));
            Equal(null, d.Find("Untranslated port text", "port-description"));
            Equal("移动", c.Find("Move", "Transform"));
        });
        Test("category-specific entry precedes generic entry", delegate {
            var c = Catalog.Parse("[{\"name\":\"Circle\",\"translation\":\"圆\"},{\"name\":\"Circle\",\"category\":\"Params\",\"translation\":\"圆参数\"}]");
            Equal("圆参数", c.Find("Circle", "Params")); Equal("圆", c.Find("Circle", "Curve"));
        });
        Test("unknown component falls back without translation", delegate { Equal(null, Catalog.Parse("[]").Find("Unknown", "Curve")); });
        Test("malformed pack rejected", delegate { Throws(delegate { Catalog.Parse("{"); }); });
        Test("missing translation rejected", delegate { Throws(delegate { Catalog.Parse("[{\"name\":\"Move\"}]"); }); });
        Test("ambiguous duplicate rejected", delegate { Throws(delegate { Catalog.Parse("[{\"name\":\"Move\",\"translation\":\"移动\"},{\"name\":\"Move\",\"translation\":\"搬移\"}]"); }); });
        Test("scoped display restores after render exception", delegate {
            string name = "Move";
            try { using (new TextScope(() => name, v => name = v, "移动")) { Equal("移动", name); throw new InvalidOperationException(); } }
            catch (InvalidOperationException) { }
            Equal("Move", name);
        });
        Test("default nickname translated but user nickname preserved", delegate {
            Equal("移动", DisplayText.Nickname("Move", "Move", "移动"));
            Equal("我的移动", DisplayText.Nickname("我的移动", "Move", "移动"));
        });
        Console.WriteLine("Failures: " + failures); return failures == 0 ? 0 : 1;
    }
}
