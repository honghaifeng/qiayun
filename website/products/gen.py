#!/usr/bin/env python3
"""Generate product detail pages from template"""
import os

products = [
    {
        "file": "ybm-12.html",
        "title": "YBM-12 Prefab Substation",
        "i18n_name": "p2_name",
        "i18n_desc": "p2_desc",
        "tags": ["12kV", "All-in-One", "IEC 62271", "CNAS", "CQC"],
        "specs": [
            ("Rated voltage (HV)", "12kV"),
            ("Rated voltage (LV)", "0.4kV"),
            ("Transformer capacity", "50~2500kVA"),
            ("Rated current (HV)", "630A"),
            ("Rated current (LV)", "1000~3150A"),
            ("Short-circuit current", "31.5kA (4s)"),
            ("Standard", "IEC 62271-202, GB/T 17467"),
            ("Certification", "CNAS, CQC, ISO 9001"),
        ],
        "svg": '<svg width="280" height="280" viewBox="0 0 280 280" fill="none"><rect x="20" y="50" width="240" height="180" rx="12" stroke="white" stroke-width="3" opacity="0.6"/><rect x="10" y="30" width="260" height="30" rx="8" stroke="white" stroke-width="2" opacity="0.4"/><line x1="100" y1="50" x2="100" y2="230" stroke="white" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.4"/><line x1="180" y1="50" x2="180" y2="230" stroke="white" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.4"/><text x="60" y="150" text-anchor="middle" fill="#e8a838" font-size="16" font-weight="bold">HV</text><text x="140" y="150" text-anchor="middle" fill="#e8a838" font-size="16" font-weight="bold">Transformer</text><text x="220" y="150" text-anchor="middle" fill="#e8a838" font-size="16" font-weight="bold">LV</text></svg>',
        "features": [
            ("&#127981;", "All-in-One Design", "Integrates HV switchgear, transformer, and LV switchgear in a single compact enclosure."),
            ("&#9201;", "Rapid Deployment", "Factory pre-assembled and tested, minimal on-site installation time."),
            ("&#127758;", "Weather Resistant", "IP33 outdoor protection, suitable for tropical and humid climates."),
        ]
    },
    {
        "file": "hxgn-12.html",
        "title": "HXGN-12 Ring Main Unit",
        "i18n_name": "p3_name",
        "i18n_desc": "p3_desc",
        "tags": ["12kV", "SF6", "Compact", "CNAS", "CQC"],
        "specs": [
            ("Rated voltage", "12kV"),
            ("Rated current", "630A"),
            ("Short-circuit current", "20kA (4s)"),
            ("Insulation medium", "SF6 gas"),
            ("Protection level", "IP3X"),
            ("Standard", "IEC 62271-200, GB/T 12706"),
            ("Certification", "CNAS, CQC"),
        ],
        "svg": '<svg width="280" height="280" viewBox="0 0 280 280" fill="none"><circle cx="140" cy="140" r="100" stroke="white" stroke-width="3" opacity="0.6"/><circle cx="140" cy="140" r="60" stroke="white" stroke-width="2" opacity="0.4"/><circle cx="140" cy="140" r="20" fill="#e8a838" opacity="0.6"/><line x1="140" y1="40" x2="140" y2="80" stroke="#e8a838" stroke-width="3"/><line x1="140" y1="200" x2="140" y2="240" stroke="#e8a838" stroke-width="3"/><line x1="40" y1="140" x2="80" y2="140" stroke="#e8a838" stroke-width="3"/><line x1="200" y1="140" x2="240" y2="140" stroke="#e8a838" stroke-width="3"/></svg>',
        "features": [
            ("&#128268;", "SF6 Insulation", "Sealed SF6 gas insulation ensures long-term reliability with zero maintenance."),
            ("&#128207;", "Compact Size", "Small footprint ideal for urban underground substations and space-limited areas."),
            ("&#128260;", "Flexible Configuration", "Various combinations of load switch, circuit breaker, and fuse units."),
        ]
    },
    {
        "file": "gck.html",
        "title": "GCK LV Switchgear",
        "i18n_name": "p4_name",
        "i18n_desc": "p4_desc",
        "tags": ["0.4kV", "6300A", "Modular", "CNAS", "CQC"],
        "specs": [
            ("Rated voltage", "AC 380/660V"),
            ("Rated current (main busbar)", "6300A"),
            ("Rated current (branch)", "630A"),
            ("Short-circuit current", "80kA (peak)"),
            ("Protection level", "IP30 / IP40"),
            ("Standard", "IEC 61439-2, GB/T 7251"),
            ("Certification", "CNAS, CQC, ISO 9001"),
        ],
        "svg": '<svg width="280" height="280" viewBox="0 0 280 280" fill="none"><rect x="30" y="20" width="220" height="240" rx="12" stroke="white" stroke-width="3" opacity="0.6"/><rect x="50" y="45" width="80" height="55" rx="6" stroke="white" stroke-width="2" opacity="0.4"/><rect x="150" y="45" width="80" height="55" rx="6" stroke="white" stroke-width="2" opacity="0.4"/><rect x="50" y="115" width="80" height="55" rx="6" stroke="white" stroke-width="2" opacity="0.4"/><rect x="150" y="115" width="80" height="55" rx="6" stroke="white" stroke-width="2" opacity="0.4"/><rect x="50" y="185" width="180" height="30" rx="6" fill="#e8a838" opacity="0.2" stroke="#e8a838" stroke-width="2"/><text x="140" y="205" text-anchor="middle" fill="#e8a838" font-size="14" font-weight="bold">6300A BUSBAR</text></svg>',
        "features": [
            ("&#128268;", "Drawer-type Design", "Hot-swappable drawer units allow maintenance without system shutdown."),
            ("&#129513;", "Modular Structure", "Standardized modules for flexible configuration and easy expansion."),
            ("&#128737;", "High Protection", "Up to IP40 protection level, suitable for various environments."),
        ]
    },
    {
        "file": "svc.html",
        "title": "SVC Reactive Power Compensation",
        "i18n_name": "p5_name",
        "i18n_desc": "p5_desc",
        "tags": ["Auto PFC", "Energy Saving", "CNAS", "CQC"],
        "specs": [
            ("Rated voltage", "AC 380/400V"),
            ("Compensation capacity", "30~600kvar"),
            ("Power factor target", ">0.95"),
            ("Response time", "<20ms"),
            ("Controller", "Intelligent auto-switching"),
            ("Standard", "IEC 61921, GB/T 15576"),
            ("Certification", "CNAS, CQC"),
        ],
        "svg": '<svg width="280" height="280" viewBox="0 0 280 280" fill="none"><rect x="60" y="30" width="160" height="220" rx="12" stroke="white" stroke-width="3" opacity="0.6"/><path d="M100 120 L140 80 L180 120 L140 160 Z" stroke="#e8a838" stroke-width="3" fill="none"/><text x="140" y="128" text-anchor="middle" fill="#e8a838" font-size="22" font-weight="bold">PF</text><line x1="140" y1="160" x2="140" y2="220" stroke="white" stroke-width="2" opacity="0.6"/><text x="140" y="60" text-anchor="middle" fill="white" font-size="14" opacity="0.7">cosφ > 0.95</text></svg>',
        "features": [
            ("&#9889;", "Auto Compensation", "Intelligent controller automatically adjusts compensation based on real-time power factor."),
            ("&#128176;", "Cost Savings", "Avoid reactive power penalties, reduce electricity bills by 10-25%."),
            ("&#128202;", "Energy Efficiency", "Reduce line losses, improve power quality and system efficiency."),
        ]
    },
    {
        "file": "xgl.html",
        "title": "XGL LV Power Cabinet",
        "i18n_name": "p6_name",
        "i18n_desc": "p6_desc",
        "tags": ["0.4kV", "Industrial", "CNAS", "CQC"],
        "specs": [
            ("Rated voltage", "AC 380/400V"),
            ("Rated current", "Up to 3200A"),
            ("Short-circuit current", "50kA (peak)"),
            ("Protection level", "IP30"),
            ("Mounting", "Fixed / Plug-in"),
            ("Standard", "IEC 61439, GB/T 7251"),
            ("Certification", "CNAS, CQC"),
        ],
        "svg": '<svg width="280" height="280" viewBox="0 0 280 280" fill="none"><rect x="50" y="20" width="180" height="240" rx="12" stroke="white" stroke-width="3" opacity="0.6"/><rect x="70" y="50" width="140" height="40" rx="6" stroke="white" stroke-width="2" opacity="0.4"/><rect x="70" y="105" width="140" height="40" rx="6" stroke="white" stroke-width="2" opacity="0.4"/><rect x="70" y="160" width="140" height="40" rx="6" stroke="white" stroke-width="2" opacity="0.4"/><circle cx="190" cy="70" r="10" fill="#e8a838" opacity="0.6"/><circle cx="190" cy="125" r="10" fill="#e8a838" opacity="0.6"/><circle cx="190" cy="180" r="10" fill="#e8a838" opacity="0.6"/></svg>',
        "features": [
            ("&#127981;", "Heavy-Duty Design", "Robust construction for demanding industrial environments."),
            ("&#128268;", "Flexible Layout", "Fixed or plug-in mounting options for different requirements."),
            ("&#128736;", "Easy Maintenance", "Front access design for convenient maintenance and operation."),
        ]
    },
    {
        "file": "jxf.html",
        "title": "JXF Distribution Box",
        "i18n_name": "p7_name",
        "i18n_desc": "p7_desc",
        "tags": ["0.4kV", "Flexible", "Residential", "Commercial"],
        "specs": [
            ("Rated voltage", "AC 380/400V"),
            ("Rated current", "Up to 630A"),
            ("Protection level", "IP30 / IP54"),
            ("Mounting", "Wall-mount / Floor-standing"),
            ("Material", "Cold-rolled steel / Stainless steel"),
            ("Standard", "IEC 61439, GB/T 7251"),
            ("Certification", "CQC"),
        ],
        "svg": '<svg width="280" height="280" viewBox="0 0 280 280" fill="none"><rect x="70" y="40" width="140" height="200" rx="12" stroke="white" stroke-width="3" opacity="0.6"/><rect x="90" y="70" width="100" height="25" rx="4" stroke="white" stroke-width="2" opacity="0.4"/><rect x="90" y="110" width="100" height="25" rx="4" stroke="white" stroke-width="2" opacity="0.4"/><rect x="90" y="150" width="100" height="25" rx="4" stroke="white" stroke-width="2" opacity="0.4"/><circle cx="140" cy="210" r="12" stroke="#e8a838" stroke-width="2.5" fill="none"/><line x1="134" y1="210" x2="146" y2="210" stroke="#e8a838" stroke-width="2"/></svg>',
        "features": [
            ("&#128207;", "Compact Design", "Space-saving design perfect for wall mounting in limited spaces."),
            ("&#128736;", "Easy Installation", "Simple wiring and mounting, reduces installation time significantly."),
            ("&#127758;", "Versatile Application", "Suitable for residential, commercial, and light industrial use."),
        ]
    },
]

