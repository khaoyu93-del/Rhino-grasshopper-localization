import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / 'docs/pufferfish-catalog.json').read_text(encoding='utf-8-sig'))
source['tools'] += source.get('users', [])


def pairs(text):
    return dict(line.rsplit('|', 1) for line in text.strip().splitlines() if '|' in line)


terms = pairs('''
Twisted Boxes|扭曲盒
Twisted Box|扭曲盒
Polysurfaces|多重曲面
Polysurface|多重曲面
Domain²s|二维区间
Domain²|二维区间
Sub-Domain²s|二维子区间
Sub-Domain U|U 子区间
Sub-Domain V|V 子区间
Sub-Domains|子区间
Arithmetic mean|算术平均值
Arc/Circle/Ellipse|圆弧/圆/椭圆
Curve Graph Mapper|曲线图形映射器
Curve Align Curve Seams|沿曲线对齐曲线接缝
Parameter Curve Divide Rectangle|按曲线参数分割矩形
Parameter Curve Divide Surface|按曲线参数分割曲面
Parameter Plane Divide Surface|按平面参数分割曲面
Parameter Point Divide Surface|按点参数分割曲面
Parameter Plane In Rectangle|矩形内参数平面
Parameter Plane On Surface|曲面上参数平面
Parameter Point In Rectangle|矩形内参数点
Parameter Point On Surface|曲面上参数点
Parameter Rectangle Grid|矩形参数网格
Parameter Rectangular Grid|矩形参数网格
Parameter Rectangle Isocurve|矩形参数等参线
Parameter Surface Isocurve|曲面参数等参线
Parameter Rectangle Mesh|矩形参数网格面
Parameter Plane Mesh|平面参数网格面
Parameter Surface Mesh|曲面参数网格面
Parameter Surface Grid|曲面参数网格
Parameter Grid On Surface|曲面上参数网格
Parameter Subdivide Surface|按参数细分曲面
Parameter Loft Mesh|按参数放样网格
Parameter Extrude Mesh|按参数挤出网格
Parameter Pipe Mesh|按参数生成管状网格
Point Divide Curve Segments|按点等分曲线段
Point Divide Curve Target Length|按目标长度分割曲线
Point Fit Rectangle|通过点拟合矩形
Point Sort Items|按点排序项目
Point Surface Edge|点的最近曲面边
Point Mesh Side|点相对网格的侧别
Point Plane Side|点相对平面的侧别
Point Surface Side|点相对曲面的侧别
Pinch'n'Spread Points|点收拢与扩散
Pinch'n'Spread|收拢与扩散
Are Points Collinear|点是否共线
Are Points Coplanar|点是否共面
Is Arc/Circle/Ellipse|是否为圆弧/圆/椭圆
Is Curve Kinky|曲线是否有折角
Is Curve Linear|曲线是否为直线
Is Curve Segmented|曲线是否分段
Is Mesh Closed|网格是否闭合
Is Mesh Disjoint|网格是否有分离部分
Is Polysurface Closed|多重曲面是否闭合
Is Surface Closed|曲面是否闭合
Is Surface Collapsed|曲面是否退化
Is Surface Singular|曲面是否有奇点
Is Surface Trimmed|曲面是否已修剪
Equality Within Tolerance|容差内相等判断
Fit Curve Smooth|平滑拟合曲线
Fit Curve Segments|拟合曲线段
Prude Curve|曲线折角平滑连接
Mesh Boolean Twisted Boxes|用网格布尔裁剪扭曲盒
Polysurface Boolean Twisted Boxes|用多重曲面布尔裁剪扭曲盒
Mesh Trim Twisted Boxes|用网格裁剪扭曲盒
Plane Trim Twisted Boxes|用平面裁剪扭曲盒
Surface Trim Twisted Boxes|用曲面裁剪扭曲盒
Morph To Twisted Box|映射至扭曲盒
Reference Twisted Box|引用扭曲盒
2Pt Twisted Box|两点扭曲盒
Move 2Pt|两点移动
Move To Point|移动至点
Twisted Box Curve Variable|可变曲线扭曲盒
Twisted Box Pipe Variable|可变圆管扭曲盒
Twisted Box Tube Variable|可变空心管扭曲盒
Twisted Box Strip Variable|可变条带扭曲盒
Twisted Box Sweep Variable|可变扫掠扭曲盒
Twisted Box Two Curves|两曲线间扭曲盒
Twisted Box Two Meshes|两网格间扭曲盒
Twisted Box Two Surfaces|两曲面间扭曲盒
Twisted Box Consecutive Curves|相邻曲线间扭曲盒
Twisted Box Consecutive Meshes|相邻网格间扭曲盒
Twisted Box Consecutive Surfaces|相邻曲面间扭曲盒
Twisted Box Through Curves|贯穿曲线组扭曲盒
Twisted Box Through Meshes|贯穿网格组扭曲盒
Twisted Box Through Surfaces|贯穿曲面组扭曲盒
Twisted Box Centers|扭曲盒中心点
Twisted Box Corners|扭曲盒角点
Twisted Box Volume|扭曲盒体积
Twisted Box Array|扭曲盒阵列
Twisted Box Curve|沿曲线扭曲盒
Twisted Box Mesh|网格扭曲盒
Twisted Box Surface|曲面扭曲盒
Twisted Box Extrude|挤出扭曲盒
Twisted Box Loft|放样扭曲盒
Twisted Box Sweep|扫掠扭曲盒
Twisted Box Pipe|圆管扭曲盒
Twisted Box Tube|空心管扭曲盒
Twisted Box Strip|条带扭曲盒
Twisted Box Strips|多条带扭曲盒
Vector World|世界方向向量
Vector Star|星形向量
X Plus One|X 加一
X Minus One|X 减一
Zeroed Transform|单位变换
Zero Distance Tolerance|零距离容差
Default Angle Tolerance|默认角度容差
Document Angle Tolerance|文档角度容差
Document Distance Tolerance|文档距离容差
Highest & Lowest Numbers|最大值与最小值
Odd & Even Numbers|奇数与偶数
Color To Point|颜色转点
Point To Color|点转颜色
Last Index Range|末项索引范围
List Length Range|列表长度范围
Reparameterized Range|归一化范围
Last Index|末项索引
Item Index List|项目索引列表
List Indices|列表索引
Dispatch Indices|按索引分派
Sift Indices|按索引筛分
Null Placeholder|空值占位符
Mass Division|连续除法
Mass Subtraction|连续减法
Mass Transform|复合变换
Net On Surface|曲面曲线网
Mesh To Polysurface|网格转多重曲面
Polyline To Mesh|多段线转网格
Seam To Curve Corner|接缝移至曲线角点
Trim Curve With Points|用点修剪曲线
Trim Curve With Plane|用平面修剪曲线
Trim Mesh With Plane|用平面修剪网格
Trim Planes With Plane|用平面裁剪平面组
Trim Points With Plane|用平面裁剪点组
Trim Surface With Plane|用平面修剪曲面
Points Trim Curve|用点修剪曲线
Plane Trim Curve|用平面修剪曲线
Plane Trim Mesh|用平面修剪网格
Plane Trim Planes|用平面裁剪平面组
Plane Trim Points|用平面裁剪点组
Plane Trim Surface|用平面修剪曲面
Slide Curve Along Curve|沿曲线滑动曲线
Slide Within Domain²|二维区间内滑动
Slide Within Domain|区间内滑动
Slide Within Transform|变换内插值
Closest Plane Orientation|最近平面朝向
Constrained Area Ellipse|指定面积椭圆
Constrained Area Polygon|指定面积多边形
Constrained Area Rectangle|指定面积矩形
Constrained Volume Box|指定体积盒
Constrained Volume Ellipsoid|指定体积椭球
Unsplit Rail Revolve Surface|不分裂沿轨道旋转曲面
Unsplit Sum Surface|不分裂和曲面
Automatic Edge Surface|自动边缘曲面
Automatic Network Surface|自动网络曲面
Curve Coil Points|沿曲线螺旋点
Curve Wave Points|沿曲线波浪点
Rotate Quaternion|四元数旋转
Rotate Euler|欧拉旋转
Rotate World|世界坐标旋转
Round To Decimal Place|按小数位舍入
Round To Factor|按倍数舍入
Round To Nearest|舍入至最近值
Scale To Area|缩放至指定面积
Scale To Length|缩放至指定长度
Scale To Volume|缩放至指定体积
Recursive Morph Mesh|递归网格形变
Recursive Transform|递归变换
Extrude Tapered Polysurface|锥度挤出多重曲面
Unsplit Edge Surface|不分裂边缘曲面
Unsplit Extrude Surface|不分裂挤出曲面
Extrude Unsplit Surface|不分裂挤出曲面
Unsplit Loft Surface|不分裂放样曲面
Loft Unsplit Surface|不分裂放样曲面
Unsplit Revolve Surface|不分裂旋转曲面
Revolve Unsplit Surface|不分裂旋转曲面
Unsplit Sweep Surface|不分裂扫掠曲面
Sweep Unsplit Surface|不分裂扫掠曲面
Edge Unsplit Surface|不分裂边缘曲面
Map Point To Surface|点映射至曲面
Remap Surface Domain²|重映射曲面二维区间
Reduce Mesh By Faces|按面数简化网格
Relocate Curve Ends|重定位曲线端点
Swap Surface Directions|交换曲面方向
Shrink Trimmed Surface|收缩已修剪曲面
Split Kinky Surface|按折角分裂曲面
Mesh Loop Edges|网格环边
Mesh Naked Edges|网格裸边
Average|平均
Weighted Average|加权平均
Tween Two|两者补间
Tween Consecutive|相邻补间
Tween Through|贯穿补间
Along Curve|沿曲线
On Curve|在曲线上
On Surface|在曲面上
Curve Middle Point|曲线中点
Curve Length At|曲线至点长度
Curve Length Between|曲线上两点间长度
Curve Edit Points|曲线编辑点
Surface Edit Points|曲面编辑点
Control Point Count|控制点数
Edit Point Count|编辑点数
Kink Point Count|折角点数
Knot Vector Count|节点向量数
Trimmed Face Count|已修剪面数
Untrimmed Face Count|未修剪面数
Triangle Face Count|三角面数
Quad Face Count|四边面数
Count Difference|数量差
First Number|第一个数
Second Number|第二个数
Result Booleans|结果布尔值
Result Boolean|结果布尔值
Number X|X 数值
Sorted Indices|排序后索引
Sorted Items|排序后项目
Sorted Points|排序后点
Kept Indicies|保留索引
Original SU|原始 U 起始值
Original SV|原始 V 起始值
Original EU|原始 U 结束值
Original EV|原始 V 结束值
Original S|原始起始值
Original E|原始结束值
Original U|原始 U 值
Original V|原始 V 值
Original X|原始 X 值
Original Y|原始 Y 值
Original Z|原始 Z 值
Remap Number x|重映射数值 x
Remapped Number x|重映射后数值 x
Remap x|重映射 x
Remapped x|重映射后 x
Pinched & Spread|收拢与扩散结果
At i|位于索引 i
Not i|不位于索引 i
Add One|加一
Minus One|减一
Plus One|加一
Out Of Bounds|超出范围
Both Sides|两侧
Keep Length|保持长度
Flip Normals|反转法向量
Rebuild Normals|重算法向量
Unify Normals|统一法向量
Cull Unused|剔除未使用项
Weld Vertices|焊接顶点
Weld Tolerance|焊接容差
Identical Combine|合并相同项
Partial Transforms|中间变换
Unrolled Curves|展开后曲线
Unrolled Points|展开后点
End Point|终点
End Tangents|末端切向量
Sample Point|采样点
Point Sample|采样点
Point Start|起点
Point End|终点
Mirror Plane|镜像平面
Mirror Index|镜像索引
Mirror Cut|镜像裁剪
Mirror Type|镜像类型
Connection Type|连接类型
Interpolation Type|插值类型
Continuity Type|连续性类型
Subdivision Type|细分类型
Deconstruct Type|解构类型
Division Type|分割类型
Center Type|中心类型
Colored Type|颜色类型
Luminosity Type|亮度类型
Direction Type|方向类型
Evaluation Type|求值类型
Close Type|闭合类型
Corner Type|角点类型
Trim Type|修剪类型
Loft Type|放样类型
Get Type|获取类型
Boolean Type|布尔运算类型
Round Type|舍入类型
Start Type|起始类型
End Type|末端类型
Cap Type|封端类型
Face Type|面类型
Create Solid|生成实体
Face Merge|合并面
Base Mesh|基础网格
Offset Plane|偏移平面
Reach Plane|作用距离平面
Graph Curves|图形曲线
Graph Points|图形点
Value Lines|数值线
Value Points|数值点
Mapped Lines|映射线
Mapped Points|映射点
Number A|数值 A
Number B|数值 B
Domain A|区间 A
Domain B|区间 B
Plane A|平面 A
Plane B|平面 B
Surface A|曲面 A
Surface B|曲面 B
Transform A|变换 A
Transform B|变换 B
Vector A|向量 A
Vector B|向量 B
Curve A|曲线 A
Curve B|曲线 B
Point A|点 A
Point B|点 B
Mesh A|网格 A
Mesh B|网格 B
Twisted Box A|扭曲盒 A
Twisted Box B|扭曲盒 B
Color A|颜色 A
Color B|颜色 B
Accuracy|精度
Actual|实际值
Adjusted|调整后
Align|对齐
Aligned|已对齐
Alpha|透明度
Alternate|交替
Amount|数量
Anchors|锚点
Angle|角度
Angle Tolerance|角度容差
Appended|合并结果
Arc|圆弧
Area|面积
Area Tolerance|面积容差
Automatic|自动
Axis|轴
Back|后侧
Blend|混合
Boolean|布尔值
Boundary|边界
Bounding|包围
Box|盒
Bulge|凸度
Cap|封端
Cells|单元
Center|中心
Centroid|形心
Circle|圆
Closed|闭合
Closest|最近
Coiled|螺旋点
Collinear|共线
Color|颜色
Colored|着色结果
Colors|颜色
Compatibilize|统一兼容
Compatibilized|兼容结果
Control Points|控制点
Coordinates|坐标
Coplanar|共面
Corner|角点
Corners|角点
Count|数量
Curve|曲线
Curves|曲线
Decimal Place|小数位
Deconstruct|解构
Deconstructed|解构结果
Deform|变形
Deformed|变形结果
Degree|次数
Degrees|角度/次数
Deviation Tolerance|偏差容差
Diameter|直径
Diameters|直径
Difference|差值
Dimension|尺寸
Dimensionality|维度
Direction|方向
Discrete|离散
Disjoint|分离
Displace|位移
Displaced|位移结果
Distance|距离
Distances|距离
Distort|扭曲
Divided|分割结果
Division|分割
Divisions|分割数
Domain|区间
Domains|区间
Edge|边
Edges|边
Edit|编辑
Ellipse|椭圆
Ellipsoid|椭球
End|末端
Ends|结束值
Equalized|均匀化
Equality|相等
Inequality|不等
Evaluation|求值
Even|偶数
Explode|分解
Exponents|指数
Extent|范围
Extruded|挤出结果
Face|面
Factor|因子
Factors|因子
Falloffs|衰减
Fit|拟合
Flip|反转
Flipped|反转结果
Front|前侧
Geometries|几何对象
Geometry|几何对象
Grayscale|灰度
Grayscaled|灰度结果
Guide|引导
Highest|最大值
Hollow|空心
Include|包含
Index|索引
Indices|索引
Integer|整数
Intersected|相交状态
Invert|取反
Inverted|取反结果
Isocurve|等参线
Items|项目
Iterative|迭代
Join|连接
Keep|保留
Kinked|折角状态
Kinks|折角
Knots|节点
Labels|标签
Last|最后
Length|长度
Lengths|长度
Linear|线性
Linearize|线性化
Linearized|线性化结果
Lines|直线
List|列表
Location|位置
Locations|位置
Lofted|放样结果
Loopback|循环回接
Loops|环
Lowest|最小值
Mapped|映射结果
Mesh|网格
Meshes|网格
Middle|中间
Mirrored|镜像结果
Morphed|形变结果
Motions|位移向量
Moved|移动结果
Multiplier|乘数
Naked|裸边
Nearest|最近值
Network|网络
New|新
Normal|法向量
Normalize|归一化
Normalized|归一化
Normals|法向量
Null|空值
Number|数值
Numbers|数值
Odd|奇数
Offset|偏移
Offsets|偏移
Open|打开
Openings|开口
Opposite|反向
Original|原始
Parameter|参数
Parameters|参数
Partial|中间结果
Partitions|分段
Partition|分段
Percent|百分比
Percentage|百分比
Piece|部分
Piped|管状结果
Placeholders|占位符
Plane|平面
Planes|平面
Point|点
Points|点
Polygon|多边形
Polyline|多段线
Polylines|多段线
Profile|截面
Quadrangulate|四边形化
Quaternion|四元数
Radians|弧度
Radii|半径
Radius|半径
Radiuses|半径
Rail|轨道
Rails|轨道
Range|范围
Reach|作用距离
Rebuild|重建
Rebuilt|重建结果
Rectangle|矩形
Reduce|简化
Reduced|简化结果
Reference|参考
References|参考
Refit|重新拟合
Relocated|重定位结果
Relocate|重定位
Remainder|余数
Remap|重映射
Remapped|重映射结果
Removal|移除
Reparameterize|重新参数化
Reparameterized|重新参数化结果
Resolution|分辨率
Reverse|反转
Revolution|旋转生成
Rotated|旋转结果
Rotation|旋转
Rotations|旋转
Rotate|旋转
Rounded|舍入结果
Scale|缩放
Scaled|缩放结果
Seam|接缝
Seams|接缝
Search|搜索
Sections|截面
Segment|曲线段
Segments|曲线段
Shell|壳体
Shrunken|收缩结果
Side|侧
Sides|侧
Singular|奇点
Size|尺寸
Sizes|尺寸
Slid|滑动结果
Slide|滑动
Smoothed|平滑结果
Smooth|平滑
Snap|吸附
Source|源
Span|跨度
Spans Only|仅跨度
Split|分割
Start|起始
Starts|起始值
Steps|步数
Strength|强度
Strengths|强度
Subdivided|细分结果
Subdivide|细分
Subtracted|相减结果
Superimpose|套用属性
Superimposed|套用结果
Surface|曲面
Surfaces|曲面
Swap UV|交换 UV
Swapped|交换结果
Tangent|切向量
Tangents|切向量
Target|目标
Targets|目标
Text Size|文字大小
Thickened|加厚结果
Thicken|加厚
Thickness|厚度
Thicknesses|厚度
Tolerance|容差
Transform|变换
Transformed|变换结果
Transforms|变换
Triangles|三角形
Triangulate|三角化
Trim|修剪
Trimmed|修剪结果
Trims|修剪边界
Tween|补间
Underlying|底层曲面
Union|并集
Unroll|展开
Unrolled|展开结果
Unsplit|不分裂
Values|数值
Vector|向量
Vectors|向量
Vertex|顶点
Volume|体积
Voxel|体素
Voxelized|体素化结果
Waved|波浪点
Weighted|加权
Weights|权重
Whole|整数部分
X Axis|X 轴
Y Axis|Y 轴
Statistics|统计
Spans|跨度
Bounding Rectangle|包围矩形
''')


terms.update(pairs('''
SubD A|细分曲面 A
SubD B|细分曲面 B
SubDs|细分曲面
SubD|细分曲面
Crease Type|折痕类型
Interpolate Vertices|插值顶点
Levels|层级
Tweens|补间结果
Blend Type|混合类型
Keep Type|保留类型
Fitted|拟合结果
Opened|打开结果
Prude|平滑连接结果
'''))

term_pattern = re.compile(r'(?<![A-Za-z])(?:' + '|'.join(re.escape(k) for k in sorted(terms, key=len, reverse=True)) + r')(?![A-Za-z])', re.I)
term_lookup = {k.casefold(): v for k, v in terms.items()}


def replace_terms(text):
    return term_pattern.sub(lambda m: term_lookup[m[0].casefold()], text)


name_exceptions = pairs('''
Average SubD|平均细分曲面
Weighted Average SubD|加权平均细分曲面
Tween Two SubDs|两细分曲面补间
Tween Consecutive SubDs|相邻细分曲面补间
Tween Through SubDs|贯穿细分曲面组补间
Mirror Cut SubD|镜像裁剪细分曲面
Twisted Box SubD|细分曲面扭曲盒
Twisted Box Two SubDs|两细分曲面间扭曲盒
Twisted Box Consecutive SubDs|相邻细分曲面间扭曲盒
Twisted Box Through SubDs|贯穿细分曲面组扭曲盒
Blend Two Meshes|两网格逐顶点混合
Blend Consecutive Meshes|相邻网格逐顶点混合
Blend Through Meshes|贯穿网格组逐顶点混合
Evaluate Twisted Box|扭曲盒求值
Rotate Plane XYZ|XYZ 旋转平面
Two Way Domain|双向区间
Two Way Domain²|双向二维区间
Align Curve Seams|对齐曲线接缝
Angle Split Mesh|按角度分割网格
Append Polysurfaces|合并分离的多重曲面
Average Twisted Box|平均扭曲盒
Center Twisted Box|居中扭曲盒
Closest Vector|最近方向向量
Construct Twisted Box|构造扭曲盒
Deconstruct Twisted Box|解构扭曲盒
Curve Degree|曲线次数
Curve Spans|曲线跨度
Curve Statistics|曲线统计
Surface Degree|曲面次数
Surface Spans|曲面跨度
Surface Statistics|曲面统计
Mesh Statistics|网格统计
Close Curve|闭合曲线
Close Mesh|封闭网格
Discrete Polyline|方向离散多段线
Displace Mesh|沿法向位移网格
Fit Surface|拟合曲面
Flip Plane|反转平面
Flip Polysurface|反转多重曲面
Invert Boolean|布尔取反
Invert Color|反色
Offset Curve From Surface|从曲面偏移曲线
Offset Curve|偏移曲线
Offset Mesh|偏移网格
Offset Plane|偏移平面
Offset Surface|偏移曲面
Open Curve|打开曲线
Rectangle Fit|拟合矩形
Rotate Plane Euler|欧拉旋转平面
Rotate Plane XYZ|XYZ 旋转平面
Remap Curve Domain|重映射曲线区间
Rebuild Curve Segments|重建曲线段
Thicken Twisted Box|加厚扭曲盒
Transform Twisted Box|变换扭曲盒
Subdivide Twisted Box|细分扭曲盒
Unroll Polysurface|展开多重曲面
Voxel Mesh|体素网格
Deconstruct Number|解构数值
Partition Number|数值分段
''')


def translate_name(text):
    if text in name_exceptions:
        return name_exceptions[text]
    m = re.fullmatch(r'(Weighted Average|Average|Tween Two|Tween Consecutive|Tween Through|Mirror Combine|Mirror Cut) (.*)', text)
    if m:
        actions = {'Weighted Average': '加权平均', 'Average': '平均', 'Tween Two': '两者补间', 'Tween Consecutive': '相邻补间', 'Tween Through': '贯穿补间', 'Mirror Combine': '镜像合并', 'Mirror Cut': '镜像裁剪'}
        return actions[m[1]] + replace_terms(m[2]).replace(' ', '')
    return replace_terms(text).replace(' ', '')


