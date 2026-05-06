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
            <span class="pill">📍 {{ profile.parish || 'Location not set' }}</span>
            <span class="pill">{{ genderLabel }}</span>
          </div>
        </div>

        <!-- Own profile: show Edit button -->
        <button v-if="isOwnProfile" class="btn-edit" @click="goToEditProfile">
          ✏️ Edit Profile
        </button>

        <!-- Other user's profile: show Like / Favourite buttons -->
        <div v-else class="action-buttons">
          <button class="btn-like" @click="likeProfile">❤️ Like</button>
          <button class="btn-favourite" @click="toggleFavourite">
            {{ isFavourited ? '🔖 Saved' : '🔖 Save' }}
          </button>
        </div>
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
              <span class="pref-value">{{ profile.looking_for || 'Any' }}</span>
            </div>
            <div class="pref-item">
              <span class="pref-label">Age Range</span>
              <span class="pref-value">
                {{ profile.preferred_age_min || '18' }}–{{ profile.preferred_age_max || '99' }}
              </span>
            </div>
            <div class="pref-item">
              <span class="pref-label">Max Distance</span>
              <span class="pref-value">{{ profile.max_distance || '50' }} km</span>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route  = useRoute()
const router = useRouter()

// Matches the group's pattern from Favorites.vue
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const profile      = ref({})
const loading      = ref(true)
const error        = ref(null)
const isFavourited = ref(false)

// ── COMPUTED ──────────────────────────────────────────────────────────────

const loggedInUserId = computed(() => Number(localStorage.getItem('user_id')))


// Always show own profile
const isOwnProfile = computed(() => true)

// Handles both a full URL and a relative path returned by Flask
const profilePhotoUrl = computed(() => {
  const photo = profile.value.photo || profile.value.profile_photo || profile.value.photo_url
  //if (!photo) return 'https://media.istockphoto.com/id/2221915585/vector/grey-avatar-icon-user-avatar-photo-icon-social-media-user-icon-vector.jpg'
  //if (photo.startsWith('http')) return photo
  return `${apiUrl}/${photo}`
})

const interestNames = computed(() => {
  if (!profile.value.interests) return [];
  return profile.value.interests.map(i =>
    typeof i === 'object' ? (i.name || i.interest || '') : i
  ).filter(Boolean);
});

const age = computed(() => {
  const dob = profile.value.date_of_birth || profile.value.dob
  if (!dob) return '?'
  const birth = new Date(dob)
  if (isNaN(birth.getTime())) return '?'
  const today = new Date()
  let years   = today.getFullYear() - birth.getFullYear()
  const m     = today.getMonth() - birth.getMonth()
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) years--
  return years
})

const genderLabel = computed(() => {
  const map = { M: '♂ Male', F: '♀ Female', O: '⚧ Other' }
  return map[profile.value.gender] || profile.value.gender || 'Not specified'
})

// ── METHODS ───────────────────────────────────────────────────────────────

// const loadCurrentUser = async () => {
//   try {
//     const response = await fetch(`${apiUrl}/api/user/me`, {
//       method: "GET",
//       credentials: "include",
//     });
// 
//     if (response.ok) {
//       const data = await response.json();
//       if (data.success && data.data) {
//         userName.value = data.data.fname || data.data.username || "";
//         isLoggedIn.value = true;
//         return;
//       }
//     }
//   } catch (error) {
//     console.error("Fetch current user error:", error);
//   }
// 
//   userName.value = "";
//   isLoggedIn.value = false;
// };

async function fetchProfile() {
  loading.value = true
  error.value   = null
  try {
    const url = `${apiUrl}/api/user/info`
    const res  = await fetch(url, { method: "GET", credentials: 'include' })
    if (res.ok){
      const data = await res.json()
      if (data.success && data.data) {
        profile.value = {
          first_name : data.data.fname,
          last_name : data.data.lname,
          username : data.data.username,
          bio : data.data.bio || data.data.description,
          interests : data.data.interests || [], 
          parish : data.data.location,
          looking_for : data.data.gender_preference || '',
          preferred_age_min : data.data.age_min || '',
          preferred_age_max : data.data.age_max || '',
          max_distance : data.data.max_distance || '',
          match_count : data.data.match_count || 0,
          likes_received : data.data.likes_received || 0,
          profile_views : data.data.profile_views || 0,
          gender : data.data.gender || 'Not Specified',
          date_of_birth : data.data.dob || ''
        }
      }
    }
    // // Handles both { success: true, data: {...} } and a plain object response
    // let p = data.success ? data.data : data
    // 
    // // Map backend fields to frontend expectations for display
    // profile.value = {
    //   ...p,
    //   first_name: p.first_name || p.fname || '',
    //   last_name: p.last_name || p.lname || '',
    //   username: p.username || p.handle || '',
    //   bio: p.bio || p.description || '',
    //   interests: p.interests || [],
    //   parish: p.parish || p.location || '',
    //   looking_for: p.looking_for || p.gender_preference || '',
    //   preferred_age_min: p.preferred_age_min || p.age_min || '',
    //   preferred_age_max: p.preferred_age_max || p.age_max || '',
    //   max_distance: p.max_distance || '',
    //   match_count: p.match_count || 0,
    //   likes_received: p.likes_received || 0,
    //   profile_views: p.profile_views || 0,
    //   gender: p.gender || '',
    //   date_of_birth: p.date_of_birth || p.dob || '',
    // }

  } catch (err) {
    error.value = 'Could not load profile. Please try again.'
    console.error('Error loading profile:', err)
  } finally {
    loading.value = false
  }
}

