# QiaYun Power Website

恰云电力（QiaYun Power）企业官网静态站点，面向海外客户展示公司能力、产品中心、服务项目、客户与场景、资质证书和联系方式。

## 项目内容

- 多语言官网首页：中文、英文、越南语、泰语
- 产品中心：中压开关柜、箱式变电站、环网柜、低压开关柜、无功补偿柜、动力柜、配电箱
- 服务项目：高低压成套设备、电力配套附件、智慧电力系统升级、全流程技术服务
- 企业信息：公司介绍、发展历程、资质证书、客户场景、全球布局
- 静态部署：无需构建工具，可直接用浏览器或静态服务器访问

## 目录结构

```text
qiayun/
├── website/
│   ├── index.html          # 官网首页
│   ├── css/style.css       # 页面样式
│   ├── js/i18n.js          # 多语言文案配置
│   ├── images/             # 产品图、证书图、企业图册素材
│   └── products/           # 产品详情页
├── extract_images.py       # 图册图片提取脚本
├── update_product_imgs.py  # 产品图片更新脚本
├── crop_products.py        # 产品图片裁剪脚本
└── README.md
```

## 本地预览

进入项目目录后启动任意静态服务器：

```bash
cd website
python3 -m http.server 8080
```

然后打开：

```text
http://localhost:8080
```

也可以直接用浏览器打开 `website/index.html`。

## 多语言说明

多语言文案集中维护在：

```text
website/js/i18n.js
```

当前支持语言：

- `zh`：中文
- `en`：English
- `vi`：Tiếng Việt
- `th`：ไทย

页面中通过 `data-i18n="key"` 绑定文案。新增页面文案时，需要同步在四种语言对象中补齐对应 key，避免页面显示原始 key。

## 内容维护

### 更新首页文案

1. 在 `website/index.html` 中确认对应元素的 `data-i18n` key。
2. 在 `website/js/i18n.js` 中更新四种语言的文案。
3. 刷新页面并切换语言检查展示效果。

### 更新产品详情页

产品详情页位于：

```text
website/products/
```

如需新增产品，可参考现有页面结构，并同步更新首页产品卡片与相关图片资源。

### 更新图片资源

网站图片位于：

```text
website/images/
```

建议使用清晰、压缩后的 JPG/JPEG 图片，避免单张图片过大影响加载速度。

## 验证

检查语言包语法：

```bash
node --check website/js/i18n.js
```

检查首页 `data-i18n` 是否都有翻译：

```bash
node - <<'NODE'
const fs = require('fs');
const html = fs.readFileSync('website/index.html', 'utf8');
const i18n = fs.readFileSync('website/js/i18n.js', 'utf8');
const htmlKeys = [...new Set([...html.matchAll(/data-i18n="([^"]+)"/g)].map(match => match[1]))];
for (const lang of ['vi', 'zh', 'en', 'th']) {
  const start = i18n.indexOf(`  ${lang}: {`, i18n.indexOf('const T = {'));
  const next = ['vi', 'zh', 'en', 'th']
    .map(item => i18n.indexOf(`  ${item}: {`, start + 1))
    .filter(index => index > start)
    .sort((a, b) => a - b)[0] ?? i18n.indexOf('\n};', start);
  const keys = new Set([...i18n.slice(start, next).matchAll(/^    ([a-zA-Z0-9_]+):/gm)].map(match => match[1]));
  const missing = htmlKeys.filter(key => !keys.has(key));
  console.log(`${lang}: ${missing.length ? `missing ${missing.join(', ')}` : 'all keys present'}`);
}
NODE
```

## 部署

这是纯静态网站，可部署到任意静态托管服务，例如：

- GitHub Pages
- Vercel
- Netlify
- Nginx / Apache 静态目录
- 对象存储静态网站托管

部署目录建议指向：

```text
website/
```

## 最近更新

- 补齐首页缺失的多语言 key，修复 `markets_title`、`global_title`、`scenario_*`、`strength_*` 等 key 直接显示的问题。
- 完成首页新增模块的中文、英文、越南语、泰语文案同步。

## 客户需求后台

项目内置一个轻量 Node.js 后台，用于接收官网联系表单并查看客户提交信息。

### 启动方式

```bash
ADMIN_PASSWORD='your-secure-password' npm start
```

默认访问地址：

```text
http://localhost:3000
```

后台地址：

```text
http://localhost:3000/admin
```

### 功能说明

- 前台联系表单提交到 `POST /api/inquiries`
- 客户信息保存到本地 `data/inquiries.json`
- 管理后台通过 `ADMIN_PASSWORD` 登录
- 后台可查看提交时间、姓名、邮箱、电话、公司、需求描述和页面语言

### 部署注意

如果只部署 `website/` 到 GitHub Pages、对象存储或普通静态空间，提交功能不会生效，因为静态空间不能运行后台 API。

要使用客户需求后台，需要部署整个项目并运行 Node 服务，例如：

- 云服务器 + Nginx 反向代理到 Node 服务
- Render / Railway / Fly.io 等 Node 托管平台
- 自有服务器用 `pm2` 常驻运行 `npm start`

生产环境务必设置：

```bash
ADMIN_PASSWORD='强密码'
SESSION_SECRET='随机长字符串'
PORT=3000
```
