from flask import Flask, request, redirect, url_for, render_template_string
import json
import os

app = Flask(__name__)
DATA_FILE = "roles.json"

# 初始化数据文件
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

# 读取角色
def load():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 保存角色
def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# -------------------------- 主页 --------------------------
@app.route("/")
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>回响纪元</title>
    <style>
        body{background:#121212; color:white; padding:40px; text-align:center}
        .menu{margin-top:40px; display:flex; flex-direction:column; gap:14px; max-width:360px; margin:auto}
        .btn{background:#222; color:white; padding:18px; border-radius:12px; text-decoration:none}
        .btn:hover{background:#4285F4}
        img{width:200px; border-radius:12px}
    </style>
    </head>
    <body>
        <img src="logo.jpg">
        <h1>回响纪元</h1>
        <div class="menu">
            <a class="btn" href="/roles">角色档案</a>
            <a class="btn" href="/world">世界观</a>
            <a class="btn" href="/story">主线剧情</a>
            <a class="btn" href="/music">音乐库</a>
        </div>
    </body>
    </html>
    ''')

# -------------------------- 角色档案（完整功能） --------------------------
@app.route("/roles")
def roles():
    data = load()
    html = ""

    for i, item in enumerate(data):
        score = item["up"] - item["down"]
        if score < -3:
            continue

        html += f'''
        <div style="background:#222; padding:20px; margin:10px 0; border-radius:12px;">
            <h3>{item["name"]}</h3>
            <p>{item["content"]}</p>
            <p>评分：{score}</p>
            <a href="/up/{i}" style="color:green">👍 +1</a> |
            <a href="/down/{i}" style="color:red">👎 -1</a> |
            <a href="/delete/{i}" style="color:orange" onclick="return confirm('确定删除？')">🗑️ 删除</a>
        </div>
        '''

    return render_template_string(f'''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>角色档案</title>
    <style>
        body{{background:#121212; color:white; padding:20px}}
        .back{{color:#aaa}}
        .form{{background:#222; padding:20px; margin-top:20px; border-radius:12px}}
        input,textarea{{width:100%; padding:10px; margin:5px 0; background:#333; color:white; border:none; border-radius:6px}}
        button{{background:#4285F4; color:white; padding:10px 20px; border:none; border-radius:6px}}
    </style>
    </head>
    <body>
        <a class="back" href="/">← 返回主页</a>
        <h2>角色档案</h2>
        {html}

        <div class="form">
            <h3>发布新角色</h3>
            <form method="POST" action="/add">
                <input name="name" placeholder="角色名" required>
                <textarea name="content" placeholder="设定内容" required></textarea>
                <button type="submit">发布</button>
            </form>
        </div>
    </body>
    </html>
    ''')

# -------------------------- 功能：发布 --------------------------
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    content = request.form["content"]
    data = load()
    data.append({"name": name, "content": content, "up": 0, "down": 0})
    save(data)
    return redirect("/roles")

# -------------------------- 功能：点赞 +1 --------------------------
@app.route("/up/<int:i>")
def up(i):
    data = load()
    if 0 <= i < len(data):
        data[i]["up"] += 1
        save(data)
    return redirect("/roles")

# -------------------------- 功能：点踩 -1 --------------------------
@app.route("/down/<int:i>")
def down(i):
    data = load()
    if 0 <= i < len(data):
        data[i]["down"] += 1
        save(data)
    return redirect("/roles")

# -------------------------- 功能：删除 --------------------------
@app.route("/delete/<int:i>")
def delete(i):
    data = load()
    if 0 <= i < len(data):
        del data[i]
        save(data)
    return redirect("/roles")

# -------------------------- 其他页面 --------------------------
@app.route("/world")
def world():
    return render_template_string('''
    <body style="background:#121212;color:white;padding:20px">
        <a href="/">← 返回</a><h2>世界观设定</h2>
        <p>在这里填写世界体系、国家、历史等</p>
    </body>
    ''')

@app.route("/story")
def story():
    return render_template_string('''
    <body style="background:#121212;color:white;padding:20px">
        <a href="/">← 返回</a><h2>主线剧情</h2>
    </body>
    ''')

@app.route("/music")
def music():
    return render_template_string('''
    <body style="background:#121212;color:white;padding:20px">
        <a href="/">← 返回</a><h2>音乐库</h2>
        <audio controls src="bgm1.mp3"></audio>
    </body>
    ''')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)