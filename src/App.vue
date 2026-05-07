<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
</script>

<template>
  <AppHeader />

  <main>
    <RouterView />
  </main>
  
  <AppFooter />
</template>

<style>
/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  padding-top: 75px;
  background: var(--bg-primary);
  color: var(--text-primary);
  transition: background 0.3s ease, color 0.3s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Light Theme (Default) */
:root {
  --bg-primary: #fdf0ed;
  --bg-card: #ffffff;
  --text-primary: #3e2b2b;
  --text-secondary: #8a6b6b;
  --border-color: #e8d5c8;
  --header-bg: #a83232;
  --header-text: #ffffff;
  --like-btn: #4ecdc4;
  --pass-btn: #ff6b6b;
  --favorite-btn: #ffb347;
  --shadow: rgba(168, 50, 50, 0.08);
}

/* Dark Theme */
.dark-mode {
  --bg-primary: #1a1a2e;
  --bg-card: #16213e;
  --text-primary: #e8e8e8;
  --text-secondary: #aaaaaa;
  --border-color: #2a2a4a;
  --header-bg: #0f3460;
  --header-text: #e8e8e8;
  --like-btn: #4ecdc4;
  --pass-btn: #ff6b6b;
  --favorite-btn: #f7d794;
  --shadow: rgba(0, 0, 0, 0.2);
}

/* Dark Mode Component Styles */
.dark-mode .filters-card,
.dark-mode .profile-card,
.dark-mode .match-card {
  background: var(--bg-card);
  border-color: var(--border-color);
}

.dark-mode input,
.dark-mode select,
.dark-mode textarea {
  background: #0f3460;
  color: var(--text-primary);
  border-color: var(--border-color);
}

.dark-mode input::placeholder {
  color: #888;
}

.dark-mode .interest-tag {
  background: #0f3460;
  color: var(--text-primary);
}

.dark-mode .empty-matches,
.dark-mode .no-search-message {
  background: var(--bg-card);
  color: var(--text-secondary);
}

/* Buttons keep their colors in dark mode */
.dark-mode .action-btn.like {
  background: var(--like-btn);
}

.dark-mode .action-btn.pass {
  background: var(--pass-btn);
}

.dark-mode .search-btn {
  background: #a83232;
}

/* Smooth transitions for theme switching */
.filters-card,
.profile-card,
.match-card,
input,
select,
textarea {
  transition: background 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}
</style>