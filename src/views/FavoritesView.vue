<template>
  <div class="favorites-container">
    <div class="favorites-header">
      <h1>❤️ Your Saved Profiles</h1>
      <p>Profiles you've liked and saved</p>
    </div>

    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
    </div>

    <div v-else-if="favorites.length === 0" class="empty-state">
      <p>No saved profiles yet.</p>
      <router-link to="/dashboard">Browse Matches →</router-link>
    </div>

    <div v-else class="profiles-grid">
      <ProfileCard 
        v-for="profile in favorites" 
        :key="profile.id"
        :profile="profile"
        @favorite-toggled="loadFavorites"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ProfileCard from '@/components/ProfileCard.vue'

const favorites = ref([])
const loading = ref(true)
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const loadFavorites = async () => {
  loading.value = true
  try {
    const response = await fetch(`${apiUrl}/api/favorites`, {
      credentials: 'include'
    })
    const data = await response.json()
    if (data.success) {
      favorites.value = data.data
    }
  } catch (error) {
    console.error('Error loading favorites:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadFavorites()
})
</script>

<style scoped>
.favorites-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
}

.favorites-header {
  text-align: center;
  margin-bottom: 40px;
}

.favorites-header h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 10px;
}

.favorites-header p {
  color: #666;
  font-size: 1.1rem;
}

.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.empty-state {
  text-align: center;
  padding: 60px;
  background: #f9f9f9;
  border-radius: 16px;
}

.empty-state p {
  margin-bottom: 15px;
  color: #666;
}

.empty-state a {
  color: #ff6b6b;
  text-decoration: none;
  font-weight: 600;
}

.empty-state a:hover {
  text-decoration: underline;
}

.loading-spinner {
  text-align: center;
  padding: 60px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #ff6b6b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .profiles-grid {
    grid-template-columns: 1fr;
  }
}
</style>