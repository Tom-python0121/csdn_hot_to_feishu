import time
from csdn_spider import get_csdn_hot
from feishu_config import get_token, create_table, write_to_bitable


# =========================================================
# ⚙️ 配置
# =========================================================
SLEEP = 2  # 每个分类上传间隔（防止API限速）
CATEGORIES = ["CSDN", ]  # 可自行添加更多分类

# =========================================================
# 🚀 主逻辑
# =========================================================
if __name__ == "__main__":
    print("🔐 正在连接飞书API...")
    token = get_token()

    print("✅ 已成功获取飞书 token！\n")

    for category in CATEGORIES:
        print(f"🚀 正在抓取 CSDN 热榜分类：{category}")

        # 直接抓取前50条，不做任何过滤
        records = get_csdn_hot()
        if not records:
            print(f"❌ 没抓到 {category} 热榜数据，请检查爬虫模块返回。")
            continue

        print(f"✅ 成功抓取 {len(records)} 条 {category} 热榜数据。")

        # 创建或获取对应表格
        table_id = create_table(token, category)

        # 上传数据到飞书表格
        write_to_bitable(records, token, table_id)

        # 限速保护
        time.sleep(SLEEP)

    print("\n🎯 所有分类热榜数据已上传至飞书多维表格！")
