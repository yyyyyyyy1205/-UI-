import json, os, struct, subprocess, sys

EDSDK = r"E:\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\tencent-local-office-edit\edsdk.py"
PY = r"C:\Users\源\.workbuddy\binaries\python\versions\3.13.12\python.exe"
DOC = r"D:\cxdownload\02 实验二：Vue组件化开发（学号+姓名）.doc"
SHOTS = r"E:\新建文件夹\exp2-vue\.workbuddy\exp2-report\screenshots"
REPORT = r"E:\新建文件夹\exp2-vue\.workbuddy\exp2-report"
FID = DOC
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    LOG.append(s)
    print(s, flush=True)


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


def find_all(text):
    r = call("doc_find", {"file_id": FID, "text": text})
    return r.get("locations", [])


def find_one(text):
    locs = find_all(text)
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


tables = call("doc_list_tables", {"file_id": FID})["tables"]
MAIN_TID = next(t["table_id"] for t in tables if "姓名" in t["first_row_texts"][0])
AI_TID = next(t["table_id"] for t in tables if "AI工具名称" in "".join(t["first_row_texts"]))
log("tables:", MAIN_TID, AI_TID)

AI_ROWS = [
    (2, ["1", "WorkBuddy（AI 助手）", "把单页 HTML 迁移到 Vue3 工程并拆分单文件组件",
         "把实验一的个人主页迁移到 Vue3 工程，用 script setup 组合式 API 实现，按页面职责拆分为 TopHeader、SearchArea、UserInfo 等单文件组件，并用 defineProps、defineEmits 完成父子通信",
         "给出了工程目录结构、App.vue 根组件写法和各子组件的 template / script setup / style 代码，并说明了 props 与 emit 的命名约定",
         "约 80%，组件命名与拆分边界由本人调整"]),
    (3, ["2", "WorkBuddy（AI 助手）", "设计项目展示页面的数据结构与可复用插槽组件",
         "用数组保存项目名称、简介、技术栈、状态等信息；设计一个可复用卡片组件 BaseCard，通过默认插槽和 header、footer 具名插槽定制卡片头部、主体、底部",
         "输出了 projectList 数组结构、BaseCard 的三个 slot 定义，以及 ProjectShow 中 template#header、#default、#footer 的用法示例",
         "约 70%，字段设计与卡片样式由本人补充"]),
    (4, ["3", "WorkBuddy（AI 助手）", "排查运行问题并解释 v-model 双向绑定原理",
         "SearchArea 输入框搜索不生效，请说明 v-model:search-key（defineModel）的双向绑定流程，以及如何用 Vue DevTools 检查组件 props、状态和事件",
         "解释了 v-model:search-key 等价于传入 modelValue 并监听 update:modelValue 事件，并给出用 DevTools 查看组件树、props 与事件时间线的操作步骤",
         "约 90%，按提示定位后由本人修改代码"]),
]
cells = []
for row, vals in AI_ROWS:
    for col, v in enumerate(vals, start=1):
        cells.append({"row": row, "col": col, "text": v})
log("AI table ->", call("doc_set_table_cells",
                        {"file_id": FID, "table_id": AI_TID, "cells": cells}))

# ---- result cell: clear to marker, insert markdown, drop marker ----
call("doc_set_table_cells", {"file_id": FID, "table_id": MAIN_TID,
                             "cells": [{"row": 15, "col": 2, "text": "RESANCHOR"}]})
b, e = find_one("RESANCHOR")
call("doc_insert_markdown", {"file_id": FID, "idx": b,
                             "markdown": "file://" + os.path.join(REPORT, "md_result.md")})
b, e = find_one("RESANCHOR")
call("doc_delete_paragraph", {"file_id": FID, "idx": b})
log("result cell markdown ok")

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
    log(f"image {fname} {w}x{h} ok")

# ---- record cell: replace instruction, insert markdown ----
b, e = find_one("解释关键代码的作用；")
call("doc_delete_paragraph", {"file_id": FID, "idx": b})
b, e = find_one("（以上信息在提交时请删除）")
call("doc_delete_paragraph", {"file_id": FID, "idx": b})
b, e = find_one("AI工具使用说明")
call("doc_insert_markdown", {"file_id": FID, "idx": b,
                             "markdown": "file://" + os.path.join(REPORT, "md_record.md")})
log("record cell markdown ok")

call("save_file", {"file_id": FID})
log("saved phase1")

with open(os.path.join(REPORT, "fill3.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(LOG))
print("PHASE1 DONE")