manual_descriptions = pairs('''
Add one to x.|将 x 加一。
Subtract one from x.|将 x 减一。
Subtract one from {x}.|将 {x} 减一。
Calculate the percentage of a number.|计算数值的百分比。
Construct a domain from one number that becomes the negative and positive extents of the domain from zero.|以单个数值指定从零向正负方向延伸的范围，构造一维区间。
Construct a domain² from one {u} number and one {v} number that becomes the negative and positive extents for each direction of the domain² from zero.|以 {u} 和 {v} 数值指定各方向从零向正负方向延伸的范围，构造二维区间。
Construct a twisted box from a set of 8 corner points.|使用 8 个角点构造扭曲盒。
Convert a color to a point by using the colors RGB values for the points XYZ values.|将颜色 RGB 分量转换为点的 XYZ 坐标。
Convert a point to a color by using the points XYZ values for the colors RGB values.|将点的 XYZ 坐标转换为颜色 RGB 分量。
Convert a color to grayscale by a variety of common luminosity weighting schemes.|使用常见亮度权重方案将颜色转换为灰度。
Convert a mesh into a nurbs polysurface (Brep).|将网格转换为 NURBS 多重曲面（Brep）。
Close an open curve in a variety of ways, if curve is already closed or linear it will output with no change.|使用不同方法闭合开放曲线。曲线已闭合或为直线时原样输出。
Close an open mesh by filling its openings with new mesh faces, if mesh is already closed it will output with no change.|使用新网格面填补开口以封闭网格；已闭合时原样输出。
Create a mesh from a closed or open polyline boundary.|由闭合或开放多段线边界生成网格。
Create a net of interpolated curves on a surface.|在曲面上生成插值曲线网。
Create a plane oriented recursive spatial subdivision of vectors outward from a base planes origin|从基础平面原点向外生成按平面定向的递归空间细分向量。
Create plane axis aligned vectors outward from a base planes origin|从基础平面原点向外生成与平面轴对齐的向量。
Create a plane oriented union bounding rectangle or separate bounding rectangles for geometry.|沿指定平面为几何对象生成联合包围矩形或分别生成包围矩形。
Create a polyline made of target vector oriented segments by finding the closest target vector by angle to each vector between the reference vertices.|为参考顶点之间的每段方向查找夹角最小的目标向量，生成各段沿目标向量定向的多段线。
Create a range of numbers between 0 and 1.|生成 0 到 1 的数值范围。
Create a range of numbers between 0 and the last index of a list (list length -1).|生成从 0 到列表末项索引（列表长度减一）的数值范围。
Create a range of numbers between 0 and the length of a list.|生成从 0 到列表长度的数值范围。
Get the last index of a list (list length -1).|获取列表末项索引（列表长度减一）。
The last index of a list (list length -1).|列表末项索引（列表长度减一）。
Create a series of points which coil along a curve.|生成沿曲线呈螺旋分布的一系列点。
Create a series of points which wave along a curve.|生成沿曲线呈波浪分布的一系列点。
Create a single mass transform by compounding a set of transforms, like Grasshopper's Compound component but with access to partial results (each step of the mass transformation).|复合一组变换生成单个复合变换，类似 Grasshopper 的 Compound 组件，同时可获取每一步的中间结果。
Create a surface between 2, 3, or 4 auto sorted edge curves.|自动排序 2、3 或 4 条边缘曲线并生成边缘曲面。
Create a surface from an auto sorted curve network.|自动排序曲线网并生成网络曲面。
Create a twisted box centered on a plane.|生成以平面为中心的扭曲盒。
Create a twisted box defined by 2 points.|用两个点定义扭曲盒。
Create a twisted box defined by a base plane and size domains.|由基础平面和尺寸区间定义扭曲盒。
Create twisted boxes between section curves or surfaces|在截面曲线或曲面之间生成扭曲盒。
Creates a hallowed out thickened shell from a closed polysurface (Brep).|将闭合多重曲面（Brep）向内掏空，生成具有厚度的壳体。
Creates a list of indices from a list of items.|根据项目列表生成索引列表。
Get a list of the indices from a list of items.|根据项目列表获取索引列表。
Deconstruct a number into its whole integer and decimal remainder.|将数值分解为整数部分和小数余数。
Deconstruct a twisted box into sets of its 8 corner points, 12 edge lines, or 6 face polylines.|将扭曲盒解构为 8 个角点、12 条边线或 6 个面多段线。
Deform a twisted box by moving corner points with motion vectors.|使用位移向量移动角点，使扭曲盒变形。
Divide a curve into equal lengths that are as close as possible to a target length.|将曲线等分，使每段长度尽量接近目标长度。
Divide each segment of a curve into equal lengths.|分别将每个曲线段按等长分割。
Extract the edit points on a curve at knot averages, the points an interpolated curve interpolated through.|在节点平均位置提取曲线编辑点，即插值曲线经过的点。
Extract the edit points on a surface at knot averages, the points an interpolated surface interpolated through.|在节点平均位置提取曲面编辑点，即插值曲面经过的点。
Extract the naked edge polylines of a mesh if any exist.|提取网格裸边多段线（若存在）。
Extrude a profile with a taper from draft angle.|按拔模角进行带锥度的截面挤出。
Find on which side of a mesh a point exists.|判断点位于网格的哪一侧。
Find on which side of a mesh a point exists, if mesh has mis-matched face directions its normals will be unified.|判断点位于网格的哪一侧；网格面方向不一致时先统一法向量。
Find on which side of a plane a point exists.|判断点位于平面的哪一侧。
Find on which side of a surface a point exists.|判断点位于曲面的哪一侧。
Find the center point (average) of a twisted boxes corner points, edge lines, or face polylines.|求扭曲盒角点、边线或面多段线的平均中心点。
Find the closest target plane by axis or axes orientation to a reference plane.|依据一个或多个轴的朝向，查找与参考平面方向最接近的目标平面。
Find the closest target vector by angle to a reference vector.|按夹角查找与参考向量最接近的目标向量。
Find the surface edge which is closest to a point.|查找距离指定点最近的曲面边。
Fit a new curve through an existing curve with kink angle smoothing, without changing the general shape.|对现有曲线进行折角平滑并拟合新曲线，保持整体形状。
Fit a new surface through an existing surface when possible without changing the general shape, also works with trimmed surfaces.|在可行时通过现有曲面拟合新曲面，保持整体形状，也支持已修剪曲面。
Fit a new surface through an existing surface when possible, without changing the general shape.|在可行时通过现有曲面拟合新曲面，保持整体形状。
Fit a rectangle through a set of points.|通过一组点拟合矩形。
Flip a plane by specified axes with the option of using a guide plane.|按指定轴反转平面，可使用引导平面。
Flip the normals of a polysurface (Brep), closed polysurfaces (Breps) cannot be flipped and will output with no change.|反转多重曲面（Brep）的法向量；闭合多重曲面不能反转，将原样输出。
Get all 8 corners of a twisted box.|获取扭曲盒的全部 8 个角点。
Get the arc, circle, or ellipse representation of a curve.|获取曲线对应的圆弧、圆或椭圆表示。
Get the degree value of a curve.|获取曲线次数。
Get the degree value of a surface for its {u} and {v} directions.|获取曲面 {u} 和 {v} 方向的次数。
Get the highest and lowest values from a set of numbers.|获取一组数值的最大值与最小值。
Get the point at the middle of a curves length or domain.|获取曲线长度或参数区间的中点。
Invert a boolean by making a true boolean false or a false boolean true.|将布尔值取反：真变为假，假变为真。
Invert a color.|将颜色反色。
Make a set of polylines compatible(equal) in control point count without changing their shapes.|在不改变形状的情况下，使多段线组的控制点数量相同。
Map point to a target surface space from its location relative to a source surface space.|依据点相对源曲面的位置，将其映射到目标曲面空间。
Move (translate) an object from one point to another.|将对象从一个点平移到另一个点。
Translate (Move) an object from one point to another.|将对象从一个点平移到另一个点。
Open a closed curve from its seam, or shorten an open curve from its ends.|从接缝处打开闭合曲线，或从两端缩短开放曲线。
Outputs a null item which can be used as a placeholder in lists.|输出可在列表中作为占位符的空值。
Outputs a zeroed out transform which represents no transformation or the state before any transforming occured, also known as an identity transform matrix.|输出表示未发生变换或变换前状态的单位变换矩阵。
Outputs the Rhino documents absolute distance tolerance value (Document Properties > Units > Model > Absolute tolerance).|输出 Rhino 文档的绝对距离容差（文档属性 → 单位 → 模型 → 绝对容差）。
Outputs the Rhino documents angle tolerance value (Document Properties > Units > Model > Angle tolerance).|输出 Rhino 文档的角度容差（文档属性 → 单位 → 模型 → 角度容差）。
Outputs the RhinoMath default angle tolerance value (1 deg | 0.017453 rad ).|输出 RhinoMath 默认角度容差（1°，约 0.017453 弧度）。
Outputs the RhinoMath zero distance tolerance value (1.0e-12).|输出 RhinoMath 零距离容差（1.0e-12）。
Partition a number as equally as possible by a specified amount of divisions.|按指定分割数将数值尽可能均等地分段。
Perform mass division on a set of numbers.|对数值列表进行连续除法。
Perform mass subtraction on a set of numbers.|对数值列表进行连续减法。
Rebuild a curve to a given point count, degree, and domain.|按指定控制点数、次数和参数区间重建曲线。
Rebuild a mesh with various operations|使用多种操作重建网格。
Rebuild a mesh with various operations, good for fixing invalid meshes|使用多种操作重建网格，可用于修复无效网格。
Recursively subdivide a twisted box into smaller twisted boxes.|递归细分扭曲盒，生成更小的扭曲盒。
Recursively transform geometry to get a self-referential step sequence of transformed geometry.|递归变换几何对象，生成以上一步结果为输入的变换序列。
Reduce the face count of a mesh to a target amount (look at Rhino command line to see progress % of operation).|将网格面数简化到目标数量，可在 Rhino 命令行查看进度百分比。
Relocate a curves ends to new start and end point locations without having to rebuild the curve.|无需重建曲线，将两端重新定位到新的起点和终点。
Remap values with a custom graph using input curves.|使用输入曲线构成的自定义图形重映射数值。
Reparameterize a curve to have a (t) domain range from 0 to 1.|将曲线的 {t} 参数区间重新设为 0 到 1。
Reparameterize a curve to have a domain range from 0 to 1.|将曲线参数区间重新设为 0 到 1。
Reparameterize a set of numbers to have a domain range from 0 to 1.|将一组数值重新参数化到 0 到 1。
Reparameterize a surface's {u} and {v} directions to have a domain range from 0 to 1.|将曲面 {u} 和 {v} 方向的参数区间重新设为 0 到 1。
Round a number to a decimal place or truncate a number at a decimal place.|按指定小数位数舍入或截断数值。
Round a number to a decimal place.|按指定小数位数舍入数值。
Round a number to a multiplication factor.|将数值舍入到指定倍数。
Search a curve for segments at specified degrees and fit new curve segments through them to a specified degree, without changing the general shape.|查找指定次数的曲线段，将其拟合为目标次数的新曲线段并保持整体形状。
Search a curve for segments at specified degrees and rebuild them to a specified degree and control point count.|查找指定次数的曲线段，并按目标次数和控制点数重建。
Slide a curve along a guide curve (or optionally along two guide curves).|沿一条或两条引导曲线滑动曲线。
Slide within the start and end of a domain to get a number from inside the domain.|在区间起止值之间滑动，获取区间内的数值。
Slide within the start and end of a domain² to get a {u} and {v} domain number from inside the domain².|在二维区间起止值之间滑动，获取内部 {u}、{v} 数值。
Slide within the start and end of a transform to get a transformation state from inside the transform.|在变换的起止状态之间插值，获取中间变换状态。
Smooth a curve recursively by fairing, without changing its control point count.|通过递归匀顺平滑曲线，保持控制点数量不变。
Solve volume properties for a twisted box.|计算扭曲盒的体积属性。
Test a curve for linearity.|判断曲线是否为直线。
Test a set of points for collinearity.|判断一组点是否共线。
Test a set of points for coplanarity.|判断一组点是否共面。
Test for equality of two numbers within a tolerance (|A - B| <= t).|判断两个数是否在容差内相等（绝对差值不大于 t）。
Test if a curve is an arc, circle, or ellipse as defined by Rhino. Curves can be multiple types.|按 Rhino 的定义判断曲线是否为圆弧、圆或椭圆，可能同时符合多种类型。
Test if a mesh has disjoint pieces.|判断网格是否包含相互分离的部分。
Test if a mesh is closed.|判断网格是否闭合。
Test if a polysurface (Brep) is closed.|判断多重曲面（Brep）是否闭合。
Test if a surface has edges collapsed to a point (singularities).|判断曲面是否有退化为点的边（奇点）。
Test if a surface has singularities (sides collapsed to a point).|判断曲面是否存在奇点（边退化为点）。
Test if a surface is closed and if its edges are closed in the {u} or {v} directions.|判断曲面是否闭合及其边在 {u}、{v} 方向的闭合状态。
Test if a surface is trimmed, can also test a polysurface (Brep) for trimmed faces.|判断曲面是否已修剪，也可检测多重曲面（Brep）的已修剪面。
Thicken a twisted box with layers of twisted boxes from thickness domain dividing parameters.|按厚度区间分割参数，生成分层扭曲盒以加厚原扭曲盒。
Transform a twisted box (because twisted boxes do not work with regular transform components like Move, Scale, Rotate, etc).|变换扭曲盒，因为其不适用于普通移动、缩放、旋转等变换组件。
''')


manual_descriptions.update(pairs('''
Adjust the seam of a closed curve with corners so that the seam is on the closest corner from the initial seam location (or optionally from a guide point), if curve is not closed or has no corners it will output with no change.|将闭合曲线接缝移至距原接缝或引导点最近的角点；曲线不闭合或无角点时原样输出。
Align the seams for a set of closed curves along a guide curve with the option of snapping to corners, if curve is not closed it will output with no change.|沿引导曲线对齐一组闭合曲线的接缝，可吸附到角点；开放曲线原样输出。
Align the seams for a set of closed curves starting from the first curve in the set (or optionally from a guide start point).|从第一条曲线或指定引导起点开始，对齐一组闭合曲线的接缝。
Append a set of polysurfaces (Breps) which are disjoint to become a single polysurface (Brep) even though they are not touching or joined. Can also append surfaces.|将互不接触或连接的多重曲面（Brep）合并为单个对象，也可合并曲面。
Blend between two meshes by their vertices with a set of blend factors where each factor controls the blend amount between each pair of vertices which share the same vertex index from one mesh to the other, meshes must have the same topology. Can also blend mesh vertex colors.|在两个相同拓扑网格之间逐顶点混合，每个因子控制相同索引顶点之间的混合量，也可混合顶点颜色。
Blend consecutively between a set of meshes by their vertices with a set of blend factors where each factor controls the blend amount between each set of vertices which share the same vertex index from mesh to mesh, meshes must have the same topology. Can also blend mesh vertex colors.|在相邻的相同拓扑网格之间逐顶点混合，每个因子控制相同索引顶点组的混合量，也可混合顶点颜色。
Blend through a set of meshes by their vertices with a set of blend factors where each factor controls the blend amount through each set of vertices which share the same vertex index across the meshes, meshes must have the same topology. Can also blend mesh vertex colors.|贯穿一组相同拓扑网格逐顶点混合，每个因子控制相同索引顶点的混合路径，也可混合顶点颜色。
Create a layered array of connected twisted boxes between curves from a thickness and domain dividing parameters.|依据厚度和区间分割参数，在曲线之间生成分层连接的扭曲盒阵列。
Create a layered array of connected twisted boxes between surfaces from domain dividing parameters.|依据区间分割参数，在曲面之间生成分层连接的扭曲盒阵列。
Create a layered array of connected twisted boxes consecutively between a set of surfaces from domain dividing parameters.|依据区间分割参数，在相邻曲面之间生成分层连接的扭曲盒阵列。
Create a layered array of connected twisted boxes consecutively between curves from a thickness and domain dividing parameters.|依据厚度和区间分割参数，在相邻曲线之间生成分层连接的扭曲盒阵列。
Create a layered array of connected twisted boxes in a box from domain dividing parameters.|依据区间分割参数，在盒内生成分层连接的扭曲盒阵列。
Create a layered array of connected twisted boxes on a mesh from the faces and a parameter domain divided thickness, works on quad and triangle faces.|沿网格面和厚度区间分割参数生成分层连接的扭曲盒阵列，支持四边面和三角面。
Create a layered array of connected twisted boxes on a mesh from the faces, works on quad and triangle faces.|沿网格面生成分层连接的扭曲盒阵列，支持四边面和三角面。
Create a layered array of connected twisted boxes on a surface from a thickness and domain dividing parameters.|依据厚度和区间分割参数，在曲面上生成分层连接的扭曲盒阵列。
Create a layered array of connected twisted boxes on a surface from domain dividing parameters.|依据区间分割参数，在曲面上生成分层连接的扭曲盒阵列。
Create a layered array of connected twisted boxes through a set of curves from a thickness and domain dividing parameters.|依据厚度和区间分割参数，贯穿曲线组生成分层连接的扭曲盒阵列。
Create a layered array of connected twisted boxes through a set of surfaces from domain dividing parameters.|依据区间分割参数，贯穿曲面组生成分层连接的扭曲盒阵列。
Create a layered pipe array of connected twisted boxes along a curve from domain dividing parameters, with variable diameters, thicknesses, and rotations.|依据区间分割参数，沿曲线生成分层连接的管状扭曲盒阵列，可变直径、厚度和旋转。
Create a layered pipe array of connected twisted boxes along a curve from domain dividing parameters.|依据区间分割参数，沿曲线生成分层连接的管状扭曲盒阵列。
Create a layered tube array of connected twisted boxes along a curve from domain dividing parameters, with variable diameters, thicknesses, and rotations.|依据区间分割参数，沿曲线生成分层连接的空心管扭曲盒阵列，可变直径、厚度和旋转。
Create a layered tube array of connected twisted boxes along a curve from domain dividing parameters.|依据区间分割参数，沿曲线生成分层连接的空心管扭曲盒阵列。
Create a rectangle or square the size of a specified area with {x} and {y} proportion factors, centered on a plane.|按指定面积及 {x}、{y} 比例因子生成矩形或正方形，以平面为中心。
Create a rectangular or regular box the size of a specified volume with {x}, {y}, and {z} proportion factors, centered on a plane.|按指定体积及 {x}、{y}、{z} 比例因子生成长方体或正方体，以平面为中心。
Create a twisted box from a Rhino referenced box like Polysurface (Brep) that has 6 faces and 8 corners. Best if used with Polysurfaces initially made in Rhino with the 'Box' command and referenced into Grasshopper as it follows that corner vertice order. For other boxes try grasshoppers Twisted Box parameter component or grasshoppers regular Twisted Box component.|从 Rhino 引用具有 6 个面、8 个角点的盒状多重曲面生成扭曲盒。优先使用 Rhino 的 Box 命令创建的盒，以匹配角点顺序；其他盒可用 Grasshopper 的扭曲盒参数或组件。
Create an ellipse or circle the size of a specified area with {x} and {y} proportion factors, centered on a plane.|按指定面积及 {x}、{y} 比例因子生成椭圆或圆，以平面为中心。
Create an ellipsoid or sphere the size of a specified volume with {x}, {y}, and {z} proportion factors, centered on a plane.|按指定体积及 {x}、{y}、{z} 比例因子生成椭球或球，以平面为中心。
Create an irregular or regular polygon the size of a specified area with {x} and {y} proportion factors, centered on a plane.|按指定面积及 {x}、{y} 比例因子生成不规则或正多边形，以平面为中心。
Create an untrimmed edge surface between 2, 3, or 4 edge curves which doesn't split into a polysurface(Brep) at kinks.|由 2、3 或 4 条边缘曲线生成未修剪边缘曲面，折角处不分裂为多重曲面。
Create an untrimmed extruded surface from a profile curve or surface along a vector, curve, or to a point, which doesn't split into a polysurface(Brep) at kinks.|沿向量、曲线或朝向一点挤出截面曲线或曲面，生成未修剪曲面，折角处不分裂为多重曲面。
Create an untrimmed lofted surface through a set of section curves or surfaces which doesn't split into a polysurface(Brep) at kinks.|贯穿截面曲线或曲面放样生成未修剪曲面，折角处不分裂为多重曲面。
Create an untrimmed revolved surface from a profile curve or surface around an axis line which doesn't split into a polysurface(Brep) at kinks.|绕轴线旋转截面曲线或曲面，生成未修剪曲面，折角处不分裂为多重曲面。
Create an untrimmed revolved surface from a profile curve or surface guided by a rail curve around an axis line which doesn't split into a polysurface(Brep) at kinks.|绕轴线沿轨道引导旋转截面曲线或曲面，生成未修剪曲面，折角处不分裂为多重曲面。
Create an untrimmed sum surface from two edge curves which doesn't split into a polysurface(Brep) at kinks.|由两条边缘曲线生成未修剪和曲面，折角处不分裂为多重曲面。
Create an untrimmed swept surface through a set of section curves or surfaces along a rail curve (or optionally along two rail curves) which doesn't split into a polysurface(Brep) at kinks.|沿一条或两条轨道扫掠截面曲线或曲面，生成未修剪曲面，折角处不分裂为多重曲面。
Create connected twisted boxes along a curve from domain dividing parameters, with variable sizes and rotations.|依据区间分割参数沿曲线生成连接扭曲盒，支持可变尺寸和旋转。
Create connected twisted boxes along a curve from domain dividing parameters.|依据区间分割参数沿曲线生成连接扭曲盒。
Create connected twisted boxes along a set of rail curves from domain dividing parameters.|依据区间分割参数沿轨道曲线组生成连接扭曲盒。
Create connected twisted boxes along four rail curves from a separate set of domain dividing parameters for each rail curve.|各轨道使用独立的区间分割参数，沿四条轨道曲线生成连接扭曲盒。
Create connected twisted boxes along four rail curves from domain dividing parameters.|依据区间分割参数沿四条轨道曲线生成连接扭曲盒。
Create connected twisted boxes along the inside of a pipe-like surface from a separate set of {u} domain dividing parameters for each {v} parameter.|为各 {v} 参数使用独立的 {u} 区间分割参数，沿管状曲面内部生成连接扭曲盒。
Create connected twisted boxes along the inside of a pipe-like surface from domain dividing parameters.|依据区间分割参数沿管状曲面内部生成连接扭曲盒。
Create connected twisted boxes along two rail curves from a separate set of domain dividing parameters for each rail curve.|各轨道使用独立的区间分割参数，沿两条轨道曲线生成连接扭曲盒。
Create connected twisted boxes along two rail curves from domain dividing parameters.|依据区间分割参数沿两条轨道曲线生成连接扭曲盒。
Create connected twisted boxes between four rail curves from domain dividing parameters.|依据区间分割参数在四条轨道曲线之间生成连接扭曲盒。
Create connected twisted boxes from a profile curve or surface along a vector, curve, or to a point from domain dividing parameters.|依据区间分割参数，沿向量、曲线或朝向一点从截面曲线或曲面生成连接扭曲盒。
Cut a curve with a plane, mirror the kept side of the cut across a mirror plane, and combine it with the kept side.|用平面裁剪曲线，将保留侧相对镜像平面镜像，再与保留侧拼接。
Cut a mesh with a plane, mirror the kept side of the cut across a mirror plane, and combine it with the kept side.|用平面裁剪网格，将保留侧相对镜像平面镜像，再与保留侧拼接。
Cut a polysurface(Brep) with a plane, mirror the kept side of the cut across a mirror plane, and combine it with the kept side. Can also mirror cut surfaces.|用平面裁剪多重曲面（Brep），镜像保留侧后拼接，也支持曲面。
Cut a set of planes with a plane, mirror the kept side of the cut across a mirror plane, and combine it with the kept side.|用平面裁剪平面组，镜像保留侧后拼接。
Cut a set of points with a plane, mirror the kept side of the cut across a mirror plane, and combine it with the kept side.|用平面裁剪点组，镜像保留侧后拼接。
Cut a surface with a plane, mirror the kept side of the cut across a mirror plane, and combine it with the kept side (for trimmed surfaces use Mirror Cut Polysurface).|用平面裁剪曲面，镜像保留侧后拼接；已修剪曲面请使用镜像裁剪多重曲面组件。
Cut a surface with a plane, mirror the kept side of the cut across a mirror plane, and combine it with the kept side.|用平面裁剪曲面，镜像保留侧后拼接。
Dispatch a list of items into two lists based on a set of indices, those that are at the indices and those which are not. Items which are at the indices will be ordered based on the input set of indices.|按索引将项目分派为命中和未命中的两个列表，命中项目按输入索引顺序排列。
Displace a mesh by its vertices with a set of displacement distances where each distance controls the displacement amount of each vertex along its normal direction.|使用一组位移距离逐顶点移动网格，每个距离控制对应顶点沿法向的位移量。
Generate a grid of curves on a rectangle from domain dividing {x} and {y} parameters, or generate a rectangle isocurve.|按 {x}、{y} 区间分割参数在矩形上生成曲线网格或等参线。
Generate a grid of curves on a surface from domain dividing {u} and {v} parameters, or generate a surface isocurve.|按 {u}、{v} 区间分割参数在曲面上生成曲线网格或等参线。
Generate a grid of points on a surface from domain dividing {u} and {v} parameters.|按 {u}、{v} 区间分割参数在曲面上生成点网格。
Generate a grid of rectangular cells in a rectangle from domain dividing {x} and {y} parameters.|按 {x}、{y} 区间分割参数在矩形内生成矩形单元网格。
Generate a grid of rectangular cells on a surface from domain dividing {u} and {v} parameters.|按 {u}、{v} 区间分割参数在曲面上生成矩形单元网格。
Generate a grid of subdivision surfaces on a surface from domain dividing {u} and {v} parameters.|按 {u}、{v} 区间分割参数将曲面划分成子曲面网格。
Generate a grid of surface normal oriented planes on a surface from domain dividing {u} and {v} parameters.|按 {u}、{v} 区间分割参数在曲面上生成沿法向定向的平面网格。
Generate a mesh on a surface from domain dividing {u} and {v} parameters.|按 {u}、{v} 区间分割参数在曲面上生成网格。
Generate a planar mesh in a rectangle from domain dividing {x} and {y} parameters.|按 {x}、{y} 区间分割参数在矩形内生成平面网格。
Generate an isocurve on a rectangle from a domain dividing {x} or {y} parameter.|按 {x} 或 {y} 区间分割参数生成矩形等参线。
Generate an isocurve on a surface from a domain dividing {u} or {v} parameter.|按 {u} 或 {v} 区间分割参数生成曲面等参线。
Get statistics about a curve such as control point count, edit point count, kink point count, segment count, span count, and knot vector count.|统计曲线的控制点、编辑点、折角点、曲线段、跨度和节点向量数量。
Get statistics about a mesh such as vertex count, face count, quad face count, triangle face count, color count, and piece count.|统计网格顶点、面、四边面、三角面、颜色和分离部分数量。
Get statistics about a surface or polysurface (Brep) such as face count, untrimmed face count, trimmed face count, edge count, vertex count, and countrol point count.|统计曲面或多重曲面的面、未修剪面、已修剪面、边、顶点和控制点数量。
Get the length along a curve from its start to a point on the curve (or optionally to a parameter on the curve), if point is not on the curve it will be pulled to it.|计算从曲线起点到指定点或参数的曲线长度；点不在曲线上时先投影到曲线。
Get the lengths along a curve between points on the curve (or optionally parameters on the curve), if points are not on the curve they will be pulled to it.|计算曲线上指定点或参数之间的长度；点不在曲线上时先投影到曲线。
Gets the curve sub-domain for each span in a curve and gets information about the spans such as, amount of spans, length of each span, degree of each span, and curve parameters at the span ends.|获取各曲线跨度的子区间，以及跨度数量、各跨度长度和次数、末端曲线参数。
Gets the surface sub-domain²s for each span in a surface and gets information about the spans such as, sub-domains of each span, amount of spans in each direction, lengths of each span, degrees of each span, isocurve span parameters, and surface parameter coordinates at the span ends.|获取各曲面跨度的二维子区间，以及各方向跨度数量、长度、次数、等参线跨度参数和末端曲面参数坐标。
Iteratively or non-iteratively align the seams for a set of closed curves starting from the first curve in the set (or optionally from a guide start point) with the option of snapping to corners, if curve is not closed it will output with no change.|从第一条曲线或引导起点开始，以迭代或非迭代方式对齐闭合曲线接缝，可吸附到角点；开放曲线不变。
Linearize a set of numbers so a repeating wave type number set is remapped to increasing increments between a domain bounds, while maintaining the interval proportions between numbers.|将周期波动数值组重映射为区间内递增序列，同时保持数值间隔比例。
Locate a point in a rectangle from a domain dividing {x} and {y} parameter.|按 {x}、{y} 区间分割参数定位矩形内的点。
Locate a point inside or on a twisted box, evaluated in normalized {uvw} space.|在归一化 {uvw} 空间中求值，定位扭曲盒内部或表面的点。
Locate a point on a surface from a domain dividing {u} and {v} parameter.|按 {u}、{v} 区间分割参数定位曲面上的点。
Locate a rectangle normal oriented plane in a rectangle from a domain dividing {x} and {y} parameter.|按 {x}、{y} 参数在矩形内定位沿矩形法向的平面。
Locate a surface normal oriented plane on a surface from a domain dividing {u} and {v} parameter.|按 {u}、{v} 参数在曲面上定位沿曲面法向的平面。
Offset a curve away from a surface by the surface normal directions with the option of offsetting both sides and capping the ends.|沿曲面法向将曲线偏离曲面，可向两侧偏移并封闭末端。
Offset a curve away from a surface by the surface normal directions with the option of offsetting both sides at different distances and capping the ends.|沿曲面法向将曲线偏离曲面，可向两侧按不同距离偏移并封闭末端。
Offset a curve with the option of offsetting both sides and capping the ends.|偏移曲线，可向两侧偏移并封闭末端。
Offset a curve with the option of offsetting both sides at different distances and capping the ends.|偏移曲线，可向两侧按不同距离偏移并封闭末端。
Offset a mesh with the option of offsetting both sides and creating a solid.|偏移网格，可向两侧偏移并生成实体。
Offset a mesh with the option of offsetting both sides at different distances and creating a solid.|偏移网格，可向两侧按不同距离偏移并生成实体。
Offset a plane by specified axes with the option of offsetting both sides at different distances.|沿指定轴偏移平面，可向两侧按不同距离偏移。
Offset a plane by specified axes with the option of offsetting both sides.|沿指定轴偏移平面，可向两侧偏移。
Offset a surface with the option of offsetting both sides and creating a solid, also works with trimmed surfaces and polysurface (Brep) faces as separated offsets.|偏移曲面，可向两侧偏移并生成实体；支持已修剪曲面和多重曲面各面的独立偏移。
Offset a surface with the option of offsetting both sides and creating a solid, can also offset polysurface (Brep) faces.|偏移曲面，可向两侧偏移并生成实体，也支持多重曲面的面。
Offset a surface with the option of offsetting both sides at different distances and creating a solid, also works with trimmed surfaces and polysurface (Brep) faces as separated offsets.|偏移曲面，可向两侧按不同距离偏移并生成实体；支持已修剪曲面和多重曲面各面的独立偏移。
Pinch & Spread a set of points by radius, strength, and falloff values at each location point. Positive strengths Pinch, Negative strengths Spread.|依据各作用点的半径、强度和衰减值收拢或扩散点组；正强度收拢，负强度扩散。
Pinch & spread a set of points by radius and strength values at each location point. Positive strengths pinch, negative strengths spread.|依据各作用点的半径和强度收拢或扩散点组；正强度收拢，负强度扩散。
Pinch & spread points by a radius and strength value at a location point. Positive strengths pinch, negative strengths spread.|依据作用点的半径和强度收拢或扩散点；正强度收拢，负强度扩散。
Rebuild a mesh with options for recomputing normals, removing unused faces and vertices, combining duplicate vertices, unifying normals, flipping normals, and welding vertices within proximity of eachother.|重建网格，可重算法向、删除未使用面和顶点、合并重复顶点、统一或反转法向、焊接邻近顶点。
Rebuild a surface to a given point count, degree, and domain in the {u} and {v} directions, also works with trimmed surfaces.|按 {u}、{v} 方向的控制点数、次数和参数区间重建曲面，支持已修剪曲面。
Rebuild a surface to a given point count, degree, and domain in the {u} and {v} directions.|按 {u}、{v} 方向的控制点数、次数和参数区间重建曲面。
Recursively morph mesh geometries onto mesh faces starting from morphing onto a base mesh, the resulting mesh of each recursive morphing step becomes the new base mesh for the next steps mesh geometry to morph onto its faces.|从基础网格开始将网格几何映射到面上，每一步结果作为下一步的基础网格，进行递归形变。
Remap a curves {t} domain range to an input domain range with the option of matching the {t} domain range of a guide curve.|将曲线 {t} 区间重映射为输入区间，可匹配引导曲线的 {t} 区间。
Remap a surfaces {uv} domain² range to an input domain² range with the option of matching the {uv} domain² range of a guide surface, also works with trimmed surfaces.|将曲面 {uv} 二维区间重映射为输入二维区间，可匹配引导曲面区间，也支持已修剪曲面。
Removes the kinky parts of a curve (discontinuities) by blending the curve segments togther, if curve already has no kinks it will output with no change.|通过混合连接曲线段去除折角不连续处；无折角时原样输出。
Reparameterize a set of domains to have a start and end value range from 0 to 1, or an inverted start and end value range from 1 to 0.|将区间组的起止值范围归一化为 0 到 1，或反向为 1 到 0。
Reparameterize a set of domain²s to have a start and end value range from 0 to 1 for their {u} and {v} domains, or an inverted start and end value range from 1 to 0.|将二维区间组的 {u}、{v} 起止值范围归一化为 0 到 1，或反向为 1 到 0。
Reparameterize a set of numbers to have a domain range from 0 to 1, or an inverted domain range from 1 to 0.|将数值组归一化为 0 到 1，或反向为 1 到 0。
Reparameterize a set of points to have {x}, {y}, and {z} coordinates which range from 0 to 1.|将点组的 {x}、{y}、{z} 坐标分别归一化到 0 到 1。
Reparameterize a set of points to have {x}, {y}, {z} coordinates which range from 0 to 1, or an inverted coordinate range from 1 to 0.|将点组的 {x}、{y}、{z} 坐标分别归一化到 0 到 1，或反向为 1 到 0。
Reparameterize a set of vectors to have a length (amplitude) range from 0 to 1, or an inverted length range from 1 to 0.|将向量组的长度归一化到 0 到 1，或反向为 1 到 0。
Reparameterize a surface to have a (uv) domain² range from 0 to 1, also works with trimmed surfaces.|将曲面 {uv} 参数区间重新设为 0 到 1，支持已修剪曲面。
Rotate an object by three plane axes and three angles in degrees, each axis derived from the initial base plane.|按三个平面轴及三个角度值旋转对象，各轴均来自初始基础平面。
Rotate an object by three plane axes and three angles in degrees, each axis derived from the initial base planes world.|按三个平面轴及三个角度值旋转对象，各轴均来自初始基础平面的世界坐标系。
Rotate an object by three plane axes and three angles in degrees, each axis derived from the plane previous.|按三个平面轴及三个角度值依次旋转对象，每个轴均来自前一步的平面。
Rotate an object from one plane to another by a rotation factor, derived from quaternion rotation.|使用四元数旋转，按旋转因子将对象从一个平面旋转到另一个平面。
Round numbers in x to nearest numbers in y with the option to remap numbers in x to the domain of numbers in y.|将 x 中数值舍入到 y 中最近值，可先将 x 重映射到 y 的范围。
Round numbers in x to the nearest numbers in y with the option of remapping number set x to the domain bounds of number set y.|将 x 中数值舍入到 y 中最近值，可先将 x 数值组重映射到 y 的区间边界。
Scale a curve to a specified length with {x}, {y}, and {z} proportion factors.|按指定长度及 {x}、{y}、{z} 比例因子缩放曲线。
Scale geometry to a specified area with {x}, {y}, and {z} proportion factors.|按指定面积及 {x}、{y}、{z} 比例因子缩放几何对象。
Scale geometry to a specified volume with {x}, {y}, and {z} proportion factors.|按指定体积及 {x}、{y}、{z} 比例因子缩放几何对象。
Shrinks the underlying untrimmed surface of a trimmed surface to be as close as possible to the trimmed surface edges, can also shrink trimmed polysurface (Brep) faces.|收缩已修剪曲面的底层未修剪曲面，使其尽可能贴近修剪边，也支持多重曲面的已修剪面。
Sift a list of items into two lists based on a set of indices, those that are at the indices and those which are not. Each resulting list will have the same length and order as the input list but will be filled with null placeholders for items that went to the other list.|按索引将项目筛分为两个列表，各列表保持原长度和顺序，未归入该列表的位置用空值占位。
Sort a set of list items synchronously by the iterative closest point sorting of a set of points sequentially from a start point.|从起点开始按迭代最近点顺序排序点组，并同步排序对应项目列表。
Split a set of numbers into odd and even number sets with the option of using null placeholders in the split number sets.|将数值组分为奇数和偶数两组，可在缺失位置使用空值占位。
Split the output surface from an unsplit surface component into a polysurface(Brep) if it has kinks, if surface has no kinks it will output with no change.|将不分裂曲面组件的输出按折角分裂为多重曲面；无折角时原样输出。
Superimpose the control point count, degree, and domain properties of a reference curve onto a target curve.|将参考曲线的控制点数量、次数和参数区间套用到目标曲线。
Superimpose the {uv} control point count, {uv} degree, {uv} domain, and trims of a reference surface onto a target surface, also works with trimmed surfaces.|将参考曲面的 {uv} 控制点数、次数、区间和修剪边界套用到目标曲面，支持已修剪曲面。
Superimpose the {u} and {v} control point count, degree, and domain properties of a reference surface onto a target surface.|将参考曲面的 {u}、{v} 控制点数、次数和区间套用到目标曲面。
Swap or reverse the {u} and {v} directions of a surface, also works with trimmed surfaces but trims will swap as well.|交换或反转曲面 {u}、{v} 方向；支持已修剪曲面，修剪边界也同步交换。
Swap or reverse the {u} and {v} directions of a surface.|交换或反转曲面 {u}、{v} 方向。
Test if a curve has kinks, and gets information about the kinks such as, amount of kinks and the length along curve where each kink exists.|判断曲线是否有折角，并获取折角数量及其沿曲线的长度位置。
Test if a curve has segments, and gets information about the segments such as, amount of segments, length of each segment, and degree of each segment.|判断曲线是否分段，并获取段数、各段长度和次数。
Trim (remove) the parts of a curve on one side of a plane.|移除曲线位于平面一侧的部分。
Trim (remove) the parts of a curve outside of every two points (or optionally every two parameters), if points are not on the curve they will be pulled to it.|移除曲线每对点或参数之间范围以外的部分；点不在曲线上时先投影到曲线。
Trim (remove) the parts of a mesh on one side of a plane.|移除网格位于平面一侧的部分。
Trim (remove) the parts of a plane set on one side of a plane.|移除平面组位于裁剪平面一侧的部分。
Trim (remove) the parts of a point set on one side of a plane.|移除点组位于裁剪平面一侧的部分。
Trim (remove) the parts of a surface on one side of a plane, also works with trimmed surfaces and polysurfaces (Breps).|移除曲面位于平面一侧的部分，支持已修剪曲面和多重曲面。
Trim (remove) the parts of a surface on one side of a plane, can also trim polysurfaces (Breps).|移除曲面位于平面一侧的部分，也支持多重曲面。
Trim a curve with a set of points (or optionally a set of parameters) like a dash pattern, if points are not on the curve they will be pulled to it.|按点组或参数组以虚线模式修剪曲线；点不在曲线上时先投影到曲线。
Unroll a polysurface (Brep) so its faces lay flat on a plane, with the options to unroll points and curves along with the polysurface (Brep) faces.|展开多重曲面，使各面平铺在平面上，可同时展开附属点和曲线。
Unroll a polysurface (Brep) so its faces lay flat on a plane, with the options to unroll points and curves along with the polysurface (Brep) faces. Can also unroll surfaces.|展开多重曲面，使各面平铺在平面上，可同时展开附属点和曲线，也支持曲面。
'''))

