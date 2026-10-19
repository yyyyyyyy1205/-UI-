<template>
  <div>
    <p>姓名：<input v-model="localInfo.name" /></p>
    <p>学号：<input v-model="localInfo.stuId" /></p>
    <p>班级：<input v-model="localInfo.className" /></p>
    <button @click="handleSave">保存</button>
    <button @click="handleCancel">取消</button>
  </div>
</template>
<script setup>
import { ref, watch } from "vue";
const props = defineProps({
  originInfo: {
    type: Object,
    required: true
  }
});
const emit = defineEmits(["save", "cancel"]);
// 本地副本，不直接修改props
const localInfo = ref({ ...props.originInfo });
watch(
  () => props.originInfo,
  (newVal) => {
    localInfo.value = { ...newVal };
  }
);
const handleSave = () => {
  emit("save", { ...localInfo.value });
};
const handleCancel = () => {
  emit("cancel");
};
</script>
