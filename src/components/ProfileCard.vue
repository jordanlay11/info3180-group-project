<template>
  <div class="profile-card">
    <div class="card-image">
      <img 
        :src="profile.photo_url || '/default-avatar.png'" 
        :alt="profile.name"
        @error="handleImageError"
      />
      
      <!-- Match Score Badge -->
      <div v-if="matchScore" class="match-score-badge">
        {{ matchScore }}% Match
      </div>
      
      <!-- Like/Pass Buttons -->
      <div v-if="showLikeButtons" class="action-buttons">
        <button @click="handlePass" class="action-btn pass" :disabled="isLiked">
          ✗ Pass
        </button>
        <button 
          @click="handleLike" 
          class="action-btn like" 
          :class="{ 'liked': isLiked }"
          :disabled="isLiked"
        >
          {{ isLiked ? '✓ Liked' : '♥ Like' }}
        </button>
      </div>
      
      <!-- Favorite Button -->
      <button 
        @click="toggleFavorite" 
        class="favorite-btn"
        :class="{ 'favorited': isFavorited }"
      >
        {{ isFavorited ? '❤️' : '🤍' }}
      </button>
    </div>
    
    <!-- Card Content -->
    <div class="card-content">
      <div class="profile-header">
        <h3>{{ profile.name }}, {{ profile.age }}</h3>
        <span class="location">📍 {{ profile.location || 'Location not specified' }}</span>
      </div>
      
      <!-- Match Reasons (Optional) -->
      <div v-if="matchReasons && matchReasons.length" class="match-reasons">
        <span v-for="reason in matchReasons.slice(0, 2)" :key="reason" class="reason-tag">
          {{ reason }}
        </span>
      </div>
      
      <p class="bio">{{ truncateBio(profile.bio) }}</p>
      
      <div class="interests">
        <span 
          v-for="interest in profile.interests?.slice(0, 4)" 
          :key="interest"
          class="interest-tag"
        >
          {{ interest }}
        </span>
        <span v-if="profile.interests?.length > 4" class="interest-tag more">
          +{{ profile.interests.length - 4 }}
        </span>
      </div>
      
      <div class="profile-footer">
        <div class="occupation" v-if="profile.occupation">
          💼 {{ profile.occupation }}
        </div>
        <!-- View Profile Button - Just visual for now -->
        <button class="view-profile-btn">
          View Profile →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  profile: {
    type: Object,
    required: true
  },
  showLikeButtons: {
    type: Boolean,
    default: false
  },
  matchScore: {
    type: Number,
    default: null
  },
  matchReasons: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['favorite-toggled', 'like', 'pass'])

const isFavorited = ref(false)
const isLiked = ref(false)
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'

// Check if profile is already liked
const checkLikeStatus = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/liked/check/${props.profile.id}`, {
      credentials: 'include'
    })
    const data = await response.json()
    if (data.success) {
      isLiked.value = data.is_liked
    }
  } catch (error) {
    console.error('Error checking like status:', error)
  }
}

// Check if profile is favorited
const checkFavoriteStatus = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/favorites/check/${props.profile.id}`, {
      credentials: 'include'
    })
    const data = await response.json()
    if (data.success) {
      isFavorited.value = data.is_favorited
    }
  } catch (error) {
    console.error('Error checking favorite status:', error)
  }
}

// Toggle favorite
const toggleFavorite = async () => {
  try {
    if (isFavorited.value) {
      const response = await fetch(`${apiUrl}/api/favorites/${props.profile.id}`, {
        method: 'DELETE',
        credentials: 'include'
      })
      const data = await response.json()
      if (data.success) {
        isFavorited.value = false
        emit('favorite-toggled', props.profile.id)
      }
    } else {
      const response = await fetch(`${apiUrl}/api/favorites/${props.profile.id}`, {
        method: 'POST',
        credentials: 'include'
      })
      const data = await response.json()
      if (data.success) {
        isFavorited.value = true
        emit('favorite-toggled', props.profile.id)
      }
    }
  } catch (error) {
    console.error('Error toggling favorite:', error)
  }
}

// Handle Like
const handleLike = async () => {
  if (isLiked.value) return
  
  try {
    const response = await fetch(`${apiUrl}/api/like/${props.profile.id}`, {
      method: 'POST',
      credentials: 'include'
    })
    const data = await response.json()
    if (data.success) {
      isLiked.value = true
      if (data.mutual_match) {
        alert(`🎉 It's a match! You and ${props.profile.name} liked each other!`)
      }
      emit('like', props.profile.id)
    } else if (data.message === 'Already liked') {
      isLiked.value = true
    }
  } catch (error) {
    console.error('Error liking profile:', error)
  }
}

// Handle Pass
const handlePass = async () => {
  try {
    await fetch(`${apiUrl}/api/pass/${props.profile.id}`, {
      method: 'POST',
      credentials: 'include'
    })
    emit('pass', props.profile.id)
  } catch (error) {
    console.error('Error passing on profile:', error)
  }
}

// Helper functions
const truncateBio = (bio) => {
  if (!bio) return 'No bio available.'
  if (bio.length > 100) {
    return bio.substring(0, 100) + '...'
  }
  return bio
}

const handleImageError = (e) => {
  e.target.src = '/default-avatar.png'
}

onMounted(() => {
  checkFavoriteStatus()
  checkLikeStatus()
})
</script>

<style scoped>
.profile-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.card-image {
  position: relative;
  height: 240px;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Match Score Badge */
.match-score-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: linear-gradient(135deg, #ff6b6b, #ee5a5a);
  color: white;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: bold;
  z-index: 2;
}

/* Like/Pass Action Buttons */
.action-buttons {
  position: absolute;
  bottom: 12px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 15px;
  z-index: 2;
}

.action-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 30px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
}

.action-btn:hover {
  transform: scale(1.05);
}

.action-btn.pass {
  background: rgba(255, 107, 107, 0.9);
  color: white;
}

.action-btn.pass:hover {
  background: #ff6b6b;
}

.action-btn.like {
  background: rgba(78, 205, 196, 0.9);
  color: white;
}

.action-btn.like:hover {
  background: #4ecdc4;
}

.action-btn.like.liked {
  background: #2e7d32;
  cursor: default;
  opacity: 0.7;
}

.action-btn.like.liked:hover {
  transform: none;
}

.action-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.action-btn:disabled:hover {
  transform: none;
}

/* Favorite Button */
.favorite-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.favorite-btn:hover {
  transform: scale(1.1);
}

.favorite-btn.favorited {
  background: #ff6b6b;
  color: white;
}

/* Card Content */
.card-content {
  padding: 16px;
}

.profile-header {
  margin-bottom: 8px;
}

.profile-header h3 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 4px;
}

.location {
  font-size: 0.85rem;
  color: #888;
}

/* Match Reasons */
.match-reasons {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 8px 0;
}

.reason-tag {
  background: #e8f5e9;
  color: #2e7d32;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.7rem;
}

/* Bio */
.bio {
  color: #666;
  font-size: 0.85rem;
  line-height: 1.4;
  margin-bottom: 12px;
}

/* Interests */
.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.interest-tag {
  background: #f0f0f0;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.7rem;
  color: #555;
}

.interest-tag.more {
  background: #ff6b6b;
  color: white;
}

/* Profile Footer */
.profile-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 8px;
}

.occupation {
  font-size: 0.75rem;
  color: #888;
}

.view-profile-btn {
  background: none;
  border: none;
  color: #ff6b6b;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 20px;
  transition: all 0.2s;
}

.view-profile-btn:hover {
  background: #fff0f0;
  text-decoration: underline;
}
</style>