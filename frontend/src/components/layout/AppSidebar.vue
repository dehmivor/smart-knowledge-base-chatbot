<template>
  <aside class="app-sidebar">
    <div class="logo">
      <span class="logo-text">Brother SKB</span>
    </div>

    <nav class="nav-menu">
      <router-link to="/" class="nav-item">
        <span class="label">Chat Assistant</span>
      </router-link>
      <router-link to="/documents" class="nav-item">
        <span class="label">Knowledge Base</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <div class="status-indicator">
        <span class="status-text">System Online</span>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.app-sidebar {
  width: 260px;
  background-color: var(--color-bg-tertiary);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  padding: 24px;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 48px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: var(--color-accent-primary);
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.5px;
  background: var(--color-accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  text-decoration: none;
  color: var(--color-text-secondary);
  border-radius: 12px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.03);
  color: var(--color-text-primary);
}

.nav-item.router-link-active {
  background: rgba(108, 99, 255, 0.1);
  color: var(--color-accent-primary);
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 24px;
  border-top: 1px solid var(--color-border);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  background-color: var(--color-success);
  border-radius: 50%;
}

.pulse {
  box-shadow: 0 0 0 rgba(0, 230, 118, 0.4);
  animation: pulse 2s infinite;
}

.status-text {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

@keyframes pulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 230, 118, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 230, 118, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 230, 118, 0); }
}
</style>
