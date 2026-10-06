# 杰哥 AI 实验室 · Jie's AI Lab

围绕真实业务问题开展 AI 工作坊与实验的双语静态网站。中文在根目录，英文在 `en/`；使用原生 HTML、CSS、JavaScript 与本地字体、图片，没有运行时依赖或内容管理后台。

交付目录是 `design/site`，Git 在此目录初始化。公开仓库为 [liunoly-design/jielabcc](https://github.com/liunoly-design/jielabcc)，`main` 分支已存在；网站托管尚未部署。公开仓库根目录只承载本静态站点，不包含上层项目的旧服务、环境变量或个人保存网页。

## 本地预览

从本仓库根目录（即原项目的 `design/site`）执行：

```sh
python3 -m http.server 8765
```

打开 [中文首页](http://localhost:8765/) 或 [英文首页](http://localhost:8765/en/)。从原项目根目录预览可执行：

```sh
python3 -m http.server 8765 --directory design/site
```

通过 HTTP 预览，以便核对资源与跨页路径。

## 当前内容

五种页面各有中文与英文版本，共十个 HTML：`index.html` 首页、`cases.html` 行业索引、`case.html` 查询参数详情模板、`articles.html` 客户报道、`clients.html` 合作客户。全站导航提供工作坊、行业案例、客户报道、合作客户、团队、合作咨询六个目的地。语言切换保留当前页面、查询参数与 hash；首页行业标签状态未写入地址，不能保证切换语言后保留其临时选择。

工作坊五项产品是半天沙龙、1 天 Skill 工作坊、2 天 1 夜 Hackathon、5 天 BootCamp、3 个月组织陪跑。BootCamp 成果支持继续推进部署与使用，阶段验收目标在开营前共同确定。

医药案例分为医药流通（国润医疗、保钰鑫医疗）、医药科技（国药数科）、医疗器械生产企业（威高骨科）。资产评估、法律、教育各有一个明确披露的实验示例，展示问题、实验与拟交付物，非已实施客户项目；各行业第 2、3 入口显示资料待整理。详情由共享模板与数据生成，不代表十二个已完成客户项目。

客户报道现为五篇唯一原文入口；未知 I83 条目已删除。威高报道由用户保存的本地原文核验，发布日期 2026-08-12，工作坊日期为 2026-08-07 至 08-08：25 人、9 部门、39 件作品、21 件进入业务成果池、8 件优先继续推进，原文建议后续继续试点 2–3 个场景。这些是工作坊产物与后续建议，不等于全部已投产。数据保留原文机构名称及关联证据边界；英文标题为编辑翻译，页面保留中文原题。

六家合作客户为国药数科、国润医疗、保钰鑫医疗、威高骨科、华润医药商业（CR Pharma Comm）、洁诺医疗集团（Steriguard），关系来自用户指定。当前有三份原始标志，三家仍缺原稿，页面保留诚实的名称占位与待整理说明。

首页团队区列出杰哥、念念老师、Lily 老师、老田、罗伯特牛仔五名成员，每人有角色与 1–2 句介绍。英文对应 Jie、Niannian、Lily、Lao Tian、Robert Cowboy；简介按用户提供的经历及分工整理。

## 内容与双语维护

| 文件 | 用途 |
| --- | --- |
| 根目录五个中文 HTML | 页面结构、静态文案、报道列表与来源 caption |
| `cases.json` | 双语案例；`illustrative` 披露、正文、原图与报道索引 |
| `articles.json` | 报道原标题、日期、来源、核验状态、原文 URL、本地图片及关联说明 |
| `clients.json` | 双语客户分类、真实 Logo 路径、报道路径、国药裁切参数 |
| `locales-en.json` | 中文静态文案对应英文翻译 |
| `consultation-config.json` | 后续真实合作登记 HTTPS URL |
| `scripts/build_locales.py` | 生成英文 HTML 与 `case-data.js`，维护报道标题 `TITLE_EN` |
| `app.js` / `style.css` | 共享交互与响应式外观 |

从仓库根目录依次执行：

```sh
python3 scripts/build_locales.py
python3 scripts/update_fonts.py
```

从原项目根目录则在脚本路径前加 `design/site/`。先构建双语，再更新字体。不要手改生成的 `en/*.html` 或 `case-data.js`；下次构建会覆盖。新中文文案需先补齐 `locales-en.json`，构建器遇到缺失翻译会报错。

添加报道时在 `articles.json` 写入真实证据，手工增加中文 `articles.html` 的列表项，需要首页展示则同步 `index.html`；构建器不会自动增加静态报道容器。同步 `TITLE_EN` 与报道顺序，检查 `cases.json.reports` 的零基索引。只核验到入口时保持未知字段，不补造标题、日期、署名或收益。

## 品牌、Logo 与图像

原始 VI 使用纸面、深空灰、科技蓝和少量生命橙，界面以留白、字体层级与细线分隔组织信息。正式实验室 Logo 为用户原稿 `assets/logo-bilingual.png`，来源见 `assets/logo-source.json`；保留完整杰哥、黄猫与双语字标组合、原比例和颜色，普通混合模式显示在匹配的 `#F8FAFC` 纸面上。独立黄猫为角色延展，不能替换正式 Logo。

客户素材来源记录在 `assets/clients/sources.json`。威高与华润来自各自官网原标志；国药数科来自客户报道的 `assets/photos/report-1.jpg` 原图，由 `clients.json.logoCrop` 与 CSS 视窗裁切展示，不重绘、重新排字或用集团标志替代。展示框桌面统一高 132px，移动 125px，原稿等比例放入框内；裁切是显示方式，源图保持原样。

国润、保钰鑫、洁诺正式 Logo 尚未取得。洁诺官网证书无效，未绕过验证取图。补齐原稿后更新 `clients.json` 与来源记录，再构建双语；全部素材到齐时，还需手动修改中文 `clients.html` 的总体待整理说明、更新英文词典并重建，该说明不会自动消失。

真实客户图片均为本地原图，记录在 `assets/photos/sources.json`：四篇报道封面和三张威高工作坊现场图片。理念与威高详情显示威高照片，团队区使用保钰鑫实际工作坊合影并显示来源；它不是实验室员工编制合影。缺图时保留明确不可用状态，不用合成场景当现场证据。

团队头像显示框统一为 76 × 76px、4px 圆角、`object-fit:cover` 与 `object-position:50% 20%`。杰哥使用现有 `assets/founder.png` 原始 VI 形象；念念老师、Lily 老师、老田、罗伯特牛仔尚未提供真实头像，当前用姓名或字母占位，带头像待补的 `aria-label` 和列表下方可见说明。本轮未生成新的栅格图。具名成员网格桌面三栏、850px 以下两栏、650px 以下单栏；旧三个泛化角色已从页面移除，旧 `.people` CSS 仍存在。

替换头像时，将中文 `index.html` 中对应的 `.member-avatar.avatar-pending` div 换为 `<img class="member-avatar" src="本地原图路径" alt="人物描述">`，去掉 `avatar-pending`，补充原图宽高与加载属性；保留统一头像框及裁切规则。按实际待补名单更新 `.team-photo-note`，全部补齐后再移除说明。同步 `locales-en.json` 的新文案和 alt，再运行双语构建与字体更新，不直接手改英文生成页。

首屏已恢复原来的细蓝色回环方法路径：内联 SVG 显示“痛点挖掘 / 实验验证 / 价值实现”，英文为“Discover pain points / Validate experiments / Realise value”，使用 `role=img` 与对应语言的 `aria-label`。既有黄猫 `assets/cat-v2.png` 保持原样。废弃雕塑概念图及其 prompt 已移除，本轮未生成新的栅格图。方法图为 `methodology-zh.png` 与 `methodology-en.png`，caption 在图下方显示“问题 · 实验 · 价值 / Problem · Experiment · Value”，不显示 AI 生成标签；生成来源与 prompt 保留在 `assets/GENERATED-IMAGES.json` 及对应 `.prompt.txt`。这些图表达品牌与方法，不能作客户事件照片或项目成果凭证。

## 字体与交互

中文字体 `LabChinese` 来源为 Noto Sans SC，与思源黑体同源；英文与数字 `LabLatin` 来源为 Inter。两者自托管 400、500、600、700、800 真实字重，使用 `font-display:swap` 和 `font-synthesis:none`。许可证在 `assets/Noto-OFL.txt` 与 `assets/Inter-OFL.txt`。

`scripts/update_fonts.py` 递归扫描 HTML 及 `app.js`、`cases.json`、`clients.json`，通过 Google Fonts 更新字形子集与 `fonts.css`，执行需要网络。团队简介更新后已重建至 706 字形。新增文字后核对字形，单独修改 `articles.json` 未必纳入字体集合，须同步实际页面。

实际断点为 1200、980、850、650px；980px 以下折叠导航，650px 以下堆叠主要内容。容器最大 1400px，边距依次 68、48、32、20px。页面采用原生滚动与 proximity scroll snap，不劫持滚轮、不保证每次整屏停靠；长内容自然增高，详情自然滚动。减少动态模式关闭平滑滚动、动画、过渡和停靠。

行业标签支持方向键、Home、End与唯一选中状态，普通模式有 300ms 文字区过渡。页头显示阅读进度与同页章节激活状态；细指针设备的链接使用品牌 SVG 光标，保留 pointer 回退，未实现全页追踪光标。首屏方法路径为静态图形，已移除指针跟随位移。菜单支持 Escape 关闭并恢复焦点。初始 hash 恢复等待字体与本地图片建立布局，仅在用户未操作且 hash 未变时恢复目标。

双语首屏共用 `minmax(0,1fr) 32%` 网格与 45px 间距，850px 以下为 33% 与 25px，650px 以下堆叠。方法路径容器桌面 340 × 420px，移动 260 × 315px，最大宽度 100%。英文桌面工作坊仍保留既有列宽规则；既定 VI 与基础 token 保持原样。

## 验证与交付边界

2026-10-06 团队扩展记录为原项目 `.impeccable/review/team-members-{zh,en}-{desktop,mobile}.png` 与 `team-members-zh-tablet.png`，共五张完整 `#team` 区域截图，并非全站截图；捕获视口分别为 1101 × 876、768 × 900、390 × 844。实施方在各捕获状态测得无横向溢出，均为五个姓名及五个头像框。静态 detector 记录 16 项警告（8 项 padding、5 项 contrast、1 项 tiny-text、2 项 leading）。独立评审已完成，报告为原项目 `team-members-finish-review.md`，结论为 **Ship — scoped pass for the bilingual named profiles and truthful pending-portrait state**。评审逐张检查五张截图与当前源码，未操作浏览器，未发现需要修复、重截图或重建的实质缺陷；成员经历来自用户，未独立认证。该结论仅覆盖这些团队区域，不认证英文平板、全站、完整无障碍或部署，也不表示四位实际头像已交付。此前首屏恢复结论仍保留其原有范围；这些评审资料不在本静态仓库内。

2026-10-06 首屏恢复后的独立 finish review 已完成，结论为 **Ship — scoped pass for the restored bilingual homepage hero**，报告为原项目 `.impeccable/review/hero-restored-finish-review.md`。评审逐张打开截图及视觉参考，未操作浏览器；结论仅覆盖本轮双语首屏恢复和两种视口，不认证全站或中间宽度。静态 detector 记录18项警告（8项 padding、5项 contrast、1项 tiny-text、4项 leading），评审未发现这些构成本轮恢复图解的实质缺陷。本轮中文与英文桌面（1101 × 876）及移动（390 × 844）四张截图为 `hero-restored-{zh,en}-{desktop,mobile}.png`；实施方测量这些首页无横向溢出或未加载图片，桌面/移动可见边距为 48/20px。上述评审资料不在本静态仓库内。此前 `oct6-finish-review.md` 的 **Ship — scoped pass for the current static prototype and truthful asset state** 是当时静态原型与素材状态的限定结论，不作为本轮首屏恢复的评审结论。

此前实施方核对十个 HTML 的六项导航、内部资源依赖、JavaScript 语法与五个唯一报道 URL；浏览器测量截图路由无横向溢出或未加载图片、六个桌面 Logo 框均为 132px，桌面/移动可见边距为 48/20px。移动测试包括 Legal 标签 ArrowRight 到 Education，以及菜单展开、Escape关闭。静态 detector 有七项 screen-wrapper 留白警告，内层容器与截图实测不支持实质拥挤问题；此结论不代表全面设备测试。

常规只读检查：

```sh
node --check app.js
node --check case-data.js
python3 -m json.tool articles.json > /dev/null
python3 -m json.tool cases.json > /dev/null
python3 -m json.tool clients.json > /dev/null
python3 -m json.tool locales-en.json > /dev/null
python3 -m json.tool consultation-config.json > /dev/null
```

当前合作登记 URL 故意留空，按钮 disabled，没有飞书提交、邮件、存储或通知后台。取得真实 HTTPS URL 后写入 `consultation-config.json` 并构建；格式校验不验证飞书域名、权限、可访问性或保存/通知结果。

GitHub 静态托管或 Cloudflare Pages 上传已提交的本目录 HTML、CSS、JS 和资源不需要构建命令。修改源内容时先本地运行上述语言/字体脚本再提交生成文件。网站托管与飞书服务接入需另行配置；限定评审不证明外部原文可访问、生产运行、全面无障碍认证、素材许可或三份缺失 Logo 已补齐。
