<template>
  <div class="star-rating">
    <span 
      v-for="(star, index) in 5" 
      :key="index" 
      class="star"
      @mousedown="editable ? startDrag(index) : null" 
      @mouseup="editable ? endDrag : null" 
      @mousemove="editable ? moveDrag : null"
    >
      <img :src="starSrc(index)" alt="star" width="30px" />
    </span>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import emptyStar from '@/assets/emptystar.png'
import halfStar from '@/assets/halfstar.png'
import fullStar from '@/assets/fullstar.png'

const props = defineProps({
  rate: {
    type: Number,
    default: 0
  },
  editable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:rate'])

const rate = ref(props.rate)
const dragging = ref(false)
const startIndex = ref(null)
const timer = ref(null)

watch(() => props.rate, (newRate) => {
  rate.value = newRate
})

const starSrc = (index) => {
  if (index + 1 <= rate.value) return fullStar
  if (index + 0.5 <= rate.value) return halfStar
  return emptyStar
}

const startDrag = (index) => {
  if (!props.editable) return

  dragging.value = true
  startIndex.value = index
  updateRate(index + 0.5)

  timer.value = setTimeout(() => {
    if (dragging.value) updateRate(index + 1)
  }, 1000)
}

const endDrag = () => {
  dragging.value = false
  clearTimeout(timer.value)
}

const moveDrag = (event) => {
  if (!props.editable) return

  if (dragging.value) {
    const starElement = event.currentTarget
    const rect = starElement.getBoundingClientRect()
    const offsetX = event.clientX - rect.left

    if (offsetX > rect.width / 2) {
      updateRate(startIndex.value + 1)
    } else {
      updateRate(startIndex.value + 0.5)
    }
  }
}

const updateRate = (newRate) => {
  rate.value = newRate
  emit('update:rate', rate.value)
  for (let i = 0; i < startIndex.value; i++) {
    rate.value = Math.max(rate.value, i + 1)
    emit('update:rate', rate.value)
  }
}
</script>

<style scoped>
.star-rating {
  display: flex;
  flex-direction: row;
}
.star {
  cursor: pointer;
}
</style>
