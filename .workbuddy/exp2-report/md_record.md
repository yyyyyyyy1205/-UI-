**第二次实验（项目展示页面）设计与实现：**

确定页面内容为"个人项目展示区域"，由 ProjectShow 组件负责；使用数组 projectList 保存项目名称、简介、技术栈、状态等信息；把卡片外壳抽成可复用组件 BaseCard，内部用默认插槽和 #header、#footer 具名插槽划分头部、主体、底部三个区域，ProjectShow 通过 template#header、template#default、template#footer 为每个项目定制标题、描述和操作按钮，避免重复书写卡片结构；项目详情弹窗与源码弹窗使用 Teleport 挂载到 body 下，保证弹窗不受父容器样式影响。

**解释关键代码的作用：**

（1）main.js：createApp(App).mount("#app") —— 以 App.vue 为根组件创建应用实例，并挂载到 index.html 的 div#app 上，是整个 Vue 工程的入口；index.html 只提供挂载点和入口脚本标签。

（2）App.vue：script setup 中用 ref 定义 isDark、info、skillArr、searchKey、showDetail 等响应式状态；computed 计算属性 filterSkill 依据 searchKey 过滤技能数组，实现关键词搜索；template 中按"顶部—主体—底部"组织各子组件。

（3）defineProps / defineEmits：TopHeader 通过 props 接收 isDark，按钮点击时 $emit('toggle-theme') 通知父组件修改状态；IntroArea 接收 descText、showDetail，通过 emit('toggle-show') 让父组件切换简介的展开与收起，全程遵循 props 单向数据流，子组件不直接改 props。

（4）双向绑定（defineModel 等价写法）：SearchArea 使用 defineProps(["modelValue"]) 与 defineEmits(["update:modelValue"])，输入框绑定 :value="modelValue"、@input="$emit('update:modelValue', $event.target.value)"，父组件以 v-model:search-key="searchKey" 完成父子双向同步。

（5）组件内部状态与共享状态：UserInfo 的 isEditMode 属于组件内部状态，控制"展示 / 编辑"切换；InfoEdit 用 ref({ ...props.originInfo }) 生成本地副本进行编辑，保存时 emit('save') 把新数据提交给父组件，取消则直接关闭编辑态，props 始终未被直接修改。

（6）插槽：BaseCard 中 slot name="header"、默认 slot、slot name="footer" 分别对应卡片头部、主体、底部；ProjectShow 传入不同内容即可得到外观统一、内容不同的项目卡片，体现了插槽在减少重复结构、提升复用性上的价值。

（7）Teleport：ProjectShow 用 Teleport to="body" 把"项目详情"和"源码片段"两个弹窗渲染到 body 下，避免受父容器 overflow 与层叠上下文影响。
