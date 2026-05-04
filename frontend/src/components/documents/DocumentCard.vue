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
  background: var(--color-bg-primary);
  border: none;
  padding: 20px 0;
  display: flex;
  align-items: center;
  gap: 24px;
  transition: all 0.2s;
}

.document-card:hover {
  opacity: 0.7;
}

.doc-type-label {
  font-size: 0.65rem;
  font-weight: 800;
  color: var(--color-text-secondary);
  width: 40px;
  flex-shrink: 0;
}

.doc-info {
  flex: 1;
  min-width: 0;
}

.doc-name {
  margin: 0 0 4px 0;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.doc-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.65rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.separator {
  opacity: 0.3;
}

.badge {
  font-size: 0.6rem;
  padding: 2px 0;
  text-transform: uppercase;
  font-weight: 800;
  letter-spacing: 1px;
}

.badge.indexed { color: var(--color-success); }
.badge.processing { color: var(--color-text-secondary); }
.badge.failed { color: var(--color-error); }

.delete-btn {
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 0;
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: color 0.2s;
}

.delete-btn:hover {
  color: var(--color-error);
}

</style>
