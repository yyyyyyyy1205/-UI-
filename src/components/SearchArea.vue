<template>
  <div class="module normal-module">
    <div class="part-title">技能搜索区域</div>
    <input
      :value="searchKey"
      @input="$emit('update:searchKey', $event.target.value)"
      placeholder="输入关键词搜索技能"
    />
  </div>
</template>
<script setup>
const props = defineProps(["searchKey"]);
const emit = defineEmits(["update:searchKey"]);
</script>
