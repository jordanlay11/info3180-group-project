<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>Browse Potential Matches</h1>
      <p>Discover people who share your interests</p>
    </div>

    <!-- Search Filters Section -->
    <div class="filters-card">
      <div class="filters-header">
        <h3>🔍 Filter Matches</h3>
        <button @click="resetFilters" class="reset-btn">Reset Filters</button>
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
          <select v-model="filters.sort_by">
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
        <button @click="resetFilters" class="clear-btn">Clear All Filters</button>
      </div>
    </div>

    <!-- Results Section -->
    <div class="results-section">
      <div class="results-header">
        <h3>Matches ({{ browseResults.length }})</h3>
        <p v-if="profiles.length === 0 && !loading">No matches found. Try adjusting your filters.</p>
      </div>

      <!-- Loading Spinner -->
      <div v-if="loading" class="loading-spinner">
        <div class="spinner"></div>
        <p>Finding your matches...</p>
      </div>

      <!-- Results Grid -->
      <div v-else class="profiles-grid">
        <ProfileCard 
          v-for="profile in browseResults" 
          :key="profile.id"
          :profile="profile"
          @favorite-toggled="onFavoriteToggled"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import ProfileCard from '@/components/ProfileCard.vue'
import MatchCard from '@/components/MatchCard.vue'

// State

// reactive variables
const browseResults = ref([])      
const loading = ref(false)          

const profiles = ref([])
const allInterests = ref([])
const showInterestFilters = ref(false)

// Filters
const filters = reactive({
  location: '',
  min_age: '',
  max_age: '',
  interests: '',
  interests_array: [],
  sort_by: 'newest'
})

//matches section
const mutualMatches = ref([])
const loadingMatches = ref(false)
const currentUser = ref(null)

// Watch interests_array to update interests string
watch(() => filters.interests_array, (newVal) => {
  filters.interests = newVal.join(',')
}, { deep: true })



// Search function
const search = async () => {
  loading.value = true
  
  const params = new URLSearchParams()
  if (filters.location) params.append('location', filters.location)
  if (filters.min_age) params.append('min_age', filters.min_age)
  if (filters.max_age) params.append('max_age', filters.max_age)
  if (filters.interests) params.append('interests', filters.interests)
  if (filters.sort_by) params.append('sort_by', filters.sort_by)
  
  try {
    // Use relative URL - Vite proxy will forward to backend
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

// Load all interests for filters
const loadInterests = async () => {
  try {
    const response = await fetch('/api/search/interests')
    const data = await response.json()
    if (data.success) {
      allInterests.value = data.data
    }
  } catch (error) {
    console.error('Error loading interests:', error)
  }
}

// Reset all filters
const resetFilters = () => {
  filters.location = ''
  filters.min_age = ''
  filters.max_age = ''
  filters.interests_array = []
  filters.interests = ''
  filters.sort_by = 'newest'
  search()
}

// Handle favorite toggled event
const onFavoriteToggled = (profileId) => {
  
  search()
}

// Load data on mount
onMounted(() => {
  loadInterests()
  search()
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

.reset-btn {
  background: #f5f5f5;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  color: #666;
  transition: all 0.2s;
}

.reset-btn:hover {
  background: #e0e0e0;
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
}

.results-header {
  margin-bottom: 20px;
}

.results-header h3 {
  font-size: 1.3rem;
  color: #333;
}

/* Profiles Grid */
.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
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
  
  .dashboard-header h1 {
    font-size: 1.8rem;
  }
}
</style>