manual_descriptions = {re.sub(r'\s+', ' ', k).strip(): v for k, v in manual_descriptions.items()}

nouns = {'colors': '颜色', 'curves': '曲线', 'domains': '一维区间', 'domain²s': '二维区间', 'meshes': '网格', 'numbers': '数值', 'planes': '平面', 'points': '点', 'surfaces': '曲面', 'transforms': '变换', 'twisted boxes': '扭曲盒', 'vectors': '向量', 'list items': '列表项目'}


def description(text):
    normalized = re.sub(r'\s+', ' ', text).strip()
    if text in manual_descriptions:
        return manual_descriptions[text]
    if normalized in manual_descriptions:
        return manual_descriptions[normalized]
    if normalized.endswith('(*Rhino 7 only)') and 'SubD' in normalized:
        body = normalized[:-len('(*Rhino 7 only)')].strip()
        subd = {
            'Solve the arithmetic average for a set of SubDs, SubDs must have the same topology.': '求同拓扑细分曲面组的算术平均值。',
            'Solve the arithmetic weighted average for a set of SubDs, SubDs must have the same topology.': '求同拓扑细分曲面组的加权算术平均值。',
            'Tween between two SubDs, SubDs must have the same topology.': '在两个同拓扑细分曲面之间生成补间。',
            'Tween consecutively between a set of SubDs, SubDs must have the same topology.': '在同拓扑细分曲面组的相邻项之间生成补间。',
            'Tween through a set of SubDs, SubDs must have the same topology.': '贯穿同拓扑细分曲面组生成补间。',
            'Cut a SubD with a plane, mirror the kept side of the cut across a mirror plane, and combine it with the kept side.': '用平面裁剪细分曲面，镜像保留侧后连接。',
            'Create a layered array of connected twisted boxes on a SubD from the faces and a parameter domain divided thickness.': '按细分曲面的面与厚度分割参数生成分层连接扭曲盒阵列。',
            'Create a layered array of connected twisted boxes between SubDs from the faces, SubDs must have the same topology.': '依据两个同拓扑细分曲面的面，在其间生成分层连接扭曲盒阵列。',
            'Create a layered array of connected twisted boxes consecutively between a set of SubDs from the faces, SubDs must have the same topology.': '依据同拓扑细分曲面组的面，在相邻项间生成分层连接扭曲盒阵列。',
            'Create a layered array of connected twisted boxes through a set of SubDs from the faces, SubDs must have the same topology.': '依据同拓扑细分曲面组的面，贯穿整组生成分层连接扭曲盒阵列。'
        }
        if body in subd:
            return subd[body] + '（原插件注明 Rhino 7 专用的 WIP 用户对象。）'
    special = {
        'Create a layered array of connected twisted boxes between meshes from the faces, works on quad and triangle faces. Meshes must have the same topology.': '依据同拓扑网格的四边面或三角面，在网格之间生成分层连接的扭曲盒阵列。',
        'Create a layered array of connected twisted boxes consecutively between a set of meshes from the faces, works on quad and triangle faces. Meshes must have the same topology.': '依据同拓扑网格的四边面或三角面，在相邻网格之间生成分层连接的扭曲盒阵列。',
        'Create a layered array of connected twisted boxes through a set of meshes from the faces, works on quad and triangle faces. Meshes must have the same topology.': '依据同拓扑网格的四边面或三角面，贯穿网格组生成分层连接的扭曲盒阵列。'
    }
    if normalized in special:
        return special[normalized]
    if normalized.startswith('Create a lofted mesh through a set of section curves'):
        return '依据 {u}、{v} 分割参数、控制点间长度或角度精度，在截面曲线之间生成放样网格，可指定起点和终点。基础方法来自 Mateusz Zwierzycki。'
    if normalized.startswith('Create a piped mesh along a curve'):
        return '依据 {u}、{v} 分割参数、控制点间长度或角度精度，沿曲线生成管状网格，支持多种末端类型。基础方法来自 Mateusz Zwierzycki。'
    if normalized.startswith('Create an extruded mesh from a profile curve'):
        return '依据 {u}、{v} 分割参数、控制点间长度或角度精度，沿向量、曲线或朝向一点挤出截面生成网格，可封闭闭合截面的挤出端。基础方法来自 Mateusz Zwierzycki。'
    if normalized.startswith('Create a plane oriented voxelization'):
        return '按平面朝向及 {x}、{y}、{z} 体素尺寸将点组体素化为不含内部面的网格。基础方法来自 Mateusz Zwierzycki。'
    if normalized.startswith('Extract the egde loop polylines'):
        return '在指定顶点索引处提取四边网格的环边多段线。基础方法来自 Mateusz Zwierzycki。'
    if normalized.startswith('Split a mesh into separate meshes by measuring an angle tolerance'):
        return '依据相邻网格面法向夹角容差分割网格；若未发生分割则原样输出。基础方法来自 Mateusz Zwierzycki。'
    if normalized.startswith('Morph geometries from reference boxes'):
        return '将几何对象从参考盒映射到目标扭曲盒。原插件注明 Rhino 6 及以上可用；Rhino 5 请使用 Grasshopper 的 Box Morph 组件。支持多线程。'
    if normalized.startswith('Trim (remove) a set of twisted boxes by a boolean'):
        mesh = 'closed mesh' in normalized
        return '通过与一个或多个闭合' + ('网格' if mesh else '多重曲面（Brep）') + '进行布尔交集或差集，裁剪扭曲盒组。' + ('网格方法较快但精度较低。' if mesh else '多重曲面方法较慢但精度较高。') + '支持多线程。'
    if normalized.startswith('Trim (remove) the parts of a twisted box set on one side of'):
        geometry = '网格' if 'mesh.' in normalized else '平面' if 'plane.' in normalized else '曲面'
        return '移除扭曲盒组位于' + geometry + '一侧的部分。支持多线程。'
    match = re.fullmatch(r'Tween (between two|consecutively between a set of|through a set of) (.+?)\.(.*)', normalized)
    if match:
        subject = match[2]
        suffix = ''
        for addon, translation in [
            (' along a guide curve (or optionally along two guide curves)', '沿一条或两条引导曲线'),
            (' on a surface, if curves are not on the surface they will be pulled to it', '在曲面上；不在曲面上的曲线会先投影到曲面'),
            (' on a curve, if plane origins are not on the curve they will be pulled to it', '在曲线上；不在曲线上的平面原点会先投影到曲线'),
            (' on a surface, if plane origins are not on the surface they will be pulled to it', '在曲面上；不在曲面上的平面原点会先投影到曲面'),
            (' on a curve, if points are not on the curve they will be pulled to it', '在曲线上；不在曲线上的点会先投影到曲线'),
            (' on a surface, if points are not on the surface they will be pulled to it', '在曲面上；不在曲面上的点会先投影到曲面'),
            (', meshes must have the same topology', '网格必须具有相同拓扑'),
            (', trimmed surfaces will be treated as untrimmed', '已修剪曲面按未修剪曲面处理')
        ]:
            if addon in subject:
                subject = subject.replace(addon, '')
                suffix += '；' + translation
        if subject in nouns:
            action = {'between two': '在两个', 'consecutively between a set of': '在一组相邻', 'through a set of': '贯穿一组'}[match[1]]
            ending = '之间生成补间' if match[1] != 'through a set of' else '生成补间'
            extra = '，也可补间网格顶点颜色' if 'Can also tween mesh vertex colors' in match[3] else ''
            return action + nouns[subject] + ending + suffix + extra + '。'
    match = re.fullmatch(r'Solve the (arithmetic (?:weighted )?average|weighted arithmetic average) for a set of ([^.]+)\.(.*)', normalized)
    if match:
        subject = match[2]
        suffix = ''
        for addon, translation in [(', meshes must have the same topology', '网格必须具有相同拓扑'), (', trimmed surfaces will be treated as untrimmed', '已修剪曲面按未修剪曲面处理')]:
            if addon in subject:
                subject = subject.replace(addon, '')
                suffix += '；' + translation
        if subject in nouns:
            extra = '，也可平均网格顶点颜色' if 'Can also average mesh vertex colors' in match[3] else ''
            return '计算一组' + nouns[subject] + ('的加权算术平均值' if 'weighted' in match[1] else '的算术平均值') + suffix + extra + '。'
    match = re.fullmatch(r'Mirror a set of (.+) across its end or start and combine it with the original set\.', normalized)
    if match and match[1] in nouns:
        return '以末端或起点为基准镜像一组' + nouns[match[1]] + '，并与原组拼接。'
    match = re.fullmatch(r'Cut a set of (.+) at an index, mirror the kept side of the cut across the index, and combine it with the kept side\.', normalized)
    if match and match[1] in nouns:
        return '按索引裁剪一组' + nouns[match[1]] + '，以该索引为基准镜像保留部分，再与保留部分拼接。'
    return None


def read_pack(name):
    return json.loads((ROOT / 'Languages' / name).read_text(encoding='utf-8-sig'))


port_phrases = pairs('''
For instance:|例如：
if omitted document tolerance is used|省略时使用文档容差
unless Normalized is False|归一化为假时除外
if Normalized is False, increase the tween factor range maximum by 1|归一化为假时，将补间因子范围的最大值增加 1
If True, tween distribution is evaluated between the extremes of the input|为真时，在输入的两端范围之间计算补间分布：
without considering the locations of the input|不考虑输入的位置：
If False, the rules for factor are|为假时，因子遵循以下规则
The tween factor range from one|从一个对象到下一个对象的补间因子范围：
factors between the|位于以下索引之间的因子：
index numbers will be the corresponding tweens|对应相应的补间结果
Index number of the next|下一个对象的索引：
Index number of last|最后一个对象的索引：
Index number of a|对象索引：
Index number of the|对象索引：
at last index|位于末项索引
at index|位于索引
at start|在起点
at end|在终点
Tween factor|补间因子
A tween factor of|补间因子为
will result in a tween|将生成补间结果：
halfway between the|位于以下两者的中间：
If True, allow the tween path to continue from the end back to the start as a closed loop|为真时，允许补间路径从末端返回起点，形成闭合循环
The splitting index (only if Join is false)|分割索引（仅当连接为假时有效）
To split the|要分割
at the mirror use this as the index input on Grasshopper's Split List component.|在镜像处，将此值作为 Grasshopper“分割列表”组件的索引输入。
with Grasshopper's Split List component|使用 Grasshopper 的“分割列表”组件
Collection of weights for each|各项对应的权重集合：
Arithmetic mean (average) of all input|所有输入的算术平均值：
Resulting reparameterized set of|重新参数化后的结果组：
The original domain range|原始参数区间
The original start value range|原始起始值范围
The original end value range|原始结束值范围
The original|原始
Proportion factor in the|以下方向的比例因子：
Division parameters along|沿以下对象的分割参数：
Division parameter along|沿以下对象的分割参数：
Division parameters between each|各项之间的分割参数：
Division parameters through|贯穿以下对象的分割参数：
which defines|用于定义
which define|用于定义
Determines how much of|决定以下内容的数量：
Determines how the|决定以下内容的方式：
Determines how|决定其方式：
Determines the|用于确定
Resulting untrimmed single unsplit|生成的未修剪单一不分裂
Resulting twisted box array|生成的扭曲盒阵列
Resulting|结果：
A list of|列表：
A set of|一组
Set of|一组
List of|列表：
Amount of|数量：
Number of|数量：
Control point count|控制点数
control point count|控制点数
Number to compare to|比较目标数值
Number to compare|待比较数值
True if A is within the tolerance of B|A 与 B 的差值在容差内时为真
True if A is not within the tolerance of B|A 与 B 的差值超出容差时为真
Acceptable maximum difference between A and B to be considered as equal|将 A 与 B 视为相等时允许的最大差值
A zeroed out transform|单位变换
A null item placeholder|空值占位符
To replace null items in a list use Grasshopper's Replace Nulls component.|可使用 Grasshopper“替换空值”组件替换列表中的空值。
Full Transparency|完全透明
No Transparency|不透明
First Number|第一个数
Second Number|第二个数
True for boolean intersection, False for boolean difference|真表示布尔交集，假表示布尔差集
True for boolean intersection|真表示布尔交集
False for boolean difference|假表示布尔差集
True if|为真的条件：
False if|为假的条件：
True for|以下情况为真：
False for|以下情况为假：
If True,|为真时，
If False,|为假时，
If false,|为假时，
If true,|为真时，
If Angle is not|若角度不是
Boolean indicating whether the|布尔值，表示
Boolean indicating if|布尔值，表示
unless|除非
only if|仅当
only when|仅当
when using|使用时：
if using|使用时：
if the|若
if|若
for each pair of vertices which share the same vertex index from one mesh to the other|对应两个网格中具有相同顶点索引的每一对顶点
for each set of vertices which share the same vertex index across the meshes|对应所有网格中具有相同索引的每组顶点
for each set of vertices which share the same vertex index from mesh to mesh|对应相邻网格中具有相同索引的每组顶点
from one mesh to the other|从一个网格到另一个网格
across the meshes|跨越所有网格
same topology|相同拓扑
same vertex index|相同顶点索引
vertex colors|顶点颜色
vertex blend paths|顶点混合路径
blend factors|混合因子
best results if using a lower poly mesh and smoothing the result mesh|使用低面数网格并平滑结果网格通常效果更好
best results if using lower poly meshes and smoothing the result mesh|使用低面数网格并平滑结果网格通常效果更好
typically the bounding box of each mesh geometry to morph|通常为各待变形网格的包围盒
at every|在每个
at each|在每个
for every|对应每个
on each|在每个
each|每个
around the|围绕
around curve|围绕曲线
around the curve|围绕曲线
along the|沿
along a|沿
along|沿
between|在两者之间：
from|从
to|至
in relation to the curve|相对于曲线
in relation to|相对于
within this distance from the mirror plane|位于距镜像平面该距离内的
within proximity of eachother|彼此邻近的
offset inward from the outer diameter corners|从外径角点向内偏移
offset inward from the outer radius corners|从外半径角点向内偏移
offset from mesh faces for morph heights|从网格面偏移，作为形变高度
are inside the twisted box|位于扭曲盒内部
inside the twisted box|位于扭曲盒内部
inside of the|位于以下内容内部：
outside of the|位于以下内容外部：
inside of|内部
outside of|外部
inside|内部
outside|外部
on surface|在曲面上
on curve|在曲线上
on the surface|在曲面上
on the curve|在曲线上
on the mesh|在网格上
on the plane|在平面上
are not on the curve they will be pulled to it|不在曲线上时将投影到曲线
are not on the surface they will be pulled to it|不在曲面上时将投影到曲面
not on the curve|不在曲线上
not on the surface|不在曲面上
the keep side of the|保留侧：
completely to the keep side of|完全位于保留侧
atleast halfway to the keep side of|至少一半位于保留侧
atleast partially to the keep side of|至少部分位于保留侧
kept side of the|保留侧：
keep if twisted box is|保留扭曲盒的条件：
will be used|将被使用
will be|将
will not be|不会
will get|将获取
gets applied after reduction, may change face count|在简化后应用，可能改变面数
face types are a direct result of the reduction|面类型直接取决于简化结果
The closest length larger than or equal to the target length|大于或等于目标长度的最近长度
The closest length smaller than or equal to the target length|小于或等于目标长度的最近长度
The closest length to the target length|最接近目标值的长度
Halfway|半数
Complete|完整
Partial|部分
Position|位置
Tangency|相切连续
Curvature|曲率连续
Sharp|尖角
Chamfer|倒角
Smooth|平滑
Round|圆角
Floor / Truncate|向下取整/截断
Floor|向下取整
Ceiling|向上取整
Chord|弦长
Square Root|平方根
Straight|直线
Normal|法向
Tight|紧致
Uniform|均匀
Loose|松散
None|无
Fast|快速
Accurate|精确
Cubic|立方
Spherical|球形
Reflected|反射镜像
Inverted|反向
Corner Points|角点
Edge Lines|边线
Face Polylines|面多段线
Remove faces|移除面
Shrink faces|收缩面
Split faces|分割面
with connection|带连接
without connection|无连接
Meet Ends|端点汇合
Flat|平直
Preserve start point only|仅保留起点
Preserve end point only|仅保留终点
Preserve first two points|保留前两个点
Preserve first three points|保留前三个点
Preserve last two points|保留后两个点
Preserve last three points|保留后三个点
Quadrangulate if possible|尽可能四边形化
Triangulate all|全部三角化
Cardinal + InterCardinal|主方向与中间方向
InterCardinal|中间方向
Cardinal|主方向
Default|默认
Least|最低
Most|最高
first|第一
last|最后
next|下一个
previous|上一个
current|当前
initial|初始
inital|初始
original|原始
target|目标
reference|参考
source|源
input|输入
output|输出
optional|可选
optionally|可选地
base|基础
outer|外侧
inner|内侧
negative|负
positive|正
increasing|递增
decreasing|递减
start values|起始值
end values|结束值
start value|起始值
end value|结束值
start point|起点
end point|终点
start|起始
end|末端
start,|起点，
end,|终点，
unitize|单位化
normalize|归一化
normalized|归一化
non-duplicate|不重复
non duplicate|不重复
non existance|不存在
non-existence|消失
in numerical order|按数值顺序
in degrees|以度为单位
in radians|以弧度为单位
increasing (negative to positive)|递增（负值至正值）
decreasing (positive to negative)|递减（正值至负值）
negative to positive|负值至正值
positive to negative|正值至负值
removes the duplicate|移除重复项：
removes|移除
remove|移除
recomputing|重新计算
recompute|重新计算
rebuilding|重建
rebuild|重建
flipping|反转
flip|反转
reversing|反转
reverse|反转
unifying|统一
unify|统一
welding|焊接
weld|焊接
combining|合并
combine|合并
joined|已连接
join|连接
split|分割
splitting|分割
trimming|修剪
trim|修剪
mirror combined|镜像合并后的
mirror cut|镜像裁剪
mirror combine|镜像合并
mirrored|镜像结果
mirrored across|以其为基准镜像
mirroring|镜像
mirror|镜像
averaging|求平均
average|平均
tween through|贯穿补间
consecutive tweening|相邻补间
tweening|补间
tween paths|补间路径
tween path|补间路径
tween|补间
blending|混合
blend|混合
mapping|映射
mapped|映射结果
map|映射
sorting|排序
sort|排序
sorted|已排序
displace|位移
displacement|位移
morphing|形变
morph|形变
thickening|加厚
thicken|加厚
lofting|放样
loft|放样
extrusion|挤出
extrude|挤出
revolve|旋转生成
sweep|扫掠
reparameterize|重新参数化
reparameterized|重新参数化后
reparameterization|重新参数化
remap|重映射
remapped|重映射后
scale|缩放
scaled|缩放后
rotate|旋转
rotation|旋转
rotations|旋转
weld tolerance|焊接容差
bounding box|包围盒
bounding rectangle|包围矩形
orintation|朝向
orientation|朝向
origins|原点
origin|原点
axes|轴
axis|轴
angle|角度
angles|角度
radius|半径
radii|半径
radiuses|半径
diameter|直径
diameters|直径
thickness|厚度
thicknesses|厚度
domain sizes|尺寸区间
domain defined|以区间定义的
domain dividing|区间分割
domain²s|二维区间
domain²|二维区间
domains|区间
domain|区间
control points|控制点
control point|控制点
edit points|编辑点
edit point|编辑点
corner points|角点
corner point|角点
sample points|采样点
sample point|采样点
end points|端点
kink points|折角点
kinks|折角
kink|折角
vertices|顶点
vertex|顶点
vertice|顶点
normals|法向量
normal direction|法向
normal|法向量
coordinates|坐标
coordinate|坐标
curvature|曲率
continuity|连续性
seams|接缝
seam|接缝
proportion factors|比例因子
proportion factor|比例因子
falloff|衰减
falloffs|衰减
bulge|凸度
amplitude|长度
lengths|长度
length|长度
strengths|强度
strength|强度
factors|因子
factor|因子
weights|权重
weighted distribution|加权分布
weighted|加权
weight|权重
linear|线性
interpolated|插值后的
interpolation|插值
interpolate|插值
interpolating|插值
curve segments|曲线段
curve segment|曲线段
profile curves|截面曲线
profile curve|截面曲线
section curves|截面曲线
section curve|截面曲线
rail curves|轨道曲线
rail curve|轨道曲线
pipe-like surface|管状曲面
polysurfaces(Breps)|多重曲面（Brep）
polysurface(Brep)|多重曲面（Brep）
polysurface (Brep)|多重曲面（Brep）
polysurfaces|多重曲面
polysurface|多重曲面
box-like|盒状
box like|盒状
polylines|多段线
polyline|多段线
curves|曲线
curve|曲线
surfaces|曲面
surface|曲面
meshes|网格
mesh|网格
planes|平面
plane|平面
points|点
point|点
numbers|数值
number|数值
transforms|变换
transformation|变换
transform|变换
vectors|向量
vector|向量
twisted boxes|扭曲盒
twisted box|扭曲盒
boxes|盒
box|盒
color|颜色
colors|颜色
colour|颜色
geometries|几何对象
geometry|几何对象
ellipse|椭圆
circle|圆
ellipsoid|椭球
sphere|球
polygon|多边形
rectangle|矩形
square|正方形
quads|四边面
quad|四边形
triangles|三角形
triangle|三角形
triangular|三角形
rectangular|矩形
regular|规则
irregular|不规则
non-planar|非共面
nonplanar|非共面
planar|共面
collapsed|退化
singularities|奇点
singularity|奇点
singular|奇点
closed|闭合
closing|闭合
open|开放
opening|开口
openings|开口
trimmed|已修剪
untrimmed|未修剪
surface trims|曲面修剪边界
trims|修剪边界
unify|统一
welded|焊接后
unwelded|未焊接
unused|未使用
duplicate|重复
duplicates|重复项
reduction|简化
sections|截面
section|截面
spans|跨度
span|跨度
segments|段
segment|段
pieces|部分
piece|部分
faces|面
face|面
edges|边
edge|边
knots|节点
knot|节点
get|获取
test|测试
count|数量
parameter|参数
parameters|参数
index|索引
indices|索引
indexes|索引
values|数值
value|值
boolean|布尔值
True|真
False|假
null|空值
nulls|空值
items|项目
item|项目
lists|列表
list|列表
sets|组
set|组
range|范围
ranges|范围
extents|范围
extent|范围
bounds|边界
bound|边界
boundary|边界
boundaries|边界
axis aligned|与轴对齐
aligned|已对齐
align|对齐
reference planes|参考平面
closest target planes|最近目标平面
closest|最近
closest point|最近点
nearest|最近
keep|保留
kept|保留
capped|已封端
capping|封端
cap|封端
caps|封端
reversed|已反转
reverses|反转
flips|反转
invert|取反
inverted|取反
corresponding|对应
centers|中心
centered|居中
center|中心
centroids|形心
centroid|形心
hollow|空心
hallowed|空心
starts|起始值
ends|结束值
both sides|两侧
back|后侧
front|前侧
left|左
right|右
top|顶部
bottom|底部
middle|中间
negative strengths|负强度
positive strengths|正强度
zero|零
one|一个
two|两个
three|三个
four|四个
eight|八个
zero length|零长度
smooth|平滑
smoothed|平滑后
smoothing|平滑
fit|拟合
fitted|拟合后
fitting|拟合
refit|重新拟合
matching|匹配
match|匹配
matched|已匹配
mismatched|不匹配
direction|方向
directions|方向
properties|属性
property|属性
mass|累计
arithmetic|算术
mean|平均值
average|平均
degree|次数
degrees|度
radians|弧度
integer|整数
integers|整数
decimal|小数
remainders|余数
remainder|余数
rounded|舍入后
rounding|舍入
round|舍入
position|位置
locations|位置
location|位置
guide|引导
normalization|归一化
moving|移动
move|移动
motion|位移
motions|位移向量
tangents|切向量
tangent|切向量
tangency|相切
naked|裸边
loop|环
loops|环
loopback|循环回接
looping|循环
looped|形成环
connect|连接
connected|连接后
connections|连接
connection|连接
connects|连接
control|控制
controls|控制
determines|决定
becomes|成为
make|生成
create|生成
construct|构造
constructed|构造后
convert|转换
remove|移除
removed|已移除
extract|提取
extracts|提取
find|查找
found|找到
included|包含
includes|包含
include|包含
exclude|排除
excluded|排除
omit|省略
omitted|省略
optional|可选
default|默认
original|原始
source|源
target|目标
reference|参考
input|输入
output|输出
also|也
can|可以
cannot|不能
must|必须
should|应
may|可能
will|将
would|会
result|结果
results|结果
resulting|结果
only|仅
all|全部
any|任意
every|每个
each|每个
same|相同
equal|相等
equally|均等
equivalent|等效
different|不同
differently|不同地
additional|额外
additionally|额外地
as|作为
and|和
or|或
not|不
no|无
is|为
are|为
be|为
been|已
being|正在
has|具有
have|具有
had|具有
the|该
a|一个
an|一个
of|的
for|用于
in|在
on|在
with|带
without|不带
by|通过
through|贯穿
across|跨越
from|从
to|至
than|比
this|此
these|这些
that|该
those|那些
which|其
where|其中
whether|是否
when|当
if|若
it|其
its|其
they|这些
their|其
them|这些
into|到
per|每
about|关于
between|之间
more|更多
less|更少
larger|更大
smaller|更小
higher|更高
lower|更低
most|最多
least|最少
atleast|至少
maximum|最大
minimum|最小
max|最大
min|最小
beginning|起点
continue|继续
continues|继续
continued|继续
continuing|继续
use|使用
used|使用
using|使用
gets|获取
get|获取
got|获取
being|正在
before|之前
after|之后
then|然后
instead|替代
otherwise|否则
partially|部分地
fully|完全
completely|完全
at|在
rather|而非
because|因为
so|因此
since|由于
such|例如
like|类似
''')
port_pattern = re.compile(r'(?<![A-Za-z])(?:' + '|'.join(re.escape(k) for k in sorted(port_phrases, key=len, reverse=True)) + r')(?![A-Za-z])', re.I)
port_lookup = {k.casefold(): v for k, v in port_phrases.items()}


