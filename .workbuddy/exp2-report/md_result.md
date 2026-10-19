**一、Vue 工程迁移与页面运行验证**

将实验一的单页 HTML 迁移到 Vue 工程，npm run dev 启动后页面正常渲染，顶部、主体、底部三段式结构完整，控制台无报错；页面显示姓名"杨美媛"、学号"249980740"、班级"24计科2班"，可标识本人身份。

IMG_SLOT_1

图1　迁移到 Vue 工程后的页面整体效果

**二、组件拆分与组件树**

按职责将页面拆分为 TopHeader（顶部标题栏）、SearchArea（技能搜索）、UserInfo（基础信息）、InfoEdit（信息编辑表单）、IntroArea（个人简介）、SkillArea（技能兴趣）、ProjectShow（项目展示）、BaseCard（通用卡片）、Footer（页脚），由 App.vue 作为根组件组织组件树，各模块渲染正常。

IMG_SLOT_2

图2　组件树设计图（App.vue 为根组件）

**三、defineProps 与 defineEmits 父子通信**

点击右上角"暗色模式"按钮，TopHeader 通过 emit('toggle-theme') 通知 App.vue 修改 isDark，全站主题切换为暗色；再次点击可还原为亮色，说明 props 下发、事件上抛的单向数据流通信正常。

IMG_SLOT_3

图3　defineProps 与 defineEmits：主题切换为暗色

**四、v-model（defineModel）双向同步**

在技能搜索框输入"Vue"，SearchArea 通过 update:modelValue 同步给父组件，计算属性过滤后技能列表仅显示"Vue基础"；清空输入后恢复全部 7 项技能，双向绑定生效。

IMG_SLOT_4

图4　v-model 双向绑定：关键词过滤技能列表

**五、组件内部状态与信息编辑（InfoEdit）**

点击"编辑信息"进入编辑态，InfoEdit 用 props 的本地副本编辑姓名、学号、班级；保存后通过 emit('save') 提交父组件更新，取消则放弃修改，未直接修改 props。同时个人简介区域点击"展开简介"可显示简介内容。

IMG_SLOT_5

图5　组件内部状态：信息编辑与简介展开

**六、项目展示页面与插槽复用（ProjectShow 与 BaseCard）**

BaseCard 提供默认插槽与 header、footer 具名插槽，ProjectShow 用数组数据渲染出两张结构一致、内容不同的项目卡片；点击"查看详情"通过 Teleport 弹出详情弹窗，点击"查看源码"弹出源码片段弹窗，弹窗均可正常打开与关闭。

IMG_SLOT_6

图6　项目展示：详情弹窗（Teleport）

IMG_SLOT_7

图7　项目展示：源码片段弹窗

**七、Vue DevTools 调试**

使用 Vue DevTools 的 Components 面板查看组件树，可见 App.vue 下依次挂载 TopHeader、container 容器内的 SearchArea、UserInfo、IntroArea、SkillArea、ProjectShow 以及 Footer，与设计的组件树一致；选中组件可查看其 props（如 user、skillList、searchKey）与内部状态，点击按钮时能在时间线中看到 toggle-theme、update:modelValue、toggle-show 等事件被触发，数据传递链路与预期一致。

**八、结果分析与收获**

1. 迁移后页面功能与实验一保持一致，说明 index.html 提供挂载点、main.js 创建并挂载应用、App.vue 组织页面的职责划分是正确的。

2. 搜索过滤、主题切换、简介展开、信息编辑、弹窗展示等交互全部正常，说明 defineProps、defineEmits、v-model、插槽与 Teleport 的使用方式正确。

3. 拆分组件后页面结构更清晰、样式职责更集中；插槽让卡片类结构得以复用，明显减少了重复代码。

4. 收获：理解了"数据放哪里、由谁修改"的状态归属原则和 props 单向数据流，体会到组件化开发在可维护性与复用性上的优势。
