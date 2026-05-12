#!/usr/bin/env python3
"""Rename and organize certificate images"""
import shutil, os

src = "/Users/honghaifeng/Desktop/haifeng/2026/98/20260331/qiayun/website/images"

certs = [
    ("恰云电力服务图册_p3_17.jpeg", "cert_business_license.jpg", "Business License / Giấy phép kinh doanh / 营业执照"),
    ("恰云电力服务图册_p3_16.jpeg", "cert_power_permit.jpg", "Power Installation Permit / Giấy phép lắp đặt điện / 电力设施许可证"),
    ("恰云电力服务图册_p3_1.jpeg", "cert_aaa_credit.jpg", "AAA Credit Rating / Xếp hạng tín dụng AAA / AAA信用等级"),
    ("恰云电力服务图册_p3_2.jpeg", "cert_quality_mgmt.jpg", "Quality Management System / Hệ thống quản lý chất lượng / 质量管理体系认证"),
    ("恰云电力服务图册_p3_3.jpeg", "cert_product_cert.jpg", "Product Certification / Chứng nhận sản phẩm / 产品认证证书"),
    ("恰云电力服务图册_p3_4.jpeg", "cert_integrity.jpg", "Integrity Certificate / Chứng nhận uy tín / 诚信证书"),
    ("恰云电力服务图册_p3_5.jpeg", "cert_safety_permit.jpg", "Safety Production Permit / Giấy phép an toàn / 安全生产许可"),
    ("恰云电力服务图册_p3_7.jpeg", "cert_enterprise_credit.jpg", "Enterprise Credit Rating / Xếp hạng tín dụng doanh nghiệp / 企业信用等级"),
    ("恰云电力服务图册_p3_8.jpeg", "cert_trustworthy.jpg", "Trustworthy Enterprise / Doanh nghiệp đáng tin cậy / 守信用企业"),
    ("恰云电力服务图册_p3_9.jpeg", "cert_contract_honor.jpg", "Contract Honor Certificate / Chứng nhận hợp đồng / 重合同守信用"),
    ("恰云电力服务图册_p3_10.jpeg", "cert_env_safety.jpg", "Environmental & Safety / Môi trường & An toàn / 环境安全认证"),
    ("恰云电力服务图册_p3_11.jpeg", "cert_credit_enterprise.jpg", "Credit Enterprise / Doanh nghiệp tín dụng / 信用企业"),
    ("恰云电力服务图册_p3_12.jpeg", "cert_honest_business.jpg", "AAA Honest Business / Doanh nghiệp kinh doanh trung thực AAA / AAA诚信经营示范单位"),
]

for old_name, new_name, desc in certs:
    old_path = os.path.join(src, old_name)
    new_path = os.path.join(src, new_name)
    if os.path.exists(old_path):
        shutil.copy2(old_path, new_path)
        print(f"  {new_name} <- {desc}")
    else:
        print(f"  MISSING: {old_name}")

print(f"\n{len(certs)} certificates prepared.")
