<template>
  <div :class="['message-bubble-wrapper', role]">
    <div class="avatar">
      {{ role === 'user' ? 'YOU' : 'AI' }}
    </div>
    <div class="bubble-container">
      <div class="bubble">
        <div class="content" v-html="renderedContent"></div>
        
        <div v-if="sources && sources.length > 0" class="sources-section">
          <div class="sources-header">
            <span class="label">Reference Sources</span>
          </div>
          <div class="sources-list">
            <div 
              v-for="(source, index) in uniqueSources" 
              :key="index" 
              class="source-tag"
              :title="source.text"
            >
              {{ source.filename }}
            </div>
          </div>
        </div>
      </div>
      <div class="timestamp">{{ timestamp }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
// Use a simple markdown-like renderer or a real library if available
const props = defineProps({
  role: { type: String, required: true },
  content: { type: String, required: true },
  sources: { type: Array, default: () => [] },
  timestamp: { type: String, default: () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
})

const renderedContent = computed(() => {
  // Basic markdown-like replacement for demo
  return props.content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
})

const uniqueSources = computed(() => {
  const seen = new Set()
  return props.sources.filter(s => {
    if (seen.has(s.filename)) return false
    seen.add(s.filename)
    return true
  })
})
</script>

<style scoped>
.message-bubble-wrapper {
  display: flex;
  gap: 20px;
  max-width: 90%;
  margin-bottom: 24px;
}

.message-bubble-wrapper.user {
  flex-direction: row-reverse;
  align-self: flex-end;
}

.message-bubble-wrapper.assistant {
  align-self: flex-start;
}

.avatar {
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}

.bubble-container {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.bubble {
  padding: 0;
  position: relative;
  font-size: 0.95rem;
  line-height: 1.7;
}

.user .bubble {
  color: var(--color-text-primary);
  text-align: right;
}

.assistant .bubble {
  color: var(--color-text-primary);
}

.content :deep(strong) {
  font-weight: 700;
}

.content :deep(code) {
  background-color: var(--color-bg-tertiary);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--color-text-primary);
}

.sources-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--color-border);
}

.sources-header .label {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--color-text-secondary);
  display: block;
  margin-bottom: 8px;
}

.sources-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.source-tag {
  background-color: transparent;
  color: var(--color-text-secondary);
  font-size: 0.7rem;
  padding: 4px 8px;
  border: 1px solid var(--color-border);
  cursor: help;
  transition: all 0.2s;
}

.source-tag:hover {
  border-color: var(--color-text-primary);
  color: var(--color-text-primary);
}

.timestamp {
  font-size: 0.65rem;
  color: #ccc;
  font-weight: 400;
}

.user .timestamp {
  text-align: right;
}

</style>
