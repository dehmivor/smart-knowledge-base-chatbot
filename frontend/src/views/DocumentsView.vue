<template>
  <div class="documents-view">
    <div class="view-header">
      <div class="view-info">
        <h2 class="title">Knowledge Base</h2>
        <p class="subtitle">Upload and manage your company documents</p>
      </div>
      <div class="view-stats">
        <div class="stat-item">
          <span class="stat-value">{{ documents.length }}</span>
          <span class="stat-label">Documents</span>
        </div>
      </div>
    </div>

    <div class="view-content">
      <div class="upload-section">
        <UploadZone 
          :uploading="isUploading" 
          :progress="uploadProgress"
          @upload="handleUpload" 
        />
      </div>

      <div class="list-section">
        <div class="section-header">
          <h3>Your Library</h3>
          <div class="search-bar">
            <input type="text" v-model="searchQuery" placeholder="Search documents...">
          </div>
        </div>

        <div v-if="filteredDocuments.length > 0" class="documents-list">
          <DocumentCard 
            v-for="doc in filteredDocuments" 
            :key="doc.id" 
            :doc="doc"
            @delete="confirmDelete"
          />
        </div>

        <div v-else-if="!isLoading" class="empty-state">
          <p v-if="searchQuery">No documents match your search.</p>
          <p v-else>No documents uploaded yet. Start by dropping a file above.</p>
        </div>

        <div v-if="isLoading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading library...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import UploadZone from '@/components/documents/UploadZone.vue'
import DocumentCard from '@/components/documents/DocumentCard.vue'

const API_DOCS = 'http://localhost:8000/api/v1/documents/'

const documents = ref([])
const isLoading = ref(false)
const isUploading = ref(false)
const uploadProgress = ref(0)
const searchQuery = ref('')

const filteredDocuments = computed(() => {
  if (!searchQuery.value) return documents.value
  const query = searchQuery.value.toLowerCase()
  return documents.value.filter(doc => 
    doc.filename.toLowerCase().includes(query)
  )
})

const fetchDocuments = async () => {
  isLoading.value = true
  try {
    const res = await axios.get(API_DOCS)
    documents.value = res.data
  } catch (err) {
    console.error('Failed to fetch documents:', err)
  } finally {
    isLoading.value = false
  }
}

const handleUpload = async (files) => {
  isUploading.value = true
  uploadProgress.value = 0
  
  const formData = new FormData()
  files.forEach(file => {
    formData.append('files', file)
  })

  try {
    // Simulated progress for demo
    const interval = setInterval(() => {
      if (uploadProgress.value < 90) uploadProgress.value += 10
    }, 200)

    await axios.post(`${API_DOCS}upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    clearInterval(interval)
    uploadProgress.value = 100
    
    setTimeout(() => {
      isUploading.value = false
      fetchDocuments()
      window.dispatchEvent(new CustomEvent('document-updated'))
    }, 500)
  } catch (err) {
    console.error('Upload failed:', err)
    alert('Upload failed: ' + (err.response?.data?.detail || err.message))
    isUploading.value = false
  }
}

const confirmDelete = async (id) => {
  if (confirm('Are you sure you want to delete this document? This will also remove its associated vectors from the database.')) {
    try {
      await axios.delete(`${API_DOCS}${id}`)
      fetchDocuments()
      window.dispatchEvent(new CustomEvent('document-updated'))
    } catch (err) {
      console.error('Delete failed:', err)
      alert('Failed to delete document.')
    }
  }
}

onMounted(() => {
  fetchDocuments()
})
</script>

<style scoped>
.documents-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--color-bg-primary);
}

.view-header {
  padding: 30px 60px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 0.9rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.subtitle {
  font-size: 0.7rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 4px;
}

.view-stats {
  text-align: right;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 400;
  color: var(--color-text-primary);
}

.stat-label {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--color-text-secondary);
  margin-left: 8px;
}

.view-content {
  flex: 1;
  overflow-y: auto;
  padding: 60px;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}

.upload-section {
  margin-bottom: 60px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border);
}

.section-header h3 {
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.search-bar input {
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--color-border);
  padding: 8px 0;
  color: var(--color-text-primary);
  font-size: 0.85rem;
  width: 200px;
  transition: all 0.3s;
}

.search-bar input:focus {
  outline: none;
  border-color: var(--color-text-primary);
  width: 260px;
}

.documents-list {
  display: flex;
  flex-direction: column;
  gap: 1px;
  background-color: var(--color-border);
  border: 1px solid var(--color-border);
}

.empty-state, .loading-state {
  text-align: center;
  padding: 80px 0;
  color: var(--color-text-secondary);
  font-size: 0.85rem;
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

</style>
