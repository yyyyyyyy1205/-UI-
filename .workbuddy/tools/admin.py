import json, os, shutil, subprocess

EDSDK = r"E:\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\tencent-local-office-edit\edsdk.py"
PY = r"C:\Users\源\.workbuddy\binaries\python\versions\3.13.12\python.exe"
DOC = r"D:\cxdownload\02 实验二：Vue组件化开发（学号+姓名）.doc"
BAK = r"D:\cxdownload\02 实验二：Vue组件化开发（学号+姓名）-模板备份.doc"


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


if os.environ.get("ACTION") == "reset":
    print(call("close_file", {"file_id": os.environ["FID"]}))
    shutil.copy2(BAK, DOC)
    print("restored")
    r = call("open_file", {"file_path": DOC})
    print(json.dumps(r, ensure_ascii=False))
