using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.Security.Cryptography;
using System.Text;
using System.Windows.Forms;
using Microsoft.Win32;
using GrasshopperChinese;

[assembly: AssemblyTitle("Grasshopper Offline Setup 0.3.1")]
[assembly: AssemblyVersion("0.3.1.0")]
[assembly: AssemblyFileVersion("0.3.1.0")]

namespace GrasshopperOfflineSetup
{
    [DataContract]
    sealed class PackageFile
    {
        [DataMember(Name = "path")] public string Path { get; set; }
        [DataMember(Name = "sha256")] public string Hash { get; set; }
    }

    [DataContract]
    sealed class PackageManifest
    {
        [DataMember(Name = "format")] public int Format { get; set; }
        [DataMember(Name = "package")] public string Package { get; set; }
        [DataMember(Name = "files")] public List<PackageFile> Files { get; set; }
    }

    [DataContract]
    sealed class InstalledFile
    {
        [DataMember(Name = "target")] public string Target;
        [DataMember(Name = "installedHash")] public string Hash;
        [DataMember(Name = "originalBackup")] public string OriginalBackup;
    }

    [DataContract]
    sealed class Receipt
    {
        [DataMember(Name = "format")] public int Format = 1;
        [DataMember(Name = "package")] public string Package { get; set; }
        [DataMember(Name = "installedAt")] public string InstalledAt;
        [DataMember(Name = "sdk")] public string Sdk;
        [DataMember(Name = "libraries")] public string Libraries;
        [DataMember(Name = "userObjects")] public string UserObjects;
        [DataMember(Name = "files")] public List<InstalledFile> Files;
    }

