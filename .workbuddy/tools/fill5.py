import json, os, subprocess, zipfile

EDSDK = r"E:\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\tencent-local-office-edit\edsdk.py"
PY = r"C:\Users\源\.workbuddy\binaries\python\versions\3.13.12\python.exe"
DOC = r"D:\cxdownload\02 实验二：Vue组件化开发（学号+姓名）.doc"
FID = DOC


def call(tool, args=None):
    p = subprocess.run([PY, EDSDK, "call", tool, "--json", json.dumps(args or {})],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (p.stdout or "").strip()
    if p.returncode != 0:
        raise RuntimeError(f"{tool} rc={p.returncode}\nOUT:{out}\nERR:{p.stderr}")
    i = out.find("{")
    if i < 0:
        return out
    try:
        return json.loads(out[i:])
    except Exception:
        return json.loads(out[i:out.rfind("}") + 1])


def fr(text):
    r = call("doc_find", {"file_id": FID, "text": text})
    l = r["locations"][0]
    return l["begin"], l["end"]


b1, _ = fr("页面迁移与组件拆分：")
_, e2 = fr("三段式结构。")
print("range", b1, e2)
r = call("doc_update_text_property",
         {"file_id": FID, "ranges": [{"begin": b1, "end": e2}], "color": "000000"})
print("recolor ->", json.dumps(r, ensure_ascii=False)[:200])

x = zipfile.ZipFile(DOC).read("word/document.xml").decode("utf-8")
for k in ["（1）main.js", "第二次实验（项目展示页面）", "一、Vue 工程迁移", "解释关键代码的作用"]:
    print(k, x.count(k))
call("save_file", {"file_id": FID})
print("saved")
