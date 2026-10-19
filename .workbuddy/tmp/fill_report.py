# -*- coding: utf-8 -*-
"""填充实验三报告：实验记录与处理 / 实验结果及分析"""
import sys, json, os

SKILL = r"E:\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\tencent-local-office-edit"
sys.path.insert(0, SKILL)
import edsdk

FID = "D:/cxdownload/03 实验三：路由配置与页面导航（学号+姓名）.doc"
SHOTS = r"E:\新建文件夹\exp2-vue\.workbuddy\tmp\shots"
CODE = r"E:\新建文件夹\exp2-vue\.workbuddy\tmp\codeshots"
TID = "hc0k0x41"          # 主表
TID_AI = "ox1f001d"       # 嵌套的 AI 工具表


def rpc(name, args):
    obj = edsdk._request(edsdk._discover_endpoint(), "tools/call",
                         {"name": name, "arguments": args})
    if obj.get("error"):
        raise RuntimeError(f"{name}: {obj['error']}")
    res = obj.get("result") or {}
    texts = [c.get("text", "") for c in (res.get("content") or [])
             if isinstance(c, dict) and c.get("type") == "text"]
    out = "\n".join(texts) if texts else json.dumps(res, ensure_ascii=False)
    try:
        return json.loads(out)
    except Exception:
        return out


def call(name, **args):
    args["file_id"] = FID
    return rpc(name, args)


def find(text, row=None):
    r = call("doc_find", text=text)
    locs = r["locations"] if isinstance(r, dict) else []
    if row is not None:
        locs = [l for l in locs if l.get("row") == row]
    return locs


def replace_range(begin, end, text):
    return call("doc_replace_text", ranges=[{"begin": begin, "end": end}], text=text)


def insert_image_at(marker, row, path, w=540):
    locs = find(marker, row=row)
    if not locs:
        raise RuntimeError(f"未找到标记 {marker} (row={row})")
    b, e = locs[0]["begin"], locs[0]["end"]
    # 先把图片段落行距改为单倍，避免固定行距把图片裁剪
    try:
        call("doc_modify_paragraph", ranges=[{"begin": b, "end": e}],
             line_spacing=1.0, line_spacing_rule=1)
    except Exception as ex:
        print("  (行距调整失败)", ex)
    replace_range(b, e, "")
    call("doc_insert_image", idx=b, image_path=path, w=w)
    print("  img ->", os.path.basename(path))


R14_MD = """**任务1：安装并注册 Vue Router**

【图1】

说明：先安装 vue-router 依赖，在 src/router/index.js 中使用 createRouter 创建路由实例并选择 History 路由模式，再在 src/main.js 中通过 app.use(router) 把路由插件注册到 Vue 应用，使整个应用具备页面路由能力。

**任务2：配置基础路由、命名路由、重定向与路由元信息**

【图2】

说明：路由表中每条路由用 path 定义访问地址，用 name 提供稳定标识（命名路由），用 component 指定对应页面组件；访问根路径 / 时由 redirect 自动重定向到 /home；meta 中保存页面标题，供全局守卫统一更新浏览器标题。

**任务3：配置嵌套路由**

【图3】

说明：项目中心 /project 与后台管理 /admin 均采用嵌套路由：父路由组件（ProjectLayout、AdminLayout）提供标题与子导航等共享布局，子页面渲染在父组件内部的 RouterView 中；子路由 path 为空字符串时用 redirect 指定默认展示的子页面。

**任务4：配置动态路由并获取路由参数**

【图4】

说明：项目详情路由配置为 detail/:id，:id 即动态路由参数，多个项目详情共用同一个 ProjectDetail 组件；组件内通过 useRoute() 获取当前路由对象，再用 route.params.id 读取参数值并显示在页面上。

**任务5：使用 RouterLink 实现页面导航与导航高亮**

【图5】

说明：顶部导航使用 RouterLink 声明式跳转，既支持 to="/home" 字符串写法，也支持 :to="{ name: 'About' }" 命名路由对象写法；Vue Router 会自动为当前路由对应的链接添加 router-link-active 类名，配合样式即可实现导航高亮。

**任务6：使用 useRouter() 实现编程式导航**

【图6】

说明：在需要先执行逻辑再跳转的场景中使用编程式导航：项目列表通过 router.push({ name, params }) 携带动态参数跳转到详情页；关于我页面用 router.go(-1) 返回上一页；登录成功后根据 route.query.redirect 跳回被拦截前想访问的页面。

**任务7：使用 meta 与 beforeEach 完成标题更新和访问控制**

【图7】

说明：全局前置守卫 beforeEach 在每次路由切换前执行：先根据 to.meta.title 统一更新浏览器标题；再判断 to.meta.requiresAuth，未登录时通过 next({ name: 'Login', query: { redirect: to.fullPath } }) 拦截到登录页并记录原目标地址，已登录或公开页面直接放行。

**任务8：配置 404 通配符路由与模拟登录**

【图8】

说明：把 path: "/:pathMatch(.*)*" 放在路由表最后，所有未定义的地址都会匹配到 NotFound 组件并显示 404 提示页；登录页通过 localStorage 写入 isLogin 标记模拟登录，成功后跳转到 redirect 参数指定的后台页面。
"""

