<template>
  <aside class="app-sidebar">
    <div class="logo">
      <span class="logo-text">Brother SKB</span>
    </div>

    <nav class="nav-menu">
      <router-link to="/" class="nav-item">
        <span class="label">Chat Assistant</span>
      </router-link>
      <router-link to="/documents" class="nav-item">
        <span class="label">Knowledge Base</span>
      </router-link>
    </nav>

    <div v-if="documents.length > 0" class="knowledge-section">
      <h3 class="section-title">Active Knowledge</h3>
      <div class="knowledge-list">
        <div v-for="doc in documents.slice(0, 5)" :key="doc.id" class="knowledge-item">
          {{ doc.filename }}
        </div>
        <div v-if="documents.length > 5" class="knowledge-more">
          + {{ documents.length - 5 }} more
        </div>
      </div>
    </div>

    <div class="sidebar-footer">
      <div class="status-indicator">
        <span class="status-text">System Online</span>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const documents = ref([])

const fetchDocuments = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/documents/')
    documents.value = res.data
  } catch (err) {
    console.error('Failed to fetch documents in sidebar:', err)
  }
}

onMounted(() => {
  fetchDocuments()
  // Refresh occasionally or on an event
  window.addEventListener('document-updated', fetchDocuments)
})
</script>

<style scoped>
.app-sidebar {
  width: 240px;
  background-color: var(--color-bg-secondary);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  padding: 40px 24px;
  z-index: 100;
}

.logo {
  margin-bottom: 60px;
  padding-left: 16px;
}

.logo-text {
  font-size: 0.9rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--color-text-primary);
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 40px;
}

.nav-item {
  padding: 12px 16px;
  text-decoration: none;
  color: var(--color-text-secondary);
  border-radius: 0;
  transition: all 0.2s ease;
  font-size: 0.85rem;
  font-weight: 500;
  border-left: 2px solid transparent;
}

.nav-item:hover {
  color: var(--color-text-primary);
}

.nav-item.router-link-active {
  color: var(--color-text-primary);
  font-weight: 700;
  border-left: 2px solid var(--color-text-primary);
}

.knowledge-section {
  padding: 0 16px;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.section-title {
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--color-text-secondary);
  margin-bottom: 16px;
  opacity: 0.6;
}

.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.knowledge-item {
  font-size: 0.75rem;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 400;
}

.knowledge-more {
  font-size: 0.65rem;
  color: var(--color-text-secondary);
  font-style: italic;
  margin-top: 4px;
}

.sidebar-footer {
  margin-top: auto;
  padding: 24px 16px 0;
}

.status-indicator {
  display: flex;
  align-items: center;
}

.status-text {
  font-size: 0.7rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
}
</style>

