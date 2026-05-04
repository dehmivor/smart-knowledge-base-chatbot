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
  border: 1px solid var(--color-border);
  padding: 60px;
  text-align: center;
  background: var(--color-bg-secondary);
  transition: all 0.2s ease;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-zone.is-dragging {
  border-color: var(--color-text-primary);
  background: var(--color-bg-tertiary);
}

.upload-zone.is-uploading {
  border-style: solid;
}

.upload-content h3 {
  margin-bottom: 12px;
  font-size: 0.9rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.upload-content p {
  color: var(--color-text-secondary);
  font-size: 0.75rem;
  margin-bottom: 30px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.select-btn {
  display: inline-block;
  background: var(--color-text-primary);
  color: var(--color-bg-primary);
  padding: 10px 24px;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.2s;
}

.select-btn:hover {
  opacity: 0.8;
}

.uploading-content {
  width: 100%;
  max-width: 300px;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-top-color: var(--color-text-primary);
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.progress-bar {
  width: 100%;
  height: 1px;
  background: var(--color-border);
  margin: 20px 0;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--color-text-primary);
  transition: width 0.3s ease;
}

</style>