    sealed class Options
    {
        internal string PackageRoot = AppDomain.CurrentDomain.BaseDirectory;
        internal string RhinoRoot;
        internal string Libraries = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "Grasshopper", "Libraries");
        internal string UserObjects = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "Grasshopper", "UserObjects");
        internal string Packages = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "McNeel", "Rhinoceros", "packages", "8.0");
        internal string State = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "GrasshopperChinese", "OfflineInstaller");
        internal string Log;
        internal string Action;

        internal static Options Parse(string[] args)
        {
            var options = new Options();
            for (int i = 0; i < args.Length; i++)
            {
                string key = args[i];
                if (key == "--install" || key == "--uninstall")
                {
                    if (options.Action != null) throw new ArgumentException("只能选择安装或卸载中的一项。");
                    options.Action = key;
                    continue;
                }
                if (i + 1 == args.Length) throw new ArgumentException("缺少参数值：" + key);
                string value = args[++i];
                switch (key)
                {
                    case "--rhino-root": options.RhinoRoot = value; break;
                    case "--package-root": options.PackageRoot = value; break;
                    case "--libraries": options.Libraries = value; break;
                    case "--user-objects": options.UserObjects = value; break;
                    case "--packages": options.Packages = value; break;
                    case "--state": options.State = value; break;
                    case "--log": options.Log = value; break;
                    default: throw new ArgumentException("未知参数：" + key);
                }
            }
            options.PackageRoot = Path.GetFullPath(options.PackageRoot);
            options.Libraries = Path.GetFullPath(options.Libraries);
            options.UserObjects = Path.GetFullPath(options.UserObjects);
            options.Packages = Path.GetFullPath(options.Packages);
            options.State = Path.GetFullPath(options.State);
            return options;
        }
    }

    sealed class CopyPlan
    {
        internal string Source, Target;
    }

    sealed class Change
    {
        internal string Target, Prior;
    }

    sealed class Installer
    {
        internal static readonly string[] Packs = { "zh-CN.json", "tool-text.zh-CN.json", "pufferfish.zh-CN.json", "pufferfish-text.zh-CN.json", "richedgraphmapper.zh-CN.json" };
        static readonly string[] Notices = { "README.md", "THIRD-PARTY-NOTICES.md", "LICENSE-MultilingualGH.txt" };
        readonly Options options;
        readonly Action<string> report;
        readonly string localization, fishDestination, subdDestination, receiptPath;

        internal Installer(Options options, Action<string> report)
        {
            this.options = options;
            this.report = report;
            localization = Path.Combine(options.Libraries, "GrasshopperChinese");
            fishDestination = Path.Combine(options.Libraries, "PufferfishChineseBundle");
            subdDestination = Path.Combine(options.UserObjects, "PufferfishChineseBundle");
            receiptPath = Path.Combine(options.State, "installation.json");
            var roots = new[] { options.PackageRoot, options.Libraries, options.UserObjects, options.State };
            for (int i = 0; i < roots.Length; i++)
                for (int j = i + 1; j < roots.Length; j++)
                    if (Within(roots[i], roots[j]) || Within(roots[j], roots[i]))
                        throw new ArgumentException("安装包、组件、用户对象和安装记录目录必须互相独立。");
        }

        internal static string Hash(string path)
        {
            using (var file = File.OpenRead(path))
            using (var sha = SHA256.Create()) return BitConverter.ToString(sha.ComputeHash(file)).Replace("-", "");
        }

        internal static bool Within(string path, string root)
        {
            path = Path.GetFullPath(path);
            root = Path.GetFullPath(root).TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
            return string.Equals(path.TrimEnd(Path.DirectorySeparatorChar), root, StringComparison.OrdinalIgnoreCase) ||
                path.StartsWith(root + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase);
        }

        static bool SameHash(string left, string right)
        { return string.Equals(left, right, StringComparison.OrdinalIgnoreCase); }

        static T ReadJson<T>(string path)
        {
            using (var stream = new MemoryStream(Encoding.UTF8.GetBytes(File.ReadAllText(path, Encoding.UTF8))))
                return (T)new DataContractJsonSerializer(typeof(T)).ReadObject(stream);
        }

        static void WriteReceipt(string path, Receipt receipt)
        {
            string temporary = path + "." + Guid.NewGuid().ToString("N") + ".tmp";
            try
            {
                using (var stream = File.Create(temporary)) new DataContractJsonSerializer(typeof(Receipt)).WriteObject(stream, receipt);
                if (File.Exists(path)) File.Replace(temporary, path, null);
                else File.Move(temporary, path);
            }
            finally { if (File.Exists(temporary)) File.Delete(temporary); }
        }

        static void RequireRhinoClosed()
        {
            foreach (string name in new[] { "Rhino", "Rhino8" })
            {
                var processes = Process.GetProcessesByName(name);
                try { if (processes.Length != 0) throw new InvalidOperationException("请保存工作并关闭全部 Rhino 窗口，再安装或卸载。"); }
                finally { foreach (var process in processes) process.Dispose(); }
            }
        }

        static void RequireNoLinks(string path)
        {
            var current = new DirectoryInfo(Directory.Exists(path) ? path : Path.GetDirectoryName(path));
            while (current != null)
            {
                if (current.Exists && (current.Attributes & FileAttributes.ReparsePoint) != 0)
                    throw new IOException("为保护原文件，不支持符号链接或目录联接：" + current.FullName);
                current = current.Parent;
            }
            if (File.Exists(path) && (File.GetAttributes(path) & FileAttributes.ReparsePoint) != 0)
                throw new IOException("不支持链接文件：" + path);
        }

        static IEnumerable<string> FindFiles(string root, string pattern)
        {
            if (!Directory.Exists(root)) yield break;
            var directories = new Stack<string>();
            directories.Push(root);
            while (directories.Count != 0)
            {
                string directory = directories.Pop();
                RequireNoLinks(directory);
                foreach (string file in Directory.GetFiles(directory, pattern))
                {
                    RequireNoLinks(file);
                    yield return file;
                }
                foreach (string child in Directory.GetDirectories(directory)) directories.Push(child);
            }
        }

        PackageManifest ValidatePackage()
        {
            report("正在校验离线包……");
            RequireNoLinks(options.PackageRoot);
            string manifestPath = Path.Combine(options.PackageRoot, "package-manifest.json");
            if (!File.Exists(manifestPath)) throw new IOException("安装包不完整。请完整解压 ZIP 后双击 Setup.exe，不要单独复制安装程序。");
            var manifest = ReadJson<PackageManifest>(manifestPath);
            if (manifest == null || manifest.Format != 1 || manifest.Files == null || manifest.Files.Count == 0 || string.IsNullOrWhiteSpace(manifest.Package))
                throw new InvalidDataException("不支持此安装包清单格式。");
            var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (var entry in manifest.Files)
            {
                if (entry == null || string.IsNullOrWhiteSpace(entry.Path) || Path.IsPathRooted(entry.Path) || entry.Path.Contains(":"))
                    throw new InvalidDataException("安装清单包含无效路径。");
                string path = Path.GetFullPath(Path.Combine(options.PackageRoot, entry.Path));
                if (!Within(path, options.PackageRoot) || !seen.Add(path)) throw new InvalidDataException("安装清单包含重复或越界路径。");
                RequireNoLinks(path);
                if (!File.Exists(path) || !SameHash(Hash(path), entry.Hash))
                    throw new InvalidDataException("文件校验失败：" + entry.Path + "。请重新获取并完整解压安装包。");
            }
            var required = new List<string> { "Setup.exe", "src\\Core.cs", "src\\Plugin.cs", "src\\RibbonTranslator.cs", "Pufferfish\\Pufferfish3-0.gha", "Pufferfish\\AUTHOR-NOTES.txt" };
            required.AddRange(Notices);
            required.AddRange(Packs.Select(name => "Languages\\" + name));
            foreach (string path in required)
                if (!seen.Contains(Path.GetFullPath(Path.Combine(options.PackageRoot, path)))) throw new InvalidDataException("安装清单缺少：" + path);
            var subd = manifest.Files.Where(file => file.Path.StartsWith("Pufferfish\\SubD\\", StringComparison.OrdinalIgnoreCase) && file.Path.EndsWith(".ghuser", StringComparison.OrdinalIgnoreCase)).ToList();
            if (subd.Count != 10 || subd.Any(file => Path.GetDirectoryName(file.Path) != "Pufferfish\\SubD")) throw new InvalidDataException("河豚 SubD 用户对象不完整。");
            foreach (string pack in Packs) Catalog.Parse(File.ReadAllText(Path.Combine(options.PackageRoot, "Languages", pack), Encoding.UTF8));
            return manifest;
        }

        internal static string FindRhino()
        {
            var candidates = new List<string>();
            foreach (var view in new[] { RegistryView.Registry64, RegistryView.Registry32 })
            {
                using (var machine = RegistryKey.OpenBaseKey(RegistryHive.LocalMachine, view))
                using (var install = machine.OpenSubKey(@"SOFTWARE\McNeel\Rhinoceros\8.0\Install"))
                {
                    if (install == null) continue;
                    foreach (string name in new[] { "InstallPath", "Path", "InstallDir" })
                    {
                        string path = install.GetValue(name) as string;
                        if (string.IsNullOrWhiteSpace(path)) continue;
                        path = path.TrimEnd('\\');
                        if (string.Equals(Path.GetFileName(path), "System", StringComparison.OrdinalIgnoreCase)) path = Path.GetDirectoryName(path);
                        candidates.Add(path);
                    }
                }
            }
            candidates.Add(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "Rhino 8"));
            return candidates.FirstOrDefault(path => File.Exists(Path.Combine(path, "Plug-ins", "Grasshopper", "Grasshopper.dll")));
        }

        static string CompilerPath()
        { return Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Windows), "Microsoft.NET", "Framework64", "v4.0.30319", "csc.exe"); }

        static string Quote(string value)
        {
            var result = new StringBuilder("\"");
            int slashes = 0;
            foreach (char character in value)
            {
                if (character == '\\') { slashes++; continue; }
                result.Append('\\', character == '"' ? slashes * 2 + 1 : slashes);
                result.Append(character);
                slashes = 0;
            }
            result.Append('\\', slashes * 2);
            return result.Append('"').ToString();
        }

        string Compile(string staging, out Version sdkVersion)
        {
            string rhino = options.RhinoRoot ?? FindRhino();
            if (string.IsNullOrWhiteSpace(rhino)) throw new DirectoryNotFoundException("未找到 Rhino 8。请在安装窗口选择 Rhino 8 文件夹。");
            rhino = Path.GetFullPath(rhino);
            string sdk = Path.Combine(rhino, "Plug-ins", "Grasshopper", "Grasshopper.dll");
            string rhinoCommon = Path.Combine(rhino, "System", "RhinoCommon.dll");
            foreach (string file in new[] { sdk, rhinoCommon, Path.Combine(rhino, "System", "Rhino.exe") })
                if (!File.Exists(file)) throw new FileNotFoundException("Rhino 安装不完整：" + file);
            sdkVersion = AssemblyName.GetAssemblyName(sdk).Version;
            if (sdkVersion.Major != 8) throw new InvalidOperationException("只支持 Windows Rhino 8，当前 SDK 为 " + sdkVersion + "。");
            string compiler = CompilerPath();
            if (!File.Exists(compiler)) throw new FileNotFoundException("缺少 .NET Framework 编译工具。请安装微软 .NET Framework 4.8 或 4.8.1。");
            string output = Path.Combine(staging, "GrasshopperChinese.gha");
            var references = new[] { "System.Drawing.dll", "System.Windows.Forms.dll", "System.Runtime.Serialization.dll", Path.Combine(Path.GetDirectoryName(compiler), "netstandard.dll"), Path.Combine(rhino, "System", "Eto.dll"), rhinoCommon, sdk, Path.Combine(rhino, "Plug-ins", "Grasshopper", "GH_IO.dll") };
            foreach (string file in references.Where(Path.IsPathRooted))
                if (!File.Exists(file)) throw new FileNotFoundException("离线编译依赖缺失：" + file);
            var arguments = new List<string> { "/nologo", "/utf8output", "/target:library", "/optimize+", "/platform:anycpu", "/out:" + output };
            arguments.AddRange(references.Select(file => "/r:" + file));
            arguments.AddRange(new[] { "Core.cs", "Plugin.cs", "RibbonTranslator.cs" }.Select(name => Path.Combine(options.PackageRoot, "src", name)));
            report("正在用本机 Rhino " + sdkVersion + " 离线编译汉化插件……");
            var diagnostics = new StringBuilder();
            var start = new ProcessStartInfo(compiler, string.Join(" ", arguments.Select(Quote))) {
                UseShellExecute = false, CreateNoWindow = true, RedirectStandardOutput = true, RedirectStandardError = true,
                StandardOutputEncoding = Encoding.UTF8, StandardErrorEncoding = Encoding.UTF8
            };
            using (var process = new Process { StartInfo = start })
            {
                DataReceivedEventHandler collect = delegate(object sender, DataReceivedEventArgs args) { if (args.Data != null) lock (diagnostics) diagnostics.AppendLine(args.Data); };
                process.OutputDataReceived += collect;
                process.ErrorDataReceived += collect;
                process.Start();
                process.BeginOutputReadLine();
                process.BeginErrorReadLine();
                if (!process.WaitForExit(120000)) { process.Kill(); process.WaitForExit(); throw new TimeoutException("离线编译超时，现有插件未替换。"); }
                process.WaitForExit();
                if (process.ExitCode != 0 || !File.Exists(output)) throw new InvalidOperationException("本机 SDK 编译失败，现有插件未替换：" + Environment.NewLine + diagnostics);
            }
            return output;
        }

        Receipt ReadReceipt(bool required)
        {
            RequireNoLinks(receiptPath);
            if (!File.Exists(receiptPath))
            {
                if (required) throw new FileNotFoundException("未找到本包安装记录，不会删除其他方式安装的插件。");
                return null;
            }
            var receipt = ReadJson<Receipt>(receiptPath);
            if (receipt == null || receipt.Format != 1 || receipt.Files == null || !string.Equals(Path.GetFullPath(receipt.Libraries), options.Libraries, StringComparison.OrdinalIgnoreCase) || !string.Equals(Path.GetFullPath(receipt.UserObjects), options.UserObjects, StringComparison.OrdinalIgnoreCase))
                throw new InvalidDataException("安装记录格式无效或属于其他目标目录。为保护原文件，操作已停止。");
            var targets = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (var file in receipt.Files)
            {
                if (file == null || string.IsNullOrWhiteSpace(file.Target) || string.IsNullOrWhiteSpace(file.Hash)) throw new InvalidDataException("安装记录不完整。");
                file.Target = Path.GetFullPath(file.Target);
                if (!new[] { localization, fishDestination, subdDestination }.Any(root => Within(file.Target, root) && !string.Equals(file.Target, root, StringComparison.OrdinalIgnoreCase)) || !targets.Add(file.Target))
                    throw new InvalidDataException("安装记录中存在重复或越界目标。");
                RequireNoLinks(file.Target);
                if (Directory.Exists(file.Target)) throw new IOException("安装目标被同名文件夹占用：" + file.Target);
                if (!string.IsNullOrEmpty(file.OriginalBackup))
                {
                    file.OriginalBackup = Path.GetFullPath(file.OriginalBackup);
                    if (!Within(file.OriginalBackup, Path.Combine(options.State, "Backups")) || !File.Exists(file.OriginalBackup)) throw new FileNotFoundException("原文件备份缺失或路径无效，操作已停止。");
                    RequireNoLinks(file.OriginalBackup);
                }
            }
            return receipt;
        }

        List<CopyPlan> Plan(PackageManifest manifest, Receipt previous, out List<InstalledFile> retired)
        {
            retired = new List<InstalledFile>();
            var plan = Packs.Select(name => new CopyPlan { Source = Path.Combine(options.PackageRoot, "Languages", name), Target = Path.Combine(localization, "Languages", name) }).ToList();
            plan.AddRange(Notices.Select(name => new CopyPlan { Source = Path.Combine(options.PackageRoot, name), Target = Path.Combine(localization, name) }));
            string fish = Path.Combine(options.PackageRoot, "Pufferfish", "Pufferfish3-0.gha");
            var fishName = AssemblyName.GetAssemblyName(fish);
            if (fishName.Name != "Pufferfish" || fishName.Version.ToString() != "3.0.0.0") throw new InvalidDataException("包内不是 Pufferfish 3.0 原插件。");
            var existingFish = new List<string>();
            foreach (string file in new[] { options.Libraries, options.Packages }.SelectMany(root => FindFiles(root, "*.gha")).Distinct(StringComparer.OrdinalIgnoreCase))
            {
                string name;
                try { name = AssemblyName.GetAssemblyName(file).Name; }
                catch (BadImageFormatException) { continue; }
                if (name == "GrasshopperChinese" && !Within(file, localization)) throw new IOException("发现其他汉化插件副本，请先移出扫描目录：" + file);
                if (name == "Pufferfish") existingFish.Add(file);
            }
            if (existingFish.Count > 1) throw new IOException("发现多份河豚插件，请保留一份并将其他版本移出扫描目录，不会自动删除。");
            string externalFish = existingFish.FirstOrDefault(file => !Within(file, fishDestination));
            if (externalFish != null)
            {
                if (!SameHash(Hash(externalFish), Hash(fish))) throw new IOException("现有河豚与包内 3.0 文件不同，不会覆盖：" + externalFish);
                report("保留现有河豚 3.0，不重复复制。");
            }
            else
            {
                plan.Add(new CopyPlan { Source = fish, Target = Path.Combine(fishDestination, "Pufferfish3-0.gha") });
                plan.Add(new CopyPlan { Source = Path.Combine(options.PackageRoot, "Pufferfish", "AUTHOR-NOTES.txt"), Target = Path.Combine(fishDestination, "AUTHOR-NOTES.txt") });
            }
            var existingSubD = new[] { options.UserObjects, options.Packages }.SelectMany(root => FindFiles(root, "*.ghuser")).Distinct(StringComparer.OrdinalIgnoreCase).ToList();
            foreach (var entry in manifest.Files.Where(file => file.Path.StartsWith("Pufferfish\\SubD\\", StringComparison.OrdinalIgnoreCase) && file.Path.EndsWith(".ghuser", StringComparison.OrdinalIgnoreCase)))
            {
                string source = Path.Combine(options.PackageRoot, entry.Path);
                string name = Path.GetFileName(source);
                string target = Path.Combine(subdDestination, name);
                string sourceHash = Hash(source);
                var existing = existingSubD.Where(file => string.Equals(Path.GetFileName(file), name, StringComparison.OrdinalIgnoreCase)).ToList();
                var external = existing.Where(file => !string.Equals(file, target, StringComparison.OrdinalIgnoreCase)).ToList();
                if (external.Count > 1) throw new IOException("发现多份外部 SubD 用户对象，请保留备份并先处理重复版本：" + name);
                if (external.Count == 0)
                {
                    plan.Add(new CopyPlan { Source = source, Target = target });
                    continue;
                }
                if (!SameHash(Hash(external[0]), sourceHash)) throw new IOException("现有 SubD 对象有不同内容或个人修改，不会覆盖：" + external[0]);
                var old = previous == null ? null : previous.Files.FirstOrDefault(file => string.Equals(file.Target, target, StringComparison.OrdinalIgnoreCase));
                if (old != null)
                {
                    if (!string.IsNullOrEmpty(old.OriginalBackup) || !SameHash(old.Hash, sourceHash))
                        throw new IOException("本包 SubD 有受保护的原文件备份或不同内容，请先备份并整理：" + target);
                    if (File.Exists(target) && !SameHash(Hash(target), old.Hash)) throw new IOException("本包 SubD 有个人修改，不会移除：" + target);
                    retired.Add(old);
                }
                else if (File.Exists(target)) throw new IOException("发现未由本安装器记录的重复 SubD 用户对象，不会自动移除：" + target);
                report("复用已有 SubD 用户对象：" + external[0]);
            }
            return plan;
        }

        static void CopyVerified(string source, string target)
        {
            RequireNoLinks(target);
            Directory.CreateDirectory(Path.GetDirectoryName(target));
            File.Copy(source, target, true);
            if (!SameHash(Hash(source), Hash(target))) throw new IOException("复制校验失败：" + target);
        }

        internal void Install()
        {
            RequireRhinoClosed();
            var manifest = ValidatePackage();
            RequireNoLinks(options.State);
            var previous = ReadReceipt(false);
            List<InstalledFile> retired;
            var plan = Plan(manifest, previous, out retired);
            foreach (var entry in plan)
            {
                RequireNoLinks(entry.Target);
                if (Directory.Exists(entry.Target)) throw new IOException("目标被同名目录占用：" + entry.Target);
                var old = previous == null ? null : previous.Files.FirstOrDefault(file => string.Equals(file.Target, entry.Target, StringComparison.OrdinalIgnoreCase));
                if (old != null && (!File.Exists(entry.Target) || !SameHash(Hash(entry.Target), old.Hash))) throw new IOException("上次安装文件被修改，请先备份或整理：" + entry.Target);
            }
            Directory.CreateDirectory(options.State);
            string run = DateTime.Now.ToString("yyyyMMdd-HHmmss") + "-" + Guid.NewGuid().ToString("N").Substring(0, 8);
            string staging = Path.Combine(options.State, "Staging-" + run);
            string backup = Path.Combine(options.State, "Backups", run);
            var changes = new List<Change>();
            string previousReceipt = null;
            bool receiptTouched = false;
            try
            {
                Directory.CreateDirectory(staging);
                Version sdk;
                string compiled = Compile(staging, out sdk);
                string plugin = Path.Combine(localization, "GrasshopperChinese.gha");
                RequireNoLinks(plugin);
                if (Directory.Exists(plugin)) throw new IOException("插件目标被同名目录占用。");
                var oldPlugin = previous == null ? null : previous.Files.FirstOrDefault(file => string.Equals(file.Target, plugin, StringComparison.OrdinalIgnoreCase));
                if (oldPlugin != null && (!File.Exists(plugin) || !SameHash(Hash(plugin), oldPlugin.Hash))) throw new IOException("原汉化插件有个人修改，不会覆盖。");
                RequireRhinoClosed();
                plan = Plan(manifest, previous, out retired);
                plan.Add(new CopyPlan { Source = compiled, Target = plugin });
                Directory.CreateDirectory(backup);
                if (File.Exists(receiptPath))
                {
                    previousReceipt = Path.Combine(backup, "previous-installation.json");
                    CopyVerified(receiptPath, previousReceipt);
                }
                var retiredChanges = new List<Change>();
                for (int i = 0; i < retired.Count; i++)
                {
                    var file = retired[i];
                    if (!File.Exists(file.Target)) continue;
                    if (!SameHash(Hash(file.Target), file.Hash)) throw new IOException("安装期间 SubD 文件发生变化：" + file.Target);
                    string prior = Path.Combine(backup, "subd-retired-" + i.ToString("D3") + ".backup");
                    CopyVerified(file.Target, prior);
                    retiredChanges.Add(new Change { Target = file.Target, Prior = prior });
                }
                foreach (var change in retiredChanges)
                {
                    if (!SameHash(Hash(change.Target), Hash(change.Prior))) throw new IOException("安装期间 SubD 文件发生变化：" + change.Target);
                    changes.Add(change);
                    File.Delete(change.Target);
                    report("已备份并移出本包重复 SubD：" + change.Target);
                }
                var records = new List<InstalledFile>();
                report("正在备份并安装汉化、河豚和 SubD 用户对象……");
                for (int i = 0; i < plan.Count; i++)
                {
                    var entry = plan[i];
                    string prior = null;
                    if (File.Exists(entry.Target))
                    {
                        prior = Path.Combine(backup, i.ToString("D3") + ".backup");
                        CopyVerified(entry.Target, prior);
                    }
                    var old = previous == null ? null : previous.Files.FirstOrDefault(file => string.Equals(file.Target, entry.Target, StringComparison.OrdinalIgnoreCase));
                    if (old != null && (!File.Exists(entry.Target) || !SameHash(Hash(entry.Target), old.Hash))) throw new IOException("安装期间原文件发生变化：" + entry.Target);
                    changes.Add(new Change { Target = entry.Target, Prior = prior });
                    CopyVerified(entry.Source, entry.Target);
                    records.Add(new InstalledFile { Target = entry.Target, Hash = Hash(entry.Target), OriginalBackup = old == null ? prior : old.OriginalBackup });
                }
                if (previous != null) records.AddRange(previous.Files.Where(file => !retired.Contains(file) && !records.Any(record => string.Equals(record.Target, file.Target, StringComparison.OrdinalIgnoreCase))));
                receiptTouched = true;
                WriteReceipt(receiptPath, new Receipt { Package = manifest.Package, InstalledAt = DateTime.Now.ToString("o"), Sdk = sdk.ToString(), Libraries = options.Libraries, UserObjects = options.UserObjects, Files = records });
                report("安装完成：" + localization);
                report("旧文件备份：" + backup);
                report("现在可启动 Rhino 8，输入 Grasshopper 验收。其他 Rhino 8 小版本及 WIP SubD 仍需实际验证。");
            }
            catch
            {
                for (int i = changes.Count - 1; i >= 0; i--)
                {
                    var change = changes[i];
                    try
                    {
                        if (change.Prior != null)
                        {
                            if (!File.Exists(change.Target) || !SameHash(Hash(change.Target), Hash(change.Prior))) CopyVerified(change.Prior, change.Target);
                        }
                        else if (File.Exists(change.Target)) File.Delete(change.Target);
                    }
                    catch (Exception ex) { report("回滚未完成，请保留备份 " + backup + "：" + ex.Message); }
                }
                if (receiptTouched)
                {
                    try
                    {
                        if (previousReceipt != null)
                        {
                            if (!File.Exists(receiptPath) || !SameHash(Hash(receiptPath), Hash(previousReceipt))) CopyVerified(previousReceipt, receiptPath);
                        }
                        else if (File.Exists(receiptPath)) File.Delete(receiptPath);
                    }
                    catch (Exception ex) { report("安装记录回滚未完成，请保留备份 " + backup + "：" + ex.Message); }
                }
                throw;
            }
            finally { if (Directory.Exists(staging)) Directory.Delete(staging, true); }
        }

        internal void Uninstall()
        {
            RequireRhinoClosed();
            var receipt = ReadReceipt(true);
            var remaining = new List<InstalledFile>(receipt.Files);
            foreach (var file in receipt.Files)
            {
                if (File.Exists(file.Target) && !SameHash(Hash(file.Target), file.Hash))
                {
                    report("保留个人修改：" + file.Target);
                    continue;
                }
                if (!string.IsNullOrEmpty(file.OriginalBackup)) CopyVerified(file.OriginalBackup, file.Target);
                else if (File.Exists(file.Target)) File.Delete(file.Target);
                remaining.Remove(file);
                receipt.Files = new List<InstalledFile>(remaining);
                WriteReceipt(receiptPath, receipt);
            }
            if (remaining.Count == 0)
            {
                File.Delete(receiptPath);
                report("卸载完成，已恢复原文件。已有河豚、个人文件、用户设置和备份均保留。");
            }
            else report("已卸载未修改的文件；个人修改及其安装记录已保留。");
        }
    }

    sealed class SetupForm : Form
    {
        readonly Options options;
        readonly TextBox rhino = new TextBox { Dock = DockStyle.Fill };
        readonly TextBox output = new TextBox { Multiline = true, ReadOnly = true, ScrollBars = ScrollBars.Vertical, Dock = DockStyle.Fill };
        readonly Button install = new Button { Text = "安装 / 更新", AutoSize = true };
        readonly Button uninstall = new Button { Text = "卸载并恢复旧版", AutoSize = true };
        readonly Button browse = new Button { Text = "选择 Rhino 8…", AutoSize = true };
        readonly BackgroundWorker worker = new BackgroundWorker();
        bool running;

        internal SetupForm(Options options)
        {
            this.options = options;
            Text = "Grasshopper 汉化 0.3.1 + 河豚 3.0 离线安装";
            Font = new Font("Microsoft YaHei UI", 9F);
            ClientSize = new Size(720, 460);
            MinimumSize = new Size(620, 400);
            StartPosition = FormStartPosition.CenterScreen;
            var layout = new TableLayoutPanel { Dock = DockStyle.Fill, Padding = new Padding(15), ColumnCount = 2, RowCount = 4 };
            layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
            layout.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize));
            layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            layout.RowStyles.Add(new RowStyle(SizeType.Percent, 100));
            layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            var introduction = new Label { Text = "请先保存工作并关闭 Rhino。完整解压后点击安装。\n全程离线；不使用 PowerShell，不改变系统安全策略。\n支持已安装的 Rich Graph Mapper 汉化；本包不包含该插件本体。", AutoSize = true, Padding = new Padding(0, 0, 0, 12) };
            layout.Controls.Add(introduction, 0, 0); layout.SetColumnSpan(introduction, 2);
            layout.Controls.Add(rhino, 0, 1); layout.Controls.Add(browse, 1, 1);
            layout.Controls.Add(output, 0, 2); layout.SetColumnSpan(output, 2);
            var buttons = new FlowLayoutPanel { AutoSize = true, Dock = DockStyle.Fill };
            buttons.Controls.Add(install); buttons.Controls.Add(uninstall);
            layout.Controls.Add(buttons, 0, 3); layout.SetColumnSpan(buttons, 2);
            Controls.Add(layout);
            try { rhino.Text = options.RhinoRoot ?? Installer.FindRhino() ?? ""; }
            catch (Exception ex) { Append(ex.Message); }
            browse.Click += delegate {
                using (var dialog = new FolderBrowserDialog { Description = "选择含 System 与 Plug-ins 文件夹的 Rhino 8 安装目录", SelectedPath = rhino.Text })
                    if (dialog.ShowDialog(this) == DialogResult.OK) rhino.Text = dialog.SelectedPath;
            };
            install.Click += delegate { Run(false); };
            uninstall.Click += delegate { Run(true); };
            worker.DoWork += delegate(object sender, DoWorkEventArgs args) {
                var installer = new Installer(options, Report);
                if ((bool)args.Argument) installer.Uninstall(); else installer.Install();
            };
            worker.RunWorkerCompleted += delegate(object sender, RunWorkerCompletedEventArgs args) {
                running = false;
                install.Enabled = uninstall.Enabled = browse.Enabled = rhino.Enabled = true;
                if (args.Error != null) { Append("操作停止：" + args.Error.Message); MessageBox.Show(this, args.Error.Message, "安装未完成", MessageBoxButtons.OK, MessageBoxIcon.Warning); }
                else MessageBox.Show(this, "操作已完成，请查看窗口中的安装记录。", "完成", MessageBoxButtons.OK, MessageBoxIcon.Information);
            };
            FormClosing += delegate(object sender, FormClosingEventArgs args) { if (running) { args.Cancel = true; MessageBox.Show(this, "请等待当前操作完成后关闭。", "正在处理"); } };
        }

        void Run(bool remove)
        {
            if (remove && MessageBox.Show(this, "按安装记录卸载本包并恢复旧文件？个人修改会保留。", "确认卸载", MessageBoxButtons.YesNo, MessageBoxIcon.Question) != DialogResult.Yes) return;
            options.RhinoRoot = string.IsNullOrWhiteSpace(rhino.Text) ? null : rhino.Text.Trim();
            output.Clear();
            running = true;
            install.Enabled = uninstall.Enabled = browse.Enabled = rhino.Enabled = false;
            worker.RunWorkerAsync(remove);
        }

        void Report(string text) { BeginInvoke(new Action<string>(Append), text); }
        void Append(string text) { output.AppendText(text + Environment.NewLine); }
    }

    static class Program
    {
        [STAThread]
        static int Main(string[] args)
        {
            Options options = null;
            bool commandLine = args.Contains("--install") || args.Contains("--uninstall");
            try
            {
                options = Options.Parse(args);
                if (options.Action == null)
                {
                    Application.EnableVisualStyles();
                    Application.SetCompatibleTextRenderingDefault(false);
                    Application.Run(new SetupForm(options));
                    return 0;
                }
                var lines = new List<string>();
                Action<string> report = delegate(string text) { lines.Add(text); Console.WriteLine(text); };
                try
                {
                    var installer = new Installer(options, report);
                    if (options.Action == "--install") installer.Install(); else installer.Uninstall();
                    return 0;
                }
                catch (Exception ex) { report("操作停止：" + ex.Message); return 1; }
                finally { if (options.Log != null) File.WriteAllLines(options.Log, lines, Encoding.UTF8); }
            }
            catch (Exception ex)
            {
                if (commandLine) Console.Error.WriteLine(ex.Message);
                else MessageBox.Show(ex.Message, "安装器启动失败", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return 1;
            }
        }
    }
}
