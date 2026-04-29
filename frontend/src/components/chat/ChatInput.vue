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
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 12px 16px;
  display: flex;
  align-items: flex-end;
  gap: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.chat-input-wrapper.focused {
  border-color: var(--color-accent-primary);
  box-shadow: 0 4px 25px rgba(108, 99, 255, 0.15);
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
  opacity: 0.6;
}

.send-button {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: var(--color-accent-gradient);
  border: none;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
  margin-bottom: 2px;
}

.send-button:hover:not(:disabled) {
  transform: scale(1.05) translateY(-2px);
  filter: brightness(1.1);
}

.send-button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  filter: grayscale(1);
}

.send-button svg {
  width: 20px;
  height: 20px;
}

.loader {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
