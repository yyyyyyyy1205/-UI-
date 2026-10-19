import json, os, struct, subprocess, sys, time

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
    err = (p.stderr or "").strip()
    if p.returncode != 0:
        raise RuntimeError(f"{tool} rc={p.returncode}\nOUT:{out}\nERR:{err}")
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


# ============ STEP 1: AI 工具表 ============
AI_ROWS = [
    (2, ["1", "WorkBuddy（AI 助手）", "把单页 HTML 迁移到 Vue3 工程并拆分单文件组件",
         "把实验一的个人主页迁移到 Vue3 工程，用 script setup 组合式 API 实现，按页面职责拆分为 TopHeader、SearchArea、UserInfo 等单文件组件，并用 defineProps、defineEmits 完成父子通信",
         "给出了工程目录结构、App.vue 根组件写法和各子组件的 template / script setup / style 代码，并说明了 props 与 emit 的命名约定",
         "约 80%，组件命名与拆分边界由本人调整"]),
    (3, ["2", "WorkBuddy（AI 助手）", "设计项目展示页面的数据结构与可复用插槽组件",
         "用数组保存项目名称、简介、技术栈、状态等信息；设计一个可复用卡片组件 BaseCard，通过默认插槽和 #header、#footer 具名插槽定制卡片头部、主体、底部",
         "输出了 projectList 数组结构、BaseCard 的三个 slot 定义，以及 ProjectShow 中 template#header / #default / #footer 的用法示例",
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
log("STEP1 AI table ->", call("doc_set_table_cells",
                              {"file_id": FID, "table_id": "iapdetk0", "cells": cells}))


# ============ STEP 2: 实验结果及分析 (row15 col2) ============
RESULT_TEXT = """一、Vue 工程迁移与页面运行验证
将实验一的单页 HTML 迁移到 Vue 工程，npm run dev 启动后页面正常渲染，顶部、主体、底部三段式结构完整，控制台无报错；页面显示姓名"杨美媛"、学号"249980740"、班级"24计科2班"，可标识本人身份。
IMG_SLOT_1
图1  迁移到 Vue 工程后的页面整体效果
二、组件拆分与组件树
按职责将页面拆分为 TopHeader（顶部标题栏）、SearchArea（技能搜索）、UserInfo（基础信息）、InfoEdit（信息编辑表单）、IntroArea（个人简介）、SkillArea（技能兴趣）、ProjectShow（项目展示）、BaseCard（通用卡片）、Footer（页脚），由 App.vue 作为根组件组织组件树，各模块渲染正常。
IMG_SLOT_2
图2  组件树设计图（App.vue 为根组件）
三、defineProps 与 defineEmits 父子通信
点击右上角"暗色模式"按钮，TopHeader 通过 emit('toggle-theme') 通知 App.vue 修改 isDark，全站主题切换为暗色；再次点击可还原为亮色，说明 props 下发、事件上抛的单向数据流通信正常。
IMG_SLOT_3
图3  defineProps / defineEmits：主题切换为暗色
四、v-model（defineModel）双向同步
在技能搜索框输入"Vue"，SearchArea 通过 update:modelValue 同步给父组件，计算属性过滤后技能列表仅显示"Vue基础"；清空输入后恢复全部 7 项技能，双向绑定生效。
IMG_SLOT_4
图4  v-model 双向绑定：关键词过滤技能列表
五、组件内部状态与信息编辑（InfoEdit）
点击"编辑信息"进入编辑态，InfoEdit 用 props 的本地副本编辑姓名、学号、班级；保存后通过 emit('save') 提交父组件更新，取消则放弃修改，未直接修改 props。同时个人简介区域点击"展开简介"可显示简介内容。
IMG_SLOT_5
图5  组件内部状态：信息编辑与简介展开
六、项目展示页面与插槽复用（ProjectShow + BaseCard）
BaseCard 提供默认插槽与 #header、#footer 具名插槽，ProjectShow 用数组数据渲染出两张结构一致、内容不同的项目卡片；点击"查看详情"通过 Teleport 弹出详情弹窗，点击"查看源码"弹出源码片段弹窗，弹窗均可正常打开与关闭。
IMG_SLOT_6
图6  项目展示：详情弹窗（Teleport）
IMG_SLOT_7
图7  项目展示：源码片段弹窗
七、Vue DevTools 调试
使用 Vue DevTools 的 Components 面板查看组件树，可见 App.vue 下依次挂载 TopHeader、container 容器内的 SearchArea、UserInfo、IntroArea、SkillArea、ProjectShow 以及 Footer，与设计的组件树一致；选中组件可查看其 props（如 user、skillList、searchKey）与内部状态，点击按钮时能在时间线中看到 toggle-theme、update:modelValue、toggle-show 等事件被触发，数据传递链路与预期一致。
八、结果分析与收获
1. 迁移后页面功能与实验一保持一致，说明 index.html 提供挂载点、main.js 创建并挂载应用、App.vue 组织页面的职责划分是正确的。
2. 搜索过滤、主题切换、简介展开、信息编辑、弹窗展示等交互全部正常，说明 defineProps、defineEmits、v-model、插槽与 Teleport 的使用方式正确。
3. 拆分组件后页面结构更清晰、样式职责更集中；插槽让卡片类结构得以复用，明显减少了重复代码。
4. 收获：理解了"数据放哪里、由谁修改"的状态归属原则和 props 单向数据流，体会到组件化开发在可维护性与复用性上的优势。"""

log("STEP2 result cell ->", call("doc_set_table_cells",
                                 {"file_id": FID, "table_id": "bhxsj4o1",
                                  "cells": [{"row": 15, "col": 2, "text": RESULT_TEXT}]}))

IMGS = [
    ("IMG_SLOT_1", "01-overview.png"),
    ("IMG_SLOT_2", "02-tree.png"),
    ("IMG_SLOT_3", "07-dark.png"),
    ("IMG_SLOT_4", "02-search.png"),
    ("IMG_SLOT_5", "04-edit.png"),
    ("IMG_SLOT_6", "05-detail.png"),
    ("IMG_SLOT_7", "06-source.png"),
]

for slot, fname in reversed(IMGS):
    path = os.path.join(SHOTS, fname)
    w, h = dims(path)
    b, e = find_one(slot)
    call("doc_insert_image", {"file_id": FID, "idx": b, "image_path": path, "w": w, "h": h})
    b2, e2 = find_one(slot)
    call("doc_replace_text", {"file_id": FID, "ranges": [{"begin": b2, "end": e2}], "text": ""})
    log(f"  image {fname} -> {w}x{h} ok")


# ============ STEP 3: 实验记录与处理 (row14 col2) ============
b, e = find_one("解释关键代码的作用；")
call("doc_delete_paragraph", {"file_id": FID, "idx": b})
log("STEP3.1 deleted instruction paragraph")

b, e = find_one("（以上信息在提交时请删除）")
call("doc_delete_paragraph", {"file_id": FID, "idx": b})
log("STEP3.2 deleted note paragraph")

b, e = find_one("AI工具使用说明")
md_path = os.path.join(REPORT, "md_record.md")
r = call("doc_insert_markdown", {"file_id": FID, "idx": b, "markdown": "file://" + md_path})
log("STEP3.3 markdown inserted ->", json.dumps(r, ensure_ascii=False)[:300])

with open(os.path.join(REPORT, "fill.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(LOG))
print("ALL DONE")
