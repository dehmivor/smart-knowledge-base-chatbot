<template>
  <div class="chat-view">
    <div class="chat-header">
      <div class="chat-info">
        <h2 class="title">Chat Assistant</h2>
        <p class="subtitle" v-if="documentCount > 0">Searching through {{ documentCount }} documents</p>
        <p class="subtitle" v-else>Upload documents to start searching</p>
      </div>
      <div class="chat-actions">
        <button class="action-btn" @click="clearChat">
          Clear Chat
        </button>
      </div>
    </div>

    <div class="chat-window" ref="scrollContainer">
      <div v-if="messages.length === 0" class="welcome-container">
        <div class="welcome-card">
          <h1>How can I help you?</h1>
          <p v-if="documentCount > 0">
            I'm ready to answer questions based on the <strong>{{ documentCount }}</strong> documents 
            currently in your knowledge base.
          </p>
          <p v-else>
            Welcome! Please upload some documents to the <strong>Knowledge Base</strong> 
            so I có thể hỗ trợ bạn tra cứu thông tin.
          </p>
          
          <div v-if="documentCount > 0" class="suggestion-grid">
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
const documentCount = ref(0)

const suggestions = [
  "What is the company's leave policy?",
  "Tell me about the onboarding process.",
  "What are the technical standards for development?",
  "How do I request a hardware upgrade?"
]

const fetchDocumentCount = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/documents/')
    documentCount.value = res.data.length
  } catch (err) {
    console.error('Failed to fetch document count:', err)
  }
}

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
  fetchDocumentCount()
})
</script>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--color-bg-primary);
}

.chat-header {
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

.action-btn {
  background: transparent;
  border: none;
  padding: 0;
  color: var(--color-text-secondary);
  cursor: pointer;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: color 0.2s;
}

.action-btn:hover {
  color: var(--color-text-primary);
}

.chat-window {
  flex: 1;
  overflow-y: auto;
  padding: 60px;
}

.welcome-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.welcome-card {
  max-width: 500px;
  text-align: center;
}

.welcome-card h1 {
  font-size: 1.5rem;
  font-weight: 400;
  margin-bottom: 24px;
  color: var(--color-text-primary);
  letter-spacing: -0.5px;
}

.suggestion-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 40px;
}

.suggestion-item {
  padding: 12px 20px;
  background: transparent;
  border: 1px solid var(--color-border);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  color: var(--color-text-secondary);
}

.suggestion-item:hover {
  border-color: var(--color-text-primary);
  color: var(--color-text-primary);
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 40px;
  max-width: 800px;
  margin: 0 auto;
}

.typing-bubble-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-self: flex-start;
}

.typing-bubble {
  display: flex;
  align-items: center;
  gap: 4px;
  padding-left: 0;
}

.typing-bubble span {
  width: 4px;
  height: 4px;
  background-color: var(--color-border);
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
  padding: 40px 60px;
}

.input-container {
  max-width: 800px;
  margin: 0 auto;
}

.disclaimer {
  font-size: 0.6rem;
  color: var(--color-text-secondary);
  text-align: center;
  margin-top: 24px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.5;
}

</style>
