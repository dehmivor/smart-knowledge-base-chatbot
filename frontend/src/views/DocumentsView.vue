<template>
  <div class="documents-container">
    <header class="page-header">
      <h1>🗄️ Quản lý tài liệu</h1>
      <p>Tải lên các tài liệu PDF, DOCX hoặc TXT để AI học kiến thức.</p>
    </header>

    <div class="upload-section">
      <div 
        class="drop-zone" 
        @dragover.prevent 
        @drop.prevent="handleDrop"
        @click="$refs.fileInput.click()"
        :class="{ 'uploading': isUploading }"
      >
        <input 
          type="file" 
          ref="fileInput" 
          hidden 
          accept=".pdf,.docx,.txt" 
          @change="handleFileSelect"
        >
        <div class="upload-icon">📤</div>
        <div class="upload-text">
          <p v-if="!isUploading">Kéo thả hoặc click để tải lên</p>
          <p v-else>Đang xử lý tài liệu...</p>
        </div>
      </div>
    </div>

    <div class="documents-list">
      <div class="list-header">
        <h2>Danh sách tài liệu ({{ documents.length }})</h2>
        <button @click="fetchDocuments" class="refresh-btn">🔄 Làm mới</button>
      </div>

      <div v-if="loading" class="loading-state">Đang tải danh sách...</div>
      
      <div v-else-if="documents.length === 0" class="empty-state">
        Chưa có tài liệu nào. Hãy tải lên tài liệu đầu tiên!
      </div>

      <div v-else class="grid">
        <div v-for="doc in documents" :key="doc.id" class="doc-card">
          <div class="doc-icon">📄</div>
          <div class="doc-info">
            <h3 :title="doc.filename">{{ truncate(doc.filename) }}</h3>
            <p>{{ doc.chunk_count }} chunks • {{ formatDate(doc.upload_date) }}</p>
          </div>
          <button @click="deleteDoc(doc.id)" class="delete-btn">🗑️</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api/v1/documents'
const documents = ref([])
const loading = ref(false)
const isUploading = ref(false)
const fileInput = ref(null)

const fetchDocuments = async () => {
  loading.value = true
  try {
    const res = await axios.get(API_BASE + '/')
    documents.value = res.data
  } catch (err) {
    alert('Lỗi khi tải danh sách: ' + err.message)
  } finally {
    loading.value = false
  }
}

const handleFileSelect = (e) => {
  const file = e.target.files[0]
  if (file) uploadFile(file)
}

const handleDrop = (e) => {
  const file = e.dataTransfer.files[0]
  if (file) uploadFile(file)
}

const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  isUploading.value = true
  try {
    await axios.post(API_BASE + '/upload', formData)
    await fetchDocuments()
  } catch (err) {
    alert('Lỗi khi upload: ' + (err.response?.data?.detail || err.message))
  } finally {
    isUploading.value = false
  }
}

const deleteDoc = async (id) => {
  if (!confirm('Bạn có chắc muốn xóa tài liệu này?')) return
  try {
    await axios.delete(`${API_BASE}/${id}`)
    await fetchDocuments()
  } catch (err) {
    alert('Lỗi khi xóa: ' + err.message)
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('vi-VN') + ' ' + date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
}

const truncate = (str) => str.length > 25 ? str.substring(0, 22) + '...' : str

onMounted(fetchDocuments)
</script>

<style scoped>
.documents-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  color: #e8e8e8;
}

.page-header {
  margin-bottom: 40px;
  text-align: center;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #6c63ff, #00d2ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.upload-section {
  margin-bottom: 50px;
}

.drop-zone {
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  background: rgba(255, 255, 255, 0.03);
  cursor: pointer;
  transition: all 0.3s ease;
}

.drop-zone:hover {
  border-color: #6c63ff;
  background: rgba(108, 99, 255, 0.05);
  transform: translateY(-2px);
}

.uploading {
  opacity: 0.6;
  pointer-events: none;
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.upload-text p {
  font-size: 1.1rem;
  color: #a0a0b0;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.refresh-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #a0a0b0;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.doc-card {
  background: #1a1a2e;
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  position: relative;
  transition: transform 0.2s;
}

.doc-card:hover {
  transform: scale(1.02);
  border-color: rgba(108, 99, 255, 0.3);
}

.doc-icon {
  font-size: 2rem;
}

.doc-info h3 {
  font-size: 1rem;
  margin: 0 0 5px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.doc-info p {
  font-size: 0.85rem;
  color: #a0a0b0;
  margin: 0;
}

.delete-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
}

.doc-card:hover .delete-btn {
  opacity: 1;
}

.empty-state, .loading-state {
  text-align: center;
  padding: 40px;
  color: #a0a0b0;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
}
</style>
