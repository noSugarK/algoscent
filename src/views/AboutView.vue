<template>
  <div class="citrus-selector" @mousemove="updateMousePosition">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">加载中...</div>

    <!-- 错误状态 -->
    <div v-if="error" class="error">
      加载失败: {{ error }}
    </div>

    <!-- 主内容区 - 仅在data存在时显示 -->
    <div v-if="data && !loading && !error">
      <h2>{{ data.category }}香料选择器</h2>
      <p class="category-description">{{ data.description }}</p>
      <img :src=" data.category_image.startsWith('//') ? 'https:' + data.category_image : data.category_image " />
      <div class="note-grid">
        <div
          v-for="note in data.notes"
          :key="note.name"
          class="note-item"
          :class="{ selected: isSelected(note) }"
          @click="toggleSelect(note)"
          @mouseenter="showTooltip(note)"
          @mouseleave="hideTooltip"
        >
          <img
            :src="note.image.startsWith('//') ? 'https:' + note.image : note.image"
            :alt="note.name"
            class="note-image"
            @error="handleImageError"
          />
          <div class="note-name">{{ note.name }}</div>
          <div class="note-english">{{ note.english_name }}</div>
        </div>
      </div>

      <!-- 悬浮提示框 -->
      <div
        v-if="showTooltipFlag && currentNote"
        class="tooltip"
        :style="tooltipStyle"
      >
        <div class="tooltip-content">
          <h4>{{ currentNote.name }} ({{ currentNote.english_name }})</h4>
          <div class="tooltip-description" v-if="currentNote.description">
            {{ currentNote.description }}
          </div>
        </div>
      </div>

      <div class="selected-list" v-if="selectedNotes.length > 0">
        <h3>已选中 ({{ selectedNotes.length }}):</h3>
        <ul>
          <li v-for="(note, index) in selectedNotes" :key="index">
            {{ note.name }} ({{ note.english_name }})
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

// 状态管理 - 初始化为空对象而非null
const data = ref({})
const loading = ref(true)
const error = ref(null)
const selectedNotes = ref([])

// 悬浮提示相关状态
const showTooltipFlag = ref(false)
const currentNote = ref(null)
const mousePosition = ref({ x: 0, y: 0 })


// 从JSON文件加载数据
const loadData = async () => {
  try {
    // 注意：根据你的项目结构调整路径
    // 如果是Vue CLI项目，JSON文件通常放在public文件夹下
    const response = await fetch('/data/smell/Fruits.json')
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`)
    }
    const jsonData = await response.json()
    data.value = jsonData
  } catch (err) {
    error.value = err.message
    console.error('加载数据失败:', err)
    // 错误时提供默认数据避免渲染错误
    data.value = {
      category: "柑橘类",
      description: "",
      notes: []
    }
  } finally {
    loading.value = false
  }
}

// 组件挂载时加载数据
onMounted(loadData)

// 判断是否选中
const isSelected = (note) => {
  return selectedNotes.value.some(n => n.name === note.name)
}

// 切换选中状态
const toggleSelect = (note) => {
  const index = selectedNotes.value.findIndex(n => n.name === note.name)
  if (index > -1) {
    selectedNotes.value.splice(index, 1)
  } else {
    selectedNotes.value.push(note)
  }
}

// 图片加载失败时替换为默认图
const handleImageError = (e) => {
  e.target.src = 'https://via.placeholder.com/150?text=No+Image'
}

// 显示悬浮提示
const showTooltip = (note) => {
  currentNote.value = note
  showTooltipFlag.value = true
}

// 隐藏悬浮提示
const hideTooltip = () => {
  showTooltipFlag.value = false
  currentNote.value = null
}

// 更新鼠标位置
const updateMousePosition = (event) => {
  mousePosition.value = {
    x: event.clientX,
    y: event.clientY
  }
}

// 计算提示框样式（定位在鼠标右侧）
const tooltipStyle = computed(() => {
  return {
    position: 'fixed',
    top: `${mousePosition.value.y + 10}px`,
    left: `${mousePosition.value.x + 20}px`,
    zIndex: 1000,
    maxWidth: '300px'
  }
})
</script>

<style scoped>
/* 样式保持不变 */
.citrus-selector {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error {
  color: #dc3545;
}

.category-description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 25px;
  max-width: 800px;
  white-space: pre-line; /* 保留换行符 */
}

.note-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.note-item {
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: white;
}

.note-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.1);
  border-color: #bbb;
}

.note-item.selected {
  border-color: #2c3e50;
  background-color: #f8f9fa;
  box-shadow: 0 4px 8px rgba(44, 62, 80, 0.15);
}

.note-image {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 6px;
  margin-bottom: 8px;
  transition: transform 0.3s ease;
}

.note-item:hover .note-image {
  transform: scale(1.03);
}

.note-name {
  font-weight: 600;
  font-size: 14px;
  margin: 4px 0;
  color: #2c3e50;
}

.note-english {
  font-size: 12px;
  color: #7f8c8d;
  font-style: italic;
}

.selected-list {
  margin-top: 40px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
}

.selected-list h3 {
  margin-bottom: 15px;
  color: #2c3e50;
  font-size: 18px;
}

.selected-list ul {
  list-style: none;
  padding: 0;
}

.selected-list li {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
  font-size: 14px;
  display: flex;
  justify-content: space-between;
}

.selected-list li:last-child {
  border-bottom: none;
}

/* 悬浮提示框样式 */
.tooltip {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 15px;
  font-size: 14px;
  line-height: 1.5;
  pointer-events: none; /* 防止干扰鼠标事件 */
}

.tooltip h4 {
  margin: 0 0 10px 0;
  color: #2c3e50;
  font-size: 16px;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.tooltip-description,
.tooltip-characteristics,
.tooltip-usage,
.tooltip-note {
  margin: 8px 0;
  font-size: 13px;
}

.tooltip-characteristics,
.tooltip-usage,
.tooltip-note {
  color: #555;
}

.tooltip strong {
  color: #2c3e50;
}
</style>