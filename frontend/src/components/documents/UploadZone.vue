<template>
  <div 
    class="upload-zone"
    :class="{ 'is-dragging': isDragging, 'is-uploading': uploading }"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="handleDrop"
  >
    <div v-if="!uploading" class="upload-content">
      <h3>Drop documents here</h3>
      <p>Support PDF, DOCX, and TXT files (Max 10MB)</p>
      
      <label class="select-btn">
        Select Files
        <input type="file" multiple @change="handleFileSelect" hidden accept=".pdf,.docx,.txt">
      </label>
    </div>

    <div v-else class="uploading-content">
      <div class="spinner"></div>
      <h3>Uploading...</h3>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progress + '%' }"></div>
      </div>
      <p>Processing and indexing your documents</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  uploading: { type: Boolean, default: false },
  progress: { type: Number, default: 0 }
})

const emit = defineEmits(['upload'])
const isDragging = ref(false)

const handleDrop = (e) => {
  isDragging.value = false
  const files = Array.from(e.dataTransfer.files)
  if (files.length > 0) {
    emit('upload', files)
  }
}

const handleFileSelect = (e) => {
  const files = Array.from(e.target.files)
  if (files.length > 0) {
    emit('upload', files)
    e.target.value = null // Reset
  }
}
</script>

<style scoped>
.upload-zone {
  border: 2px dashed var(--color-border);
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  background: rgba(255, 255, 255, 0.02);
  transition: all 0.3s ease;
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-zone.is-dragging {
  border-color: var(--color-accent-primary);
  background: rgba(108, 99, 255, 0.05);
  transform: scale(1.01);
}

.upload-zone.is-uploading {
  border-style: solid;
  border-color: var(--color-border);
}

.upload-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  color: var(--color-accent-primary);
  opacity: 0.8;
}

.upload-content h3 {
  margin-bottom: 8px;
  font-size: 1.25rem;
}

.upload-content p {
  color: var(--color-text-secondary);
  font-size: 0.9rem;
  margin-bottom: 24px;
}

.select-btn {
  display: inline-block;
  background: var(--color-accent-primary);
  color: white;
  padding: 10px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.select-btn:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}

.uploading-content {
  width: 100%;
  max-width: 300px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(108, 99, 255, 0.1);
  border-top-color: var(--color-accent-primary);
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  margin: 15px 0;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--color-accent-gradient);
  transition: width 0.3s ease;
}
</style>
