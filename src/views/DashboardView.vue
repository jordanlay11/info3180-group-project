<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>Ready To Mingle ?</h1>
      <p>Let's find your person 💞</p>
    </div>

    <!-- Search Filters Section -->
    <div class="filters-card">
      <div class="filters-header">
        <h3>Find your match </h3>
      </div>

      <div class="filters-grid">
        <!-- Location Filter -->
        <div class="filter-group">
          <label>📍 Location</label>
          <input 
            type="text" 
            v-model="filters.location" 
            placeholder="Filter by location..."
            @keyup.enter="search"
          />
        </div>

        <!-- Age Range Filter -->
        <div class="filter-group">
          <label>📅 Age Range</label>
          <div class="age-range">
            <input 
              type="number" 
              v-model.number="filters.min_age" 
              placeholder="Min"
              min="18"
              max="100"
            />
            <span>to</span>
            <input 
              type="number" 
              v-model.number="filters.max_age" 
              placeholder="Max"
              min="18"
              max="100"
            />
          </div>
        </div>

        <!-- Interests Filter -->
        <div class="filter-group">
          <label>⭐ Interests</label>
          <div class="interests-toggle">
            <button 
              @click="showInterestFilters = !showInterestFilters" 
              class="toggle-interests-btn"
            >
              {{ showInterestFilters ? 'Hide Interest Filters ▲' : 'Show Interest Filters ▼' }}
            </button>
          </div>
          <div v-if="showInterestFilters" class="interests-list">
            <label 
              v-for="interest in allInterests" 
              :key="interest"
              class="interest-checkbox"
            >
              <input 
                type="checkbox" 
                :value="interest" 
                v-model="filters.interests_array"
              />
              {{ interest }}
            </label>
          </div>
        </div>

        <!-- Sort Options -->
        <div class="filter-group">
          <label>📊 Sort By</label>
          <select v-model="filters.sort_by" @change="search">
            <option value="newest">Newest First</option>
            <option value="age_asc">Youngest First</option>
            <option value="age_desc">Oldest First</option>
            <option value="location_asc">Location (A-Z)</option>
          </select>
        </div>
      </div>

      <!-- Search Buttons -->
      <div class="search-actions">
        <button @click="search" class="search-btn" :disabled="loading">
          {{ loading ? 'Searching...' : '🔍 Search Matches' }}
        </button>
        <button @click="clearAllFilters" class="clear-btn">Clear All Filters</button>
      </div>
    </div>

    <!-- Results Section (Search Results) - Only visible when hasSearched is true -->
    <div v-if="hasSearched" class="results-section">
      <div class="results-header">
        <div class="results-header-left">
          <h3>Matches ({{ browseResults.length }})</h3>
          <button v-if="browseResults.length > 0" @click="clearResults" class="clear-results-btn">
            ✗ Clear Results
          </button>
        </div>
        <p v-if="browseResults.length === 0 && !loading">
          No matches found. Try adjusting your filters.
        </p>
      </div>

      <!-- Loading Spinner -->
      <div v-if="loading" class="loading-spinner">
        <div class="spinner"></div>
        <p>Finding your matches...</p>
      </div>

      <!-- Results Grid -->
      <div v-else-if="browseResults.length > 0" class="profiles-grid">
        <ProfileCard 
          v-for="profile in browseResults" 
          :key="profile.id"
          :profile="profile"
          :show-like-buttons="true"
          @like="handleLike"
          @pass="handlePass"
          @favorite-toggled="refreshData"
        />
      </div>
    </div>

    <!-- Recommendations Section - Only visible when NOT searching (hasSearched is false) -->
    <div v-if="!hasSearched" class="recommendations-section">
      <div class="section-header">
        <h2>Matches For You ✨</h2>
        <p>Fresh faces, new connections</p>
      </div>

      <div v-if="recommendationsLoading" class="loading-spinner">
        <div class="spinner"></div>
        <p>Finding recommendations...</p>
      </div>

      <div v-else-if="recommendations.length === 0" class="empty-matches">
        <p>No recommendations yet. Complete your profile to get better matches!</p>
      </div>

      <div v-else class="profiles-grid">
        <ProfileCard 
          v-for="profile in recommendations" 
          :key="profile.id"
          :profile="profile"
          :show-like-buttons="true"
          :match-score="profile.match_score"
          :match-reasons="profile.match_reasons"
          @like="handleLike"
          @pass="handlePass"
          @favorite-toggled="refreshData"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import ProfileCard from '@/components/ProfileCard.vue'

// ==========================================
// STATE
// ==========================================
const browseResults = ref([])
const loading = ref(false)
const hasSearched = ref(false)
const allInterests = ref([])
const showInterestFilters = ref(false)
const recommendations = ref([])
const recommendationsLoading = ref(false)

// Filters
const filters = reactive({
  location: '',
  min_age: '',
  max_age: '',
  interests: '',
  interests_array: [],
  sort_by: 'newest'
})

// Watch interests_array to update interests string
watch(() => filters.interests_array, (newVal) => {
  filters.interests = newVal.join(',')
}, { deep: true })

// ==========================================
// SEARCH FUNCTION
// ==========================================
const search = async () => {
  loading.value = true
  hasSearched.value = true
  
  const params = new URLSearchParams()
  if (filters.location) params.append('location', filters.location)
  if (filters.min_age) params.append('min_age', filters.min_age)
  if (filters.max_age) params.append('max_age', filters.max_age)
  if (filters.interests) params.append('interests', filters.interests)
  if (filters.sort_by) params.append('sort_by', filters.sort_by)
  
  try {
    const response = await fetch(`/api/search?${params.toString()}`, {
      credentials: 'include'
    })
    const data = await response.json()
    
    if (data.success) {
      browseResults.value = data.data
    } else {
      console.error('Search failed:', data.error)
    }
  } catch (error) {
    console.error('Error searching profiles:', error)
  } finally {
    loading.value = false
  }
}

