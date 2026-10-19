<template>
  <footer
    style="
      text-align: center;
      padding: 14px;
      color: var(--text-normal);
      margin-top: 24px;
      border-top: 1px solid var(--border-color);
      transition: all 0.3s;
    "
  >
    ©2026 Vue组件化实验
  </footer>
</template>
<script setup>
defineProps({
  isDark: {
    type: Boolean,
    default: false
  }
});
</script>
