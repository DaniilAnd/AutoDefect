<template>
    <div>
      <h6>Город: {{value.city}}</h6>
      <h6>Улица: {{value.street}}</h6>
      <h6>GPS-координаты: {{value.gps_coordinates['x']}}, {{value.gps_coordinates['y']}}</h6>
      <h6>Дата отчета: {{value.time_escalation.split('T')[0]}}</h6>
    </div>
  </template>
  
  <script setup>
  defineProps({
    value: {
      type: Object,
      default: '',
    },
  });
  
  </script>

<style>

.yandex-balloon {
    height: 150px;
    width: 200px;
}
</style>