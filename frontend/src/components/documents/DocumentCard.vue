<template>
  <div class="document-card">
    <div class="doc-type-label" :class="docType">
      {{ docTypeShort }}
    </div>
    <div class="doc-info">
      <h4 class="doc-name" :title="doc.filename">{{ doc.filename }}</h4>
      <div class="doc-meta">
        <span>{{ formatDate(doc.upload_date) }}</span>
        <span class="separator">•</span>
        <span>{{ doc.file_type }}</span>
      </div>
    </div>
    <div class="doc-status">
      <span :class="['badge', doc.status]">
        {{ doc.status }}
      </span>
    </div>
    <div class="doc-actions">
      <button class="delete-btn" @click="$emit('delete', doc.id)" title="Delete document">
        REMOVE
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  doc: { type: Object, required: true }
})

defineEmits(['delete'])

const docType = computed(() => {
  const ext = props.doc.filename.split('.').pop().toLowerCase()
  if (ext === 'pdf') return 'pdf'
  if (ext === 'docx' || ext === 'doc') return 'word'
  return 'text'
})

const docTypeShort = computed(() => {
  if (docType.value === 'pdf') return 'PDF'
  if (docType.value === 'word') return 'DOC'
  return 'TXT'
})

const formatDate = (dateStr) => {
  if (!dateStr) return 'Unknown'
  const date = new Date(dateStr)
  return date.toLocaleDateString()
}
</script>

<style scoped>
.document-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.2s;
}

.document-card:hover {
  border-color: rgba(255, 255, 255, 0.15);
  transform: translateX(4px);
  background: rgba(255, 255, 255, 0.03);
}

.doc-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.doc-icon.pdf { color: #ff5252; background: rgba(255, 82, 82, 0.1); }
.doc-icon.word { color: #2b579a; background: rgba(43, 87, 154, 0.1); }
.doc-icon.text { color: #a0a0b0; background: rgba(160, 160, 176, 0.1); }

.doc-info {
  flex: 1;
  min-width: 0;
}

.doc-name {
  margin: 0 0 4px 0;
  font-size: 0.95rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.doc-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.75rem;
  color: var(--color-text-secondary);
}

.separator {
  opacity: 0.3;
}

.badge {
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 6px;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.badge.indexed { background: rgba(0, 230, 118, 0.1); color: var(--color-success); }
.badge.processing { background: rgba(0, 210, 255, 0.1); color: var(--color-accent-secondary); }
.badge.failed { background: rgba(255, 82, 82, 0.1); color: var(--color-error); }

.delete-btn {
  background: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 8px;
  transition: all 0.2s;
  font-size: 0.65rem;
  font-weight: 700;
}
</style>
