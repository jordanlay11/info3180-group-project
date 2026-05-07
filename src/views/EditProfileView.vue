<template>
  <div class="edit-profile-container">
    <h1>Edit Profile</h1>

    <form @submit.prevent="updateProfile" class="edit-form">
      <!-- PHOTO UPLOAD SECTION -->
      <div class="form-group photo-upload-section">
        <label>Profile Photo</label>
        <div class="current-photo">
          <img 
            :src="photoPreviewUrl" 
            alt="Profile photo"
            class="profile-photo-preview"
            @error="handleImageError"
          />
        </div>
        <div class="upload-area">
          <input 
            type="file" 
            ref="fileInput"
            @change="handleFileSelect"
            accept="image/jpeg,image/png,image/jpg,image/gif"
            class="file-input"
          />
          <button type="button" @click="triggerFileInput" class="upload-btn">
            📷 Choose New Photo
          </button>
        </div>
        <div v-if="uploading" class="upload-status">Uploading...</div>
        <div v-if="uploadError" class="error-message">{{ uploadError }}</div>
      </div>

      <div class="form-group">
        <label>Bio</label>
        <textarea v-model="form.bio" rows="4" placeholder="Tell us about yourself..."></textarea>
      </div>

      <div class="form-group">
        <label>Location</label>
        <input v-model="form.location" type="text" placeholder="e.g., Kingston, Jamaica">
      </div>

      <div class="form-group">
        <label>Occupation</label>
        <input v-model="form.occupation" type="text" placeholder="e.g., Software Engineer">
      </div>

      <div class="form-group">
        <label>Zodiac Sign</label>
        <input v-model="form.zodiac_sign" type="text" placeholder="e.g., Virgo">
      </div>

      <div class="form-group">
        <label>Interests (comma separated)</label>
        <input v-model="form.interests_str" type="text" placeholder="Hiking, Movies, Music, Travel">
      </div>

      <div class="form-group">
        <label>Looking For (Gender)</label>
        <select v-model="form.looking_for_gender">
          <option value="all">Everyone</option>
          <option value="male">Men</option>
          <option value="female">Women</option>
        </select>
      </div>

      <div class="form-row">
        <div class="form-group half">
          <label>Min Age</label>
          <input type="number" v-model.number="form.preferred_age_min" min="18" max="100">
        </div>
        <div class="form-group half">
          <label>Max Age</label>
          <input type="number" v-model.number="form.preferred_age_max" min="18" max="100">
        </div>
      </div>

      <div class="form-group">
        <label>Max Distance (km)</label>
        <input type="number" v-model.number="form.preferred_location_radius" min="1" max="500">
      </div>

      <div class="form-group">
        <label>Profile Visibility</label>
        <select v-model="form.visibility">
          <option :value="true">Public</option>
          <option :value="false">Private</option>
        </select>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="loading || uploading">Save Changes</button>
        <button type="button" @click="$router.back()" class="cancel-btn">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8081'
const loading = ref(false)
const uploading = ref(false)
const uploadError = ref(null)
const fileInput = ref(null)
const selectedPhoto = ref(null)
const currentPhotoFilename = ref('')

const form = ref({
  bio: '',
  location: '',
  occupation: '',
  zodiac_sign: '',
  interests_str: '',
  visibility: true,
  looking_for_gender: 'all',
  preferred_age_min: 18,
  preferred_age_max: 99,
  preferred_location_radius: 50
})

// Photo preview URL
const photoPreviewUrl = computed(() => {
  if (selectedPhoto.value) {
    return URL.createObjectURL(selectedPhoto.value)
  }
  if (currentPhotoFilename.value) {
    return `${apiUrl}/api/uploads/${currentPhotoFilename.value}`
  }
  return '/default-avatar.png'
})

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    uploadError.value = 'Please select a valid image (JPG, PNG, or GIF)'
    return
  }
  
  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    uploadError.value = 'File size must be less than 5MB'
    return
  }
  
  uploadError.value = null
  selectedPhoto.value = file
}