// ==========================================
// CLEAR RESULTS FUNCTION
// ==========================================
const clearResults = () => {
  browseResults.value = []
  hasSearched.value = false
}

// ==========================================
// CLEAR ALL FILTERS FUNCTION
// ==========================================
const clearAllFilters = () => {
  filters.location = ''
  filters.min_age = ''
  filters.max_age = ''
  filters.interests_array = []
  filters.interests = ''
  filters.sort_by = 'newest'
  browseResults.value = []
  hasSearched.value = false
}

// ==========================================
// LOAD FUNCTIONS
// ==========================================
const loadInterests = async () => {
  try {
    const response = await fetch('/api/search/interests', {
      credentials: 'include'
    })
    const data = await response.json()
    if (data.success) {
      allInterests.value = data.data
    }
  } catch (error) {
    console.error('Error loading interests:', error)
  }
}

const loadRecommendations = async () => {
  recommendationsLoading.value = true
  try {
    const response = await fetch('/api/matching/latest', {
      credentials: 'include'
    })
    const data = await response.json()
    console.log('Recommendations response:', data)
    
    if (data.success) {
      recommendations.value = data.data
    }
  } catch (error) {
    console.error('Error loading recommendations:', error)
  } finally {
    recommendationsLoading.value = false
  }
}

// ==========================================
// LIKE / PASS HANDLERS
// ==========================================

const handleLike = async (profileId) => {
  console.log('🔄 Like/unlike event from ProfileCard for profile:', profileId)
  loadRecommendations()
  if (hasSearched.value) {
    search()
  }
}

const handlePass = async (profileId) => {
  console.log('👎 Pass event from ProfileCard for profile:', profileId)
  loadRecommendations()
  if (hasSearched.value) {
    search()
  }
}

const refreshData = () => {
  loadRecommendations()
  if (hasSearched.value) {
    search()
  }
}

// ==========================================
// ON MOUNTED
// ==========================================
onMounted(() => {
  loadInterests()
  loadRecommendations()
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 30px;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 10px;
}

.dashboard-header p {
  color: #666;
  font-size: 1.1rem;
}

/* Section Headers */
.section-header {
  margin-bottom: 20px;
}

.section-header h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 5px;
}

.section-header p {
  color: #666;
  font-size: 0.9rem;
}

/* Filters Card */
.filters-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 30px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  border: 1px solid #eee;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filters-header h3 {
  font-size: 1.3rem;
  color: #333;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  font-weight: 600;
  margin-bottom: 8px;
  color: #555;
  font-size: 0.9rem;
}

.filter-group input,
.filter-group select {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.filter-group input:focus,
.filter-group select:focus {
  outline: none;
  border-color: #ff6b6b;
}

.age-range {
  display: flex;
  gap: 10px;
  align-items: center;
}

.age-range input {
  flex: 1;
}

.age-range span {
  color: #666;
}

.interests-toggle {
  margin-bottom: 12px;
}

.toggle-interests-btn {
  background: #f0f0f0;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  color: #555;
}

.toggle-interests-btn:hover {
  background: #e0e0e0;
}

.interests-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 10px;
  max-height: 150px;
  overflow-y: auto;
  padding: 10px;
  background: #fafafa;
  border-radius: 8px;
}

.interest-checkbox {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: #555;
  cursor: pointer;
  padding: 4px 8px;
  background: white;
  border-radius: 20px;
  border: 1px solid #ddd;
}

.interest-checkbox:hover {
  background: #f0f0f0;
}

.interest-checkbox input {
  margin: 0;
}

.search-actions {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}

.search-btn {
  background: linear-gradient(135deg, #ff6b6b, #ee5a5a);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 40px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.search-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255,107,107,0.3);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.clear-btn {
  background: #f5f5f5;
  border: 1px solid #ddd;
  padding: 12px 24px;
  border-radius: 40px;
  font-size: 1rem;
  cursor: pointer;
  color: #666;
  transition: all 0.2s;
}

.clear-btn:hover {
  background: #e0e0e0;
}

/* Results Section */
.results-section {
  margin-top: 20px;
  margin-bottom: 30px;
}

.results-header {
  margin-bottom: 20px;
}

.results-header-left {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 15px;
}

.results-header-left h3 {
  font-size: 1.3rem;
  color: #333;
  margin: 0;
}

.clear-results-btn {
  background: none;
  border: 1px solid #ddd;
  padding: 6px 16px;
  border-radius: 20px;
  cursor: pointer;
  color: #666;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.clear-results-btn:hover {
  background: #f5f5f5;
  border-color: #ff6b6b;
  color: #ff6b6b;
}

/* Recommendations Section */
.recommendations-section {
  margin-top: 40px;
  padding-top: 30px;
  border-top: 2px solid #eee;
}

/* Profiles Grid */
.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.empty-matches {
  text-align: center;
  padding: 60px;
  background: #f9f9f9;
  border-radius: 16px;
  color: #888;
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

/* Responsive */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 15px;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
  }
  
  .profiles-grid {
    grid-template-columns: 1fr;
  }
  
  .search-actions {
    flex-direction: column;
  }
  
  .results-header-left {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .dashboard-header h1 {
    font-size: 1.8rem;
  }
}
.dashboard-container {
  background-color: #fdf0ed;
  min-height: 100vh;
}
</style>