template = '''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | QiaYun Power</title>
  <meta name="description" content="{title} - CNAS & CQC certified power equipment by QiaYun Power.">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
  <style>
    .product-hero{{padding:120px 24px 60px;background:linear-gradient(135deg,#0f1b2d,#1e3a5f);}}
    .product-hero-inner{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;color:white;}}
    .product-hero h1{{font-size:36px;font-weight:800;margin-bottom:16px;}}
    .product-hero .subtitle{{font-size:18px;opacity:0.9;margin-bottom:24px;line-height:1.8;}}
    .product-hero-img{{background:rgba(255,255,255,0.05);border-radius:16px;padding:40px;display:flex;align-items:center;justify-content:center;border:1px solid rgba(255,255,255,0.1);}}
    .spec-section{{padding:60px 24px;}}
    .spec-inner{{max-width:1200px;margin:0 auto;}}
    .spec-table{{width:100%;border-collapse:collapse;margin-top:24px;}}
    .spec-table th,.spec-table td{{padding:14px 20px;text-align:left;border-bottom:1px solid #e2e8f0;font-size:15px;}}
    .spec-table th{{background:#f8fafc;font-weight:600;color:#1e3a5f;width:35%;}}
    .spec-table td{{color:#475569;}}
    .features-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:32px;}}
    .feature-item{{padding:24px;background:#f8fafc;border-radius:12px;text-align:center;}}
    .feature-item h4{{color:#1e3a5f;margin-top:12px;margin-bottom:8px;}}
    .feature-item p{{font-size:14px;color:#475569;}}
    .back-link{{display:inline-flex;align-items:center;gap:8px;color:rgba(255,255,255,0.7);text-decoration:none;font-weight:500;margin-bottom:24px;}}
    .back-link:hover{{color:#e8a838;}}
    .cta-bar{{padding:60px 24px;background:#1e3a5f;text-align:center;color:white;}}
    .cta-bar h2{{font-size:28px;margin-bottom:16px;}}
    .cta-bar p{{opacity:0.8;margin-bottom:24px;}}
    @media(max-width:768px){{.product-hero-inner{{grid-template-columns:1fr;}}.features-grid{{grid-template-columns:1fr;}}}}
  </style>
</head>
<body>
<nav class="nav" id="nav">
  <div class="nav-inner">
    <a href="../index.html" class="nav-logo"><div class="nav-logo-icon">QY</div><div class="nav-logo-text">QiaYun<span>Power</span></div></a>
    <ul class="nav-links" id="navLinks">
      <li><a href="../index.html" data-i18n="nav_home">Trang chủ</a></li>
      <li><a href="../index.html#products" data-i18n="nav_products">Sản phẩm</a></li>
      <li><a href="../index.html#solutions" data-i18n="nav_solutions">Giải pháp</a></li>
      <li><a href="../index.html#about" data-i18n="nav_about">Về chúng tôi</a></li>
      <li><a href="../index.html#contact" data-i18n="nav_contact">Liên hệ</a></li>
      <li><div class="lang-switcher">
        <button class="lang-option" data-lang="vi" onclick="setLang('vi')">VI</button>
        <button class="lang-option" data-lang="zh" onclick="setLang('zh')">中</button>
        <button class="lang-option" data-lang="en" onclick="setLang('en')">EN</button>
        <button class="lang-option" data-lang="th" onclick="setLang('th')">TH</button>
      </div></li>
    </ul>
    <button class="mobile-toggle" onclick="document.getElementById('navLinks').classList.toggle('open')"><span></span><span></span><span></span></button>
  </div>
</nav>

<section class="product-hero">
  <div class="product-hero-inner">
    <div>
      <a href="../index.html#products" class="back-link" data-i18n="product_back">← Quay lại sản phẩm</a>
      <h1 data-i18n="{i18n_name}">{title}</h1>
      <p class="subtitle" data-i18n="{i18n_desc}"></p>
      <div class="product-tags" style="margin-bottom:24px;">
        {tags_html}
      </div>
      <a href="../index.html#contact" class="btn-primary" data-i18n="product_inquiry">Yêu cầu báo giá</a>
    </div>
    <div class="product-hero-img">{svg}</div>
  </div>
</section>

<section class="spec-section">
  <div class="spec-inner">
    <h2 style="font-size:28px;font-weight:700;color:#1e3a5f;">Technical Specifications</h2>
    <table class="spec-table">
      {spec_rows}
    </table>
    <h2 style="font-size:28px;font-weight:700;color:#1e3a5f;margin-top:60px;">Features</h2>
    <div class="features-grid">
      {features_html}
    </div>
  </div>
</section>

<section class="cta-bar">
  <h2>Interested in this product?</h2>
  <p>Contact us for detailed specifications, pricing, and delivery information.</p>
  <a href="../index.html#contact" class="btn-primary" data-i18n="product_inquiry">Yêu cầu báo giá</a>
</section>

<footer class="footer">
  <div class="footer-bottom" style="border:none;margin:0;">
    <span data-i18n="footer_rights">© 2026 QiaYun Power. Bảo lưu mọi quyền.</span>
  </div>
</footer>

<script src="../js/i18n.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {{
  initI18n();
  window.addEventListener('scroll', () => {{
    document.getElementById('nav').classList.toggle('scrolled', window.scrollY > 10);
  }});
}});
</script>
</body>
</html>'''

for p in products:
    tags_html = '\n        '.join(f'<span class="product-tag" style="background:rgba(255,255,255,0.15);color:white;">{t}</span>' for t in p["tags"])
    spec_rows = '\n      '.join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in p["specs"])
    features_html = '\n      '.join(f'<div class="feature-item"><div style="font-size:36px;">{icon}</div><h4>{title}</h4><p>{desc}</p></div>' for icon, title, desc in p["features"])

    html = template.format(
        title=p["title"],
        i18n_name=p["i18n_name"],
        i18n_desc=p["i18n_desc"],
        tags_html=tags_html,
        svg=p["svg"],
        spec_rows=spec_rows,
        features_html=features_html,
    )

    filepath = os.path.join(os.path.dirname(__file__), p["file"])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated: {p['file']}")

print("Done! All product pages generated.")