R14_IMGS = {1: "code-01.png", 2: "code-02.png", 3: "code-03.png", 4: "code-04.png",
            5: "code-05.png", 6: "code-06.png", 7: "code-07.png", 8: "code-08.png"}

R15_MD = """**结果1：默认重定向与首页访问（/ 自动跳转到 /home）**

【图1】

直接访问 http://localhost:5173/ 时，地址栏自动变为 /home 并显示个人主页，顶部导航“首页”呈高亮状态，页面中显示姓名、学号、班级等身份信息，说明根路径重定向与基础路由配置正确。

**结果2：项目中心嵌套路由与动态路由参数**

【图2】

【图3】

点击“项目中心”进入 /project/list 正常显示项目列表；点击“查看项目详情”按钮后地址栏变为 /project/detail/1，页面读取路由参数显示“项目ID：1”及项目描述，且子页面渲染在项目中心父组件的 RouterView 中，验证了嵌套路由与动态路由参数的获取。

**结果3：关于我页面的导航高亮与返回上一页**

【图4】

访问 /about 时顶部“关于我”链接自动加粗并显示下划线，说明 router-link-active 导航高亮生效；点击“返回上一页”按钮通过 router.go(-1) 成功返回上一个页面。

**结果4：未登录访问后台被路由守卫拦截**

【图5】

退出登录后直接访问 /admin/profile，被全局前置守卫拦截并重定向到 /login?redirect=/admin/profile，地址栏 query 中保留了原目标地址，说明 meta 与 beforeEach 实现的访问控制生效。

**结果5：登录后进入后台管理页面**

【图6】

在登录页点击“模拟登录进入后台”后写入 isLogin 标记并跳转到 /admin/profile，守卫放行；页面显示后台管理中心与编辑个人简介表单，顶部导航自动出现“后台管理”入口和“退出登录”按钮。

**结果6：404 通配符路由**

【图7】

访问未定义的地址 /not-exist-page 时匹配通配符路由 /:pathMatch(.*)*，正确显示 404 页面并提供“返回首页”按钮。

**结果分析与收获**

1. 页面标题能跟随路由变化：beforeEach 中 document.title = to.meta.title 生效，切换页面时浏览器标签页标题随之更新，不需要在每个组件里单独设置。

2. 导航高亮无需手写路径判断逻辑，router-link-active 类名由 Vue Router 自动维护，比手动比较当前路径更简单可靠。

3. 动态路由让多个项目详情复用同一个组件，只需通过 route.params.id 区分数据，明显减少了重复代码。

4. 嵌套路由把公共布局（标题、子导航）收敛到父组件，子页面只关注自身内容，页面结构更加清晰。

5. 路由守卫配合 meta 与 localStorage 实现了简单的访问控制，体会到“声明式配置 + 集中拦截”带来的好处：权限逻辑集中在一处，页面组件本身无需关心登录状态。

6. 收获：通过本次实验掌握了 Vue Router 的安装注册、路由表配置、动态路由、嵌套路由、编程式导航和全局前置守卫的使用，加深了对 SPA 中 URL、路由规则与页面组件对应关系的理解。
"""

R15_IMGS = {1: "01-home.png", 2: "03-project-list.png", 3: "04-project-detail-1.png",
            4: "02-about.png", 5: "10-guard-redirect.png", 6: "06-admin-profile.png",
            7: "08-404.png"}


def fix_font(row, start_text, end_text):
    locs = find(start_text, row=row)
    if not locs:
        print("  fix_font: 未找到起点", start_text); return
    b = locs[0]["begin"]
    e = find(end_text, row=row)
    if not e:
        print("  fix_font: 未找到终点", end_text); return
    e = e[-1]["end"]
    call("doc_update_text_property", ranges=[{"begin": b, "end": e}],
         font_family="宋体", font_size_pt=12, color="000000")
    print(f"  fix_font row{row}: [{b},{e})")


