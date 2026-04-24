<template>
  <div class="app-wrapper">
    <nav class="sidebar">
      <div class="logo">
        <span class="logo-icon">🤖</span>
        <span class="logo-text">SKBC</span>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-item">💬 Chat</router-link>
        <router-link to="/documents" class="nav-item">🗄️ Tài liệu</router-link>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

:root {
  --bg-primary: #0f0f1a;
  --bg-secondary: #16213e;
  --accent: #6c63ff;
  --text: #e8e8e8;
}

body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background-color: var(--bg-primary);
  color: var(--text);
}

.app-wrapper {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 240px;
  background: var(--bg-secondary);
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 50px;
  padding: 0 10px;
}

.logo-icon {
  font-size: 1.5rem;
}

.logo-text {
  font-weight: 600;
  font-size: 1.2rem;
  letter-spacing: 1px;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.nav-item {
  text-decoration: none;
  color: #a0a0b0;
  padding: 12px 15px;
  border-radius: 10px;
  transition: all 0.2s;
}

.nav-item:hover, .router-link-active {
  background: rgba(108, 99, 255, 0.1);
  color: var(--text);
}

.router-link-active {
  border-left: 3px solid var(--accent);
}

.main-content {
  flex: 1;
  overflow-y: auto;
  background: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #0f0f1a 100%);
}
</style>
