<template>
  <div class="profile-card">
    <div class="card-image">
      <img 
        :src="profile.photo_url || '/default-avatar.png'" 
        :alt="profile.name"
        @error="handleImageError"
      />
      <div v-if="showMatchBadge" class="match-badge">
        💕 Match!
      </div>
      <div v-if="showLikeButtons" class="action-buttons">
        <button @click="handlePass" class="action-btn pass">✗</button>
        <button @click="handleLike" class="action-btn like">♥</button>
      </div>
      <button 
        @click="toggleFavorite" 
        class="favorite-btn"
        :class="{ 'favorited': isFavorited }"
      >
        {{ isFavorited ? '❤️' : '🤍' }}
      </button>
    </div>
    
    <div class="card-content">
      <div class="profile-header">
        <h3>{{ profile.name }}, {{ profile.age }}</h3>
        <span class="location">📍 {{ profile.location || 'Location not specified' }}</span>
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
        <button class="view-btn">View Profile →</button>
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
  showMatchBadge: {
    type: Boolean,
    default: false
  },
  showLikeButtons: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['favorite-toggled', 'like', 'pass'])

const isFavorited = ref(false)

const checkFavoriteStatus = async () => {
  try {
    const response = await fetch(`/api/favorites/check/${props.profile.id}`)
    const data = await response.json()
    if (data.success) {
      isFavorited.value = data.is_favorited
    }
  } catch (error) {
    console.error('Error checking favorite status:', error)
  }
}

const toggleFavorite = async () => {
  try {
    if (isFavorited.value) {
      const response = await fetch(`/api/favorites/${props.profile.id}`, {
        method: 'DELETE'
      })
      const data = await response.json()
      if (data.success) {
        isFavorited.value = false
        emit('favorite-toggled', props.profile.id)
      }
    } else {
      const response = await fetch(`/api/favorites/${props.profile.id}`, {
        method: 'POST'
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

const handleLike = async () => {
  try {
    const response = await fetch(`/api/like/${props.profile.id}`, { method: 'POST' })
    const data = await response.json()
    if (data.success) {
      if (data.mutual_match) {
        alert(`🎉 It's a match! ${props.profile.name} liked you back!`)
      }
      emit('like', props.profile.id)
    }
  } catch (error) {
    console.error('Error liking profile:', error)
  }
}

const handlePass = async () => {
  try {
    await fetch(`/api/pass/${props.profile.id}`, { method: 'POST' })
    emit('pass', props.profile.id)
  } catch (error) {
    console.error('Error passing on profile:', error)
  }
}

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
  height: 220px;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.match-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: #ff6b6b;
  color: white;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: bold;
}

.action-buttons {
  position: absolute;
  bottom: 12px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.action-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  transition: transform 0.2s;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.action-btn:hover {
  transform: scale(1.1);
}

.action-btn.pass {
  background: #ff6b6b;
  color: white;
}

.action-btn.like {
  background: #4ecdc4;
  color: white;
}

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
}

.favorite-btn:hover {
  transform: scale(1.1);
}

.favorite-btn.favorited {
  background: #ff6b6b;
  color: white;
}

.card-content {
  padding: 16px;
}

.profile-header {
  margin-bottom: 12px;
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
  margin-bottom: 16px;
}

.interest-tag {
  background: #f0f0f0;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  color: #555;
}

.interest-tag.more {
  background: #ff6b6b;
  color: white;
}

.profile-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.occupation {
  font-size: 0.8rem;
  color: #888;
}

.view-btn {
  background: none;
  border: none;
  color: #ff6b6b;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.85rem;
}

.view-btn:hover {
  text-decoration: underline;
}
</style>