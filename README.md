
---

# 🧠《CSDN热榜→飞书多维表格》项目学习笔记总结版

---

## 🧩 一、requests库 — 让Python和网络“对话”

> 📘 requests 是 Python 最常用的网络请求库，用来访问网页、API。

---

### 🌐 基本用法：

```python
import requests

# 1. 发送 GET 请求
response = requests.get("https://example.com")
print(response.text)   # 输出网页源码

# 2. 发送 POST 请求
data = {"name": "Tony", "age": 22}
res = requests.post("https://httpbin.org/post", json=data)
print(res.json())  # 将返回的JSON字符串解析成Python字典
```

---

### 💡 项目中哪里用到：

📍**获取CSDN网页内容**

```python
response = requests.get(url, headers=headers)
```

👉 获取热榜页面HTML内容，用于后续解析。

📍**访问飞书API**

```python
res = requests.post(url, json=payload, headers=headers)
```

👉 向飞书服务器发送请求（例如获取token、创建表格、上传数据）。

---

### 🔍 常见响应属性：

| 属性             | 含义                  | 示例                     |
| -------------- | ------------------- | ---------------------- |
| `.text`        | 获取原始文本（HTML源码）      | `response.text`        |
| `.json()`      | 把返回的JSON解析为Python字典 | `response.json()`      |
| `.status_code` | HTTP状态码（200表示成功）    | `response.status_code` |

---

### 📘 小贴士：

* API 调用几乎都用 `POST`，网页爬取多用 `GET`
* JSON 格式是“机器语言”，字典格式是“Python语言”，两者可互转

---

## 🕸️ 二、BeautifulSoup — 提取HTML中的数据

> 📘 BeautifulSoup 是网页解析库，可以从HTML中提取出想要的文字和链接。

---

### 🧩 基本用法：

```python
from bs4 import BeautifulSoup

html = "<h1>Hello, Python!</h1>"
soup = BeautifulSoup(html, "html.parser")
print(soup.h1.text)  # 输出：Hello, Python!
```

---

### 💡 项目中哪里用到：

```python
soup = BeautifulSoup(response.text, "html.parser")

for li in soup.select(".rank-list li"):  # 通过CSS选择器定位标签
    title = li.select_one(".title").get_text(strip=True)
```

📘 解释：

* `.select(".rank-list li")` ：找到所有 `<li>` 元素
* `.select_one(".title")` ：找到第一个 class 为 title 的标签
* `.get_text(strip=True)` ：提取文本并去掉空格

---

### 🌈 常用方法速查：

| 方法                      | 含义        | 示例                      |
| ----------------------- | --------- | ----------------------- |
| `.select(css选择器)`       | 找出所有匹配的元素 | `.select("div p")`      |
| `.select_one(css选择器)`   | 找第一个匹配的元素 | `.select_one(".title")` |
| `.get_text(strip=True)` | 提取文本内容    | `.get_text(strip=True)` |
| `[attr]`                | 提取属性值     | `a["href"]` 提取链接        |

---

### 🧠 学到的概念：

* “HTML标签”就像Excel单元格，BeautifulSoup帮你读取其中的内容。
* CSS选择器语法和网页前端是一致的：`.class`, `#id`, `tagname`。

---

## 📦 三、Python 字典 dict 与 JSON 的关系

> 📘 dict 是 Python 内置数据结构，JSON 是网络传输格式。
> requests 在发送数据时自动帮你把 dict → JSON。

---

### 🔁 互相转换示例：

```python
import json

# Python字典
data = {"name": "Tony", "age": 18}

# 转为JSON字符串
json_str = json.dumps(data)

# JSON字符串转回字典
py_dict = json.loads(json_str)
```

---

### 💡 项目中哪里用到：

📍**构造创建表格的请求体**

```python
payload = {
    "table": {
        "name": f"{keyword}热榜",
        "fields": [
            {"field_name": "标题", "type": "text"},
            {"field_name": "链接", "type": "url"},
            {"field_name": "阅读量", "type": "text"}
        ]
    }
}
```

📘 解释：

* `dict` 嵌套 `list` 是 JSON 的常见结构
* Python 代码 → JSON → 飞书 API
* `f"{keyword}热榜"` 是 **f-string 动态字符串语法**