port_manual = pairs('''
{u} parameter (values between 0.0 and 1.0 are inside the twisted box)|{u} 参数，0 到 1 位于扭曲盒内部。
{v} parameter (values between 0.0 and 1.0 are inside the twisted box)|{v} 参数，0 到 1 位于扭曲盒内部。
{w} parameter (values between 0.0 and 1.0 are inside the twisted box)|{w} 参数，0 到 1 位于扭曲盒内部。
A zeroed out transform|单位变换。
Accuracy of reduction (1 = Least, 10 = Most)|简化精度：1 为最低，10 为最高。
Align the slide curve to the input curve, when using one guide curve|使用单条引导曲线时，将滑动曲线对齐到输入曲线。
Align with slide curve to the input curve to slide, when using one guide curve|使用单条引导曲线时，将滑动曲线与待滑动的输入曲线对齐。
Alpha transparency value for the color (0 = Full Transparency, 255 = No Transparency)|颜色透明度：0 完全透明，255 不透明。
Alpha transparency value of the color (0 = Full Transparency, 255 = No Transparency)|颜色透明度：0 完全透明，255 不透明。
Alternate the trimming pattern to switch which parts of the curve get trimmed away|切换交替修剪模式，改变被移除的曲线部分。
Amount of disjoint mesh pieces|互不连接的网格部分数量。
Amount of kinks on the curve|曲线折角数量。
Amount of openings in the input mesh|输入网格的开口数量。
Amount of partition divisions|分段数量。
Amount of segments that make up the curve|组成曲线的段数。
Amount of spans that make up the curve|组成曲线的跨度数。
Area of the ellipse|椭圆面积。
Area of the polygon|多边形面积。
Area of the rectangle|矩形面积。
Area to scale the geometry to|几何对象缩放后的目标面积。
Axis line to revolve around|旋转所绕的轴线。
Base plane|基础平面。
Base plane for box|盒的基础平面。
Base plane for center and orientation of scaling|确定缩放中心和方向的基础平面。
Base plane for ellipse|椭圆的基础平面。
Base plane for ellipsoid|椭球的基础平面。
Base plane for polygon|多边形的基础平面。
Base plane for rectangle|矩形的基础平面。
Base plane for vector star orientation and location|确定星形向量方向和位置的基础平面。
Base plane for vector world orientation and location|确定世界方向向量位置和朝向的基础平面。
Base surface for initial coordinate space|定义初始坐标空间的基础曲面。
Boolean to invert|待取反的布尔值。
Box like polysurface (Brep), preferably referenced from Rhino|盒状多重曲面（Brep），建议从 Rhino 引用。
Bulge factor for curve closing segment|曲线闭合连接段的凸度因子。
Calculate the percentage of this number|待计算百分比的数值。
Color to invert|待反色的颜色。
Color to convert to grayscale|待转换为灰度的颜色。
Curve to mirror cut|待镜像裁剪的曲线。
Curve to offset|待偏移曲线。
Curve to rebuild|待重建曲线。
Curve to reparameterize|待重新参数化的曲线。
Curve to get edit points from|用于提取编辑点的曲线。
Curve to get degree value from|用于获取次数的曲线。
Curve to get spans from|用于获取跨度信息的曲线。
Curve to get statistics from|用于统计的曲线。
Curve to close|待闭合曲线。
Curve to open|待打开的曲线。
Curve to smooth|待平滑曲线。
Curve to fit|待拟合曲线。
Curve to test for linearity|待检测是否为直线的曲线。
Curve to test for kinks|待检测折角的曲线。
Curve to test for segments|待检测分段的曲线。
Curve to test for arc, circle, or ellipse|待检测圆弧、圆或椭圆类型的曲线。
Mesh to rebuild|待重建网格。
Mesh to offset|待偏移网格。
Mesh to close|待封闭网格。
Mesh to reduce|待简化网格。
Mesh to displace|待逐顶点位移的网格。
Mesh to get statistics from|用于统计的网格。
Mesh to test for closure|待检测闭合状态的网格。
Surface to rebuild|待重建曲面。
Surface to reparameterize|待重新参数化曲面。
Surface to get edit points from|用于提取编辑点的曲面。
Surface to get degree value from|用于获取次数的曲面。
Surface to get spans from|用于获取跨度的曲面。
Surface to offset|待偏移曲面。
Surface to fit|待拟合曲面。
Plane to offset|待偏移平面。
Plane to flip|待反转平面。
Number to compare|待比较数值。
Number to compare to|比较目标数值。
True if A is within the tolerance of B|A 与 B 的差值在容差内时为真。
True if A is not within the tolerance of B|A 与 B 的差值超出容差时为真。
Acceptable maximum difference between A and B to be considered as equal (if omitted document tolerance is used)|将 A 与 B 视为相等的最大允许差值，省略时使用文档容差。
Flip the mirror direction|反转镜像方向。
Join the mirror cut curves|连接镜像裁剪后的曲线。
Keep the curve and mirror it normally if it is mirror cut into non-existence|若镜像裁剪导致曲线消失，则保留曲线并执行普通镜像。
Plane that the kept side of the curve cut gets mirrored across|曲线裁剪后保留侧所用的镜像平面。
Parts of the curve within this distance from the mirror plane will be additionally cut away|距镜像平面该距离内的曲线部分也会移除。
Distance to offset the kept parts of the curve from the mirror plane (or offset from the reach if reach in not zero)|保留曲线相对镜像平面的偏移距离；作用距离非零时从作用边界开始偏移。
Number to deconstruct|待解构的数值。
Whole integer part of the number|数值的整数部分。
Decimal remainder of the number|数值的小数余数。
Amount of numbers to partition into|数值的目标分段数。
Geometry to transform|待变换几何对象。
Geometry to scale|待缩放几何对象。
Geometry to move|待移动几何对象。
Geometry to rotate|待旋转几何对象。
Geometries to transform|待变换几何对象。
Resulting geometry|结果几何对象。
Resulting geometries|结果几何对象。
Resulting curve|结果曲线。
Resulting curves|结果曲线。
Resulting mesh|结果网格。
Resulting meshes|结果网格。
Resulting surface|结果曲面。
Resulting surfaces|结果曲面。
Resulting points|结果点。
Resulting planes|结果平面。
Resulting twisted boxes|结果扭曲盒。
''')
port_manual = {re.sub(r'\s+', ' ', k).strip(): v for k, v in port_manual.items()}


port_manual.update(pairs('''
Angle between the reference vector and closest target vector in radians|参考向量与最近目标向量的夹角，单位为弧度。
Average the mesh vertex colors|同时平均网格顶点颜色。
Blend the mesh vertex colors|同时混合网格顶点颜色。
Box to create twisted box array in|用于容纳扭曲盒阵列的盒。
Bulge factor for kink blend|折角混合连接的凸度因子。
Cap the open ends of a closed profile curve mesh extrusion|封闭闭合截面曲线挤出网格的开放末端。
Closed curve with corners to adjust the seam of|需要调整接缝的带角点闭合曲线。
Closed mesh or meshes to trim with|用于裁剪的一个或多个闭合网格。
Closed mesh to trim with|用于裁剪的闭合网格。
Closed polysurface to shell (Brep)|需要生成壳体的闭合多重曲面（Brep）。
Closed polysurface(Brep) or polysurfaces(Breps) to trim with|用于裁剪的一个或多个闭合多重曲面（Brep）。
Closed polysurface(Brep) to trim with|用于裁剪的闭合多重曲面（Brep）。
Closest surface edge to the point|距离该点最近的曲面边。
Closest target plane by axis or axes orientation to the reference plane|依据一个或多个轴的朝向，与参考平面最接近的目标平面。
Closest target vector by angle to the reference vector|与参考向量夹角最小的目标向量。
Color to convert to point|待转换为点的颜色。
Control point count (if omitted input curve control point count is used)|控制点数，省略时使用输入曲线的控制点数。
Create a solid offset|生成实体偏移。
Curvature degree of the tween path, degree should be a positive odd number|补间路径的次数，应为正奇数。
Curve parameter at the point on curve|曲线上该点的参数。
Curve parameters at the points on curve|曲线上各点的参数。
Curve segment degree values to search for|需要查找的曲线段次数。
Curve sub-domain for each remaining part of the curve after trimming|修剪后各保留曲线部分的子区间。
Curve to create coil points along|用于沿线生成螺旋点的曲线。
Curve to create pipe along as mesh|用于沿线生成管状网格的曲线。
Curve to create twisted box array from|扭曲盒阵列的起始曲线。
Curve to create twisted box array to|扭曲盒阵列的目标曲线。
Curve to create twisted box pipe array around|用于环绕生成管状扭曲盒阵列的曲线。
Curve to create twisted box tube array along|用于沿线生成空心管扭曲盒阵列的曲线。
Curve to create twisted box tube array around|用于环绕生成空心管扭曲盒阵列的曲线。
Curve to create twisted boxes along|用于沿线生成扭曲盒的曲线。
Curve to create wave points along|用于沿线生成波浪点的曲线。
Curve to fit segments of|待拟合曲线段的曲线。
Curve to get arc, circle, or ellipse|用于获取圆弧、圆或椭圆表示的曲线。
Curve to get length along|用于计算沿线长度的曲线。
Curve to get lengths along|用于计算沿线各段长度的曲线。
Curve to get middle point of|用于求中点的曲线。
Curve to get span information of|用于获取跨度信息的曲线。
Curve to get statistics of|用于统计的曲线。
Curve to get the degree value of|用于获取次数的曲线。
Curve to get the edit points of|用于获取编辑点的曲线。
Curve to offset away from surface|需要偏离曲面的曲线。
Curve to rebuild segments of|需要重建各段的曲线。
Curve to relocate end points of|需要重定位端点的曲线。
Curve to remap the {t} domain range of|需要重映射 {t} 参数区间的曲线。
Curve to remove kinks from|需要去除折角的曲线。
Curve to scale|待缩放曲线。
Curve to slide along guide curve|需要沿引导曲线滑动的曲线。
Curve to test for segments, and get segment information of.|用于检测分段并获取段信息的曲线。
Curve to tween plane on|用于在其上补间平面的曲线。
Curve to tween planes on|用于在其上补间平面组的曲线。
Curve to tween point on|用于在其上补间点的曲线。
Curve to tween points on|用于在其上补间点组的曲线。
Curve with segments to divide|各段需要分割的曲线。
Curves for averaging|用于求平均的曲线组。
Decimal place to round to|舍入的小数位数。
Degree of curve (if omitted input curve degree is used)|曲线次数，省略时使用输入曲线次数。
Degree to fit the curve to (if omitted input curve degree is used)|曲线拟合的目标次数，省略时使用输入曲线次数。
Degree value of the curve|曲线次数。
Difference in face count between the original mesh and the reduced mesh|原始网格和简化网格之间的面数差。
Displacement distances, one distance for each vertex|位移距离，每个顶点对应一个距离。
Division points at equal lengths along the curve|沿曲线等长分割的点。
Division points on each curve segment|各曲线段上的分割点。
Domain of curve (if omitted input curve domain is used)|曲线参数区间，省略时使用输入曲线区间。
Domain of revolution in degrees (0 = Revolve start, 360 = Revolve end)|旋转生成的角度区间：0 为起始，360 为结束，单位为度。
Domain range to remap the curve to|曲线重映射的目标区间。
Domain to slide within|需要在内部滑动的一维区间。
Domain² range to remap the surface to|曲面重映射的目标二维区间。
Domain² to slide within|需要在内部滑动的二维区间。
Edit points of the curve|曲线编辑点。
Edit points on the curve|曲线上的编辑点。
Edit points on the surface|曲面上的编辑点。
Evaluation point at {uvw} coordinate|{uvw} 坐标处的求值点。
First corner|第一个角点。
Second corner|第二个角点。
First corner (0,0,0)|第一个角点（0,0,0）。
Second corner (1,0,0)|第二个角点（1,0,0）。
Fourth corner (0,1,0)|第四个角点（0,1,0）。
Fifth corner (0,0,1)|第五个角点（0,0,1）。
Last corner (0,1,1)|最后一个角点（0,1,1）。
Fix inconsistencies in the mesh vertex and face normals|修复网格顶点与面法向的不一致。
Flip direction of net curves along surface|反转曲面上曲线网的方向。
Flip the mirror direction (False = End of set, True = Start of set)|反转镜像方向：假为组末端，真为组起点。
Flip the mirror direction (false = End of set, true = Start of set)|反转镜像方向：假为组末端，真为组起点。
Flip the planes X axis|反转平面 X 轴。
Flip the planes Y axis|反转平面 Y 轴。
Flip the planes Z axis|反转平面 Z 轴。
Flip the trim direction|反转裁剪方向。
Geometries to morph|待形变几何对象。
Geometry to contain with bounding rectangle|需要用包围矩形包围的几何对象。
Geometry to move (translate)|待平移几何对象。
Geometry to recursively transform|需要递归变换的几何对象。
Guide curve to align the seams along|用于沿线对齐接缝的引导曲线。
Guide curve to slide along|用于滑动的引导曲线。
Guide curve to tween along (best if flowing from Curve A to Curve B)|用于沿线补间的引导曲线，建议方向从曲线 A 指向曲线 B。
Guide curve to tween along (best if flowing from Surface A to Surface B)|用于沿线补间的引导曲线，建议方向从曲面 A 指向曲面 B。
Highest number in the set|组内最大数值。
Lowest number in the set|组内最小数值。
Include 0 and 1 in the range|在范围内包含 0 和 1。
Include 0 and the last index in the range|在范围内包含 0 和末项索引。
Include 0 and the list length in the range|在范围内包含 0 和列表长度。
Include the transparencies (alpha values) of the colors in the tweening|补间时同时包含颜色透明度（Alpha 值）。
Index of each corner point that was deformed|各已变形角点的索引。
Index of the closest surface edge|最近曲面边的索引。
Index of the closest target vector by angle to the reference vector|与参考向量夹角最小的目标向量索引。
Index of the mesh vertice to extract edge loop polylines at|用于提取环边多段线的网格顶点索引。
Integer division|整数除法。
Interpolate with quaternion rotation|使用四元数旋转插值。
Intial base plane the rotation starts from|旋转起始的基础平面。
Intial base plane which defines the {x}, {y}, and {z} rotation axes|定义 {x}、{y}、{z} 旋转轴的初始基础平面。
Intial base plane which defines the {x}, {y}, and {z} world axes|定义 {x}、{y}、{z} 世界轴的初始基础平面。
Invert the coordinate range to be from 1 to 0 instead of 0 to 1|将坐标范围反向为 1 到 0，而非 0 到 1。
Invert the domain range to be from 1 to 0 instead of 0 to 1|将区间范围反向为 1 到 0，而非 0 到 1。
Invert the length (amplitude) range to be from 1 to 0 instead of 0 to 1|将长度范围反向为 1 到 0，而非 0 到 1。
Invert the start and end value range to be from 1 to 0 instead of 0 to 1|将起止值范围反向为 1 到 0，而非 0 到 1。
Invert the start and end value ranges to be from 1 to 0 instead of 0 to 1|将各起止值范围反向为 1 到 0，而非 0 到 1。
Invert the transparencies (alpha values) of the mirrored colors|反转镜像颜色的透明度（Alpha 值）。
Invert the transparency (alpha value) of the color|反转颜色透明度（Alpha 值）。
Join the mirror cut mesh|连接镜像裁剪后的网格。
Join the mirror cut polysurface(Brep) or surface|连接镜像裁剪后的多重曲面或曲面。
Join the mirror cut surfaces|连接镜像裁剪后的曲面。
Keep adjacent mesh faces together which have opposite normals|保持法向相反的相邻网格面相连。
Keep the length of the reference vector|保持参考向量的长度。
Length along curve from start to the point on curve|从曲线起点到曲线上该点的长度。
Length along the curve where each kink exists|各折角沿曲线的长度位置。
Length at the curves length or domain middle point|曲线长度或区间中点处的长度。
Length of each segment that makes up the curve|各曲线段的长度。
Length of each span that makes up the curve|各曲线跨度的长度。
Length to scale the curve to|曲线缩放后的目标长度。
Lengths along curve between points on curve|曲线上各点之间的长度。
Line representation of the vectors|向量的直线表示。
List of data to obtain the last index of|用于获取末项索引的数据列表。
List of data to obtain the length of|用于获取长度的数据列表。
List of indices for the item list|项目列表的索引列表。
List of indices from the item list|来自项目列表的索引列表。
List of items to dispatch|待分派项目列表。
List of items to get index list of|用于获取索引列表的项目列表。
List of items to make index list of|用于生成索引列表的项目列表。
List of items to sift|待筛分项目列表。
Locally scale the revolution|局部缩放旋转生成结果。
Make quad mesh faces where possible|在可行处生成四边网格面。
Merge coplanar polysurface faces into single surfaces|将多重曲面的共面面合并为单一曲面。
Merge duplicate mesh vertices|合并重复网格顶点。
Mesh to convert into polysurface|待转换为多重曲面的网格。
Mesh to create twisted box array on|用于生成扭曲盒阵列的网格。
Mesh to create twisted boxes from|扭曲盒的起始网格。
Mesh to create twisted boxes to|扭曲盒的目标网格。
Mesh to determine on which side the point is located|用于判断点所在侧别的网格。
Mesh to get naked edge polylines of|用于获取裸边多段线的网格。
Mesh to get statistics of|用于统计的网格。
Mesh to mirror cut|待镜像裁剪网格。
Mesh to split|待分割网格。
Mesh to test if it has disjoint pieces|待检测分离部分的网格。
Mesh to test if it is closed|待检测闭合状态的网格。
Mesh to trim|待裁剪网格。
Mesh to trim with|用于裁剪的网格。
Meshes for averaging|用于求平均的网格组。
Middle point at the curves length or domain|曲线长度或区间中点。
More equally distribute the mesh face sizes|使网格面尺寸分布更均匀。
Motion vector for each corner point to deform|各待变形角点的位移向量。
Movement (translation) vector|平移向量。
Multiplication factor to round to|舍入的目标倍数因子。
Net curves on surface|曲面上的网状曲线。
Network curves to auto sort and create the network surface from|用于自动排序并生成网络曲面的曲线网。
Normal vectors at edit points|编辑点处的法向量。
Number to calculate the percentage of|需要计算百分比的数值。
Number to partition|待分段数值。
Number to round|待舍入数值。
Number x to add one to|需要加一的数值 x。
Number x to subtract one from|需要减一的数值 x。
Numbers to round|待舍入数值组。
Numbers to round nearest to|用于最近值舍入的目标数值组。
Numerical representation of the inverted boolean|取反布尔值的数值表示。
Offset both sides|向两侧偏移。
Offset by plane X direction|沿平面 X 方向偏移。
Offset by plane Y direction|沿平面 Y 方向偏移。
Offset by plane Z direction|沿平面 Z 方向偏移。
Offset distance away from surface|离开曲面的偏移距离。
One or multiple graph curves to graph map values with|用于图形映射的一条或多条图形曲线。
Opening polyline outlines of the input mesh|输入网格开口的多段线轮廓。
Optional plane to unroll to, if no plane is set the world XY plane is used|可选的展开目标平面，未设置时使用世界 XY 平面。
Orientation plane of the bounding rectangle|包围矩形的朝向平面。
Orientation plane of the voxelization|体素化的朝向平面。
Outer diameter of the twisted box pipe array|管状扭曲盒阵列的外径。
Outer diameter of the twisted box tube array|空心管扭曲盒阵列的外径。
Outer radius of the twisted box tube array|空心管扭曲盒阵列的外半径。
Overall thickness of the twisted box array, offset from the curves|从曲线偏移的扭曲盒阵列总厚度。
Overall thickness of the twisted box array, offset from the surface|从曲面偏移的扭曲盒阵列总厚度。
Parameter coordinates at edit points|编辑点处的参数坐标。
Parameter to adjust the opening location (seam) for a closed curve|用于调整闭合曲线开口位置（接缝）的参数。
Parameter value at the curves length or domain middle point|曲线长度或区间中点处的参数值。
Parameter values at edit points|编辑点处的参数值。
Parameter values at the plane curve intersection points|平面与曲线交点处的参数值。
Partial result transformations (steps) of the mass transform|复合变换各步骤的中间变换结果。
Partial results (steps) of the mass division|连续除法各步骤的中间结果。
Partial results (steps) of the mass subtraction|连续减法各步骤的中间结果。
Partitions of the number|数值的各分段。
Percent to calculate|需要计算的百分比。
Pinched & Spread points|收拢与扩散后的点。
Pinched & spread points|收拢与扩散后的点。
Pipe-like surface to create twisted boxes along the inside of|用于沿内部生成扭曲盒的管状曲面。
Plane for offset operation|偏移操作的参考平面。
Plane that the kept side of the mesh cut gets mirrored across|网格裁剪保留侧使用的镜像平面。
Plane that the kept side of the plane set cut gets mirrored across|平面组裁剪保留侧使用的镜像平面。
Plane that the kept side of the point set cut gets mirrored across|点组裁剪保留侧使用的镜像平面。
Plane that the kept side of the surface cut gets mirrored across|曲面裁剪保留侧使用的镜像平面。
Plane the rotation ends at|旋转结束时的平面。
Plane the rotation starts from|旋转开始时的平面。
Plane to determine on which side the point is located|用于判断点所在侧别的平面。
Plane to trim with|用于裁剪的平面。
Planes for averaging|用于求平均的平面组。
Point at location to pinch & spread|收拢与扩散的作用位置点。
Point at the curve seam adjusted to the closest corner|调整至最近角点的曲线接缝点。
Point on curve to get length to|用于计算曲线长度的终点。
Point to convert to color|待转换为颜色的点。
Point to find on which side of the mesh it is located|用于判断相对网格侧别的点。
Point to find on which side of the plane it is located|用于判断相对平面侧别的点。
Point to find on which side of the surface it is located|用于判断相对曲面侧别的点。
Point to find the closest surface edge to|用于查找最近曲面边的点。
Point to map|待映射的点。
Point to move from|移动起点。
Point to move to|移动终点。
Points at locations to pinch & spread|收拢与扩散的各作用位置点。
Points at the aligned curve seams|对齐后的曲线接缝点。
Points that define the locations to pinch & spread at|定义收拢与扩散作用位置的点组。
Points to pinch & spread|需要收拢与扩散的点组。
Points to trim with|用于修剪的点组。
Points to trim with (even number of points)|用于修剪的点组，数量应为偶数。
Polyline boundary which represents the naked edges of the mesh|表示网格裸边的多段线边界。
Polysurface (Brep) or surface to unroll|待展开的多重曲面（Brep）或曲面。
Polysurface (Brep) to flip|待反转的多重曲面（Brep）。
Polysurface (Brep) to test if it is closed|待检测闭合状态的多重曲面（Brep）。
Polysurface (Brep) to unroll|待展开的多重曲面（Brep）。
Polysurface(Brep) or surface to mirror cut|待镜像裁剪的多重曲面或曲面。
Preserve the end tangents of target curve|保持目标曲线的端点切向量。
Preserve the end tangents of the curve|保持曲线端点切向量。
Preserve the end tangents of the rebuilt segments|保持重建曲线段的端点切向量。
Profile curve or surface to extrude|待挤出的截面曲线或曲面。
Profile curve or surface to extrude, works best if profile is planar|待挤出的截面曲线或曲面，平面截面效果更好。
Profile curve or surface to revolve|待旋转生成的截面曲线或曲面。
Profile curve to extrude as mesh|待挤出为网格的截面曲线。
Quad mesh to extract edge loop polylines from|用于提取环边多段线的四边网格。
Radius from location(L), of points(P) to pinch & spread|以 L 位置为中心对 P 点组收拢或扩散的半径。
Radius of the pipe mesh|管状网格半径。
Radiuses from locations(L), of points(P) to pinch & spread|以各 L 位置为中心对 P 点组收拢或扩散的半径列表。
Rail curve that guides the profile curves revolution around the axis line|引导截面曲线绕轴线旋转的轨道曲线。
Range of numbers between 0 and 1|从 0 到 1 的数值范围。
Range of numbers between 0 and the last index|从 0 到末项索引的数值范围。
Range of numbers between 0 and the list length|从 0 到列表长度的数值范围。
Recompute the mesh vertex and face normals|重新计算网格顶点与面法向量。
Rectangle to divide|待分割矩形。
Rectangle to divide as mesh|需要分割为网格的矩形。
Rectangle to get isocurve of|用于获取等参线的矩形。
Rectangle to locate plane in|用于定位内部平面的矩形。
Rectangle to locate point in|用于定位内部点的矩形。
Reference boxes to morph from (typically the geometries bounding box)|形变的参考盒，通常为几何对象的包围盒。
Reference curve to take properties from|提供属性的参考曲线。
Reference plane to search from|用于方向搜索的参考平面。
Reference surface to take properties from|提供属性的参考曲面。
Reference vector to search from|用于方向搜索的参考向量。
Reference vertices|参考顶点。
Remainder decimal part of the number|数值的小数余数部分。
Remap number set x to the domain bounds of number set y|将数值组 x 重映射到数值组 y 的区间范围。
Remap numbers x to domain of numbers y|将 x 数值重映射到 y 的数值区间。
Remove the center twisted box|移除中心扭曲盒。
Remove the transparency (alpha value) of the color|移除颜色透明度（Alpha 值）。
Remove unused vertices and faces from the mesh|移除网格中未使用的顶点和面。
Reparameterize the domain sets end values|重新参数化区间组的结束值。
Reparameterize the domain sets start values|重新参数化区间组的起始值。
Result of x minus one|x 减一的结果。
Result of x plus one|x 加一的结果。
Reverse the mesh vertex and face normals|反转网格顶点和面法向量。
Reverse the surface {u} direction|反转曲面 {u} 方向。
Reverse the surface {v} direction|反转曲面 {v} 方向。
Rhino documents absolute distance tolerance value|Rhino 文档的绝对距离容差。
Rhino documents angle tolerance value in degrees|Rhino 文档角度容差，单位为度。
Rhino documents angle tolerance value in radians|Rhino 文档角度容差，单位为弧度。
RhinoMath default angle tolerance value in degrees|RhinoMath 默认角度容差，单位为度。
RhinoMath default angle tolerance value in radians|RhinoMath 默认角度容差，单位为弧度。
RhinoMath zero distance tolerance value|RhinoMath 零距离容差。
Rotation around curve of the twisted box curve, in degrees|曲线扭曲盒绕曲线的旋转角，单位为度。
Rotation around curve of the twisted box pipe array, in degrees|管状扭曲盒阵列绕曲线的旋转角，单位为度。
Rotation of the pipe mesh radius around the curve, in degrees|管状网格半径绕曲线的旋转角，单位为度。
Round result to nearest integer|将结果舍入到最近整数。
Round results to nearest integers|将各结果舍入到最近整数。
'''))
port_manual = {re.sub(r'\s+', ' ', k).strip(): v for k, v in port_manual.items()}