const uploadProfilePhoto = async () => {
  if (!selectedPhoto.value) return null
  
  uploading.value = true
  uploadError.value = null
  
  const formData = new FormData()
  formData.append('photo', selectedPhoto.value)
  
  try {
    const response = await fetch(`${apiUrl}/api/profile/photo`, {
      method: 'POST',
      credentials: 'include',
      body: formData
    })
    
    const data = await response.json()
    
    if (response.ok && data.success) {
      // Extract filename from URL
      const photoUrl = data.photo_url
      const filename = photoUrl.split('/').pop()
      currentPhotoFilename.value = filename
      return filename
    } else {
      uploadError.value = data.error || 'Failed to upload photo'
      return null
    }
  } catch (error) {
    console.error('Error uploading photo:', error)
    uploadError.value = 'Network error while uploading'
    return null
  } finally {
    uploading.value = false
  }
}

const loadProfile = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/user/info`, {
      credentials: 'include'
    })
    const data = await response.json()
    if (data.success) {
      form.value = {
        bio: data.data.bio || '',
        location: data.data.location || '',
        occupation: data.data.occupation || '',
        zodiac_sign: data.data.zodiac_sign || '',
        interests_str: (data.data.interests || []).join(', '),
        visibility: data.data.visibility !== false,
        looking_for_gender: data.data.looking_for_gender || 'all',
        preferred_age_min: data.data.preferred_age_min || 18,
        preferred_age_max: data.data.preferred_age_max || 99,
        preferred_location_radius: data.data.preferred_location_radius || 50
      }
      
      // Store current photo filename
      if (data.data.profile_photo) {
        currentPhotoFilename.value = data.data.profile_photo
      }
    }
  } catch (error) {
    console.error('Error loading profile:', error)
  }
}

const updateProfile = async () => {
  loading.value = true
  
  try {
    // Upload photo first if a new one was selected
    if (selectedPhoto.value) {
      const uploaded = await uploadProfilePhoto()
      if (!uploaded && uploadError.value) {
        alert('Failed to upload photo. Please try again.')
        loading.value = false
        return
      }
    }
    
    // Update profile text fields
    const interests = form.value.interests_str.split(',').map(i => i.trim()).filter(Boolean)
    const payload = {
      bio: form.value.bio,
      location: form.value.location,
      occupation: form.value.occupation,
      zodiac_sign: form.value.zodiac_sign,
      interests: interests,
      visibility: form.value.visibility,
      looking_for_gender: form.value.looking_for_gender,
      preferred_age_min: form.value.preferred_age_min,
      preferred_age_max: form.value.preferred_age_max,
      preferred_location_radius: form.value.preferred_location_radius
    }
    
    console.log('Sending payload:', payload)

    const response = await fetch(`${apiUrl}/api/profile/update`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(payload)
    })
    
    const data = await response.json()
    console.log('Response:', data)
    
    if (data.success) {
      alert('Profile updated successfully!')
      window.location.href = '/profile'
    } else {
      alert(data.error || 'Update failed')
    }
  } catch (error) {
    console.error('Error updating profile:', error)
    alert('An error occurred')
  } finally {
    loading.value = false
  }
}

const handleImageError = (e) => {
  e.target.src = '/default-avatar.png'
}

onMounted(loadProfile)
</script>

<style scoped>
.edit-profile-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
}

.edit-profile-container h1 {
  text-align: center;
  color: #a83232;
  margin-bottom: 30px;
}

.edit-form {
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
}

.form-group textarea {
  resize: vertical;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #a83232;
}

.form-row {
  display: flex;
  gap: 15px;
}

.form-group.half {
  flex: 1;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 25px;
}

button {
  background: #a83232;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover:not(:disabled) {
  background: #c94f4f;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-btn {
  background: #ccc;
  color: #333;
}

.cancel-btn:hover {
  background: #bbb;
}

/* Photo upload styles */
.photo-upload-section {
  border-bottom: 2px solid #eee;
  padding-bottom: 20px;
  margin-bottom: 20px;
}

.current-photo {
  text-align: center;
  margin-bottom: 15px;
}

.profile-photo-preview {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #a83232;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.upload-area {
  text-align: center;
}

.file-input {
  display: none;
}

.upload-btn {
  background: #666;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s;
}

.upload-btn:hover {
  background: #888;
}

.upload-status {
  text-align: center;
  margin-top: 10px;
  color: #666;
  font-size: 0.9rem;
}

.error-message {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 10px;
  text-align: center;
}
</style>