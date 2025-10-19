import requests, yaml, json

# =============================
# 读取配置
# =============================
with open("config.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

APP_ID = CONFIG["feishu"]["app_id"]
APP_SECRET = CONFIG["feishu"]["app_secret"]
APP_TOKEN = CONFIG["feishu"]["app_token"]

# =============================
# 获取 token
# =============================
def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    data = {"app_id": APP_ID, "app_secret": APP_SECRET}
    res = requests.post(url, json=data).json()
    if res.get("code") != 0:
        raise Exception(res)
    print("✅ 获取飞书 Token 成功")
    return res["tenant_access_token"]

# =============================
# 创建表格（自动复用）
# =============================
def create_table(token, table_name):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "table": {
            "name": table_name,
            "fields": [
                {"field_name": "标题", "type": 1},
                {"field_name": "链接", "type": 11},
                {"field_name": "阅读量", "type": 1}
            ]
        }
    }
    res = requests.post(url, headers=headers, json=payload).json()
    print("📦 创建表格返回：", json.dumps(res, ensure_ascii=False, indent=2))

    # ✅ 如果表名重复则自动复用
    if res.get("code") == 1254013:
        print(f"⚠️ 表 {table_name} 已存在，自动复用。")
        tables = list_tables(token)
        for t in tables:
            if t["name"] == table_name:
                print(f"✅ 复用表格 ID: {t['table_id']}")
                return t["table_id"]

    # ✅ 创建成功
    if res.get("code") == 0:
        return res["data"]["table_id"]

    raise Exception(f"❌ 创建表失败：{res}")

# =============================
# 获取当前已有表格列表
# =============================
def list_tables(token):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers).json()
    if res.get("code") == 0:
        return [{"table_id": t["table_id"], "name": t["name"]} for t in res["data"]["items"]]
    return []

# =============================
# 上传记录
# =============================
def write_to_bitable(records, token, table_id):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{table_id}/records/batch_create"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    data = {"records": []}
    for r in records:
        data["records"].append({
            "fields": {
                "标题": r.get("标题", ""),
                "链接": {"text": r.get("标题", ""), "link": r.get("链接", "")},   #需要手动把字符类型设置为超链接，代码没有作用，后面研究
                "阅读量": r.get("阅读量", "")
            }
        })

    res = requests.post(url, headers=headers, json=data).json()
    print("📤 上传结果：", json.dumps(res, ensure_ascii=False, indent=2))

    if res.get("code") == 0:
        print("✅ 上传成功")
    else:
        raise Exception(f"❌ 上传失败：{res}")