port_manual.update(pairs('''
A null item placeholder To replace null items in a list use Grasshopper's Replace Nulls component.|空值占位符；可用 Grasshopper“替换空值”组件替换列表中的空值。
Angle tolerance to measure between adjacent mesh face normals, in degrees. Adjacent mesh faces with angles between their normals smaller than this angle will split at their shared edge|相邻网格面法向夹角容差，单位为度。夹角小于该值的相邻面将在共享边处分割。
Axis of the orientation plane to find the bounding rectangle along 0 = {z} axis of orintation plane 1 = {y} axis of orintation plane 2 = {x} axis of orintation plane|包围矩形所沿的朝向平面轴：0 为 Z，1 为 Y，2 为 X。
Base mesh to morph the first mesh geometry onto its faces (best results if using a lower poly mesh and smoothing the result mesh)|第一步形变所依附的基础网格。建议使用低面数网格并平滑结果。
Corner points to deform (if the points are not exact corner points, the closest corner points will be deformed)|待移动的角点；输入点不是精确角点时，移动最近角点。
Curve parameters at the span ends To get the point between each span use these as the Parameters(t) input on Grasshopper's Evaluate Curve component.|各跨度末端的曲线参数，可输入 Grasshopper“曲线求值”组件的参数 t 获取对应点。
Curve sub-domain for each span that makes up the curve To extract each span as a separate curve use these as the Domain(D) input on Grasshopper's Sub Curve component.|各曲线跨度的子区间，可输入 Grasshopper“子曲线”组件的区间 D 单独提取各跨度。
Determines the surface continuity 0 = Loose 1 = Position 2 = Tangency 3 = Curvature|曲面连续性：0 松散；1 位置连续；2 相切连续；3 曲率连续。
Determines the vector world directions to use 0 = Cardinal 1 = InterCardinal 2 = Cardinal + InterCardinal|世界向量方向：0 主方向；1 中间方向；2 主方向与中间方向。
Determines what type of curve to get 0 = Arc 1 = Circle 2 = Ellipse|获取类型：0 圆弧；1 圆；2 椭圆。
Determines which closest division length is used 0 = Nearest (The closest length to the target length) 1 = Floor (The closest length smaller than or equal to the target length) 2 = Ceiling (The closest length larger than or equal to the target length)|分割长度选择：0 最接近目标；1 不大于目标的最近长度；2 不小于目标的最近长度。
Determines which common grayscale luminosity weighting scheme to use 0 = R*0.2989, G*0.5870, B*0.1140 1 = R*0.2627, G*0.6780, B*0.0593 2 = R*0.2126, G*0.7152, B*0.0722 3 = R*0.3333, G*0.3333, B*0.3333|灰度亮度权重：0 为 RGB（0.2989、0.5870、0.1140）；1 为（0.2627、0.6780、0.0593）；2 为（0.2126、0.7152、0.0722）；3 为三通道等权（各 0.3333）。
Determines which parts of the twisted box to deconstruct 0 = Corner Points 1 = Edge Lines 2 = Face Polylines|扭曲盒解构类型：0 角点；1 边线；2 面多段线。
Determines which parts of the twisted box to get the center point (average) of 0 = Corner Points 1 = Edge Lines 2 = Face Polylines|中心点求平均对象：0 角点；1 边线；2 面多段线。
Determines which plane axis or axes to search the closest orientation to 0 = {xyz} 1 = {xy} 2 = {xz} 3 = {yz} 4 = {x} 5 = {y} 6 = {z}|最近朝向比较轴：0 XYZ；1 XY；2 XZ；3 YZ；4 X；5 Y；6 Z。
Domain defined offset center location of the twisted box tube array in relation to the curve (0.0 to 0.0 = centered on curve)|以区间定义空心管扭曲盒阵列相对曲线的偏移中心；0 到 0 表示居中于曲线。
Domain of revolution in degrees around the axis line (0 = start, 360 = end)|绕轴线旋转生成的角度区间，0 为起始、360 为结束，单位为度。
Domain of the graphs X Axis, where the values get plotted (if omitted the input value lists domain bounds is used)|图形 X 轴的区间，用于绘制输入数值；省略时使用输入数值列表的范围。
Domain of the graphs Y Axis, where the values get mapped to (if omitted the input value lists domain bounds is used)|图形 Y 轴的区间，用于映射数值；省略时使用输入数值列表的范围。
Extrusion direction vector, curve, or point Input a vector to exrude along a vector Input a curve to exrude along a curve Input a point to extrude to a point|挤出方向可输入向量、曲线或点：沿向量或曲线挤出，或向指定点挤出。
Extrusion direction vector, works best if direction is perpendicular to profile|挤出方向向量，建议垂直于截面。
Flip the graphs X Axis from the bottom of the graph to the top of the graph|将图形 X 轴从底部翻转到顶部。
Flip the mirror direction (False = Mirror after index, True = Mirror before index)|镜像方向：假为索引之后，真为索引之前。
Flip the mirror direction (false = Mirror after index, true = Mirror before index)|镜像方向：假为索引之后，真为索引之前。
Flip the trimming pattern to switch which parts of the curve get trimmed away|反转修剪模式，交换曲线被移除的部分。
Flip the twisted box flow if they are not flowing in the correct direction along the the inside of the pipe-like surface|管状曲面内部扭曲盒流向不正确时，反转流向。
Guide curve to tween along (best if flowing from first Curve in C to last Curve in C)|补间的引导曲线，建议方向从 C 首曲线指向末曲线。
Include the transparencies (alpha values) of the colors in the tweening|补间时同时包含颜色透明度（Alpha 值）。
Index of number in y nearest to each number in x (if Remap(R) is set to true then index of number in y nearest to each remapped number in x)|y 中距各 x 最近的数值索引；启用重映射 R 时使用重映射后的 x。
Index of the closest target plane by axis or axes orientation to the reference plane|按轴朝向与参考平面最接近的目标平面索引。
Indices from the input plane set of the planes that remained after the trim operation|裁剪后保留平面在输入平面组中的索引。
Indices from the input point set of the points that remained after the trim operation|裁剪后保留点在输入点组中的索引。
Indices from the input twisted box set of the twisted boxes that remained after the trimming|裁剪后保留扭曲盒在输入组中的索引。
Indicies of closed polysurface faces to remove for shelling, atleast one face must be removed|壳体操作需要移除的闭合多重曲面面索引，至少移除一个面。
Invert the transparencies (alpha values) of the mirrored colors|反转镜像颜色的透明度（Alpha 值）。
Invert the transparency (alpha value) of the color|反转颜色透明度（Alpha 值）。
Isocurve parameter along rectangle (0.0 = Rectangle direction start, 1.0 = Rectangle direction end)|矩形等参线参数，0 为方向起点，1 为终点。
Isocurve parameter along surface (0.0 = Surface direction start, 1.0 = Surface direction end)|曲面等参线参数，0 为方向起点，1 为终点。
Keep the lengths between reference vertices for the discrete polyline segment lengths, result discrete polyline will deviate more from reference vertices but have the same length as a regular polyline through the vertices would have|使用参考顶点间距作为离散多段线段长。结果可能更偏离参考顶点，但总长度与连接参考顶点的普通多段线相同。
Length along curve from kink to blend start (if omitted document tolerance is used)|从折角到混合连接起点的曲线长度，省略时使用文档容差。
Length of curve to remove, from each side of the seam for closed curves, from each end for open curves.(if omitted document tolerance is used)|需要移除的曲线长度：闭合曲线从接缝两侧移除，开放曲线从两端移除；省略时使用文档容差。
Merge coplanar polysurface faces into single surfaces WARNING: this option may be heavy depending on the amount of coplanar faces, please be sure to save before use|将多重曲面的共面面合并为单一曲面。警告：共面面较多时可能运算繁重，使用前请保存文件。
Merge coplanar polysurface faces into single surfaces WARNING: this option may be heavy depending on the amount of coplanar mesh faces, please be sure to save before use|将多重曲面的共面面合并为单一曲面。警告：共面网格面较多时可能运算繁重，使用前请保存文件。
Number in y nearest to number x (if Remap(R) is set to true then number in y nearest to remapped number x)|y 中最接近 x 的数值；启用重映射 R 时使用重映射后的 x。
Number to tween from|补间起始数值。
Number to tween to|补间目标数值。
Number which will be the negative and positive extents of the domain from zero|指定区间从零向正负方向延伸的范围值。
Optional allowable distance between start and end of curve. If gap is larger than tolerance the curve will not close. If tolerance is 0 the curve will close no matter the gap size.|可选端点距离容差。端点间隙大于容差时不闭合；容差为 0 时不限制间隙。
Optional allowable distance between start and end of curve. If gap is larger than tolerance the curve will not close. If tolerance is 0.0 the curve will close no matter the gap size.|可选端点距离容差。端点间隙大于容差时不闭合；容差为 0 时不限制间隙。
Optional anchor points from the set of points to pinch & spread which will not be moved by the pinch & spread|可选锚点，来自输入点组，不受收拢与扩散影响。
Optional curves to unroll with the polysurface (Brep) or surface, curves should lay exactly on the polysurface (Brep) faces or surface|可选附属曲线，将随多重曲面或曲面展开，曲线应精确位于其面上。
Optional curves to unroll with the polysurface (Brep), curves should lay exactly on the polysurface (Brep) faces|可选附属曲线，将随多重曲面展开，曲线应精确位于其面上。
Optional end point of the mesh loft (can also be used to cap the end of a mesh loft which has a closed end section curve)|可选网格放样终点，也可用于封闭末端截面闭合的放样网格。
Optional guide curve to match the {t} domain range of (will override domain if a domain is also input)|可选引导曲线，用于匹配其 {t} 区间；同时输入区间时，引导曲线优先。
Optional guide plane to determine if the plane should flip, based on the guide plane axis angle to the axis of plane to flip|可选引导平面，根据其轴与目标平面轴的夹角判断是否反转。
Optional guide point for the start of the seam alignment (will override the seam location of the first curve in the set)|可选接缝对齐起始引导点，优先于首曲线的接缝位置。
Optional guide point for the start of the seam alignment (will override the seam point of the first curve in the set)|可选接缝对齐起始引导点，优先于首曲线的接缝点。
Optional guide point to find the closest corner to (will override the initial seam location)|可选引导点，用于查找最近角点，优先于原接缝位置。
Optional guide surface to match the {uv} domain² range of (will override domain² if a domain² is also input)|可选引导曲面，用于匹配其 UV 二维区间；同时输入区间时，引导曲面优先。
Optional indices of corners to deform instead of points (will override corner points if points are also input)|可选角点索引，用于指定变形角点，优先于角点坐标输入。
Optional number which will explode the unrolled polysurface (Brep) faces as a disconnected linear array spaced apart by the amount of the number, unrolled points and curves will follow|可选展开间距，将展开后的各面拆开成线性阵列，附属点和曲线也随之移动。
Optional offset distance to offset both sides, use the inverse number of the distance to offset in the opposite direction (so if distance is a positive number then use a negative number and vice versa)|可选另一侧偏移距离，使用相反符号向反方向偏移。
Optional parameter on curve to get length to instead of a point (will override point if a point is also input)|可选曲线参数，用于代替点计算长度；同时输入点时参数优先。
Optional parameters to trim with instead of points (will override points if points are also input)|可选修剪参数组，用于代替点组；同时输入点时参数优先。
Optional plane to mirror the vector directions when using reflected mirror type, otherwise only the set order is reflected|反射镜像类型的可选参考平面，用于镜像向量方向；未指定时仅镜像组顺序。
Optional points from points(P) that act as anchored points which will not be effected by pinching & spreading|可选锚点，取自 P 点组，不受收拢与扩散影响。
Optional points to unroll with the polysurface (Brep) or surface, points should lay exactly on the polysurface (Brep) faces or surface|可选附属点，将随多重曲面或曲面展开，点应精确位于其面上。
Optional points to unroll with the polysurface (Brep), points should lay exactly on the polysurface (Brep) faces|可选附属点，将随多重曲面展开，点应精确位于其面上。
Optional second guide curve to slide along (best if flowing in the direction of Guide 1)|可选第二引导曲线，用于滑动，建议与引导曲线 1 同向。
Optional second guide curve to tween along (best if flowing in the direction of Guide 1)|可选第二引导曲线，用于补间，建议与引导曲线 1 同向。
Optional second rail curve to sweep along (best if flowing in the direction of Rail 1)|可选第二扫掠轨道，建议与轨道 1 同向。
Optional set of parameters on curve to get lengths between instead of points (will override points if points are also input)|可选曲线参数组，用于代替点计算长度；同时输入点时参数优先。
Optional start point of the mesh loft (can also be used to cap the start of a mesh loft which has a closed start section curve)|可选网格放样起点，也可用于封闭起始截面闭合的放样网格。
Optional {u} degree of surface (if omitted input surface {u} degree is used)|可选曲面 U 次数，省略时使用输入曲面 U 次数。
Optional {v} degree of surface (if omitted input surface {v} degree is used)|可选曲面 V 次数，省略时使用输入曲面 V 次数。
Overall thickness of the twisted box array from the mesh, offset from the faces|扭曲盒阵列从网格面偏移的总厚度。
Parameter to adjust the seam of the first curve in the set (unless a guide point is used)|用于调整首曲线接缝的参数；使用引导点时不采用此值。
Point to relocate the curves end to (if no point it supplied then the curve end will not be relocated)|曲线的新终点，未提供时不移动终点。
Point to relocate the curves start to (if no point it supplied then the curve start will not be relocated)|曲线的新起点，未提供时不移动起点。
Profile curve or surface to extrude as twisted boxes Profile should preferably be a quadrilateral polygon (4 sided polyline with 4 corners). If profile is not a quadrilateral polygon it will be converted. Profile does not need to be planar or closed. Triangles are acceptable.|用于挤出扭曲盒的截面曲线或曲面。建议四边形截面，否则进行转换；无需共面或闭合，也支持三角形。
Rail curve to sweep along (best if flowing from first Section in S to last Section in S)|扫掠轨道，建议方向从 S 首截面指向末截面。
Rectangle which defines the boundary of the graph, graph curves should be atleast partially inside this boundary|定义图形边界的矩形，图形曲线至少部分位于边界内部。
Remapped number set x to the domain bounds of number set y if Remap(R) is true. Same number as number set x if Remap(R) is false|R 为真时返回映射到 y 区间范围的 x 数值组；R 为假时返回原 x 数值组。
Remapped number x to domain of numbers y if Remap(R) is true. Same number as number x if Remap(R) is false|R 为真时返回映射到 y 区间的 x；R 为假时返回原 x。
Remove the transparency (alpha value) of the color|移除颜色透明度（Alpha 值）。
Resize the graph by snapping it to the extents of the graph curves, in the plane of the boundary rectangle|在边界矩形平面内将图形大小吸附至图形曲线范围。
Rotation factor (0.0 = Plane Pl¹, 1.0 = Plane Pl²)|旋转因子，0 对应平面 Pl¹，1 对应平面 Pl²。
Rotation of the twisted box curve around the curve, in degrees (if the twisted box curve is centered on the curve the effect will look the same as rotation 1)|曲线扭曲盒绕曲线的旋转角，单位为度；居中于曲线时与旋转 1 效果相同。
Rotation of the twisted box curve around the twisted box centers, in degrees|曲线扭曲盒绕各盒中心的旋转角，单位为度。
Rotation of the twisted box tube array around the curve, in degrees (if the twisted box tube array is centered on the curve the effect will look the same as rotation 1)|空心管扭曲盒阵列绕曲线的旋转角，单位为度；居中于曲线时与旋转 1 效果相同。
Rotation of the twisted box tube array around the diameter centers, in degrees|空心管扭曲盒阵列绕直径中心的旋转角，单位为度。
Rotation of the twisted box tube array around the radius centers, in degrees|空心管扭曲盒阵列绕半径中心的旋转角，单位为度。
Section curves or surfaces to loft through|用于放样的截面曲线或曲面组。
Section curves or surfaces to make twisted boxes between Sections should preferably be quadrilateral polygons (4 sided polylines with 4 corners). If sections are not quadrilateral polygons they will be converted. Sections do not need to be planar or closed. Triangles are acceptable.|用于在其间生成扭曲盒的截面组，建议四边形；否则转换，无需共面或闭合，也支持三角形。
Section curves or surfaces to sweep through|用于扫掠的截面曲线或曲面组。
Set of 2, 3, or 4 edge curves to auto sort and create the edge surface between|用于自动排序并生成边缘曲面的 2、3 或 4 条边缘曲线。
Set of 2, 3, or 4 edge curves to create the edge surface between|用于生成边缘曲面的 2、3 或 4 条边缘曲线。
Set of 8 corner points that make a twisted box|组成扭曲盒的 8 个角点。
Set of closed curves to align seams of|需要对齐接缝的闭合曲线组。
Set of dispatching indices (should not have duplicate index values)|分派索引组，索引值不应重复。
Set of exponents that determine the exponential pulling power of the falloffs, one exponent for each falloff|各衰减函数的指数拉力参数，每个衰减对应一个指数。
Set of falloffs that determine how the strengths pull gradually falls off, one falloff for each strength Falloff (0.0 = Sharpest, 1.0 = Smoothest)|各强度对应的衰减系数，0 最尖锐，1 最平滑。
Set of list items to sort synchronously with the set of points (if nothing is input then only the set of points will be sorted)|与点组同步排序的项目列表；未输入时仅排序点组。
Set of numbers to get highest and lowest values of|用于求最大值和最小值的数值组。
Set of numbers to round nearest to (best to not have duplicate y values)|最近值舍入的目标数值组，建议 y 值不重复。
Set of points on curve to get lengths between|用于计算曲线长度的曲线上点组。
Set of points that define the locations to pinch & spread at|定义收拢与扩散作用位置的点组。
Set of polysurfaces (Breps) or surfaces to append|需要合并的多重曲面或曲面组。
Set of radii that determine how far the pinch & spread reaches from the location points, one radius for each location point|各作用点的收拢与扩散影响半径，每个点对应一个半径。
Set of rail curves that the twisted boxes flow between|扭曲盒流动于其间的轨道曲线组。
Set of section curves or surfaces to loft through|用于放样的截面曲线或曲面组。
Set of section curves to loft through as mesh|用于生成放样网格的截面曲线组。
Set of sifting indices (should not have duplicate index values)|筛分索引组，索引值不应重复。
Set of strengths that determine how much to pinch & spread within each radius, one strength for each radius Pinch (0.0 = Weakest, 1.0 = Strongest) Spread (0.0 = Weakest, -1.0 = Strongest)|各半径对应的作用强度：收拢为 0 到 1，扩散为 0 到 -1，绝对值越大作用越强。
Set of transformations to compound into a mass transform (X outputs of components that perform transformations like Move, Scale, Rotate, etc.)|需要复合为累计变换的变换组，可连接移动、缩放、旋转等组件的 X 输出。
Set of twsisted boxes to trim|待裁剪扭曲盒组。
Set of weights that pulls the falloffs sharply towards the pinch & spread direction, one weight 2 for each falloff Weight 2 (0.0 = Lightest, 1.0 = Heaviest)|各衰减函数的权重 2，控制沿作用方向的尖锐拉伸；0 最轻，1 最重。
Set of weights that pulls the falloffs smoothly towards the pinch & spread direction, one weight 1 for each falloff Weight 1 (0.0 = Lightest, 1.0 = Heaviest)|各衰减函数的权重 1，控制沿作用方向的平滑拉伸；0 最轻，1 最重。
Seventh corner (1,1,1)|第七个角点（1,1,1）。
Shrinks the underlying untrimmed surface of a trimmed surface to be as close as possible to the trimmed surface edges, also works with polysurface (Brep) faces.|收缩已修剪曲面的底层曲面，使其贴近修剪边界，也支持多重曲面的面。
Sixth corner (1,0,1)|第六个角点（1,0,1）。
Slide the bounding rectangle along the axis (0.0 = Start of bounding volume, 1.0 = End of bounding volume)|沿轴滑动包围矩形，0 为包围体起点，1 为终点。
Start point to sort the set of points from|点组排序的起始点。
Strength of pinch & spread. (pinch = 0.0[weakest] to 1.0[strongest], spread = 0.0[weakest] to -1.0[strongest])|收拢与扩散强度：收拢为 0 到 1，扩散为 0 到 -1，绝对值越大作用越强。
Strengths of pinch & spread. (pinch = 0.0[weakest] to 1.0[strongest], spread = 0.0[weakest] to -1.0[strongest])|收拢与扩散强度列表：收拢为 0 到 1，扩散为 0 到 -1，绝对值越大作用越强。
Surface (or polysurface (Brep)) to offset|待偏移曲面或多重曲面。
Surface (or polysurface (Brep)) to test if it is trimmed|用于检测是否已修剪的曲面或多重曲面。
Surface (or polysurface (Brep)) to trim|待修剪曲面或多重曲面。
Surface for target coordinate space|定义目标坐标空间的曲面。
Surface or Polysurface (Brep) to get statistics of|用于统计的曲面或多重曲面。
Surface parameter coordinates at the span ends To get the point between each span use these as the Point(uv) input on Grasshopper's Evaluate Surface component.|曲面跨度末端的参数坐标，可输入 Grasshopper“曲面求值”组件的 UV 端口获取点。
Surface sub-domain² for each span that makes up the surface To extract each span as a separate surface use these as the Domain(D) input on Grasshopper's Isotrim component.|各曲面跨度的二维子区间，可输入 Grasshopper 的 Isotrim 组件提取各跨度。
Swap the surface {u} and {v} directions|交换曲面 U、V 方向。
Tangent vector at the curves length or domain middle point|曲线长度或区间中点处的切向量。
Tangent vectors at edit points|编辑点处的切向量。
Taper draft angle in degrees|锥度挤出的拔模角，单位为度。
Target curve to superimpose properties onto|需要套用属性的目标曲线。
Target face count. This number is just a target goal, face count in resulting reduced mesh may differ|目标面数，仅为目标值，简化结果的实际面数可能不同。
Target length of curve divisions|曲线分割的目标长度。
Target plane set to search|用于搜索的目标平面组。
Target surface to superimpose properties onto|需要套用属性的目标曲面。
Target twisted boxes to morph to|形变映射的目标扭曲盒组。
Target vector set|目标向量组。
Target vector set to search|用于搜索的目标向量组。
The actual domain range of the linearized set of numbers before fitting between the domain bounds|线性化数值在拟合目标区间边界前的实际范围。
The center point (average) of the selected twisted box parts Use Pufferfish's Twisted Box Volume component to get the volumetric center point|扭曲盒所选部分的平均中心点；体积形心请使用河豚“扭曲盒体积”组件。
The curves which unrolled with the polysurface (Brep) faces|随多重曲面各面展开的曲线。
The curves which unrolled with the polysurface (Brep) faces or surface|随多重曲面各面或曲面展开的曲线。
The difference between the resulting nearest number set and the input number set x|最近值结果与输入数值组 x 的差值。
The difference between the resulting rounded number and the input number X|舍入结果与输入数值 X 的差值。
The difference between the resulting rounded number and the input number x|舍入结果与输入数值 x 的差值。
The domain bounds to linearize the number set between|数值线性化的目标区间边界。
The graph boundary background as a surface|作为曲面的图形边界背景。
The graph curves inside the boundary of the graph|图形边界内的曲线。
The graph labels as curve outlines|作为曲线轮廓的图形标签。
The last index of the list|列表末项索引。
The length value used for the divisions|分割所使用的实际长度。
The lines from the X Axis input values to the graph curves|从 X 轴输入值连接到图形曲线的线。
The lines from the graph curves to the Y Axis graph mapped values|从图形曲线连接到 Y 轴映射值的线。
The new {t} domain range of the curve|曲线的新 {t} 参数区间。
The new {uv} domain² range of the surface|曲面的新 UV 二维区间。
The number of times the multiplication factor fits into the input number X|输入数值 X 包含乘法因子的倍数。
The number of times the multiplication factor fits into the input number x|输入数值 x 包含乘法因子的倍数。
The number of times the multiplication factor fits into the resulting rounded number|舍入结果包含乘法因子的倍数。
The plane at the offset distance|偏移距离处的平面。
The plane at the reach distance|作用距离处的平面。
The points mapped on the Y Axis which represent the graph mapped values|Y 轴上表示映射数值的点。
The points on the graph curves where the X Axis input values intersected|X 轴输入值与图形曲线相交的点。
The points plotted on the X Axis which represent the input values|X 轴上表示输入数值的点。
The points which unrolled with the polysurface (Brep) faces|随多重曲面各面展开的点。
The points which unrolled with the polysurface (Brep) faces or surface|随多重曲面各面或曲面展开的点。
The quaternion plane at the rotation factor|指定旋转因子对应的四元数旋转平面。
The quaternion rotation angle in degrees|四元数旋转角，单位为度。
The quaternion rotation axis vector|四元数旋转轴向量。
The selected deconstructed twisted box parts|解构得到的扭曲盒所选部分。
The shrunken underlying untrimmed surface of the trimmed surface (or polysurface (Brep))|已修剪曲面或多重曲面收缩后的底层未修剪曲面。
The splitting index To split the mirror cut plane set at the mirror use this as the index input on Grasshopper's Split List component.|镜像裁剪平面组的分割索引，可输入 Grasshopper“分割列表”组件在镜像处分开结果。
The splitting index To split the mirror cut point set at the mirror use this as the index input on Grasshopper's Split List component.|镜像裁剪点组的分割索引，可输入 Grasshopper“分割列表”组件在镜像处分开结果。
The welding tolerance for the mesh joining if J is true (you won't need to change this unless join is true but does not make properly welded meshes)|J 为真时网格连接的焊接容差，仅在连接后未正确焊接时需要调整。
Thickness factor (0.0 = No Thickness, 1.0 = Full Thickness)|厚度因子，0 无厚度，1 完整厚度。
Thickness of the shell|壳体厚度。
Thickness of the twisted box pipe array, offset inward from the outer diameter corners|管状扭曲盒阵列厚度，从外径角点向内偏移。
Thickness of the twisted box strip, offset from the rail curves|条带扭曲盒从轨道曲线偏移的厚度。
Thickness of the twisted box strips, offset from the rail curves|多条带扭曲盒从轨道曲线偏移的厚度。
Thickness of the twisted box tube array, offset inward from the outer diameter corners|空心管扭曲盒阵列厚度，从外径角点向内偏移。
Thickness of the twisted box tube array, offset inward from the outer radius corners|空心管扭曲盒阵列厚度，从外半径角点向内偏移。
Third corner (1,1,0)|第三个角点（1,1,0）。
Tolerance angle in degrees for kink smoothing|折角平滑的角度容差，单位为度。
Tolerance angle in degrees for kink smoothing (if omitted document angle tolerance is used)|折角平滑的角度容差，单位为度；省略时使用文档角度容差。
Tolerance distance the fit curve is allowed to deviate from the curve to fit (if omitted document tolerance is used)|拟合曲线相对原曲线允许的距离偏差，省略时使用文档容差。
Tolerance distance the smooth curve is allowed to deviate from the curve to smooth|平滑曲线相对原曲线允许的距离偏差。
Tolerance for fitting (if omitted document tolerance is used)|拟合容差，省略时使用文档容差。
Tolerance for the allowable surface area deviation that determines if the polysurface (Brep) or surface can be unrolled (if omitted document tolerance is used)|允许的展开面积偏差容差，用于判断曲面或多重曲面能否展开；省略时使用文档容差。
Tolerance for the allowable surface edge deviation that determines if the polysurface (Brep) or surface can be unrolled (if omitted document tolerance is used)|允许的展开边缘偏差容差，用于判断曲面或多重曲面能否展开；省略时使用文档容差。
Tolerance to determine if a curve is an arc, circle, or ellipse (if omitted RhinoMath zero distance tolerance (1.0e-12) is used)|圆弧、圆或椭圆类型判断容差，省略时使用 RhinoMath 零距离容差 1.0e-12。
Tolerance to get arc, circle, or ellipse (if omitted RhinoMath zero distance tolerance (1.0e-12) is used)|圆弧、圆或椭圆提取容差，省略时使用 RhinoMath 零距离容差 1.0e-12。
Transform to slide within|用于获取中间状态的变换。
Transformation data (X output of components that perform transformations like Move, Scale, Rotate, etc.)|变换数据，可连接移动、缩放、旋转等组件的 X 输出。
Transformation that will be used to transform the geometry at each recursive step (X outputs of components that perform transformations like Move, Scale, Rotate, etc.) Use Pufferfish's Mass Transform component or Grasshopper's Compound component to combine multiple transformations into one transform to use in this input, so multiple transformations can affect the geometry. (*Be extra careful with transformations such as scaling as recursively scaling with many steps can quickly generate extremely large or small sized geometry, which may freeze Grasshopper)|每步递归使用的变换，可连接移动、缩放、旋转等组件的 X 输出。多个变换可用河豚“复合变换”或 Grasshopper 的 Compound 合并。警告：多步递归缩放可能迅速产生极大或极小几何，导致无响应。
Transformation that will be used to transform the twisted box (X outputs of components that perform transformations like Move, Scale, Rotate, etc.)|扭曲盒变换数据，可连接移动、缩放、旋转等组件的 X 输出。
Translation (Move) vector|平移向量。
Triangulate the mesh faces|将网格面三角化。
Trimmed surface (or polysurface (Brep)) to shrink underlying untrimmed surface of|需要收缩底层未修剪曲面的已修剪曲面或多重曲面。
Tween the mesh vertex colors|同时补间网格顶点颜色。
Tween the transparencies (alpha values) of the colors|同时补间颜色透明度（Alpha 值）。
Unroll the polysurface (Brep) faces as a disconnected linear array, unrolled points and curves will follow|将展开后的多重曲面各面拆开成线性阵列，附属点和曲线随之移动。
Use null placeholders in each resulting number set for values that go into the opposite number set so that the resulting number sets orders and lengths are the same as the input set of numbers|在各结果数组中用空值占位归入另一组的数值，使结果顺序和长度与输入一致。
Values to graph map. Values are plotted along the X Axis, intersected with the graph curves, then mapped to the Y Axis|用于图形映射的数值：先绘制在 X 轴上，与图形曲线相交，再映射到 Y 轴。
Volume centroid of twisted box|扭曲盒的体积形心。
Volume of the box|盒的体积。
Volume of the ellipsoid|椭球体积。
Volume of twisted box|扭曲盒体积。
Volume to scale the geometry to|几何对象缩放后的目标体积。
Weld mesh vertices that are within a specified proximity of eachother (0.0 = No weld, Number greater than 0 = Weld vertices within proximity of the number)|焊接指定邻近距离内的网格顶点；0 不焊接，正数作为焊接距离。
'''))
port_manual = {re.sub(r'\s+', ' ', k).strip(): v for k, v in port_manual.items()}


