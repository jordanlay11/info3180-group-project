<template>
  <div class="message-page">
    <div class="chat-header">
      <h2>{{ otherUserName }}</h2>
    </div>

    <div class="messages-container" ref="messageContainer">
      <div
        v-for="message in messages"
        :key="message.id"
        :class="[
          'message-bubble',
          message.from_user_id === currentUserId ? 'sent' : 'received',
        ]"
      >
        <p>{{ message.content }}</p>
        <small>{{ formatDate(message.sent_at) }}</small>
      </div>
    </div>

    <div class="message-input-section">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        placeholder="Type a message"
      />

      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const matchId = route.params.matchId;
const receiverId = route.query.receiverId;

const messages = ref([]);
const newMessage = ref("");
const messageContainer = ref(null);

const currentUserId = Number(localStorage.getItem("user_id"));
const otherUserName = ref("Matched User");

const fetchMessages = async () => {
  try {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `http://localhost:5000/messages/conversation/${matchId}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      },
    );

    if (!response.ok) {
      throw new Error("Failed to fetch messages");
    }

    const data = await response.json();

    messages.value = data;

    scrollToBottom();
  } catch (error) {
    console.error("Error fetching messages", error);
  }
};

const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  try {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `http://localhost:5000/messages/send/${matchId}`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          receiver_id: receiverId,
          content: newMessage.value,
        }),
      },
    );

    if (!response.ok) {
      throw new Error("Failed to send message");
    }

    const data = await response.json();

    messages.value.push(data.data);

    newMessage.value = "";

    await nextTick();

    scrollToBottom();
  } catch (error) {
    console.error("Error sending message", error);
  }
};
const scrollToBottom = async () => {
  await nextTick();

  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
  }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
};

onMounted(() => {
  fetchMessages();

  setInterval(() => {
    fetchMessages();
  }, 3000);
});
</script>

<style scoped>
.message-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f5f5f5;
}

.chat-header {
  padding: 15px;
  background: white;
  border-bottom: 1px solid #ddd;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message-bubble {
  max-width: 70%;
  padding: 10px;
  border-radius: 15px;
  word-break: break-word;
}

.sent {
  align-self: flex-end;
  background: #4caf50;
  color: white;
}

.received {
  align-self: flex-start;
  background: white;
}

.message-input-section {
  display: flex;
  padding: 15px;
  background: white;
  border-top: 1px solid #ddd;
}

.message-input-section input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.message-input-section button {
  margin-left: 10px;
  padding: 10px 15px;
}
</style>
