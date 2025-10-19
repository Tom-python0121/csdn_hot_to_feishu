"""
csdn_spider.py
--------------
🔥 最终稳定版：自动识别 CSDN 热榜接口返回结构（兼容 list / dict / 嵌套）
"""

import requests


def get_csdn_hot():
    """
    获取 CSDN 全站热榜前 50 条。
    自动判断返回结构类型。
    """
    url = "https://blog.csdn.net/phoenix/web/blog/hotRank?page=0&pageSize=50"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://blog.csdn.net/",
        "Accept": "application/json, text/plain, */*"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("❌ 请求或解析失败：", e)
        print("响应内容：", response.text[:300])
        return []

    # ✅ 自动判断结构
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        # 有些版本是 {"data": [...]} 或 {"data": {"list": [...]}}
        if isinstance(data.get("data"), list):
            items = data["data"]
        elif isinstance(data.get("data"), dict):
            items = data["data"].get("list", [])
        else:
            items = []
    else:
        print("⚠️ 未知返回结构类型：", type(data))
        items = []

    # ✅ 提取字段
    results = []
    for item in items:
        title = item.get("articleTitle", "")
        link = item.get("articleDetailUrl", "")
        read = item.get("viewCount", item.get("readCount", 0))
        results.append({
            "标题": title,
            "链接": link,
            "阅读量": str(read)
        })

    print(f"✅ 成功抓取 {len(results)} 条 CSDN 热榜数据。")
    return results