def port_description(text):
    normalized = re.sub(r'\s+', ' ', text).strip().replace('虏', '²').replace('鹿', '¹')
    if normalized in port_manual:
        return port_manual[normalized]
    subd_ports = pairs('''
Set of SubDs for averaging|用于求平均的细分曲面组。
Collection of weights for each SubD|每个细分曲面的权重。
Arithmetic mean (average) of all input SubDs|所有输入细分曲面的算术平均值。
Determines how SubDs are creased (0 = None, 1 = At Creases, 2 = At Edges)|细分曲面折痕方式：0 无；1 沿折痕；2 沿边缘。
Determines how SubDs are cornered (0 = None, 1 = At Corners)|细分曲面角点方式：0 无；1 在角点。
If True, SubDs are interpolated through their control polygon vertices|为真时，使细分曲面插值通过控制多边形顶点。
Number of subdivision levels for each SubD face|各细分曲面面片的细分层级数。
SubD to mirror cut|待镜像裁剪的细分曲面。
SubD to tween from|补间起始细分曲面。
SubD to tween to|补间目标细分曲面。
SubD to create twisted boxes from|扭曲盒生成的起始细分曲面。
SubD to create twisted boxes to|扭曲盒生成的目标细分曲面。
SubD to create twisted box array on|用于生成扭曲盒阵列的细分曲面。
Set of SubDs to tween between|用于补间的细分曲面组。
Set of SubDs to tween through|用于贯穿补间的细分曲面组。
Set of SubDs to create twisted box array between|用于在相邻项间生成扭曲盒阵列的细分曲面组。
Set of SubDs to create twisted box array through|用于贯穿生成扭曲盒阵列的细分曲面组。
Resulting tween SubD|补间生成的细分曲面。
Resulting tween SubDs|补间生成的细分曲面组。
Resulting mirror cut SubDs|镜像裁剪后的细分曲面组。
Resulting twisted box array on SubD|细分曲面上的扭曲盒阵列。
Resulting twisted box array between SubDs|细分曲面间的扭曲盒阵列。
Resulting twisted box array consecutively between SubDs|相邻细分曲面间的扭曲盒阵列。
Resulting twisted box array through SubDs|贯穿细分曲面组的扭曲盒阵列。
Join the mirror cut SubD|连接镜像裁剪后的细分曲面。
Keep the SubD and mirror it normally if it is mirror cut into non-existence|镜像裁剪导致细分曲面消失时，保留原对象并执行普通镜像。
Number of SubD edge loop divisions per side of the SubD connection|细分曲面连接各侧的环边分割数。
Overall thickness of the twisted box array from the SubD, offset from the faces|从细分曲面各面偏移的扭曲盒阵列总厚度。
Parts of the SubD within this distance from the mirror plane will be additionally cut away|距镜像平面该距离内的细分曲面部分也会移除。
Plane that the kept side of the SubD cut gets mirrored across|细分曲面保留侧所用的镜像平面。
True if the SubD was intersected by the mirror cut, False if the SubD was not intersected by the mirror cut|镜像裁剪与细分曲面相交时为真，否则为假。
Determines how the mirror cut SubDs are connected (0 = Split faces, with connection, 1 = Remove faces, with connection, 2 = Shrink faces, with connection, 3 = Split faces, without connection, 4 = Remove faces, without connection, 5 = Shrink faces, without connection)|镜像裁剪连接方式：0 分割面并连接；1 移除面并连接；2 收缩面并连接；3 分割面但不连接；4 移除面但不连接；5 收缩面但不连接。
Determines how the tween path is interpolated (0 = Linear, 1 = Chord, 2 = Square Root, 3 = Uniform)|补间路径插值方式：0 线性；1 弦长；2 平方根；3 均匀。
Determines how the {w} interpolation path is interpolated (0 = Linear, 1 = Chord, 2 = Square Root, 3 = Uniform)|W 路径插值方式：0 线性；1 弦长；2 平方根；3 均匀。
Distance to offset the kept parts of the SubD from the mirror plane (or offset from the reach if reach in not zero)|保留细分曲面相对镜像平面的偏移距离，作用距离非零时从作用边界开始偏移。
Weld SubD vertices that are within a specified proximity of eachother (0.0 = No weld, Number greater than 0 = Weld vertices within proximity of the number)|焊接指定距离内的细分曲面顶点：0 不焊接，正数作为焊接距离。
The splitting index (only if Join is false). To split the mirror cut SubD set at the mirror use this as the index input on Grasshopper's Split List component.|连接为假时有效的分割索引，可输入 Grasshopper“分割列表”组件在镜像处分开结果。
''')
    if normalized in subd_ports:
        return subd_ports[normalized]
    if normalized.startswith('Tween factor') and 'SubD' in normalized:
        return '细分曲面补间因子：0 起始、1 结束；相邻模式为当前至下一项，贯穿模式可使用归一化或列表索引范围。'
    prefix_templates = {
        'Set of ': ('一组', {' for averaging': '，用于求平均值', ' to tween through': '，用于贯穿补间', ' to tween between': '，用于补间', ' to tween consecutively': '，用于相邻补间', ' to mirror cut': '，用于镜像裁剪', ' to mirror combine': '，用于镜像合并', ' to reparameterize': '，用于重新参数化', ' to trim': '，用于裁剪', ' to sort': '，用于排序'}),
        'Collection of weights for each ': ('对应每个', {'': '的权重集合'}),
        'Arithmetic mean (average) of all input ': ('所有输入', {'': '的算术平均值'})
    }
    singular_nouns = {'color': '颜色', 'curve': '曲线', 'domain': '一维区间', 'domain²': '二维区间', 'mesh': '网格', 'number': '数值', 'plane': '平面', 'point': '点', 'surface': '曲面', 'transform': '变换', 'twisted box': '扭曲盒', 'vector': '向量'}
    if normalized.startswith('Collection of weights for each '):
        rest = normalized[len('Collection of weights for each '):]
        if rest in singular_nouns:
            return '每个' + singular_nouns[rest] + '的权重。'
    if normalized.startswith('Resulting '):
        rest = normalized[len('Resulting '):]
        qualified = {**singular_nouns, **nouns}
        qualified.update({'polysurface (Brep)': '多重曲面（Brep）', 'polysurfaces(Breps) or surfaces': '多重曲面或曲面', 'polylines': '多段线', 'polyline': '多段线', 'geometries': '几何对象', 'geometry': '几何对象', 'plane set': '平面组', 'point set': '点组', 'color set': '颜色组', 'domain set': '区间组', 'domain² set': '二维区间组', 'number set': '数值组', 'transform set': '变换组', 'vector set': '向量组', 'list items set': '项目列表', 'list item set': '项目列表', 'set of numbers': '数值组', 'set of domains': '区间组', 'set of domain²s': '二维区间组', 'set of points': '点组', 'set of vectors': '向量组', 'set of list items': '项目列表', 'set of indices': '索引列表', 'arc, circle, or ellipse': '圆弧、圆或椭圆', 'percentage': '百分比', 'two way domain': '双向区间', 'two way domain²': '双向二维区间'})
        for modifier, chinese in [('tween ', '补间'), ('mirror combined ', '镜像合并后的'), ('mirror cut ', '镜像裁剪后的'), ('rebuilt ', '重建后的'), ('reparameterized ', '重新参数化后的'), ('trimmed ', '修剪后的'), ('offset ', '偏移后的'), ('fitted ', '拟合后的'), ('blend ', '混合后的'), ('closed ', '闭合后的'), ('opened ', '打开后的'), ('flipped ', '反转后的'), ('sorted ', '排序后的'), ('deformed ', '变形后的'), ('displaced ', '位移后的'), ('reduced ', '简化后的'), ('smoothed ', '平滑后的'), ('superimposed ', '套用属性后的'), ('swapped direction ', '交换方向后的'), ('split ', '分割后的'), ('inverted ', '取反后的'), ('transformed ', '变换后的'), ('reference ', '引用的'), ('center ', '居中的'), ('domain ', '区间定义的'), ('2Pt ', '两点定义的')]:
            if rest.startswith(modifier) and rest[len(modifier):] in qualified:
                return chinese + qualified[rest[len(modifier):]] + '。'
        if rest in qualified:
            return '生成的' + qualified[rest] + '。'
        for suffix, chinese in [(' on surface', '曲面上的'), (' on curve', '曲线上的'), (' along curve', '沿曲线的')]:
            if rest.startswith('tween ') and rest.endswith(suffix) and rest[len('tween '):-len(suffix)] in qualified:
                return chinese + qualified[rest[len('tween '):-len(suffix)]] + '补间结果。'
    m = re.fullmatch(r'(Curve|Surface|Mesh|Plane|Point|Domain|Domain²|Transform|Vector|Twisted Box|Color) to (tween|blend) (from|to)', normalized)
    if m:
        return ('起始' if m[3] == 'from' else '目标') + singular_nouns[m[1].lower()] + '，用于' + ('补间' if m[2] == 'tween' else '混合') + '。'
    if normalized.startswith('Resulting untrimmed single unsplit'):
        kind = normalized[len('Resulting untrimmed single unsplit'):].split('surface', 1)[0].strip()
        types = {'edge': '边缘', 'extruded': '挤出', 'lofted': '放样', 'rail revolved': '沿轨道旋转', 'revolved': '旋转', 'sum': '和', 'swept': '扫掠'}
        if kind in types:
            return '生成的未修剪单一不分裂' + types[kind] + '曲面。烘焙到 Rhino 时通常会在折角处拆分；可先将 Rhino 的 CreaseSplitting 设为 No，或用河豚“按折角分裂曲面”组件显式分裂。'
    if normalized.startswith('Resulting rounded number from rounding'):
        result = '按小数位舍入后的数值。' if 'decimal place' in normalized else '按倍数因子舍入后的数值。'
        if 'formatting options' in normalized:
            result += '显示小数位受 Grasshopper 格式设置限制，该设置不改变实际数值，末尾多余零不显示。'
        return result
    if normalized.startswith(('Resulting rebuilt surface To include surface trims', 'Resulting superimposed surface To include surface trims')):
        return '重建或套用属性后的曲面。若需保留修剪边界，可将其作为目标输入 Grasshopper 的 Retrim 或 Copy Trim 组件。'
    if normalized.startswith('Resulting list of items') and 'sifting indices' in normalized:
        return '按筛分索引得到的项目列表，用空值占位另一列表中的项目。处理后可用 Grasshopper 的 Combine Data 组件合并两个列表并替换空值。'
    if normalized.startswith('Resulting grid cell outlines on surface To pull'):
        return '曲面上的网格单元轮廓；可用 Grasshopper 的 Pull Curve 组件将轮廓贴合曲面曲率。'
    result_manual = pairs('''
twisted box array|扭曲盒阵列
appended single disjoint polysurface (Brep)|合并后的单个分离多重曲面
automatic edge surface|自动边缘曲面
automatic network surface|自动网络曲面
axis aligned vectors|与轴对齐的向量
bounding rectangle or rectangles|包围矩形
color from point|由点转换的颜色
compatible polylines|控制点数量一致的多段线
constrained area ellipse|指定面积椭圆
constrained area polygon|指定面积多边形
constrained area rectangle|指定面积矩形
constrained volume box|指定体积盒
constrained volume ellipsoid|指定体积椭球
curve coil points|沿曲线螺旋点
curve scaled to length|缩放至目标长度的曲线
curve slid along curve|沿曲线滑动后的曲线
curve wave points|沿曲线波浪点
curve with remapped {t} domain range|重映射 {t} 区间后的曲线
curve with seam adjusted to the closest corner|接缝移至最近角点后的曲线
curve without kinks|无折角曲线
curves with aligned seams|接缝对齐后的曲线组
discrete polyline|方向离散多段线
displacing normal vectors|用于位移的法向量
division curves on rectangle flowing in {x} direction|矩形上 X 方向分割曲线
division curves on rectangle flowing in {y} direction|矩形上 Y 方向分割曲线
division curves on surface flowing in {u} direction|曲面上 U 方向分割曲线
division curves on surface flowing in {v} direction|曲面上 V 方向分割曲线
division planes on surface|曲面上的分割平面
division points on surface|曲面上的分割点
even number set|偶数组
odd number set|奇数组
extrude mesh|挤出网格
extruded twisted boxes|挤出扭曲盒
fitted segment curve|拟合后的分段曲线
geometries morphed to twisted boxes|映射到扭曲盒的几何对象
geometry scaled to area|缩放至目标面积的几何对象
geometry scaled to volume|缩放至目标体积的几何对象
graph mapped values, mapped on the Y Axis|映射到 Y 轴的图形映射数值
grayscale color|灰度颜色
grid cell outlines in rectangle|矩形内网格单元轮廓
grid cell outlines on surface|曲面上网格单元轮廓
inverted boolean|取反后的布尔值
isocurve on rectangle|矩形等参线
isocurve on surface|曲面等参线
linearized set of numbers|线性化数值组
list of items at the dispatching indices|命中分派索引的项目列表
list of items not at the dispatching indices|未命中分派索引的项目列表
loft mesh|放样网格
lofted twisted boxes|放样扭曲盒
mass division|连续除法结果
mass subtraction|连续减法结果
mass transform|复合变换
mesh edge loop polylines|网格环边多段线
mesh from polyline boundary|由多段线边界生成的网格
mesh from surface|由曲面生成的网格
mesh naked edge polylines|网格裸边多段线
moved (translated) geometry|平移后的几何对象
moved geometry|移动后的几何对象
number within domain|区间内数值
offset curve from surface|从曲面偏移的曲线
offset surface (or polysurface (Brep))|偏移曲面或多重曲面
pinched & spread points|收拢与扩散后的点
pipe mesh|管状网格
planar mesh from rectangle|矩形内平面网格
plane in rectangle|矩形内平面
plane on surface|曲面上平面
point from color|由颜色转换的点
point in rectangle|矩形内点
point mapped to the target surface space|映射到目标曲面空间的点
point on surface|曲面上的点
polysurface shell (Brep)|多重曲面壳体
polysurface(Brep) split at kinks|按折角分裂的多重曲面
rebuilt segment curve|重建后的分段曲线
rectangle fit through the point set|通过点组拟合的矩形
rectangle normal vector at plane|平面处的矩形法向量
rectangle normal vector at point|点处的矩形法向量
recursive morphed mesh|递归形变后的网格
recursively transformed geometry|递归变换后的几何对象
relocated ends curve|端点重新定位后的曲线
reparameterized curve with a (t) domain range from 0 to 1|参数区间归一化为 0 到 1 的曲线
reparameterized curve with a domain range from 0 to 1|参数区间归一化为 0 到 1 的曲线
reparameterized set of numbers with a domain range from 0 to 1|归一化为 0 到 1 的数值组
reparameterized set of points with a domain range in the {x}, {y}, and {z} coordinates from 0 to 1|XYZ 坐标分别归一化为 0 到 1 的点组
reparameterized surface with a domain range in the {u} and {v} directions from 0 to 1|UV 参数区间归一化为 0 到 1 的曲面
reparameterized surface with a {uv} domain² range from 0 to 1|UV 二维区间归一化为 0 到 1 的曲面
rotated geometry|旋转后的几何对象
slide curve along curve|沿引导曲线滑动的曲线
spatial subdivision vectors|空间细分向量
strip twisted boxes|条带扭曲盒
subdivision surfaces|细分子曲面
subdivision twisted boxes|细分扭曲盒
surface normal vector at plane|平面位置的曲面法向量
surface normal vector at point|点位置的曲面法向量
surface normal vectors at division plane origins|各分割平面原点处的曲面法向量
surface normal vectors at division points|各分割点处的曲面法向量
surface with remapped {uv} domain² range|重映射 UV 二维区间后的曲面
sweep twisted boxes|扫掠扭曲盒
swept twisted boxes|扫掠扭曲盒
tapered extrusion|锥度挤出结果
thickness twisted boxes|厚度方向扭曲盒
transformation state within transform|变换的中间状态
trimmed surface (or polysurface (Brep))|修剪后的曲面或多重曲面
trimmed surface (or polysurface (Brep)) with shrunken underlying untrimmed surface|底层未修剪曲面已收缩的修剪曲面或多重曲面
trimmed twisted box set|裁剪后的扭曲盒组
twisted box connecting the set of 8 corner points|连接 8 个角点的扭曲盒
twisted box pipe array along curve|沿曲线管状扭曲盒阵列
twisted box tube array along curve|沿曲线空心管扭曲盒阵列
twisted boxes along curve|沿曲线扭曲盒
twisted boxes along the inside of the pipe-like surface|沿管状曲面内部扭曲盒
unrolled polysurface (Brep) faces|展开后的多重曲面各面
unrolled polysurface (Brep) faces or surface|展开后的多重曲面各面或曲面
voxel mesh|体素网格
{u} domain number within domain²|二维区间内的 U 数值
{v} domain number within domain²|二维区间内的 V 数值
''')
    if normalized.startswith('Resulting ') and normalized[len('Resulting '):] in result_manual:
        return result_manual[normalized[len('Resulting '):]] + '。'
    m = re.fullmatch(r'Resulting twisted box array (between|consecutively between|through|on) (curves|meshes|surfaces|mesh|surface)', normalized)
    if m:
        where = {'between': '之间', 'consecutively between': '相邻两项之间', 'through': '贯穿', 'on': '之上'}[m[1]]
        geometry = {'curves': '曲线组', 'meshes': '网格组', 'surfaces': '曲面组', 'mesh': '网格', 'surface': '曲面'}[m[2]]
        return geometry + where + '的扭曲盒阵列。'
    if normalized.startswith('Resulting numbers in y nearest to each number in x'):
        return 'y 中与各 x 值最近的数值；启用重映射 R 时，使用重映射后的 x 进行最近值查找。'
    m = re.fullmatch(r'Boolean indicating whether the point is to the (back|front) of the (mesh|plane|surface) \(also true if point is on (mesh|plane|surface)\)', normalized)
    if m:
        return '点位于' + singular_nouns[m[2]] + ('后侧' if m[1] == 'back' else '前侧') + '时为真，点在对象上时也为真。'
    if normalized.startswith('True for boolean intersection (Trim away'):
        return '真：布尔交集，移除闭合裁剪对象外部的扭曲盒；假：布尔差集，移除闭合裁剪对象内部的扭曲盒。'
    simple_boolean = pairs('''
True for 2D. False for 3D|真表示二维，假表示三维。
True if curve has kinks|曲线有折角时为真。
True if curve has more than one segment|曲线包含多个段时为真。
True if curve is a circle|曲线为圆时为真。
True if curve is an arc|曲线为圆弧时为真。
True if curve is an ellipse|曲线为椭圆时为真。
True if curve is linear|曲线为直线时为真。
True if mesh is closed|网格闭合时为真。
True if points are collinear|点组共线时为真。
True if points are coplanar|点组共面时为真。
True if polysurface (Brep) is closed|多重曲面闭合时为真。
True if surface (or polysurface (Brep)) is trimmed|曲面或多重曲面已修剪时为真。
True if surface is closed as a solid|曲面闭合形成实体时为真。
True if surface was fitted|曲面拟合成功时为真。
True if curve is closed with a seam at a corner, False if curve is opened or does not have corners|曲线闭合且接缝位于角点时为真；曲线开放或无角点时为假。
True if curve is closed with an aligned seam, False if curve is opened|曲线闭合且接缝已对齐时为真；开放曲线为假。
True if closed curve was opened, False if curve did not open or already was opened|闭合曲线成功打开时为真；未打开或原本开放时为假。
True if open curve was closed, False if curve did not close or already was closed|开放曲线成功闭合时为真；未闭合或原本闭合时为假。
True if open mesh was closed, False if mesh did not close or already was closed|开放网格成功封闭时为真；未封闭或原本闭合时为假。
True if plane was flipped, False if plane was not flipped|平面成功反转时为真，否则为假。
True if point is inside or on the twisted box, False if point is outside the twisted box|点在扭曲盒内部或表面时为真，在外部时为假。
True if curve segment was fit, False if curve segment was not fit|曲线段拟合成功时为真，否则为假。
True if curve segment was rebuilt, False if curve segment was not rebuilt|曲线段重建成功时为真，否则为假。
True if kinks were removed from curve, False if curve already had no kinks|曲线折角已去除时为真，原本无折角时为假。
True if polyline was made compatible(control point count changed), False if polyline was already compatible|多段线控制点数已调整为兼容时为真，原本兼容时为假。
True if polysurface (Brep) was flipped, False if polysurface (Brep) was not flipped or is closed|多重曲面成功反转时为真；未反转或已闭合时为假。
True if surface had kinks and was split, False if surface had no kinks and was not split|曲面有折角并被分裂时为真；无折角且未分裂时为假。
True if the mesh has naked edges, False if the mesh does not have naked edges|网格存在裸边时为真，否则为假。
True if the mesh split, False if mesh did not split|网格已分割时为真，否则为假。
True if the target length was smaller than the curve length, False if the target length was larger than the curve length|目标长度小于曲线长度时为真，大于曲线长度时为假。
True if the twisted box set was trimmed, False if the twisted box set was not trimmed|扭曲盒组已裁剪时为真，否则为假。
True for each opening in the mesh that was closed, False for each opening in the mesh that was not closed or the entire mesh already was closed|各网格开口成功封闭时为真；未封闭或网格原本闭合时为假。
True for input values on the X Axis which intersect a graph curve False for input values on the X Axis which do not intersect a graph curve|X 轴输入值与图形曲线相交时为真，否则为假。
True for input values outside of the X Axis domain bounds False for input values inside of the X Axis domain bounds|输入值超出 X 轴区间边界时为真，在边界内时为假。
True if mesh has disjoint pieces To extract each disjoint piece as a separate mesh use the input mesh with Grasshopper's Disjoint Mesh component.|网格有分离部分时为真。可将输入网格连接到 Grasshopper 的 Disjoint Mesh 组件分别提取。
True if the trimmed surface's underlying untrimmed surface shrank False if the trimmed surface's underlying untrimmed surface was already shrunk or the input surface was untrimmed|已修剪曲面的底层曲面成功收缩时为真；原本已收缩或输入为未修剪曲面时为假。
''')
    if normalized in simple_boolean:
        return simple_boolean[normalized]
    m = re.fullmatch(r'True if surface (edge|side) (\d) \((south|east|north|west)\) is (collapsed|singular)', normalized)
    if m:
        return '曲面' + ('边 ' if m[1] == 'edge' else '侧 ') + m[2] + '（' + {'south':'南','east':'东','north':'北','west':'西'}[m[3]] + '）' + ('退化' if m[4] == 'collapsed' else '存在奇点') + '时为真。'
    m = re.fullmatch(r'True if surface edge is closed in (\{[uv]\}) direction', normalized)
    if m:
        return '曲面边在 ' + m[1] + ' 方向闭合时为真。'
    m = re.fullmatch(r'True if the (.+) was intersected by the mirror cut, False if the (.+) was not intersected by the mirror cut', normalized)
    if m and m[1] == m[2]:
        subject = {'curve':'曲线','mesh':'网格','plane set':'平面组','point set':'点组','polysurface(Brep) or surface':'多重曲面或曲面','surface':'曲面'}.get(m[1])
        if subject:
            return '镜像裁剪与' + subject + '相交时为真，否则为假。'
    m = re.fullmatch(r'True if the mirror index intersected the (.+) set, False if the mirror index did not intersect the (.+) set', normalized)
    if m and m[1] == m[2]:
        subject = {**singular_nouns, 'list item':'列表项目'}.get(m[1])
        if subject:
            return '镜像索引命中' + subject + '组时为真，否则为假。'
    m = re.fullmatch(r'True if the (plane|mesh|surface|polysurface\(Brep\)|points) trimmed the (.+), False if the (.+) did not trim the (.+)', normalized)
    if m and m[1] == m[3] and m[2] == m[4]:
        subject = {**singular_nouns, 'polysurface(Brep)':'多重曲面','points':'点组'}.get(m[1])
        target = {**singular_nouns, 'plane set':'平面组','point set':'点组','twisted box set':'扭曲盒组','surface (or polysurface (Brep))':'曲面或多重曲面'}.get(m[2])
        if subject and target:
            return subject + '成功裁剪' + target + '时为真，否则为假。'
    m = re.fullmatch(r'Proportion (?:scale )?factor in the plane (\{[xyz]\}) direction \(use the same value for (.+) for (.+)\)', normalized)
    if m:
        target = {'circle':'圆','regular polygon':'正多边形','square':'正方形','regular box':'正方体','sphere':'球','uniform scaling':'等比例缩放'}.get(m[3])
        if target:
            return '平面 ' + m[1] + ' 方向的比例因子。要得到' + target + '，各方向应使用相同值。'
    if normalized.startswith('Number of recursive') and 'WARNING:' in normalized or normalized.startswith('Number of subdividing iterations for the twisted box'):
        return '递归或细分的步数。警告：结果数量可能指数增长，步数大于 3 时可能产生大量网格面或扭曲盒，执行前请保存文件以防程序无响应。'
    if normalized.startswith('Number of '):
        counts = pairs('''
curve control points|曲线控制点
curve edit points|曲线编辑点
curve kink points|曲线折角点
curve knot vectors|曲线节点向量
curve segments|曲线段
curve spans|曲线跨度
disjoint mesh pieces|分离网格部分
divisions per segment|每个曲线段的分割
mesh colors|网格顶点颜色
mesh edge loop divisions per side of the mesh connection|网格连接各侧的环边分割
mesh faces|网格面
mesh faces per side of the mesh connection|网格连接各侧的面
mesh vertices|网格顶点
quad mesh faces|四边网格面
recursive smoothing steps|递归平滑步骤
recursive subdivision steps|递归细分步骤
recursive transformation steps|递归变换步骤
sides of the polygon|多边形边
steps in the range|范围内步骤
surface or polysurface (Brep) control points|曲面或多重曲面控制点
surface or polysurface (Brep) edges|曲面或多重曲面边
surface or polysurface (Brep) faces|曲面或多重曲面面
surface or polysurface (Brep) vertices|曲面或多重曲面顶点
triangle mesh faces|三角网格面
trimmed surface or polysurface (Brep) faces|曲面或多重曲面的已修剪面
untrimmed surface or polysurface (Brep) faces|曲面或多重曲面的未修剪面
''')
        subject = normalized[len('Number of '):]
        if subject in counts:
            return counts[subject] + '数量。'
        m = re.fullmatch(r'(edit points along the surface|net curves in the|net waves in the) (\{[uv]\}) direction', subject)
        if m:
            return m[2] + ' 方向的' + {'edit points along the surface':'曲面编辑点','net curves in the':'网状曲线','net waves in the':'网状波浪'}[m[1]] + '数量。'
    if normalized.startswith('Determines how') or normalized.startswith('Determines what type of') or normalized.startswith('If the curve has kinks, determines how'):
        split = re.search(r'0\s*=', normalized)
        if split:
            heading = normalized[:split.start()].strip()
            headings = pairs('''
Determines how kinks are blended|折角混合连接方式
Determines how mesh vertex colors are blended|网格顶点颜色混合方式
Determines how mesh vertex colors are tweened|网格顶点颜色补间方式
Determines how much of the trimmed twisted box set to keep|裁剪后扭曲盒的保留判定
Determines how the color set is mirrored|颜色组镜像方式
Determines how the corners are made on outward tapering extrusions|向外锥度挤出的角点方式
Determines how the curve is closed|曲线闭合方式
Determines how the domain set is mirrored|区间组镜像方式
Determines how the domain² set is mirrored|二维区间组镜像方式
Determines how the end of the curve is preserved|曲线末端保留方式
Determines how the mesh is trimmed|网格裁剪方式
Determines how the mirror cut curves are connected|镜像裁剪曲线连接方式
Determines how the mirror cut meshes are connected|镜像裁剪网格连接方式
Determines how the mirror cut polysurfaces(Breps) or surfaces are connected|镜像裁剪多重曲面或曲面连接方式
Determines how the mirror cut surfaces are connected|镜像裁剪曲面连接方式
Determines how the number is rounded|数值舍入方式
Determines how the number set is mirrored|数值组镜像方式
Determines how the section curves are lofted|截面曲线放样方式
Determines how the start of the curve is preserved|曲线起点保留方式
Determines how the tween path is interpolated|补间路径插值方式
Determines how the vector set is mirrored|向量组镜像方式
Determines how the vector star is subdivided|星形向量细分方式
Determines how the vertex blend paths are interpolated|顶点混合路径插值方式
Determines how the {u} interpolation path is interpolated|U 插值路径类型
Determines how the {w} interpolation path is interpolated|W 插值路径类型
Determines how to cap the curve ends|曲线端点封闭方式
Determines how to end the pipe mesh|管状网格末端方式
Determines what type of curve to get|获取的曲线类型
If the curve has kinks, determines how they are offset|曲线折角偏移方式
''')
            if heading in headings:
                options = normalized[split.start():]
                if 'Complete (keep if twisted box is' in options:
                    return headings[heading] + '：0 完全位于保留侧；1 至少一半位于保留侧（最快）；2 至少部分位于保留侧。'
                translated = port_pattern.sub(lambda m: port_lookup[m[0].casefold()], options)
                translated = re.sub(r'(?<!^)(?<!\n)(\d+\s*=)', r'\n\1', translated).replace('反射镜像 1 = 取反', '反射镜像\n1 = 反向')
                if not re.search(r'[A-Za-z]{2,}', translated):
                    return headings[heading] + '：\n' + translated
    m = re.fullmatch(r'(?:Degree|Domain|Approximate length|Parameter) in (\{[uv]\}) direction of each span(?: isocurve)?(?: that)? makes up the surface', normalized)
    if m:
        return '各曲面跨度在 ' + m[1] + ' 方向的' + {'Degree':'次数','Domain':'区间','Approximate':'近似长度','Parameter':'等参线参数'}[normalized.split()[0]] + '。'
    m = re.fullmatch(r'(Degree|Domain|Approximate length) in (\{[uv]\}) direction of each span that makes up the surface', normalized)
    if m:
        return '各曲面跨度在 ' + m[2] + ' 方向的' + {'Degree':'次数','Domain':'区间','Approximate length':'近似长度'}[m[1]] + '。'
    if normalized.startswith('Degree of each segment'):
        return '各曲线段的次数。'
    if normalized == 'Degree of each span that makes up the curve':
        return '各曲线跨度的次数。'
    if normalized.startswith(('Degree of surface ', 'Degree to fit the surface ', 'Degree value of the surface in the ')):
        variable = re.search(r'\{[uv]\}', normalized)
        if variable:
            return '曲面 ' + variable[0] + ' 方向的次数。' + ('省略时使用输入曲面的对应次数。' if 'omitted' in normalized else '')
    if normalized.startswith(('Degree to fit the searched segments to', 'Degree to rebuild the searched segments to')):
        return '匹配曲线段的目标次数，省略时使用输入各段的次数。'
    m = re.fullmatch(r'Rail curve that the (first|second|third|fourth|fifth|sixth|seventh|eighth) and (first|second|third|fourth|fifth|sixth|seventh|eighth|eigth) corners of the twisted boxes are on', normalized)
    if m:
        numbers = {'first':'一','second':'二','third':'三','fourth':'四','fifth':'五','sixth':'六','seventh':'七','eighth':'八','eigth':'八'}
        return '扭曲盒第' + numbers[m[1]] + '与第' + numbers[m[2]] + '角点所在的轨道曲线。'
    m = re.fullmatch(r'Size (?:of|in).*?(\{[xyz]\}).*', normalized)
    if m:
        return m[1] + ' 方向的' + ('体素尺寸；使用负值可省略该方向的网格面。' if 'voxels' in normalized else '扭曲盒尺寸。')
    m = re.fullmatch(r'Domain (?:of|size of).*?(\{[xyz]\}).*', normalized)
    if m:
        return '扭曲盒 ' + m[1] + ' 方向尺寸区间。'
    if normalized.startswith('The original '):
        variable = ''.join(dict.fromkeys(re.findall(r'\{[tuvwxyz]+\}', normalized)))
        if 'length (amplitude)' in normalized:
            return '输入向量组的原始长度范围。'
        if 'start value' in normalized or 'end value' in normalized:
            return '输入区间组 ' + variable + ' 方向的原始' + ('起始' if 'start value' in normalized else '结束') + '值范围。'
        if 'domain' in normalized:
            target = '点组坐标' if 'points' in normalized else '数值组' if 'numbers' in normalized else '曲面' if 'surface' in normalized else '曲线'
            return target + ' ' + variable + ' 原始区间范围。'
    m = re.fullmatch(r'Angle between the reference planes (\{[xyz]\}) axis and closest target planes (\{[xyz]\}) axis in radians', normalized)
    if m:
        return '参考平面与最近目标平面 ' + m[1] + ' 轴的夹角，单位为弧度。'
    m = re.fullmatch(r'Collection of weights for each of the domain²s (\{[uv]\}) domains', normalized)
    if m:
        return '各二维区间 ' + m[1] + ' 方向区间的权重。'
    m = re.fullmatch(r'(Distance between the point and|Side of) (mesh|plane|surface).*', normalized)
    if m:
        subject = {'mesh':'网格','plane':'平面','surface':'曲面'}[m[2]]
        return '点相对' + subject + '的' + ('有符号距离：负值在后侧，正值在前侧。' if m[1] == 'Distance between the point and' else '侧别：-1 后侧，0 在对象上，1 前侧。')
    m = re.fullmatch(r'Domain of surface (\{[uv]\}) direction \(if omitted input surface (\{[uv]\}) domain is used\)', normalized)
    if m:
        return '曲面 ' + m[1] + ' 方向区间，省略时使用输入曲面的对应区间。'
    m = re.fullmatch(r'Edge curve that defines the sum surface (\{[uv]\}) edges', normalized)
    if m:
        return '定义和曲面 ' + m[1] + ' 方向边的曲线。'
    m = re.fullmatch(r'Number which will be the negative and positive (\{[uv]\}) extents of the domain² from zero', normalized)
    if m:
        return '二维区间 ' + m[1] + ' 方向从零向正负方向延伸的范围值。'
    m = re.fullmatch(r'Parameter along (rectangle|surface) (\{[xyuv]\}) domain .*', normalized)
    if m:
        return ('矩形' if m[1] == 'rectangle' else '曲面') + ' ' + m[2] + ' 方向参数，0 起始、1 结束。'
    if normalized.startswith('Slide factor'):
        variable = ''.join(dict.fromkeys(re.findall(r'\{[uv]\}', normalized)))
        return variable + ' 滑动因子，0 对应起始状态，1 对应结束状态。'
    if normalized.startswith('Transformation that will be used to transform the geometry at each recursive step'):
        return '每步递归使用的变换，可连接移动、缩放、旋转等组件的 X 输出。多个变换可先用河豚复合变换或 Grasshopper 的 Compound 合并。警告：递归缩放可能迅速产生极大或极小几何，导致无响应。'
    grouped = {
        'Twisted Box for volume computation': '用于计算体积的扭曲盒。',
        'Twisted Box to deconstruct': '待解构扭曲盒。', 'Twisted Box to deform': '待变形扭曲盒。',
        'Twisted Box to evaluate': '待求值扭曲盒。', 'Twisted Box to find center point (average) of': '用于求平均中心点的扭曲盒。',
        'Twisted Box to get corners of': '用于获取角点的扭曲盒。', 'Twisted Box to subdivide': '待细分扭曲盒。',
        'Twisted Box to thicken': '待加厚扭曲盒。', 'Twisted Box to transform': '待变换扭曲盒。',
        'Twisted Boxes for averaging': '用于求平均的扭曲盒组。', 'Surface to apply net on': '用于生成曲线网的曲面。',
        'Surface to change directions of': '待改变方向的曲面。', 'Surface to create twisted box array from': '扭曲盒阵列的起始曲面。',
        'Surface to create twisted box array on': '用于生成扭曲盒阵列的曲面。', 'Surface to create twisted box array to': '扭曲盒阵列的目标曲面。',
        'Surface to create twisted boxes from': '扭曲盒的起始曲面。', 'Surface to create twisted boxes to': '扭曲盒的目标曲面。',
        'Surface to determine on which side the point is located': '用于判断点所在侧别的曲面。',
        'Surface to divide as mesh': '需要划分为网格的曲面。', 'Surface to find the closest edge to point of': '用于查找点的最近边的曲面。',
        'Surface to get isocurve of': '用于获取等参线的曲面。', 'Surface to get span information of': '用于获取跨度信息的曲面。',
        'Surface to get the edit points of': '用于获取编辑点的曲面。', 'Surface to get the {u} and {v} degree value of': '用于获取 UV 次数的曲面。',
        'Surface to locate plane on': '用于定位平面的曲面。', 'Surface to locate point on': '用于定位点的曲面。',
        'Surface to mirror cut': '待镜像裁剪曲面。', 'Surface to offset curve away from': '曲线偏移所参考的曲面。',
        'Surface to remap the {uv} domain² range of': '需要重映射 UV 二维区间的曲面。',
        'Surface to split at kinks into a polysurface(Brep)': '需要按折角分裂为多重曲面的曲面。',
        'Surface to test for collapsed edges': '用于检测边退化的曲面。', 'Surface to test for singular sides': '用于检测侧边奇点的曲面。',
        'Surface to test if it is closed': '用于检测闭合状态的曲面。', 'Surface to trim with': '用于裁剪的曲面。',
        'Surface to tween curve on': '用于在其上补间曲线的曲面。', 'Surface to tween curves on': '用于在其上补间曲线组的曲面。',
        'Surface to tween plane on': '用于在其上补间平面的曲面。', 'Surface to tween planes on': '用于在其上补间平面组的曲面。',
        'Surface to tween point on': '用于在其上补间点的曲面。', 'Surface to tween points on': '用于在其上补间点组的曲面。',
        'Surfaces for averaging': '用于求平均的曲面组。', 'Size of the graph labels': '图形标签文字大小。'
    }
    if normalized in grouped:
        return grouped[normalized]
    m = re.fullmatch(r'(Curve|Plane|Point|Surface) (on surface|on curve|along guide curve) to tween (from|to)', normalized)
    if m:
        return ('起始' if m[3] == 'from' else '目标') + singular_nouns[m[1].lower()] + '，' + {'on surface':'在曲面上','on curve':'在曲线上','along guide curve':'沿引导曲线'}[m[2]] + '补间。'
    m = re.fullmatch(r'(Surface|Mesh|Curve) to (?:tween|blend) (from|to)', normalized)
    if m:
        return ('起始' if m[2] == 'from' else '目标') + singular_nouns[m[1].lower()] + '。'
    m = re.fullmatch(r'Set of (curves|planes|points) (along guide curve|on surface|on curve) to tween (between|through)', normalized)
    if m:
        return '用于' + ('贯穿补间' if m[3] == 'through' else '补间') + '的' + {'along guide curve':'沿引导曲线','on surface':'曲面上','on curve':'曲线上'}[m[2]] + nouns[m[1]] + '组。'
    m = re.fullmatch(r'Set of (curves|meshes|surfaces) to create twisted box array (between|through)', normalized)
    if m:
        return '用于' + ('贯穿生成' if m[2] == 'through' else '在相邻项之间生成') + '扭曲盒阵列的' + nouns[m[1]] + '组。'
    m = re.fullmatch(r'Set of (meshes|numbers|points|polylines) to (blend between|blend through|linearize|mass divide|mass subtract|round|split into odd and even numbers|fit rectangle through|pinch & spread|test for collinearity|test for coplanarity|voxelize as mesh|make compatible)', normalized)
    if m:
        actions = {'blend between':'逐顶点混合','blend through':'贯穿混合','linearize':'线性化','mass divide':'连续除法','mass subtract':'连续减法','round':'舍入','split into odd and even numbers':'分成奇偶两组','fit rectangle through':'拟合矩形','pinch & spread':'收拢与扩散','test for collinearity':'共线检测','test for coplanarity':'共面检测','voxelize as mesh':'网格体素化','make compatible':'控制点兼容处理'}
        return '用于' + actions[m[2]] + '的' + {**nouns,'polylines':'多段线'}[m[1]] + '组。'
    if normalized.startswith('Optional Refit method.'):
        return '可选重新拟合方法（假：关闭；真：开启）。依据曲率重分布和增减控制点，保持形状并生成较紧致的滑动曲线。'
    if normalized.startswith('Optional Sample Point method.'):
        return '可选点采样方法（0 或未输入：关闭；正整数：启用并指定点数）。按点数等距划分曲线并重建控制点，得到较松散的滑动曲线和均匀控制点分布。'
    if normalized.startswith('If False, the rules for {'):
        variable = re.search(r'\{[uw]\}', normalized)[0]
        return '归一化为假时，' + variable + ' 参数使用 0 到末项索引范围；参数应按数值顺序排列且不重复。'
    if normalized.startswith('Join the mirror combined') or normalized.startswith('Join the mirror cut'):
        return '连接镜像结果，并移除组中间的重复项目。'
    if normalized.startswith('Keep the ') and 'mirror it normally if it is mirror cut into non-existence' in normalized:
        return '若镜像裁剪导致对象消失，则保留原对象并执行普通镜像。'
    if normalized.startswith('Index that the kept side of'):
        return '保留侧进行镜像所依据的索引。负索引将反转项目组并从另一端裁剪。'
    if normalized.startswith('Distance to offset the kept'):
        return '保留对象相对镜像平面的偏移距离；作用距离非零时，从作用距离边界开始偏移。'
    if (normalized.startswith('Parts of ') or normalized.startswith('Planes within ') or normalized.startswith('Points within ')) and 'will be additionally cut away' in normalized:
        return '位于距镜像平面该距离内的对象部分也将移除。'
    if normalized.startswith('Plane that the kept side of'):
        return '裁剪后保留对象所使用的镜像平面。'
    if normalized.startswith('Blend factors,'):
        return '逐顶点混合因子，每个因子对应网格中相同索引的顶点；0 和 1 分别对应起始与结束网格，相邻模式对应当前与下一网格。贯穿模式可切换归一化范围。'
    if normalized.startswith('Bulge factor for the mirror cut'):
        return '镜像裁剪连接的凸度因子：负 B 为负凸度，0 为无凸度，正 B 为正凸度。'
    if normalized.startswith('Closed loft,'):
        return '为真时，最后一个截面重新连接首截面形成闭合放样。' + ('也可连接指定起点或终点。' if 'optional start or end point' in normalized else '')
    if normalized.startswith('Closed strips,'):
        return '为真时，最后一条轨道曲线通过扭曲盒回接第一条轨道，形成闭合条带。'
    if normalized.startswith('Control point count '):
        variable = ''.join(dict.fromkeys(re.findall(r'\{[uv]\}', normalized)))
        return variable + ' 方向或匹配曲线段重建的控制点数；省略时使用对应输入的控制点数。'
    if normalized.startswith('Curvature degree of'):
        return '插值或混合路径的次数，应为正奇数。'
    m = re.fullmatch(r'Plane (\{[xyz]\}) dimension of the (.+)', normalized)
    if m:
        return '对象沿平面 ' + m[1] + ' 方向的尺寸。'
    m = re.fullmatch(r'(Reparameterize|Reparametrize) the (domain²|point) sets (\{[xyzuv]\}) (end values|start values|coordinates)', normalized)
    if m:
        return '重新参数化' + ('二维区间组' if m[2] == 'domain²' else '点组') + '的 ' + m[3] + {'end values':'结束值','start values':'起始值','coordinates':'坐标'}[m[4]] + '。'
    if normalized.startswith('The angle in degrees to rotate around axis '):
        return '绕轴 ' + re.search(r'axis (\d)', normalized)[1] + ' 的旋转角度，单位为度。'
    if normalized.startswith('The plane after the rotation around axis '):
        return '绕轴 ' + re.search(r'axis (\d)', normalized)[1] + ' 旋转后的平面。' + ('该轴来自初始基础平面。' if 'initial base plane' in normalized else '该轴来自前一步旋转后的平面。')
    if normalized.startswith('The ') and 'plane axis to rotate around, derived from' in normalized:
        ordinal = {'first':'一','second':'二','third':'三'}[normalized.split()[1]]
        return '第' + ordinal + '个旋转轴：0 为 X，1 为 Y，2 为 Z。' + ('各轴来自初始基础平面。' if 'inital base plane' in normalized else '各轴来自前一步旋转后的平面。')
    if normalized.startswith('Superimpose the '):
        variable = ''.join(dict.fromkeys(re.findall(r'\{[uv]\}', normalized)))
        prop = '控制点数量' if 'control points' in normalized else '次数' if 'degree' in normalized else '参数区间' if 'domain' in normalized else '修剪边界'
        return '将参考几何的 ' + variable + prop + '套用到目标几何。'
    if normalized.startswith('A list of rotations'):
        variable = ''.join(dict.fromkeys(re.findall(r'\{[tu]\}', normalized)))
        result = '各 ' + variable + ' 分割位置处的旋转角列表，单位为度。'
        result += '绕扭曲盒中心旋转。' if 'twisted box centers' in normalized else '绕直径或半径中心旋转。' if 'diameter centers' in normalized or 'radii centers' in normalized else '绕引导曲线旋转。'
        if 'centered on the curve' in normalized:
            result += '阵列居中于曲线时，与旋转 1 的效果相同。'
        return result
    if normalized.startswith('A list of thicknesses'):
        return '各分割参数或递归步骤对应的厚度列表，从外径或外半径角点向内偏移；网格形变时作为偏移高度。'
    if normalized.startswith('A list of domain sizes for the twisted box curve'):
        return '各 {t} 分割位置处扭曲盒曲线的 ' + re.search(r'\{[xy]\}', normalized)[0] + ' 尺寸区间列表。'
    if normalized.startswith('A list of domain defined offset'):
        return '各分割参数位置的偏移位置区间列表，相对于引导曲线；0 到 0 表示居中于曲线。'
    if normalized.startswith('A list of mesh geometries to morph'):
        return '每个递归形变步骤对应一个网格。建议使用低面数网格并平滑最终结果。'
    if normalized.startswith('A list of reference boxes to morph from'):
        return '每个递归形变步骤对应一个参考盒，通常为该步网格的包围盒。'
    if normalized.startswith('Division parameter along pipe-like surface {v} domain that'):
        digits = {'first and fifth':('1、5','最小参数值'), 'fourth and eigth':('4、8','最大参数值'), 'second and sixth':('2、6','介于 v1 与 v3'), 'third and seventh':('3、7','介于 v2 与 v4')}
        for key, (corners, rule) in digits.items():
            if key in normalized:
                return '管状曲面的 {v} 参数，用于角点 ' + corners + ' 所在位置；0 到 1 对应起止，建议取' + rule + '。'
    if normalized.startswith('Tween factor') and 'The tween factor range from one' in normalized:
        return '补间因子使用列表索引：0 对应首项，末项索引对应末项；相邻整数索引之间生成对应对象的补间。例如 2.5 位于索引 2 与 3 的一半位置。启用归一化时使用 0 到 1 范围。'
    if normalized.startswith('Tween factor'):
        payload = normalized[len('Tween factor'):]
        for key, value in {**nouns, **singular_nouns, 'start': '起始', 'end': '结束', 'at': '位于', 'index': '索引', 'unless': '除非', 'Normalized': '归一化', 'False': '假', 'True': '真'}.items():
            payload = re.sub(r'(?<![A-Za-z])' + re.escape(key) + r'(?![A-Za-z])', value, payload, flags=re.I)
        payload = payload.replace(' is ', '为').replace(' to ', '到')
        if re.search(r'[A-Za-z]{2,}', payload):
            tokens = re.findall(r'[A-Za-z]{2,}', payload)
            if all(token in {'Cl', 'Pl', 'TB'} for token in tokens):
                return '补间因子' + payload + '。'
        if not re.search(r'[A-Za-z]{2,}', payload):
            return '补间因子' + payload + '。'
    if normalized.startswith('If False, the rules for factor are'):
        variables = ''.join(dict.fromkeys(re.findall(r'\{[uvwtxzy]+\}', normalized)))
        return '归一化为假时，补间因子' + variables + '使用列表索引范围：0 对应首项，最后一个索引对应末项；相邻整数索引之间生成对应两项的补间。例如因子 2.5 位于索引 2 和 3 对象之间的一半位置。'
    if normalized.startswith('Optional Refit match method.'):
        return '可选的重新拟合匹配方法（假：关闭；真：开启）。可行时依据曲率重新分布、增减控制点并保持形状，生成较紧致的结果和按曲率分布的控制点。'
    if normalized.startswith('Optional Point Sample match method.'):
        return '可选的点采样匹配方法（未输入整数或 0：关闭；正整数：开启并指定采样点数）。通过按点数等分曲线重新生成控制点，得到较松散的形状和均匀控制点分布。'
    if normalized.startswith('Optional Sample Point match method.'):
        return '可选的采样点匹配方法。输入正整数可启用采样并指定点数，沿曲线等距重建控制点；0 或未输入时关闭。'
    if normalized.startswith('If True, tween distribution is evaluated'):
        result = '为真时，补间分布依据输入对象的整体两端范围求值，不考虑中间各对象的位置。'
        if 'along the curve' in normalized:
            result = '为真时，沿曲线按输入对象的整体两端范围求补间分布，不考虑中间对象的位置。'
        if 'on the surface' in normalized:
            result = '为真时，在曲面上按输入对象的整体两端范围求补间分布，不考虑中间对象的位置。'
        return result
    if normalized.startswith('Division parameters along') or normalized.startswith('Division parameter along'):
        head = normalized.split('(', 1)[0].strip()
        location = head.split(' along ', 1)[1]
        extras = {
            'each rail curves': '各轨道曲线', "rail curve one's": '轨道曲线一', "rail curve two's": '轨道曲线二', "rail curve three's": '轨道曲线三', "rail curve four's": '轨道曲线四',
            'profile curve': '截面曲线', 'section curves': '截面曲线组', 'the curves': '曲线', 'the extrusion': '挤出',
            'curve': '曲线', 'rail curve': '轨道曲线', 'rail curves': '轨道曲线组',
            'pipe-like surface': '管状曲面', 'surface': '曲面', 'rectangle': '矩形', 'thickness': '厚度',
            'the box': '盒', 'box': '盒', 'extrusion direction': '挤出方向', 'at parameter': '在参数', 'at paramater': '在参数',
            'for curves flowing in the rectangle {y} direction, use one parameter value to make a rectangle isocurve': '生成 Y 方向曲线；单个参数生成等参线',
            'for curves flowing in the rectangle {x} direction, use one parameter value to make a rectangle isocurve': '生成 X 方向曲线；单个参数生成等参线',
            'for curves flowing in the surface {v} direction, use one parameter value to make a surface isocurve': '生成 V 方向曲线；单个参数生成等参线',
            'for curves flowing in the surface {u} direction, use one parameter value to make a surface isocurve': '生成 U 方向曲线；单个参数生成等参线',
            'for mesh faces': '用于网格面', 'domains': '区间', 'domain': '区间', 'for each': '对应每个',
            'parameter': '参数', 'mesh face': '网格面'
        }
        for key in sorted(extras, key=len, reverse=True):
            location = re.sub(r'(?<![A-Za-z])' + re.escape(key) + r'(?![A-Za-z])', extras[key], location)
        if not re.search(r'[A-Za-z]{2,}', location):
            note = '沿' + location.replace(' ', '') + '的分割参数，0 和 1 分别对应起点与终点。'
            if 'length' in normalized or 'angle' in normalized:
                note += '沿曲线挤出时，若启用按长度或角度细分，则使用对应细分方式。'
            if 'For best results' in normalized:
                note += '建议参数位于 0 到 1、按数值顺序排列且不重复。'
            if 'same amount' in normalized:
                note += '各参数列表的数量应保持一致。'
            return note
    if normalized.startswith(('Division parameters between', 'Division parameters through', 'Division parameters around', 'Division parameters for layers')):
        variable = ''.join(dict.fromkeys(re.findall(r'\{[tuvw]\}', normalized)))
        target = '曲线' if 'curves' in normalized or 'curve' in normalized else '网格' if 'meshes' in normalized or 'mesh' in normalized else '曲面' if 'surface' in normalized else '厚度层'
        result = target + ' ' + variable + ' 方向的分割参数。'
        if 'Index number of last' in normalized:
            result += '未归一化时使用 0 到末项索引范围；归一化时使用 0 到 1。'
        elif 'at C +1' in normalized or 'at M +1' in normalized or 'at S +1' in normalized:
            result += '0 对应当前项，1 对应下一项。'
        else:
            result += '0 和 1 分别对应起始与结束位置。'
        if 'For best results' in normalized:
            result += '参数应按数值顺序排列且不重复。'
        return result
    if normalized.startswith('If True, allow the ') and 'from the end back to the start as a closed loop' in normalized:
        result = '为真时，允许插值或补间路径从末端回到起点，形成闭合循环。'
        if 'increase' in normalized:
            result += '归一化为假时，因子或分割参数范围的最大值增加 1。'
        return result
    if normalized.startswith('If True, use a normalized tween factor'):
        return '为真时使用归一化补间因子：0 对应首项，1 对应末项。'
    if normalized.startswith('If True, use normalized {w} division parameters'):
        return '为真时使用归一化 {w} 分割参数：0 对应首项，1 对应末项。'
    if normalized.startswith('If True, parameters') and 'weighted by' in normalized:
        variable = ''.join(dict.fromkeys(re.findall(r'\{[tuvw]\}', normalized)))
        return '为真时，依据输入几何或插值路径的曲率，对 ' + variable + ' 参数分布加权。' + ('仅当挤出方向使用曲线时有效。' if 'extrusion direction' in normalized else '')
    if normalized.startswith('If True, tween distribution is weighted by'):
        return '为真时，依据输入对象及补间路径的曲率对补间分布加权。'
    if normalized.startswith('If True, blend distribution is weighted by'):
        return '为真时，依据输入网格顶点和顶点混合路径的曲率对混合分布加权。'
    if normalized.startswith('If True, blend distribution is evaluated along'):
        return '为真时，沿顶点混合路径求混合分布，不考虑中间输入网格顶点的位置。'
    if normalized.startswith('If True, parameters') and 'distribution is evaluated along the interpolation path' in normalized:
        return '为真时，沿插值路径求参数分布，不考虑中间输入对象的位置。'
    if normalized.startswith('If Angle is not 0.0,'):
        variable = '{v}' if 'instead of the {v} parameters' in normalized else '{u}'
        return '角度不为零时，依据曲线角度精度（度）划分网格面，替代 ' + variable + ' 分割参数，以适应曲率变化。' + ('仅当挤出方向为曲线时有效。' if 'extrusion direction' in normalized else '')
    if normalized.startswith('If True,') and 'mesh face divisions are defined by the lengths between' in normalized:
        return '为真时，按曲线控制点之间的长度划分网格面，替代 {u} 参数，以适应多段线的各个段。'
    if normalized.startswith('If True, the parameters') and 'normalized lengths' in normalized:
        variable = ''.join(dict.fromkeys(re.findall(r'\{[tu]\}', normalized)))
        return '为真时，' + variable + ' 输入表示归一化长度（0.5 为长度中点）；为假时表示曲线或挤出参数（0.5 为区间中点）。'
    conditions = {
        'If True, create a solid offset': '为真时生成实体偏移。',
        'If True, the domain is increasing (negative to positive) If False, the domain is decreasing (positive to negative)': '真：区间递增（负值到正值）；假：区间递减（正值到负值）。',
        'If True, the domain² is increasing (negative to positive) If False, the domain² is decreasing (positive to negative)': '真：二维区间递增（负值到正值）；假：二维区间递减（正值到负值）。',
        'If True, one overall bounding rectangle is made for all input geometry If False, each input geometry gets its own separate bounding rectangle': '真：为所有输入几何生成联合包围矩形；假：为每个对象分别生成包围矩形。',
        'If True, only the last step of the recursive transform is calculated and output. If False, every step of the recursive transform is calculated and output.': '真：只计算和输出递归变换的最后一步；假：计算和输出全部步骤。',
        'If True, the curves domain middle will be evaluated. If False, the curves length middle will be evaluated.': '真：求曲线参数区间中点；假：求曲线长度中点。',
        'If True, the length input is used as normalized length (0.5 = Curve middle).If False, the length input is used as actual length (Curve length/2 = Curve middle).': '真：输入为归一化长度（0.5 为曲线中点）；假：输入为实际长度（总长度的一半为曲线中点）。',
        'If curve has corners, snap the aligned seam to the closest corner': '曲线有角点时，将对齐接缝吸附到最近角点。',
        'If curve has corners, snap the aligned seam to the closest corner or kink': '曲线有角点时，将对齐接缝吸附到最近角点或折角。',
        'If the curve is closed, include the end point (point that is duplicate with the start point)': '曲线闭合时，包含与起点重复的终点。',
        'If true, the length output is normalized (0.0 - 1.0)': '为真时，输出长度归一化为 0 到 1。',
        'If true, the lengths output is normalized (0.0 - 1.0)': '为真时，输出长度归一化为 0 到 1。',
        'If true, mesh will reduce to reach the desired face count If false, mesh will reduce only until the point at which the mesh shape would be required to change': '真：简化到目标面数；假：仅简化到不必改变网格形状的限度。',
        'If true, triangle faces will be converted into trimmed triangle surfaces If false, triangle faces will be converted into untrimmed surfaces where the first and fourth corner points overlap': '真：三角面转换为已修剪三角曲面；假：转换为首尾角点重合的未修剪曲面。'
    }
    if normalized in conditions:
        return conditions[normalized]
    if normalized.startswith('If True, each curves seam is aligned'):
        return '真：依次将每条曲线接缝对齐到前一条已调整接缝；假：直接对齐到首条曲线或引导起点。'
    if normalized.startswith('If True, get isocurve flowing in'):
        return '真：取 ' + ('矩形 X' if 'rectangle' in normalized else '曲面 U') + ' 方向等参线；假：取 ' + ('矩形 Y' if 'rectangle' in normalized else '曲面 V') + ' 方向等参线。'
    if normalized.startswith(('If True, only the edit points', 'If true, only the edit points')):
        return '真：仅提取节点或跨度末端的编辑点，即插值几何经过的点；假：提取全部编辑点。'
    for prefix, (start, endings) in prefix_templates.items():
        if not normalized.startswith(prefix):
            continue
        rest = normalized[len(prefix):]
        for noun, translation in nouns.items():
            if rest.startswith(noun) and rest[len(noun):] in endings:
                return start + translation + endings[rest[len(noun):]] + '。'
    m = re.fullmatch(r'Amount of spans in the (\{[uv]\}) direction that make up the surface', normalized)
    if m:
        return '组成曲面的 ' + m[1] + ' 方向跨度数量。'
    m = re.fullmatch(r'A list of (outer diameters|outer radii|sizes) for the twisted box (pipe array|tube array|curve \{[xy]\} dimensions) at every (?:division parameter (\{[ut]\})|(\{[ut]\}) division parameter)', normalized)
    if m:
        value = {'outer diameters': '外径', 'outer radii': '外半径', 'sizes': '尺寸'}[m[1]]
        target = {'pipe array': '圆管阵列', 'tube array': '空心管阵列', 'curve {x} dimensions': '曲线 X 方向', 'curve {y} dimensions': '曲线 Y 方向'}[m[2]]
        return '各 ' + (m[3] or m[4]) + ' 分割参数处扭曲盒' + target + '的' + value + '列表。'
    m = re.fullmatch(r'The original (start|end) value range of the set of (.+)', normalized)
    if m and m[2] in nouns:
        return nouns[m[2]] + '组的原始' + ('起始' if m[1] == 'start' else '结束') + '值范围。'
    m = re.fullmatch(r'The splitting index \(only if Join is false\) To split the (.+) at the mirror use this as the index input on Grasshopper\'s Split List component\.', normalized)
    if m:
        return '连接为假时有效的分割索引；若要在镜像处拆分结果列表，可将其输入 Grasshopper 的“分割列表”组件。'
    if normalized.startswith('0 = '):
        translated = port_pattern.sub(lambda m: port_lookup[m[0].casefold()], text)
        if not re.search(r'[A-Za-z]{2,}', translated):
            return translated
    return None