async function likeProfile() {
  try {
    // NOTE: Confirm the like endpoint with your Backend Lead
    const res  = await fetch(`${apiUrl}/api/users/${profileId.value}/like`, {
      method: 'POST',
      credentials: 'include'
    })
    const data = await res.json()
    if (data.success) alert('❤️ Liked!')
  } catch (err) {
    console.error('Error liking profile:', err)
  }
}

async function toggleFavourite() {
  try {
    // NOTE: Confirm the favourites endpoint with your Backend Lead
    const res  = await fetch(`${apiUrl}/api/favorites/${profileId.value}`, {
      method: isFavourited.value ? 'DELETE' : 'POST',
      credentials: 'include'
    })
    const data = await res.json()
    if (data.success) isFavourited.value = !isFavourited.value
  } catch (err) {
    console.error('Error toggling favourite:', err)
  }
}

function goToEditProfile() {
  // NOTE: Confirm the edit route name with whoever set up the router
  router.push({ name: 'EditProfile', params: { id: profileId.value } })
}

function handleImageError(e) {
  e.target.src = 'https://media.istockphoto.com/id/2221915585/vector/grey-avatar-icon-user-avatar-photo-icon-social-media-user-icon-vector.jpg'
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
}

/* ── Loading / Error — matches Favorites.vue ── */
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
  0%   { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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

.btn-retry {
  background: #ff6b6b;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 600;
}

/* ── Profile Card ── */
.profile-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 20px rgba(0,0,0,0.08);
  overflow: hidden;
}

/* ── Hero Banner ── */
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

.hero-info { flex: 1; }

.name {
  color: white;
  font-size: 1.8rem;
  margin: 0 0 0.2rem;
  font-weight: 700;
}

.handle {
  color: rgba(255,255,255,0.8);
  margin: 0 0 0.75rem;
  font-size: 0.95rem;
}

.meta-pills { display: flex; flex-wrap: wrap; gap: 0.5rem; }

.pill {
  background: rgba(255,255,255,0.25);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
}

/* ── Buttons ── */
.action-buttons { display: flex; gap: 0.5rem; flex-wrap: wrap; }

.btn-edit, .btn-like, .btn-favourite {
  padding: 0.5rem 1.25rem;
  border: none;
  border-radius: 999px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.15s, opacity 0.15s;
}

.btn-edit:hover, .btn-like:hover, .btn-favourite:hover {
  transform: scale(1.05);
  opacity: 0.9;
}

.btn-edit      { background: white; color: #ff6b6b; }
.btn-like      { background: white; color: #ff6b6b; }
.btn-favourite { background: rgba(255,255,255,0.2); color: white; border: 2px solid white; }

/* ── Body ── */
.profile-body { padding: 2rem; }

.section { margin-bottom: 2rem; }

.section-title {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #ff6b6b;
  margin-bottom: 0.75rem;
}

.bio { color: #333; line-height: 1.7; }

/* ── Tags ── */
.tags { display: flex; flex-wrap: wrap; gap: 0.5rem; }

.tag {
  background: #fff0f0;
  color: #ff6b6b;
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.tag.muted { background: #f3f4f6; color: #9ca3af; }

/* ── Preferences ── */
.prefs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
}

.pref-item {
  background: #fff5f5;
  border: 1px solid #ffd5d5;
  border-radius: 12px;
  padding: 0.75rem 1rem;
}

.pref-label {
  display: block;
  font-size: 0.75rem;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.pref-value { font-size: 0.95rem; font-weight: 600; color: #333; }

/* ── Stats ── */
.stats-row { display: flex; gap: 1rem; flex-wrap: wrap; }

.stat {
  flex: 1;
  min-width: 100px;
  background: #fff5f5;
  border: 1px solid #ffd5d5;
  border-radius: 14px;
  padding: 1rem;
  text-align: center;
}

.stat-number { display: block; font-size: 2rem; font-weight: 800; color: #ff6b6b; }
.stat-label  { font-size: 0.8rem; color: #666; text-transform: uppercase; letter-spacing: 0.05em; }

/* ── Responsive ── */
@media (max-width: 768px) {
  .hero-banner    { flex-direction: column; text-align: center; }
  .meta-pills     { justify-content: center; }
  .action-buttons { justify-content: center; }
}
</style>