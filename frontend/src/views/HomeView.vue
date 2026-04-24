<template>
  <div class="chat-container">
    <div class="chat-messages" ref="messageContainer">
      <div v-if="messages.length === 0" class="welcome-screen">
        <div class="robot-icon">🤖</div>
        <h1>Tôi có thể giúp gì cho bạn?</h1>
        <p>Hãy hỏi tôi bất cứ điều gì về tài liệu đã upload.</p>
      </div>

      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
        <div class="bubble">
          <div class="text" v-html="renderMarkdown(msg.content)"></div>
          
          <!-- Hiển thị nguồn nếu có -->
          <div v-if="msg.sources && msg.sources.length > 0" class="sources">
            <p class="source-title">📚 Nguồn tham khảo:</p>
            <div class="source-list">
              <span v-for="(src, i) in uniqueSources(msg.sources)" :key="i" class="source-tag">
                {{ src }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="message assistant">
        <div class="bubble typing">
          <span></span><span></span><span></span>
        </div>
      </div>
    </div>

    <div class="chat-input-area">
      <div class="input-wrapper">
        <textarea 
          v-model="userInput" 
          placeholder="Nhập câu hỏi tại đây..." 
          @keydown.enter.prevent="sendMessage"
          rows="1"
          ref="chatInput"
        ></textarea>
        <button @click="sendMessage" :disabled="isLoading || !userInput.trim()">
          <span v-if="!isLoading">🚀</span>
          <span v-else>...</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
// Lưu ý: Bạn có thể cài thêm marked để render markdown đẹp hơn, tạm thời tôi dùng text thô
const renderMarkdown = (text) => text.replace(/\n/g, '<br>')

const API_CHAT = 'http://localhost:8000/api/v1/chat/'
const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const messageContainer = ref(null)

const scrollToBottom = async () => {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

const uniqueSources = (sources) => {
  return [...new Set(sources.map(s => s.filename))]
}

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return

  const userMsg = userInput.value
  messages.value.push({ role: 'user', content: userMsg })
  userInput.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    const res = await axios.post(API_CHAT, { message: userMsg })
    messages.value.push({ 
      role: 'assistant', 
      content: res.data.answer,
      sources: res.data.sources
    })
  } catch (err) {
    messages.value.push({ 
      role: 'assistant', 
      content: '❌ Có lỗi xảy ra: ' + (err.response?.data?.detail || err.message) 
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.welcome-screen {
  text-align: center;
  margin-top: 100px;
  color: #a0a0b0;
}

.robot-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.message {
  display: flex;
  max-width: 85%;
}

.message.user {
  align-self: flex-end;
}

.message.assistant {
  align-self: flex-start;
}

.bubble {
  padding: 15px 20px;
  border-radius: 20px;
  line-height: 1.5;
  font-size: 1.05rem;
}

.user .bubble {
  background: linear-gradient(135deg, #6c63ff, #00d2ff);
  color: white;
  border-bottom-right-radius: 4px;
}

.assistant .bubble {
  background: #1a1a2e;
  color: #e8e8e8;
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-bottom-left-radius: 4px;
}

.sources {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.source-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6c63ff;
  margin-bottom: 5px;
}

.source-tag {
  display: inline-block;
  background: rgba(108, 99, 255, 0.1);
  color: #00d2ff;
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 4px;
  margin-right: 5px;
}

.chat-input-area {
  padding: 20px 0;
}

.input-wrapper {
  background: #16213e;
  border-radius: 15px;
  padding: 10px 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

textarea {
  flex: 1;
  background: transparent;
  border: none;
  color: white;
  resize: none;
  font-family: inherit;
  font-size: 1rem;
  outline: none;
  max-height: 150px;
}

button {
  background: #6c63ff;
  border: none;
  width: 45px;
  height: 45px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

button:hover:not(:disabled) {
  transform: scale(1.05);
  background: #00d2ff;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Typing animation */
.typing span {
  width: 8px;
  height: 8px;
  background: #a0a0b0;
  display: inline-block;
  border-radius: 50%;
  margin: 0 2px;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing span:nth-child(1) { animation-delay: -0.32s; }
.typing span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
}
</style>
