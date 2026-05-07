<template>
  <div class="match-card">
    <div class="match-image">
      <img :src="match.photo_url || '/default-avatar.png'" :alt="match.name" />
      <div class="match-badge">💕 Match!</div>
    </div>
    <div class="match-content">
      <h3>{{ match.name }}, {{ match.age }}</h3>
      <p class="location">📍 {{ match.location || 'Location not specified' }}</p>
      <p class="matched-at">Matched {{ match.matched_at || 'recently' }}</p>
      <button @click="sendMessage" class="message-btn">💬 Send Message</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  match: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['message'])
const router = useRouter()

const sendMessage = () => {
  emit('message', props.match.id)
  router.push(`/messages/${props.match.id}`)
}
</script>

<style scoped>
.match-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  display: flex;
  transition: transform 0.2s, box-shadow 0.2s;
}

.match-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.match-image {
  position: relative;
  width: 120px;
  flex-shrink: 0;
}

.match-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.match-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: #ff6b6b;
  color: white;
  padding: 4px 8px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: bold;
}

.match-content {
  padding: 16px;
  flex: 1;
}

.match-content h3 {
  margin: 0 0 4px 0;
  font-size: 1.1rem;
  color: #333;
}

.location {
  color: #888;
  font-size: 0.85rem;
  margin: 0 0 8px 0;
}

.matched-at {
  color: #aaa;
  font-size: 0.75rem;
  margin: 0 0 12px 0;
}

.message-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: transform 0.2s;
}

.message-btn:hover {
  transform: scale(1.02);
}
</style>