runtime_manual = pairs('''
North|北
South|南
East|东
West|西
X Axis - Input Values|X 轴 - 输入数值
Y Axis - Mapped Values|Y 轴 - 映射数值
Area cannot be calculated for this type of geometry|此几何类型无法计算面积。
Area cannot be less than or equal to zero|面积必须大于零。
Volume cannot be calculated for this type of geometry|此几何类型无法计算体积。
Volume cannot be less than or equal to zero|体积必须大于零。
Length cannot be calculated|无法计算长度。
Length cannot be less than or equal to zero|长度必须大于零。
Cannot cap extrusion of an open profile curve.|无法封闭开放截面曲线的挤出末端。
Cannot create closed loft.|无法创建闭合放样。
Cannot cut one plane.|无法仅对一个平面执行裁剪。
Cannot cut one point.|无法仅对一个点执行裁剪。
Cannot extrude zero length.|无法按零长度挤出。
Cannot flip closed Polysurfaces(Breps).|无法反转闭合多重曲面。
Cannot loft with one section|无法仅用一个截面放样。
Cannot loft with one section curve|无法仅用一条截面曲线放样。
Cannot loft with one section curve and no start or end point|仅有一条截面曲线且未提供起点或终点，无法放样。
Cannot trim one twisted box.|无法仅对一个扭曲盒执行裁剪。
Collinearity test requires atleast 2 non-duplicate points|共线检测至少需要两个不重复点。
coplanarity test requires atleast 2 non-duplicate points|共面检测至少需要两个不重复点。
Curve could not convert to arc, circle, or ellipse. Try adjusting the tolerance|曲线无法转换为圆弧、圆或椭圆，请尝试调整容差。
Curve does not have corners so the seam will not be adjusted.|曲线无角点，接缝不作调整。
Curve end could not be relocated.|无法重定位曲线终点。
Curve start could not be relocated.|无法重定位曲线起点。
Curve has no segments, if you want to fit it use Fit Curve component.|曲线无分段，请使用“拟合曲线”组件进行拟合。
Curve has no segments, if you want to rebuild it use Rebuild Curve component.|曲线无分段，请使用“重建曲线”组件进行重建。
Curve is already closed.|曲线已闭合。
Curve is linear, it cannot be closed.|曲线为直线，无法闭合。
Curve is open, open curves do not have a seam so it will not be adjusted.|曲线开放，没有接缝，不作调整。
Curve must be a polyline, try converting it to a polyline with Grasshopper's Curve To Polyline component.|输入必须是多段线，可使用 Grasshopper“曲线转多段线”组件转换。
Curve must be closed for area calculation|计算面积需要闭合曲线。
Curve must be planar for area calculation|计算面积需要平面曲线。
Curve set includes open curves, open curves do not have a seam so they will not be adjusted.|曲线组含开放曲线；开放曲线无接缝，不作调整。
Curve was scaled into non existance|曲线缩放后退化或消失。
Geometry was scaled into non existance|几何对象缩放后退化或消失。
Curves could not be auto sorted, try sorting your curves into A, B, C, and D edges and using Grasshopper's Edge Surface component.|曲线无法自动排序，请按 A、B、C、D 边排序后使用 Grasshopper“边缘曲面”组件。
Curves could not be auto sorted, try sorting your curves into U and V directions and using Grasshopper's Network Surface component.|曲线无法自动排序，请按 U、V 方向排序后使用 Grasshopper“网络曲面”组件。
Degree cannot be less than or equal to 0 and must be an odd number. The next highest positive odd number will be used.|次数必须为正奇数，将使用下一个较大的正奇数。
Discrete Polyline requires atleast 2 points.|离散多段线至少需要两个点。
Dispatching indices set contains duplicate index values. An index can only be used once to dispatch, only the first instance of each duplicate index was used.|分派索引存在重复，只使用每个索引首次出现的位置。
Dispatching indices set contains index values higher or lower than the bounds of the list of items to dispatch, only the index values within list bounds were used.|分派索引超出项目列表范围，只使用范围内的索引。
Extrusion direction must be a vector, curve, or point.|挤出方向必须为向量、曲线或点。
Faces removal index exceeds the polysurface (Brep) face count.|待移除面索引超出多重曲面面数。
If a curve is already closed it cannot be closed again.|已闭合曲线无需再次闭合。
If a curve is linear, it cannot be closed.|直线曲线无法闭合。
Index value cannot be higher than 7 because twisted boxes only have 8 points.|扭曲盒只有 8 个角点，索引不能大于 7。
Linear and degree 1 curves cannot be weighted, weighted distribution requires a curve with curvature.|直线及一次曲线不能使用加权分布，需要有曲率的曲线。
Mesh area mass properties could not be solved|无法计算网格面积属性。
Mesh could not be capped.|网格无法封端。
Mesh could not be made.|网格生成失败。
Mesh does not intersect or it fully encloses the twisted box set, no trimming occured.|网格未相交或完全包围扭曲盒组，未发生裁剪。
Mesh does not intersect the twisted box set, no trimming occured.|网格未与扭曲盒组相交，未发生裁剪。
Mesh has no naked edges.|网格无裸边。
Mesh hole could not be closed.|网格孔洞无法封闭。
Mesh hole could not be filled.|网格孔洞无法填补。
Mesh is already closed.|网格已闭合。
Mesh is not closed, volume results are not to be trusted|网格未闭合，体积结果不可靠。
Mesh must be closed for trimming.|裁剪需要闭合网格。
Mesh volume mass properties could not be solved|无法计算网格体积属性。
Meshes are required to have the same topology as the first mesh in the list, meshes with different topologies and their corresponding weight will be omitted from the mesh averaging.|网格必须与首网格拓扑相同，拓扑不同的网格及其权重将从平均计算中排除。
Meshes are required to have the same topology as the first mesh in the list, meshes with different topologies will be omitted from the mesh averaging.|网格必须与首网格拓扑相同，拓扑不同的网格将从平均计算中排除。
Meshes do not intersect or fully enclose the twisted box set, no trimming occured.|网格未相交或完全包围扭曲盒组，未发生裁剪。
Meshes must be closed for trimming, opened meshes will be ignored.|裁剪需要闭合网格，开放网格将被忽略。
Meshes must be closed for trimming.|裁剪需要闭合网格。
No segments of the curve match the search degrees.|曲线没有符合指定次数的段。
No trimming occured.|未发生裁剪。
Normalized opening length is larger than half the normalized length of the curve.|归一化开口长度大于曲线归一化长度的一半。
Normalized opening length shouldn't be larger than half the normalized length of the curve.|归一化开口长度不应大于曲线归一化长度的一半。
Not enough corner points in the set to construct a twisted box, 8 corner points are required.|构造扭曲盒至少需要 8 个角点，当前数量不足。
Not enough curves to create an edge surface, atleast 2 curves are required.|生成边缘曲面至少需要两条曲线，当前数量不足。
One or more input values are outside of the X Axis domain end, they will be plotted on the end of the X Axis|部分输入值超出 X 轴区间末端，将绘制到区间末端。
One or more input values are outside of the X Axis domain start, they will be plotted on the start of the X Axis|部分输入值超出 X 轴区间起点，将绘制到区间起点。
One or more input values on the X Axis does not intersect any graph curves, they will be mapped to the Y Axis domain start number.|部分 X 轴输入值未与图形曲线相交，将映射到 Y 轴区间起始值。
Opening length is larger than half the length of the curve.|开口长度大于曲线长度的一半。
Opening length shouldn't be larger than half the length of the curve.|开口长度不应大于曲线长度的一半。
Pipe mesh radius cannot be zero.|管状网格半径不能为零。
Points do not intersect the curve.|点组未与曲线相交。
Polygon cannot have less than 3 sides (triangle), a side count of 3 will be used.|多边形至少需要三条边，将使用三角形。
Polysurface (Brep) could not be unrolled.|多重曲面展开失败。
Polysurface (Brep) does not intersect or it fully encloses the twisted box set, no trimming occured.|多重曲面未相交或完全包围扭曲盒组，未发生裁剪。
Polysurface (Brep) must be closed for trimming.|裁剪需要闭合多重曲面。
Polysurface (Brep) or surface could not be unrolled, try increasing area and edge tolerances.|曲面或多重曲面展开失败，可尝试增大面积及边容差。
polysurfaces(Breps) do not intersect or fully enclose the twisted box set, no trimming occured.|多重曲面未相交或完全包围扭曲盒组，未发生裁剪。
polysurfaces(Breps) must be closed for trimming, opened polysurfaces(Breps) will be ignored.|裁剪需要闭合多重曲面，开放多重曲面将被忽略。
polysurfaces(Breps) must be closed for trimming.|裁剪需要闭合多重曲面。
Radius cannot be zero.|半径不能为零。
Rectangle could not be fit through points.|无法通过点组拟合矩形。
Rectangle fitting requires atleast two points that are not duplicate.|拟合矩形至少需要两个不重复点。
Rectangle fitting requires atleast two points.|拟合矩形至少需要两个点。
Resolution values above 3 will create a lot of twisted boxes. Please be sure to save your work in case your computer freezes.|分辨率大于 3 将产生大量扭曲盒，请先保存文件以防无响应。
Set of list items to sort synchronously with the set of points must have the same list length as the set of points for their sorting to occur, only the set of points will be sorted.|同步排序项目列表的长度必须与点组相同，否则只排序点组。
Sifting indices set contains duplicate index values. An index can only be used once to sift, only the first instance of each duplicate index was used.|筛分索引重复，只使用每个索引首次出现的位置。
Sifting indices set contains index values higher or lower than the bounds of the list of items to sift, only the index values within list bounds were used.|筛分索引超出项目列表范围，只使用范围内索引。
Size X domain start and end cannot be the same number.|X 尺寸区间起止值不能相同。
Size Y domain start and end cannot be the same number.|Y 尺寸区间起止值不能相同。
Step number values above 3 will potentially create a lot of mesh faces. Please be sure to save your work in case your computer freezes.|步数大于 3 可能生成大量网格面，请先保存文件以防无响应。
Step number values above 3 will potentially create a lot of twisted boxes. Please be sure to save your work in case your computer freezes.|步数大于 3 可能生成大量扭曲盒，请先保存文件以防无响应。
Surface area mass properties could not be solved|无法计算曲面面积属性。
Surface does not intersect the twisted box set, no trimming occured.|曲面未与扭曲盒组相交，未发生裁剪。
Surface trims could not be swapped or reversed.|曲面修剪边界无法交换或反转。
Surface volume mass properties could not be solved|无法计算曲面体积属性。
Tapered extrusion could not be made.|锥度挤出生成失败。
Target length shouldn't be larger than the length of the curve to divide.|目标长度不应大于待分割曲线总长度。
Target length shouldn't be less than or equal to zero.|目标长度必须大于零。
The added weights of all domain²s {u} domains or {v} domains equals zero, this is not valid.|二维区间 U 或 V 方向的权重总和为零，无效。
The extrusion direction length to taper angle ratio cannot create a proper taper, the result will be split into multiple parts.|挤出长度与锥度角比例无法生成有效锥度，结果将分裂为多个部分。
There are no curves in the graph, values will be mapped to the Y Axis domain start number.|图形中无曲线，数值将映射到 Y 轴区间起始值。
There is a zero in your list, you cannot divide by zero, are you trying to implode the universe?|列表包含零，除数不能为零。
There is no mesh vertice at the input index.|输入索引处没有网格顶点。
Thickness cannot be zero.|厚度不能为零。
This cut creates holes in the surface which cannot be connected across the mirror with edge blending routines. Linear connection type was used to connect these holes. Also, try the Mirror Cut Polysurface component.|裁剪产生的孔洞无法通过边缘混合跨镜像连接，已使用线性连接，也可尝试镜像裁剪多重曲面组件。
Too many corner points in the set to construct a twisted box, only the first 8 will be used.|构造扭曲盒的角点过多，只使用前 8 个。
Too many curves in the set to create an edge surface, only the first 4 will be used.|边缘曲面输入曲线过多，只使用前 4 条。
X Axis domain is singleton (domain start and end are the same number), all input values will be plotted on the start of the X Axis.|X 轴区间起止值相同，全部输入值绘制在起点。
Y Axis domain is singleton (domain start and end are the same number), all input values will be mapped to the Y Axis singleton domain number.|Y 轴区间起止值相同，全部输入值映射到该唯一值。
{x} or {y} proportion factors cannot be zero|X 或 Y 比例因子不能为零。
{x}, {y}, and {z} proportion factors cannot be zero|X、Y、Z 比例因子不能为零。
{x}, {y}, or {z} proportion factors cannot be zero|X、Y 或 Z 比例因子不能为零。
''')


