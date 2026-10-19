import json, os, struct, subprocess

EDSDK = r"E:\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\tencent-local-office-edit\edsdk.py"
PY = r"C:\Users\源\.workbuddy\binaries\python\versions\3.13.12\python.exe"
FID = "f85a09a3-14f2-4c02-8970-e1be72b6e6c3"
SHOTS = r"E:\新建文件夹\exp2-vue\.workbuddy\exp2-report\screenshots"
REPORT = r"E:\新建文件夹\exp2-vue\.workbuddy\exp2-report"
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    LOG.append(s)
    print(s, flush=True)


def call(tool, args):
    p = subprocess.run([PY, EDSDK, "call", tool, "--json", json.dumps(args)],
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
        j = out.rfind("}")
        return json.loads(out[i:j + 1])


def find_one(text):
    r = call("doc_find", {"file_id": FID, "text": text})
    locs = r.get("locations", [])
    if not locs:
        raise RuntimeError(f"not found: {text}")
    return locs[0]["begin"], locs[0]["end"]


def png_size(path):
    with open(path, "rb") as f:
        d = f.read(33)
    return struct.unpack(">II", d[16:24])


MAXW = 440


def dims(path):
    w, h = png_size(path)
    if w > MAXW:
        h = round(h * MAXW / w)
        w = MAXW
    return w, h


# ---- A. reset result cell to a marker ----
call("doc_set_table_cells", {"file_id": FID, "table_id": "bhxsj4o1",
                             "cells": [{"row": 15, "col": 2, "text": "RESANCHOR"}]})
log("A reset ok")

# ---- B. insert markdown at marker ----
b, e = find_one("RESANCHOR")
call("doc_insert_markdown", {"file_id": FID, "idx": b,
                             "markdown": "file://" + os.path.join(REPORT, "md_result.md")})
log("B markdown ok")

# ---- C. delete marker paragraph ----
b, e = find_one("RESANCHOR")
call("doc_delete_paragraph", {"file_id": FID, "idx": b})
log("C marker removed")

# ---- D. format result region ----
b1, _ = find_one("一、Vue 工程迁移与页面运行验证")
_, e2 = find_one("体会到组件化开发在可维护性与复用性上的优势。")
call("doc_update_text_property",
     {"file_id": FID, "ranges": [{"begin": b1, "end": e2}],
      "font_family": "方正仿宋_GBK", "font_size": 12, "color": "000000"})
log("D format ok", b1, e2)

# ---- E. insert images ----
IMGS = [("IMG_SLOT_1", "01-overview.png"), ("IMG_SLOT_2", "02-tree.png"),
        ("IMG_SLOT_3", "07-dark.png"), ("IMG_SLOT_4", "02-search.png"),
        ("IMG_SLOT_5", "04-edit.png"), ("IMG_SLOT_6", "05-detail.png"),
        ("IMG_SLOT_7", "06-source.png")]
for slot, fname in reversed(IMGS):
    path = os.path.join(SHOTS, fname)
    w, h = dims(path)
    b, e = find_one(slot)
    call("doc_insert_image", {"file_id": FID, "idx": b, "image_path": path, "w": w, "h": h})
    b2, e2 = find_one(slot)
    call("doc_replace_text", {"file_id": FID, "ranges": [{"begin": b2, "end": e2}], "text": ""})
    log(f"E image {fname} {w}x{h} ok")

# ---- F. remove 14 blank paragraphs before 第二次实验 (row14) ----
ANCHOR = "第二次实验（项目展示页面）设计与实现："
b0, _ = find_one(ANCHOR)
removed = 0
for i in range(14):
    call("doc_delete_paragraph", {"file_id": FID, "idx": b0 - 1})
    b1, _ = find_one(ANCHOR)
    if b1 == b0 - 1:
        removed += 1
        b0 = b1
    else:
        log(f"F WARN: expected -1 shift, got {b1} vs {b0}; stop at {removed}")
        b0 = b1
        break
log(f"F removed {removed} blank paragraphs")

# ---- G. format row14 markdown region ----
b1, _ = find_one(ANCHOR)
_, e2 = find_one("避免受父容器 overflow 与层叠上下文影响。")
call("doc_update_text_property",
     {"file_id": FID, "ranges": [{"begin": b1, "end": e2}],
      "font_family": "方正仿宋_GBK", "font_size": 12, "color": "000000"})
log("G format ok", b1, e2)

with open(os.path.join(REPORT, "fill2.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(LOG))
print("ALL DONE")
