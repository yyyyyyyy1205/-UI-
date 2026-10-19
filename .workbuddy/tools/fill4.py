import json, os, subprocess, sys, zipfile

EDSDK = r"E:\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\tencent-local-office-edit\edsdk.py"
PY = r"C:\Users\源\.workbuddy\binaries\python\versions\3.13.12\python.exe"
DOC = r"D:\cxdownload\02 实验二：Vue组件化开发（学号+姓名）.doc"
FID = DOC
ANCHOR = "第二次实验（项目展示页面）设计与实现："


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


def find_begin(text):
    r = call("doc_find", {"file_id": FID, "text": text})
    return r["locations"][0]["begin"]


def counts():
    x = zipfile.ZipFile(DOC).read("word/document.xml").decode("utf-8")
    return {k: x.count(k) for k in ["（1）main.js", "第二次实验（项目展示页面）",
                                    "一、Vue 工程迁移", "解释关键代码的作用"]}


base = counts()
print("base counts:", base, flush=True)
assert all(v == 1 for v in base.values()), "unexpected base"

b0 = find_begin(ANCHOR)
print("anchor begin:", b0, flush=True)
removed = 0
for i in range(15):
    call("doc_delete_paragraph", {"file_id": FID, "idx": b0 - 1})
    b1 = find_begin(ANCHOR)
    c = counts()
    if b1 != b0 - 1 or any(v != 1 for v in c.values()):
        print(f"STOP at {i}: begin {b0}->{b1}, counts {c}", flush=True)
        b0 = b1
        break
    removed += 1
    b0 = b1
    print(f"  removed #{removed}, begin={b0}", flush=True)

print("removed total:", removed, flush=True)
call("save_file", {"file_id": FID})
print("saved; final counts:", counts(), flush=True)
