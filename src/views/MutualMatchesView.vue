<template>
  <div class="mutual-matches-container">
    <div class="page-header">
      <h1>💕 Your Mutual Matches</h1>
      <p>People who liked you back - start a conversation!</p>
    </div>

    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
      <p>Loading your matches...</p>
    </div>

    <div v-else-if="mutualMatches.length === 0" class="empty-state">
      <div class="empty-icon">💔</div>
      <h3>No mutual matches yet</h3>
      <p>Like some profiles and when they like you back, they'll appear here!</p>
      <router-link to="/dashboard" class="browse-btn">Browse Profiles</router-link>
    </div>

    <div v-else class="matches-grid">
      <div 
        v-for="match in mutualMatches" 
        :key="match.id"
        class="match-card"
      >
        <div class="match-image">
          <img 
            :src="match.photo_url || '/default-avatar.png'" 
            :alt="match.name"
            @error="handleImageError"
          />
          <div class="match-badge">💕 Match!</div>
        </div>
        
        <div class="match-content">
          <div class="match-header">
            <h3>{{ match.name }}, {{ match.age }}</h3>
            <span class="location">📍 {{ match.location || 'Location not specified' }}</span>
          </div>
          
          <p class="bio">{{ truncateBio(match.bio) }}</p>
          
          <div class="interests">
            <span 
              v-for="interest in match.interests?.slice(0, 3)" 
              :key="interest"
              class="interest-tag"
            >
              {{ interest }}
            </span>
          </div>
          
          <div class="match-actions">
            <p class="matched-date">Matched on {{ formatDate(match.matched_at) }}</p>
            <button @click="startConversation(match.id)" class="message-btn">
              💬 Send Message
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const mutualMatches = ref([])
const loading = ref(true)

const loadMutualMatches = async () => {
  loading.value = true
  try {
    const response = await fetch(`${apiUrl}/api/matches`, {
      credentials: 'include'
    })
    const data = await response.json()
    if (data.success) {
      mutualMatches.value = data.data
    }
  } catch (error) {
    console.error('Error loading mutual matches:', error)
  } finally {
    loading.value = false
  }
}

const startConversation = (matchId) => {
  router.push(`/messages/${matchId}`)
}

const truncateBio = (bio) => {
  if (!bio) return 'No bio available.'
  if (bio.length > 100) {
    return bio.substring(0, 100) + '...'
  }
  return bio
}

const formatDate = (dateString) => {
  if (!dateString) return 'recently'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

const handleImageError = (e) => {
  e.target.src = '/default-avatar.png'
}

onMounted(() => {
  loadMutualMatches()
})
</script>

<style scoped>
.mutual-matches-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 10px;
}

.page-header p {
  color: #666;
  font-size: 1rem;
}

/* Loading Spinner */
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
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px;
  background: #f9f9f9;
  border-radius: 20px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 10px;
}

.empty-state p {
  color: #666;
  margin-bottom: 25px;
}

.browse-btn {
  background: linear-gradient(135deg, #ff6b6b, #ee5a5a);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 40px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: transform 0.2s;
}

.browse-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255,107,107,0.3);
}

/* Matches Grid */
.matches-grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.match-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 2px 15px rgba(0,0,0,0.08);
  display: flex;
  transition: transform 0.2s, box-shadow 0.2s;
}

.match-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.match-image {
  position: relative;
  width: 180px;
  flex-shrink: 0;
}

.match-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.match-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: linear-gradient(135deg, #ff6b6b, #ee5a5a);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: bold;
}

.match-content {
  flex: 1;
  padding: 20px;
}

.match-header {
  margin-bottom: 12px;
}

.match-header h3 {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 5px;
}

.location {
  font-size: 0.85rem;
  color: #888;
}

.bio {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 12px;
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.interest-tag {
  background: #f0f0f0;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  color: #555;
}

.match-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 10px;
}

.matched-date {
  font-size: 0.75rem;
  color: #aaa;
  margin: 0;
}

.message-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 25px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.message-btn:hover {
  transform: scale(1.02);
}

/* Responsive */
@media (max-width: 768px) {
  .match-card {
    flex-direction: column;
  }
  
  .match-image {
    width: 100%;
    height: 200px;
  }
  
  .mutual-matches-container {
    padding: 20px 15px;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
}
</style>