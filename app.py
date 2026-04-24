from flask import Flask, request, redirect, render_template_string
import json
import os

app = Flask(__name__)

# 四个数据文件
ROLES_FILE = "roles.json"
WORLD_FILE = "world.json"
STORY_FILE = "story.json"
MUSIC_FILE = "music.json"

# 初始化文件
for f in [ROLES_FILE, WORLD_FILE, STORY_FILE, MUSIC_FILE]:
    if not os.path.exists(f):
        with open(f, "w", encoding="utf-8") as fobj:
            json.dump([], fobj, ensure_ascii=False, indent=2)

# 通用读写
def load(f):
    with open(f, "r", encoding="utf-8") as fobj:
        return json.load(fobj)

def save(f, data):
    with open(f, "w", encoding="utf-8") as fobj:
        json.dump(data, fobj, ensure_ascii=False, indent=2)

# -------------------- 主页 --------------------
@app.route("/")
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>回响纪元</title>
<style>
    body{background:#121212;color:white;padding:40px;text-align:center;font-family:system-ui}
    .menu{max-width:360px;margin:40px auto;display:flex;flex-direction:column;gap:14px}
    .btn{background:#222;color:white;padding:18px;border-radius:12px;text-decoration:none}
    .btn:hover{background:#4285F4}
    img{width:200px;border-radius:12px}
</style>
</head>
<body>
    <img src="logo.jpg">
    <h1>回响纪元</h1>
    <div class="menu">
        <a class="btn" href="/roles">角色档案</a>
        <a class="btn" href="/world">世界观设定</a>
        <a class="btn" href="/story">主线剧情</a>
        <a class="btn" href="/music">原创音乐</a>
    </div>
</body>
</html>
''')

# -------------------- 角色档案（可编辑可删） --------------------
@app.route("/roles")
def roles():
    items = load(ROLES_FILE)
    html = ""
    for i, x in enumerate(items):
        s = x["up"] - x["down"]
        if s < -3: continue
        html += f'''
        <div style="background:#222;padding:20px;margin:10px 0;border-radius:12px">
            <h3>{x["name"]}</h3>
            <p>{x["content"]}</p>
            <p>评分：{s}</p>
            <a href="/vote/roles/{i}/up" style="color:green">👍+1</a> |
            <a href="/vote/roles/{i}/down" style="color:red">👎-1</a> |
            <a href="/del/roles/{i}" style="color:orange" onclick="return confirm('确定删除？')">🗑删除</a>
        </div>
        '''
    return render_template_string(f'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>角色档案</title>
<style>
    body{{background:#121212;color:white;padding:20px}}
    .back{{color:#aaa}}
    .form{{background:#222;padding:20px;margin:20px 0;border-radius:12px}}
    input,textarea{{width:100%;padding:10px;margin:5px 0;background:#333;color:white;border:none;border-radius:6px}}
    button{{background:#4285F4;color:white;padding:10px 20px;border:none;border-radius:6px}}
</style>
</head>
<body>
    <a class="back" href="/">← 返回主页</a>
    <h2>角色档案</h2>
    {html}
    <div class="form">
        <h3>发布新角色</h3>
        <form action="/add/roles" method="post">
            <input name="title" placeholder="名称" required>
            <textarea name="content" placeholder="详细设定" required></textarea>
            <button type="submit">发布</button>
        </form>
    </div>
</body>
</html>
''')

# -------------------- 世界观设定（所有人可编辑！） --------------------
@app.route("/world")
def world():
    items = load(WORLD_FILE)
    html = ""
    for i, x in enumerate(items):
        html += f'''
        <div style="background:#222;padding:20px;margin:10px 0;border-radius:12px">
            <h3>{x["title"]}</h3>
            <p>{x["content"]}</p>
            <a href="/del/world/{i}" style="color:orange" onclick="return confirm('确定删除？')">🗑删除</a>
        </div>
        '''
    return render_template_string(f'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>世界观设定</title>
<style>
    body{{background:#121212;color:white;padding:20px}}
    .back{{color:#aaa}}
    .form{{background:#222;padding:20px;margin:20px 0;border-radius:12px}}
    input,textarea{{width:100%;padding:10px;margin:5px 0;background:#333;color:white;border:none;border-radius:6px}}
    button{{background:#4285F4;color:white;padding:10px 20px;border:none;border-radius:6px}}
</style>
</head>
<body>
    <a class="back" href="/">← 返回主页</a>
    <h2>世界观设定</h2>
    {html}
    <div class="form">
        <h3>新增设定</h3>
        <form action="/add/world" method="post">
            <input name="title" placeholder="设定标题" required>
            <textarea name="content" placeholder="详细内容" required></textarea>
            <button type="submit">发布</button>
        </form>
    </div>
</body>
</html>
''')

# -------------------- 主线剧情（所有人可编辑！） --------------------
@app.route("/story")
def story():
    items = load(STORY_FILE)
    html = ""
    for i, x in enumerate(items):
        html += f'''
        <div style="background:#222;padding:20px;margin:10px 0;border-radius:12px">
            <h3>{x["title"]}</h3>
            <p>{x["content"]}</p>
            <a href="/del/story/{i}" style="color:orange" onclick="return confirm('确定删除？')">🗑删除</a>
        </div>
        '''
    return render_template_string(f'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>主线剧情</title>
<style>
    body{{background:#121212;color:white;padding:20px}}
    .back{{color:#aaa}}
    .form{{background:#222;padding:20px;margin:20px 0;border-radius:12px}}
    input,textarea{{width:100%;padding:10px;margin:5px 0;background:#333;color:white;border:none;border-radius:6px}}
    button{{background:#4285F4;color:white;padding:10px 20px;border:none;border-radius:6px}}
</style>
</head>
<body>
    <a class="back" href="/">← 返回主页</a>
    <h2>主线剧情</h2>
    {html}
    <div class="form">
        <h3>新增剧情</h3>
        <form action="/add/story" method="post">
            <input name="title" placeholder="章节/标题" required>
            <textarea name="content" placeholder="剧情内容" required></textarea>
            <button type="submit">发布</button>
        </form>
    </div>
</body>
</html>
''')

# -------------------- 原创音乐（所有人可编辑！） --------------------
@app.route("/music")
def music():
    items = load(MUSIC_FILE)
    html = ""
    for i, x in enumerate(items):
        html += f'''
        <div style="background:#222;padding:20px;margin:10px 0;border-radius:12px">
            <h3>{x["title"]}</h3>
            <p>{x["content"]}</p>
            <a href="/del/music/{i}" style="color:orange" onclick="return confirm('确定删除？')">🗑删除</a>
        </div>
        '''
    return render_template_string(f'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>原创音乐</title>
<style>
    body{{background:#121212;color:white;padding:20px}}
    .back{{color:#aaa}}
    .form{{background:#222;padding:20px;margin:20px 0;border-radius:12px}}
    input,textarea{{width:100%;padding:10px;margin:5px 0;background:#333;color:white;border:none;border-radius:6px}}
    button{{background:#4285F4;color:white;padding:10px 20px;border:none;border-radius:6px}}
</style>
</head>
<body>
    <a class="back" href="/">← 返回主页</a>
    <h2>原创音乐</h2>
    {html}
    <div class="form">
        <h3>新增音乐</h3>
        <form action="/add/music" method="post">
            <input name="title" placeholder="音乐名称" required>
            <textarea name="content" placeholder="介绍/链接/备注" required></textarea>
            <button type="submit">发布</button>
        </form>
    </div>
</body>
</html>
''')

# -------------------- 通用发布 --------------------
@app.route("/add/<mod>", methods=["POST"])
def add(mod):
    title = request.form["title"]
    content = request.form["content"]
    file = {
        "roles": ROLES_FILE,
        "world": WORLD_FILE,
        "story": STORY_FILE,
        "music": MUSIC_FILE
    }.get(mod)
    if not file: return "错误"
    data = load(file)
    if mod == "roles":
        data.append({"name": title, "content": content, "up": 0, "down": 0})
    else:
        data.append({"title": title, "content": content})
    save(file, data)
    return redirect(f"/{mod}")

# -------------------- 投票 --------------------
@app.route("/vote/roles/<int:i>/<typ>")
def vote_role(i, typ):
    data = load(ROLES_FILE)
    if 0 <= i < len(data):
        data[i][typ] += 1
        save(ROLES_FILE, data)
    return redirect("/roles")

# -------------------- 删除 --------------------
@app.route("/del/<mod>/<int:i>")
def delete(mod, i):
    file = {
        "roles": ROLES_FILE,
        "world": WORLD_FILE,
        "story": STORY_FILE,
        "music": MUSIC_FILE
    }.get(mod)
    data = load(file)
    if 0 <= i < len(data):
        del data[i]
        save(file, data)
    return redirect(f"/{mod}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
