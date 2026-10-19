<template>
  <header style="text-align: center; padding: 18px; background: var(--header-bg); transition: background 0.3s">
    <div
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 540px;
        margin: 0 auto;
        padding: 0 10px;
      "
    >
      <h2 style="color: var(--text-color)">个人信息页面‑实验二组件化开发</h2>
      <button @click="$emit('toggle-theme')">
        {{ isDark ? "☀亮色模式" : "🌙暗色模式" }}
      </button>
    </div>
  </header>
</template>
<script setup>
const props = defineProps({
  isDark: {
    type: Boolean,
    default: false
  }
});
defineEmits(["toggle-theme"]);
</script>
