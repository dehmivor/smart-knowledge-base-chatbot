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
  gap: 16px;
  max-width: 85%;
  margin-bottom: 8px;
  animation: slideUp 0.4s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.message-bubble-wrapper.user {
  flex-direction: row-reverse;
  align-self: flex-end;
}

.message-bubble-wrapper.assistant {
  align-self: flex-start;
}

.avatar {
  width: 36px;
  height: 36px;
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  font-weight: 800;
  color: var(--color-text-secondary);
  flex-shrink: 0;
}

.bubble-container {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.bubble {
  padding: 16px 20px;
  border-radius: 20px;
  position: relative;
  font-size: 1rem;
  line-height: 1.6;
}

.user .bubble {
  background: var(--color-accent-gradient);
  color: white;
  border-top-right-radius: 4px;
  box-shadow: 0 4px 15px rgba(108, 99, 255, 0.2);
}

.assistant .bubble {
  background-color: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  border-top-left-radius: 4px;
}

.content :deep(code) {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.9em;
}

.sources-section {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.sources-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.sources-header .icon {
  font-size: 0.8rem;
}

.sources-header .label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-accent-secondary);
}

.sources-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.source-tag {
  background-color: rgba(0, 210, 255, 0.1);
  color: var(--color-accent-secondary);
  font-size: 0.7rem;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid rgba(0, 210, 255, 0.1);
  cursor: help;
  transition: all 0.2s;
}

.source-tag:hover {
  background-color: rgba(0, 210, 255, 0.2);
  transform: translateY(-1px);
}

.timestamp {
  font-size: 0.7rem;
  color: var(--color-text-secondary);
  margin: 0 10px;
}

.user .timestamp {
  text-align: right;
}
</style>