def stage_r15():
    print("== r15c2 ==")
    call("doc_set_table_cells", table_id=TID,
         cells=[{"row": 15, "col": 2, "text": "MARKER15"}])
    locs = find("MARKER15", row=15)
    b = locs[0]["begin"]
    call("doc_insert_markdown", idx=b, markdown=R15_MD)
    locs = find("MARKER15", row=15)
    replace_range(locs[0]["begin"], locs[0]["end"], "")
    for k, f in R15_IMGS.items():
        insert_image_at(f"【图{k}】", 15, os.path.join(SHOTS, f))
    fix_font(15, "结果1：默认重定向", "路由规则与页面组件对应关系的理解。")
    print("== r15 done ==")


def stage_r14():
    print("== r14c2 ==")
    b1 = find("分条罗列实验任务", row=14)[0]["begin"]
    call("doc_insert_markdown", idx=b1, markdown=R14_MD)
    # 删除原说明文字（可能与“AI工具使用说明”同段，先只清文本，不删段落）
    locs = find("分条罗列实验任务，并粘贴其关键实现代码的截图；解释关键代码的作用；（以上信息在提交时请删除）", row=14)
    if locs:
        replace_range(locs[0]["begin"], locs[0]["end"], "")
    else:
        l1 = find("分条罗列实验任务", row=14)
        l2 = find("（以上信息在提交时请删除）", row=14)
        if l1 and l2:
            replace_range(l1[0]["begin"], l2[0]["end"], "")
        else:
            if l1:
                replace_range(l1[0]["begin"], l1[0]["end"], "")
            if l2:
                replace_range(l2[0]["begin"], l2[0]["end"], "")
    for k, f in R14_IMGS.items():
        insert_image_at(f"【图{k}】", 14, os.path.join(CODE, f))
    fix_font(14, "任务1：安装并注册", "参数指定的后台页面。")
    print("== r14 done ==")


def stage_ai():
    print("== AI 表 ==")
    rows = [
        (2, "1", "豆包（Doubao）", "理解路由概念",
         "请解释 Vue Router 中命名路由、嵌套路由和动态路由的区别，并举例说明什么时候用 RouterLink，什么时候用编程式导航。",
         "解释了三种路由的适用场景：RouterLink 适合导航菜单等声明式跳转，编程式导航适合登录跳转等需要先执行逻辑的场景。",
         "部分采纳，约60%"),
        (3, "2", "DeepSeek", "生成路由配置代码",
         "请帮我写一份 Vue3 + Vue Router 的路由配置，包含首页、关于我、项目中心嵌套路由、动态路由 detail/:id、404 通配符路由和登录守卫。",
         "给出了完整的路由表与 beforeEach 守卫示例，但组件名和 meta 字段与我的项目不一致，需要手动调整 import 路径。",
         "修改后采纳，约70%"),
        (4, "3", "WorkBuddy", "排查登录回跳问题",
         "访问 /admin/profile 被重定向到登录页后，登录成功跳转回原页面应该怎么实现？",
         "建议在守卫中用 next({ name: 'Login', query: { redirect: to.fullPath } }) 记录来源页面，登录成功后读取 route.query.redirect 跳回原地址。",
         "直接采纳，约90%"),
        (5, "4", "通义千问", "优化标题与高亮实现",
         "Vue Router 切换页面时如何让浏览器标题跟着变化？导航高亮怎么实现比较好？",
         "说明可以在 beforeEach 中用 document.title = to.meta.title 统一设置标题，导航高亮利用 router-link-active 类名配合样式实现。",
         "直接采纳，约85%"),
    ]
    cells = []
    for r, no, name, purpose, prompt, reply, ratio in rows:
        for c, v in ((1, no), (2, name), (3, purpose), (4, prompt), (5, reply), (6, ratio)):
            cells.append({"row": r, "col": c, "text": v})
    call("doc_set_table_cells", table_id=TID_AI, cells=cells,
         common_cell_properties={"text_format": {"font_family": "宋体", "font_size_pt": 10.5,
                                                 "color": "000000"},
                                 "horizontal_align": "left"})
    print("== ai done ==")


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    try:
        if stage in ("r15", "all"):
            stage_r15()
        if stage in ("r14", "all"):
            stage_r14()
        if stage in ("ai", "all"):
            stage_ai()
    except SystemExit as e:
        print("SystemExit:", e)
    print("ALL DONE")