---

### 📊 对照表：

| Python类型  | JSON类型  | 示例             |
| --------- | ------- | -------------- |
| dict      | object  | `{"a":1}`      |
| list      | array   | `[1,2,3]`      |
| str       | string  | `"Python"`     |
| int/float | number  | `100`          |
| bool      | boolean | `true / false` |

---

## 🧮 四、f-string — 动态字符串拼接

> 📘 f-string 是 Python3 的一种字符串格式化方式。

---

### 🌈 基本用法：

```python
name = "Python"
print(f"欢迎来到{name}世界！")
# 输出：欢迎来到Python世界！
```

---

### 💡 项目中哪里用到：

```python
"name": f"{keyword}热榜"
```

📘 意思：

* `keyword` 是变量（如 `"AI"`）
* `f"{keyword}热榜"` 会自动拼成 `"AI热榜"`

🧠 优点：

* 比传统 `"{}{}".format(a,b)` 更简洁直观。

---

## ⚙️ 五、YAML 配置文件与 yaml.safe_load()

> 📘 YAML 是一种比 JSON 更“人类可读”的配置格式。

---

### 🌈 基本用法：

```python
import yaml

with open("config.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
    print(data["feishu"]["app_id"])
```

---

### 💡 项目中哪里用到：

```python
CONFIG = yaml.safe_load(f)
APP_ID = CONFIG["feishu"]["app_id"]
```

📘 safe_load() 会把 config.yaml 文件转换成 Python 字典。
比如 YAML：

```yaml
feishu:
  app_id: "12345"
```

会变成：

```python
{"feishu": {"app_id": "12345"}}
```

---

## 🧰 六、模块化开发与函数封装

> 📘 Python 文件（.py）就是一个模块，函数封装让逻辑更清晰。

---

### 🌈 示例：

```python
# my_utils.py
def add(a, b):
    return a + b

# main.py
from my_utils import add
print(add(1, 2))
```

---

### 💡 项目中哪里用到：

📍模块划分结构：

| 模块                    | 功能    |
| --------------------- | ----- |
| `csdn_spider.py`      | 数据抓取  |
| `feishu_config.py`    | API交互 |
| `upload_to_feishu.py` | 主入口逻辑 |

📘 好处：

* 可读性高
* 易维护
* 方便复用

---

## 🧠 七、time.sleep() — 控制执行节奏

> 📘 防止频繁请求API被封。

---

### 示例：

```python
import time

for i in range(3):
    print("发送请求中…")
    time.sleep(2)  # 暂停2秒
```

📍项目中：

```python
time.sleep(SLEEP)
```

→ 每次上传后暂停 1 秒（config.yaml 控制）。

---

## 🧩 八、异常处理与调试

> 📘 捕获错误，防止程序崩溃。

---

### 示例：

```python
try:
    x = 1 / 0
except ZeroDivisionError:
    print("不能除以0！")
```

📍项目中：

```python
if not token:
    raise Exception("❌ 获取飞书token失败")
```

💡 raise Exception()
→ 主动抛出错误，让你在终端看到明确提示。

---

## 🎓 九、完整项目运行逻辑思维导图

```
用户输入关键词
       ↓
get_csdn_hot(keyword)
       ↓
requests.get() 抓取网页
       ↓
BeautifulSoup 提取标题、链接、阅读量
       ↓
create_or_get_table()  检查或创建表格
       ↓
write_to_bitable()     写入数据
       ↓
飞书API响应 → 数据进入多维表格
```

---

## 🎯 十、扩展建议

| 想提升方向   | 可学知识点                       |
| ------- | --------------------------- |
| 定时任务    | `schedule` 模块               |
| 数据分析    | `pandas`                    |
| 图表可视化   | `matplotlib`                |
| 飞书机器人通知 | 飞书Webhook                   |
| 自动更新脚本  | Windows 任务计划或 Linux crontab |

---

## ❤️ 总结一句话：

> **requests 是嘴，BeautifulSoup 是眼睛，dict 是大脑，飞书API 是世界。**
>
> 学会这套套路，你就能：
> 🧠 让 Python 读懂网页 → ✍️ 组织数据 → 🚀 调用接口 → 💾 自动入库

---