def runtime_text(text):
    normalized = re.sub(r'\s+', ' ', text).strip().replace('虏', '²')
    if normalized in runtime_manual:
        return runtime_manual[normalized]
    m = re.fullmatch(r'(?:Weighted Average|Average) (.+) requires atleast two (.+), the output (.+) will be the same as the input (.+)\.', normalized)
    if m:
        return '平均运算至少需要两个输入对象，当前将原样输出。'
    m = re.fullmatch(r'(Tween (?:Consecutive|Through) .+|Blend (?:Consecutive|Through) Meshes) requires atleast two (.+)\. (?:Tweens|Blends) will be null in lists containing only one (.+)\.', normalized)
    if m:
        return '补间或混合至少需要两个输入对象；仅有一个对象的列表将输出空值。'
    if normalized.endswith('requires meshes to have the same topology.'):
        return '输入网格必须具有相同拓扑。'
    if normalized.startswith('Twisted Box ') and 'requires atleast two' in normalized:
        return '生成扭曲盒至少需要两个对应输入对象。'
    if normalized.startswith('Cannot mirror cut with one '):
        return '仅有一个项目，无法按索引镜像裁剪，将执行普通镜像。'
    if normalized.startswith('Mirror index is outside of the '):
        return '镜像索引超出输入组范围，无法继续镜像裁剪。'
    m = re.fullmatch(r'(Box|Brep|Circle|Curve|Rectangle) (area|volume) mass properties could not be solved', normalized)
    if m:
        return '无法计算' + {'Box':'盒','Brep':'多重曲面','Circle':'圆','Curve':'曲线','Rectangle':'矩形'}[m[1]] + ('面积' if m[2]=='area' else '体积') + '属性。'
    if normalized == 'Brep is not closed, volume results are not to be trusted':
        return '多重曲面未闭合，体积结果不可靠。'
    if normalized.startswith('Plane does not intersect'):
        return '平面未与输入对象相交，未发生裁剪。'
    if normalized.startswith('Linear interpolation and degree 1 '):
        return '线性插值或一次插值路径不能使用加权分布，需要具有曲率的路径。'
    if normalized.startswith('Mesh A and B') and 'same topology' in normalized:
        return '网格 A、B 必须具有相同拓扑；不同拓扑之间的补间、混合或扭曲盒结果为空值。'
    if normalized.startswith(('Mesh A and B must both have vertex colors', 'Meshes must all have vertex colors')):
        return '所有网格必须具备顶点颜色才能处理颜色，当前仅处理几何而不处理颜色。'
    if normalized.startswith('The added weights of all '):
        return '输入权重总和为零，无效。'
    if normalized.startswith('You cannot supply more '):
        return '属性输入数量不能超过对应分割参数、目标对象或递归步骤数量。'
    if normalized.startswith('You must supply equal amounts of '):
        return '对应属性、权重、几何或分割参数的输入数量必须一致。'
    if normalized.startswith('Unsplit ') and normalized.endswith('surface could not be made.'):
        return '不分裂曲面生成失败。'
    if normalized.startswith('Valid '):
        allowed = re.search(r'(?:values are from|values are) ([0-9, ]+(?:to \d+)?)', normalized)
        first = normalized.split(' will be used because ',1)[0]
        default = first.split('. ',1)[-1]
        keys = {'accuracy':'精度','axis':'轴','blend':'混合','cap':'封端','center':'中心','close':'闭合','coloring':'着色','connection':'连接','continuity':'连续性','corner':'角点','deconstruct':'解构','direction':'方向','division':'分割','end':'末端','face':'面','get':'获取','interpolation':'插值','keep':'保留','kink':'折角','loft':'放样','luminosity':'亮度','mirror':'镜像','round':'舍入','start':'起点','subdivision':'细分','trim':'修剪'}
        parameter = keys.get(normalized.split()[1], '模式')
        defaults = {'Tangency':'相切','None':'无','Corner Points':'角点','Linear':'线性','Split faces, with connection':'分割面并连接','Straight':'直线','Loose':'松散','Sharp':'尖角','Cardinal + InterCardinal':'主方向与中间方向','Orientation plane {z} direction':'朝向平面 Z 方向','Nearest':'最近','Preserve end point only':'仅保留终点','Default':'默认','Arc':'圆弧','Halfway':'半数','Normal':'法向','Reflected':'反射镜像','Preserve start point only':'仅保留起点','Cubic star':'立方星形','Split faces':'分割面','{x}':'X 轴','{xyz}':'XYZ 轴','1':'1'}
        translated = next((v for k,v in sorted(defaults.items(),key=lambda kv:-len(kv[0])) if default.startswith(k)), '插件默认值')
        if normalized.startswith('Valid luminosity values'):
            translated = 'RGB 权重（0.2989、0.5870、0.1140）'
        elif normalized.startswith('Valid accuracy values'):
            translated = '精度 1'
        axis_number = re.search(r'^Valid axis ([123]) ', normalized)
        if axis_number:
            parameter += ' ' + axis_number[1]
        return parameter + '输入值无效，允许范围：' + (allowed[1].strip().replace(' to ', ' 到 ') if allowed else '原插件指定范围') + '；将使用 ' + translated + '。'
    if normalized.startswith(('Parameters {t} cannot be weighted', 'Parameters {v} cannot be weighted', 'Angle accuracy {v} cannot be used', 'Lengths between control points {v} cannot be used')):
        return '此参数或加权选项仅当挤出方向为曲线时有效。'
    if normalized.startswith('Size {') and 'cannot be zero' in normalized:
        return re.search(r'\{[xyz]\}', normalized)[0] + ' 尺寸不能为零。'
    return None


existing_names = {r['name']: r['translation'] for r in read_pack('zh-CN.json') if r.get('category') == 'port-name'}
existing_text = {r['name']: r['translation'] for r in read_pack('tool-text.zh-CN.json') if r.get('category') == 'port-description'}
all_names = set(t['name'] for t in source['tools']) | set(t['constructor'][0] for t in source['failures'])
all_descriptions = set(t['description'] for t in source['tools']) | set(t['constructor'][2] for t in source['failures'])
port_names = {p['name'] for t in source['tools'] for p in t['inputs'] + t['outputs']}
port_descriptions = {p['description'] for t in source['tools'] for p in t['inputs'] + t['outputs']}
for row in source['failures']:
    for entry in source['method_text']:
        if entry['type'] == row['type'] and entry['method'].startswith('Register'):
            for port in entry['ports']:
                port_names.add(port['name'])
                port_descriptions.add(port['description'])

names = []
texts = []
missing = {'names': [], 'descriptions': [], 'port-names': [], 'port-descriptions': [], 'runtime': []}
for name in sorted(all_names):
    translated = translate_name(name)
    if name in name_exceptions or not re.search(r'[A-Za-z]{3,}', translated):
        names.append({'name': name, 'category': 'Pufferfish', 'translation': translated})
    else:
        missing['names'].append(name)
for name in sorted(port_names):
    translated = existing_names.get(name) or replace_terms(name)
    if re.search(r'[A-Za-z]{3,}', translated):
        missing['port-names'].append(name)
    else:
        names.append({'name': name, 'category': 'port-name', 'translation': translated})
for text in sorted(all_descriptions):
    translated = description(text)
    if translated:
        texts.append({'name': text, 'category': 'description', 'translation': translated})
    else:
        missing['descriptions'].append(text)
for text in sorted(port_descriptions):
    translated = existing_text.get(text) or port_description(text)
    if not translated:
        missing['port-descriptions'].append(text)
        continue
    remaining = re.findall(r'[A-Za-z]{2,}', translated)
    technical = {'Rhino', 'RhinoMath', 'Grasshopper', 'Brep', 'Breps', 'Alpha', 'RGB', 'XYZ', 'UV', 'UVW', 'XY', 'XZ', 'YZ', 'xyz', 'uvw', 'uv', 'Cl', 'Pl', 'TB', 'CreaseSplitting', 'No', 'Retrim', 'Copy', 'Trim', 'Combine', 'Data', 'Pull', 'Curve', 'Disjoint', 'Mesh', 'Isotrim', 'Compound'}
    if any(word not in technical for word in remaining):
        missing['port-descriptions'].append(text)
    else:
        texts.append({'name': text, 'category': 'port-description', 'translation': translated})
runtime_strings = sorted({s for entry in source['method_text'] if entry['method'] == 'SolveInstance' for s in entry['strings']})
for text in runtime_strings:
    translation = runtime_text(text)
    if translation:
        texts.append({'name': text, 'category': 'runtime', 'translation': translation})
    else:
        missing['runtime'].append(text)
for path, data in [('Languages/pufferfish.zh-CN.json', names), ('Languages/pufferfish-text.zh-CN.json', texts), ('docs/pufferfish-untranslated.json', missing)]:
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('names:', len(names), 'texts:', len(texts), 'remaining:', {k: len(v) for k, v in missing.items()})
