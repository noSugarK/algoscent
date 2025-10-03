<!-- StarRating.vue -->
<template>
  <div class="flex">
    <template v-for="i in 5" :key="i">
      <i
          class="fa text-sm"
          :class="getStarClass(i)"
      ></i>
    </template>
  </div>
</template>

<script setup>
const props = defineProps({
  rating: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 5
  }
})

const getStarClass = (index) => {
  const diff = props.rating - (index - 1)

  if (diff >= 1) return 'fa-star text-primary'
  if (diff > 0 && diff < 1) return 'fa-star-half-stroke text-primary'
  return 'fa-star text-gray-300'
}
</script>