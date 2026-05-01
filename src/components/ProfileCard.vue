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
    
    <!-- Rest of card content... -->
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
const isLiked = ref(false)  // ← ADD THIS
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
  if (isLiked.value) return  // Already liked, do nothing
  
  try {
    const response = await fetch(`${apiUrl}/api/like/${props.profile.id}`, {
      method: 'POST',
      credentials: 'include'
    })
    const data = await response.json()
    if (data.success) {
      isLiked.value = true  // Mark as liked immediately
      if (data.mutual_match) {
        alert(`🎉 It's a match! You and ${props.profile.name} liked each other!`)
      }
      emit('like', props.profile.id)
    } else if (data.message === 'Already liked') {
      isLiked.value = true  // Already liked, update UI
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
  checkLikeStatus()  // ← ADD THIS
})
</script>

<style scoped>
/* ... existing styles ... */

.action-btn.like {
  background: rgba(78, 205, 196, 0.9);
  color: white;
}

.action-btn.like:hover {
  background: #4ecdc4;
}

/* NEW: Liked button style */
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
</style>