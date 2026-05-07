<template>
  <div class="profile-container">

    <!-- LOADING -->
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
    </div>

    <!-- ERROR -->
    <div v-else-if="error" class="empty-state">
      <p>⚠️ {{ error }}</p>
      <button class="btn-retry" @click="fetchProfile">Try Again</button>
    </div>

    <!-- PROFILE CARD -->
    <div v-else class="profile-card">

      <!-- HERO BANNER -->
      <div class="hero-banner">
        <div class="avatar-wrap">
          <img
            :src="profilePhotoUrl"
            :alt="`${profile.first_name}'s photo`"
            class="avatar"
            @error="handleImageError"
          />
        </div>

        <div class="hero-info">
          <h1 class="name">{{ profile.first_name }} {{ profile.last_name }}</h1>
          <p class="handle">@{{ profile.username }}</p>
          <div class="meta-pills">
            <span class="pill">🎂 {{ age }} years old</span>
            <span class="pill">📍 {{ profile.location || 'Location not set' }}</span>
            <span class="pill">{{ genderLabel }}</span>
          </div>
        </div>

        <!-- Own profile: show Edit button -->
        <button v-if="isOwnProfile" class="btn-edit" @click="goToEditProfile">
          ✏️ Edit Profile
        </button>

      </div>

      <!-- BODY -->
      <div class="profile-body">

        <!-- BIO -->
        <section class="section">
          <h2 class="section-title">About Me</h2>
          <p class="bio">{{ profile.bio || 'No bio yet.' }}</p>
        </section>

        <!-- INTERESTS -->
        <section class="section">
          <h2 class="section-title">Interests</h2>
          <div class="tags">
            <span
              v-for="interest in interestNames"
              :key="interest"
              class="tag"
            >
              {{ interest }}
            </span>
            <span v-if="!interestNames.length" class="tag muted">
              No interests added yet
            </span>
          </div>
        </section>

        <!-- PREFERENCES -->
        <section class="section">
          <h2 class="section-title">Looking For</h2>
          <div class="prefs-grid">
            <div class="pref-item">
              <span class="pref-label">Interested In</span>
              <span class="pref-value">{{ lookingForGenderLabel }}</span>
            </div>
            <div class="pref-item">
              <span class="pref-label">Age Range</span>
              <span class="pref-value">
                {{ profile.preferred_age_min || 18 }}–{{ profile.preferred_age_max || 99 }}
              </span>
            </div>
            <div class="pref-item">
              <span class="pref-label">Max Distance</span>
              <span class="pref-value">{{ profile.max_distance || 50 }} km</span>
            </div>
          </div>
        </section>

        <!-- STATS (own profile only) -->
        <section v-if="isOwnProfile" class="section">
          <h2 class="section-title">Your Stats</h2>
          <div class="stats-row">
            <div class="stat">
              <span class="stat-number">{{ profile.match_count }}</span>
              <span class="stat-label">Matches</span>
            </div>
            <div class="stat">
              <span class="stat-number">{{ profile.likes_received }}</span>
              <span class="stat-label">Likes Received</span>
            </div>
            <div class="stat">
              <span class="stat-number">{{ profile.profile_views }}</span>
              <span class="stat-label">Profile Views</span>
            </div>
          </div>
        </section>

      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8081'

const profile = ref({})
const loading = ref(true)
const error = ref(null)
const isFavourited = ref(false)
const currentUserId = ref(null)

// ── COMPUTED ──────────────────────────────────────────────────────────────

