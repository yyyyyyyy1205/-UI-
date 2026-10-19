<template>
  <div class="module">
    <div class="part-title">个人简介</div>
    <p v-show="showDetail">{{ descText }}</p>
    <p v-show="!showDetail">{{ descText.slice(0, 30) }}……</p>
    <button @click="$emit('toggle-show')">{{ showDetail ? "收起简介" : "展开简介" }}</button>
  </div>
</template>
<script setup>
defineProps(["descText", "show-detail"]);
defineEmits(["toggle-show"]);
</script>
