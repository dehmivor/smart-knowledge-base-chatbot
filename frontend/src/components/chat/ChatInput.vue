<template>
  <div class="chat-input-wrapper" :class="{ focused: isFocused }">
    <textarea
      ref="textarea"
      v-model="text"
      placeholder="Type your question about company knowledge..."
      rows="1"
      @focus="isFocused = true"
      @blur="isFocused = false"
      @keydown.enter.prevent="handleEnter"
      @input="adjustHeight"
    ></textarea>
    
    <button 
      class="send-button" 
      :disabled="!text.trim() || disabled"
      @click="submit"
    >
      <span v-if="!disabled" class="send-text">SEND</span>
      <div v-else class="loader"></div>
    </button>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  disabled: { type: Boolean, default: false }
})

const emit = defineEmits(['send'])

const text = ref('')
const isFocused = ref(false)
const textarea = ref(null)

const adjustHeight = () => {
  const el = textarea.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = (el.scrollHeight) + 'px'
}

const handleEnter = (e) => {
  if (e.shiftKey) {
    // New line
  } else {
    submit()
  }
}

const submit = () => {
  if (text.value.trim() && !props.disabled) {
    emit('send', text.value)
    text.value = ''
    nextTick(() => adjustHeight())
  }
}

onMounted(() => {
  adjustHeight()
})
</script>

<style scoped>
.chat-input-wrapper {
  background-color: transparent;
  border-bottom: 1px solid var(--color-border);
  padding: 12px 0;
  display: flex;
  align-items: flex-end;
  gap: 12px;
  transition: all 0.2s ease;
}

.chat-input-wrapper.focused {
  border-color: var(--color-text-primary);
}

textarea {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--color-text-primary);
  font-family: inherit;
  font-size: 1rem;
  resize: none;
  outline: none;
  padding: 8px 0;
  max-height: 150px;
  line-height: 1.5;
}

textarea::placeholder {
  color: var(--color-text-secondary);
  opacity: 0.4;
}

.send-button {
  background: transparent;
  border: none;
  color: var(--color-text-primary);
  padding: 8px 0;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 1px;
  cursor: pointer;
  transition: opacity 0.2s;
  flex-shrink: 0;
  margin-bottom: 4px;
}

.send-button:hover:not(:disabled) {
  opacity: 0.7;
}

.send-button:disabled {
  opacity: 0.1;
  cursor: not-allowed;
}

.loader {
  width: 16px;
  height: 16px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-top-color: var(--color-text-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

</style>
