<template>
  <div class="module">
    <div class="avatar"></div>
    <div style="margin-left: 12px; display: inline-block; vertical-align: top">
      <p>姓名：{{ user.name }}</p>
      <p>学号：{{ user.stuId }}</p>
      <p>班级：{{ user.className }}</p>
      <button @click="openEdit">编辑信息</button>
    </div>
  </div>
</template>
<script setup>
const props = defineProps({
  user: {
    type: Object,
    required: true
  }
});
const emit = defineEmits(["update-user"]);
const openEdit = () => {
  const newData = { ...props.user };
  emit("update-user", newData);
};
</script>
