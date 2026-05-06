<template>
  <header>
    <nav class="custom-navbar">
      <div class="nav-container">
        <div class="logo-group">
          <a class="logo" href="/">APP NAME</a>
          <span v-if="userName" class="greeting">Welcome {{ userName }}</span>
        </div>
        <button class="mobile-menu-btn" type="button" @click="toggleMenu">
          <span class="menu-icon">☰</span>
        </button>
        <div class="nav-links" :class="{ show: mobileMenuOpen }">
          <!-- Only show when logged in -->
          <template v-if="isLoggedIn">
            <RouterLink class="nav-link" to="/dashboard">Browse</RouterLink>
            <RouterLink class="nav-link" to="/matches">Matches</RouterLink>
            <RouterLink class="nav-link" to="/favorites">Favorites</RouterLink>
            <RouterLink class="nav-link" to="/messages">Messages</RouterLink>
            <RouterLink class="nav-link" to="/profile">Profile</RouterLink>
            <button @click="handleLogout" class="nav-link logout-btn">
              Logout
            </button>
          </template>
          
          <!-- Only show login when NOT logged in -->
          <RouterLink v-if="!isLoggedIn" class="nav-link" to="/login">Login</RouterLink>
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

const toggleMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
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

onMounted(loadCurrentUser);
</script>

<style scoped>

.custom-navbar {
  background: #a83232;
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

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
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

/* Active link style */
.router-link-active {
  color: #ffd4c4;
  border-bottom: 2px solid #ffd4c4;
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

  .custom-navbar {
    padding: 1rem;
  }
}
</style>