// Get current logged-in user ID
const getCurrentUserId = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/user/me`, {
      credentials: 'include'
    })
    const data = await response.json()
    if (data.success) {
      currentUserId.value = data.data.id
    }
  } catch (error) {
    console.error('Error getting current user:', error)
  }
}

// Get profile ID from route params
const profileIdFromRoute = computed(() => route.params.id ? parseInt(route.params.id) : null)

// Check if viewing own profile
const isOwnProfile = computed(() => {
  // If no ID in route, it's the current user's own profile
  if (!profileIdFromRoute.value) return true
  // Otherwise, check if the ID matches the logged-in user
  return profileIdFromRoute.value === currentUserId.value
})

// Profile photo URL
const profilePhotoUrl = computed(() => {
  const photo = profile.value.profile_photo
  if (!photo) return '/default-avatar.png'
  if (photo.startsWith('http')) return photo
  return `${apiUrl}/api/uploads/${photo}`
})

const interestNames = computed(() => {
  if (!profile.value.interests) return []
  return profile.value.interests.map(i =>
    typeof i === 'object' ? (i.name || i.interest || '') : i
  ).filter(Boolean)
})

const age = computed(() => {
  const dob = profile.value.date_of_birth
  if (!dob) return '?'
  const birth = new Date(dob)
  if (isNaN(birth.getTime())) return '?'
  const today = new Date()
  let years = today.getFullYear() - birth.getFullYear()
  const m = today.getMonth() - birth.getMonth()
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) years--
  return years
})

const genderLabel = computed(() => {
  const map = { M: '♂ Male', F: '♀ Female', O: '⚧ Other' }
  return map[profile.value.gender] || profile.value.gender || 'Not specified'
})

const lookingForGenderLabel = computed(() => {
  const map = {
    'male': '👨 Men',
    'female': '👩 Women',
    'all': '👥 Everyone'
  }
  return map[profile.value.looking_for_gender] || 'Everyone'
})

// ── METHODS ───────────────────────────────────────────────────────────────

async function fetchProfile() {
  loading.value = true
  error.value = null
  
  try {
    let url
    if (isOwnProfile.value || !profileIdFromRoute.value) {
      // Fetch own profile
      url = `${apiUrl}/api/user/info`
    } else {
      // Fetch other user's profile
      url = `${apiUrl}/api/profile/${profileIdFromRoute.value}`
    }
    
    const res = await fetch(url, { 
      method: "GET", 
      credentials: 'include' 
    })
    
    if (res.ok) {
      const data = await res.json()
      if (data.success && data.data) {
        const p = data.data
        profile.value = {
          id: p.id,
          first_name: p.fname,
          last_name: p.lname,
          username: p.username,
          bio: p.bio,
          interests: p.interests || [],
          location: p.location,
          occupation: p.occupation,
          zodiac_sign: p.zodiac_sign,
          gender: p.gender,
          date_of_birth: p.date_of_birth,
          profile_photo: p.profile_photo,
          visibility: p.visibility,
          preferred_age_min: p.preferred_age_min,
          preferred_age_max: p.preferred_age_max,
          max_distance: p.preferred_location_radius,
          match_count: p.match_count || 0,
          likes_received: p.likes_received || 0,
          profile_views: p.profile_views || 0,
          looking_for_gender: p.looking_for_gender || 'all',
        }
      } else {
        error.value = data.error || 'Failed to load profile'
      }
    } else if (res.status === 401) {
      error.value = 'Please log in to view this profile'
    } else if (res.status === 403) {
      error.value = 'This profile is private'
    } else if (res.status === 404) {
      error.value = 'Profile not found'
    } else {
      error.value = 'Could not load profile'
    }
  } catch (err) {
    console.error('Error loading profile:', err)
    error.value = 'Could not load profile. Please try again.'
  } finally {
    loading.value = false
  }
}

async function likeProfile() {
  try {
    const res = await fetch(`${apiUrl}/api/like/${profile.value.id}`, {
      method: 'POST',
      credentials: 'include'
    })
    const data = await res.json()
    if (data.success && data.mutual_match) {
      alert('🎉 It\'s a match!')
    }
  } catch (err) {
    console.error('Error liking profile:', err)
  }
}

async function toggleFavourite() {
  try {
    const res = await fetch(`${apiUrl}/api/favorites/${profile.value.id}`, {
      method: isFavourited.value ? 'DELETE' : 'POST',
      credentials: 'include'
    })
    const data = await res.json()
    if (data.success) isFavourited.value = !isFavourited.value
  } catch (err) {
    console.error('Error toggling favourite:', err)
  }
}

const goToEditProfile = () => {
  router.push('/profile/edit')
}

function handleImageError(e) {
  e.target.src = '/default-avatar.png'
}

// Watch for route changes (when navigating from one profile to another)
watch(() => route.params.id, () => {
  fetchProfile()
})

onMounted(async () => {
  await getCurrentUserId()
  await fetchProfile()
})
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  background: var(--bg-primary);  /* Add this */
  min-height: 100vh;
}

/* Loading / Error */
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

.empty-state {
  text-align: center;
  padding: 60px;
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-color);
}

.empty-state p {
  margin-bottom: 15px;
  color: var(--text-secondary);
}

/* Profile Card */
.profile-card {
  background: var(--bg-card);
  border-radius: 16px;
  box-shadow: 0 2px 20px var(--shadow);
  overflow: hidden;
  border: 1px solid var(--border-color);
}

/* Hero Banner - Keep gradient, but text uses variables */
.hero-banner {
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 4px solid white;
  object-fit: cover;
  background: #ddd;
}

.name {
  color: white;
  font-size: 1.8rem;
  margin: 0 0 0.2rem;
  font-weight: 700;
}

.handle {
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 0.75rem;
  font-size: 0.95rem;
}

.meta-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.pill {
  background: rgba(255, 255, 255, 0.25);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
}

/* Buttons */
.btn-edit {
  background: white;
  color: #ff6b6b;
  padding: 0.5rem 1.25rem;
  border: none;
  border-radius: 999px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.15s, opacity 0.15s;
}

.btn-edit:hover {
  transform: scale(1.05);
  opacity: 0.9;
}

/* Profile Body */
.profile-body {
  padding: 2rem;
}

.section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #ff6b6b;
  margin-bottom: 0.75rem;
}

.bio {
  color: var(--text-primary);
  line-height: 1.7;
}

/* Tags */
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: #fff0f0;
  color: #ff6b6b;
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.tag.muted {
  background: #f3f4f6;
  color: #9ca3af;
}

/* Dark mode tags */
.dark-mode .tag {
  background: #0f3460;
  color: #ff8e8e;
}

.dark-mode .tag.muted {
  background: #2a2a4a;
  color: #888;
}

/* Preferences Grid */
.prefs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
}

.pref-item {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 0.75rem 1rem;
}

.pref-label {
  display: block;
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.pref-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

/* Stats */
.stats-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.stat {
  flex: 1;
  min-width: 100px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 1rem;
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: 800;
  color: #ff6b6b;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-banner {
    flex-direction: column;
    text-align: center;
  }
  .meta-pills {
    justify-content: center;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>