<template>
  <div class="chat-view">
    <div class="chat-header">
      <div class="chat-info">
        <h2 class="title">RAG Chat Assistant</h2>
        <p class="subtitle">AI-powered knowledge retrieval engine</p>
      </div>
      <div class="chat-actions">
        <button class="action-btn" @click="clearChat" title="Clear chat history">
          Clear
        </button>
      </div>
    </div>

    <div class="chat-window" ref="scrollContainer">
      <div v-if="messages.length === 0" class="welcome-container">
        <div class="welcome-card">
          <h1>How can I help you today?</h1>
          <p>I can search through your uploaded documents and provide precise answers based on the content.</p>
          
          <div class="suggestion-grid">
            <div 
              v-for="(suggestion, i) in suggestions" 
              :key="i" 
              class="suggestion-item"
              @click="useSuggestion(suggestion)"
            >
              {{ suggestion }}
            </div>
          </div>
        </div>
      </div>

      <div class="messages-list">
        <MessageBubble
          v-for="(msg, index) in messages"
          :key="index"
          :role="msg.role"
          :content="msg.content"
          :sources="msg.sources"
          :timestamp="msg.timestamp"
        />
        
        <div v-if="isLoading" class="typing-bubble-wrapper">
          <div class="avatar">AI</div>
          <div class="typing-bubble">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-footer">
      <div class="input-container">
        <ChatInput :disabled="isLoading" @send="handleSendMessage" />
        <p class="disclaimer">AI can make mistakes. Please verify important information with official sources.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import MessageBubble from '@/components/chat/MessageBubble.vue'
import ChatInput from '@/components/chat/ChatInput.vue'

const API_CHAT = 'http://localhost:8000/api/v1/chat/'

const messages = ref([])
const isLoading = ref(false)
const scrollContainer = ref(null)

const suggestions = [
  "What is the company's leave policy?",
  "Tell me about the onboarding process.",
  "What are the technical standards for development?",
  "How do I request a hardware upgrade?"
]

const scrollToBottom = async () => {
  await nextTick()
  if (scrollContainer.value) {
    scrollContainer.value.scrollTo({
      top: scrollContainer.value.scrollHeight,
      behavior: 'smooth'
    })
  }
}

const handleSendMessage = async (text) => {
  const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  
  messages.value.push({
    role: 'user',
    content: text,
    timestamp
  })
  
  isLoading.value = true
  scrollToBottom()

  try {
    const response = await axios.post(API_CHAT, { message: text })
    
    messages.value.push({
      role: 'assistant',
      content: response.data.answer,
      sources: response.data.sources,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    })
  } catch (error) {
    console.error('Chat error:', error)
    messages.value.push({
      role: 'assistant',
      content: "⚠️ **System Error**: I'm having trouble connecting to the backend. Please ensure the server is running.",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

const useSuggestion = (text) => {
  handleSendMessage(text)
}

const clearChat = () => {
  if (confirm('Are you sure you want to clear the chat history?')) {
    messages.value = []
  }
}

onMounted(() => {
  // Load initial welcome or history if needed
})
</script>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: relative;
}

.chat-header {
  padding: 20px 40px;
  background: rgba(15, 15, 26, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}

.title {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
}

.subtitle {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  margin: 2px 0 0 0;
}

.action-btn {
  background: transparent;
  border: 1px solid var(--color-border);
  padding: 0 15px;
  height: 36px;
  border-radius: 10px;
  color: var(--color-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 0.85rem;
  font-weight: 600;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--color-text-secondary);
}

.chat-window {
  flex: 1;
  overflow-y: auto;
  padding: 40px;
  scroll-behavior: smooth;
}

.welcome-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.welcome-card {
  max-width: 600px;
  text-align: center;
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.bot-icon {
  font-size: 4rem;
  margin-bottom: 24px;
}

.welcome-card h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 16px;
  letter-spacing: -1px;
}

.welcome-card p {
  font-size: 1.1rem;
  color: var(--color-text-secondary);
  margin-bottom: 40px;
}

.suggestion-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.suggestion-item {
  padding: 16px 20px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.suggestion-item:hover {
  border-color: var(--color-accent-primary);
  background: rgba(108, 99, 255, 0.05);
  transform: translateY(-2px);
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 1000px;
  margin: 0 auto;
}

.typing-bubble-wrapper {
  display: flex;
  gap: 16px;
  align-self: flex-start;
  animation: fadeIn 0.3s ease-out;
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
  font-size: 1.2rem;
}

.typing-bubble {
  background-color: var(--color-bg-secondary);
  padding: 12px 20px;
  border-radius: 20px;
  border-top-left-radius: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
  border: 1px solid var(--color-border);
}

.typing-bubble span {
  width: 6px;
  height: 6px;
  background-color: var(--color-text-secondary);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-bubble span:nth-child(1) { animation-delay: -0.32s; }
.typing-bubble span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
}

.chat-footer {
  padding: 20px 40px 40px;
}

.input-container {
  max-width: 900px;
  margin: 0 auto;
}

.disclaimer {
  font-size: 0.7rem;
  color: var(--color-text-secondary);
  text-align: center;
  margin-top: 12px;
  opacity: 0.6;
}
</style>
