<template>
  <div class="app-container">
    <AppSidebar />
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import AppSidebar from '@/components/layout/AppSidebar.vue'
</script>

<style>
@import '@/assets/styles/main.css';

.app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.app-main {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #0f0f1a 100%);
}

/* Page transitions */
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
