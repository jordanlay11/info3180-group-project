<template>
  <header>
    <nav class="custom-navbar">
      <div class="nav-container">
        <div class="logo-group">
          <a class="logo" href="/">LuvIsland</a>
          <span v-if="userName" class="greeting">Welcome {{ userName }}</span>
        </div>
        <div class="nav-links-wrapper">
          <div class="nav-links" :class="{ show: mobileMenuOpen }">
            <template v-if="isLoggedIn">
              <!-- Dark Mode Toggle  -->
              <button @click="toggleDarkMode" class="dark-mode-btn">
                {{ isDarkMode ? '☀️' : '🌙' }}
              </button>
              <RouterLink class="nav-link" to="/dashboard">Browse</RouterLink>
              <RouterLink class="nav-link" to="/matches">Matches</RouterLink>
              <RouterLink class="nav-link" to="/favorites">Favorites</RouterLink>
              <RouterLink class="nav-link" to="/messages">Messages</RouterLink>
              <RouterLink class="nav-link" to="/profile">Profile</RouterLink>
              <button @click="handleLogout" class="nav-link logout-btn">Logout</button>
            </template>
            <RouterLink v-if="!isLoggedIn" class="nav-link" to="/login">Login</RouterLink>
          </div>
          <button class="mobile-menu-btn" type="button" @click="toggleMenu">
            <span class="menu-icon">☰</span>
          </button>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { RouterLink, useRouter } from "vue-router";

const router = useRouter();
const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:5000";
const mobileMenuOpen = ref(false);
const userName = ref("");
const isLoggedIn = ref(false);
const isDarkMode = ref(false);

const toggleMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark-mode');
    localStorage.setItem('darkMode', 'enabled');
  } else {
    document.documentElement.classList.remove('dark-mode');
    localStorage.setItem('darkMode', 'disabled');
  }
};

const loadDarkModePreference = () => {
  const savedMode = localStorage.getItem('darkMode');
  if (savedMode === 'enabled') {
    isDarkMode.value = true;
    document.documentElement.classList.add('dark-mode');
  }
};

const loadCurrentUser = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/user/me`, {
      method: "GET",
      credentials: "include",
    });

    if (response.status === 401) {
      userName.value = "";
      isLoggedIn.value = false;
      return;
    }

    if (response.ok) {
      const data = await response.json();
      if (data.success && data.data) {
        userName.value = data.data.fname || data.data.username || "";
        isLoggedIn.value = true;
        return;
      }
    }
  } catch (error) {
    console.error("Fetch current user error:", error);
  }

  userName.value = "";
  isLoggedIn.value = false;
};

const handleLogout = async () => {
  try {
    await fetch(`${apiUrl}/logout`, {
      method: "POST",
      credentials: "include",
    });
  } catch (error) {
    console.error("Logout error:", error);
  } finally {
    userName.value = "";
    isLoggedIn.value = false;
    router.push("/login");
  }
};

onMounted(() => {
  loadCurrentUser();
  loadDarkModePreference();
});
</script>

<style scoped>
.custom-navbar {
  background: var(--header-bg, #a83232);
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.logo-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.greeting {
  color: #ffd4c4;
  font-size: 1rem;
  font-weight: 500;
}

.logo:hover {
  color: #ffd4c4;
}

.nav-links-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.dark-mode-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.2s;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dark-mode-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.nav-link:hover {
  color: #ffd4c4;
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.router-link-active {
  color: #ffd4c4;
  border-bottom: 2px solid #ffd4c4;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .mobile-menu-btn {
    display: block;
  }

  .nav-links {
    display: none;
    width: 100%;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem 0;
    margin-top: 1rem;
  }

  .nav-links.show {
    display: flex;
  }

  .nav-links-wrapper {
    width: auto;
  }

  .custom-navbar {
    padding: 1rem;
  }
}
</style>