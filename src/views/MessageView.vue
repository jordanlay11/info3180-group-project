<template>
  <div class="app-container">
    <!-- LEFT PANEL -->
    <div class="sidebar">
      <div class="tabs">
        <button
          :class="{ active: activeTab === 'chats' }"
          @click="activeTab = 'chats'"
        >
          Recent Chats
        </button>
        <button
          :class="{ active: activeTab === 'matches' }"
          @click="activeTab = 'matches'"
        >
          New Chat
        </button>
      </div>

      <div class="list">
        <div v-if="activeTab === 'chats'">
          <div v-if="chats.length === 0" class="empty">No recent chats</div>
          <div
            v-for="chat in chats"
            :key="chat.match_id"
            :class="[
              'list-item',
              { selected: chat.match_id === selectedChat?.match_id },
            ]"
            @click="selectChat(chat)"
          >
            {{ chat.name }}
          </div>
        </div>

        <div v-else>
          <div v-if="matches.length === 0" class="empty">No matches</div>
          <div
            v-for="match in matches"
            :key="match.match_id"
            class="list-item"
            @click="startChat(match)"
          >
            {{ match.name }}
          </div>
        </div>
      </div>
    </div>

    <!-- RIGHT PANEL -->
    <div class="chat-area">
      <div v-if="!selectedChat" class="no-chat">
        Select a chat to start messaging
      </div>

      <div v-else class="chat-wrapper">
        <div class="chat-header">
          {{ selectedChat.name }}
          <div class="chat-actions">
            <button @click="reportUser" class="action-btn report">
              Report
            </button>
            <button @click="blockUser" class="action-btn block">Block</button>
          </div>
        </div>

        <div class="messages" ref="messageContainer">
          <div
            v-for="msg in messages"
            :key="msg.id"
            :class="[
              'bubble',
              msg.from_user_id === currentUserId ? 'sent' : 'received',
            ]"
          >
            <p>{{ msg.content }}</p>
            <span class="time">{{ formatTime(msg.sent_at) }}</span>
          </div>
        </div>

        <div class="input-area">
          <input
            v-model="newMessage"
            @keyup.enter="sendMessage"
            placeholder="Type a message"
          />
          <button @click="sendMessage">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const activeTab = ref("chats");

const chats = ref([]);
const matches = ref([]);

const selectedChat = ref(null);
const messages = ref([]);
const newMessage = ref("");
const messageContainer = ref(null);
const currentUserId = ref(null);
const pollingTimer = ref(null);

// ---------- LOAD LISTS ----------
const loadCurrentUser = async () => {
  try {
    const res = await fetch("/api/user/me", {
      credentials: "include",
    });

    const data = await res.json();

    if (data.success) {
      currentUserId.value = data.data.id;
    }
  } catch (err) {
    console.error("Error loading current user", err);
  }
};
const loadChats = async () => {
  try {
    const res = await fetch("/api/messages/chats", {
      credentials: "include",
    });

    const data = await res.json();

    if (data.success) {
      chats.value = data.data;
    }
  } catch (err) {
    console.error("Error loading chats", err);
  }
};

const loadMatches = async () => {
  try {
    const res = await fetch("/api/messages/matches", {
      credentials: "include",
    });

    const data = await res.json();

    if (data.success) {
      matches.value = data.data;
    }
  } catch (err) {
    console.error("Error loading matches", err);
  }
};

// ---------- UI HANDLERS ----------
const selectChat = async (chat) => {
  selectedChat.value = chat;
  await fetchMessages(chat.match_id);
};

const startChat = async (match) => {
  selectedChat.value = match;
  activeTab.value = "chats";

  if (!chats.value.some((c) => c.match_id === match.match_id)) {
    chats.value.unshift(match);
  }
  matches.value = matches.value.filter((m) => m.match_id !== match.match_id);

  messages.value = [];
  await fetchMessages(match.match_id);
};

const selectMatchFromRoute = async () => {
  const matchId = Number(route.query.match_id);
  if (!matchId) return;

  const chat = chats.value.find((c) => c.match_id === matchId);
  if (chat) {
    await selectChat(chat);
    return;
  }

  const match = matches.value.find((m) => m.match_id === matchId);
  if (match) {
    await startChat(match);
  }
};

// ---------- API ----------
const fetchMessages = async (matchId, shouldScroll = true) => {
  try {
    const res = await fetch(`/api/messages/conversation/${matchId}`, {
      credentials: "include",
    });

    if (res.status === 401) {
      stopMessagePolling();
      return;
    }

    const data = await res.json();

    if (data.success) {
      const previousLastId = messages.value.length
        ? messages.value[messages.value.length - 1].id
        : null;

      messages.value = data.data;

      const currentLastId = messages.value.length
        ? messages.value[messages.value.length - 1].id
        : null;

      if (shouldScroll && currentLastId !== previousLastId) {
        scrollToBottom();
      }
    }
  } catch (err) {
    console.error("Error fetching messages", err);
  }
};

const startMessagePolling = () => {
  stopMessagePolling();

  if (!selectedChat.value) return;

  pollingTimer.value = setInterval(() => {
    if (selectedChat.value) {
      fetchMessages(selectedChat.value.match_id, false);
    }
  }, 3000);
};

const stopMessagePolling = () => {
  if (pollingTimer.value) {
    clearInterval(pollingTimer.value);
    pollingTimer.value = null;
  }
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || !selectedChat.value) return;

  try {
    const res = await fetch(
      `/api/messages/send/${selectedChat.value.match_id}`,
      {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: newMessage.value,
        }),
      },
    );

    const data = await res.json();

    if (data.success) {
      messages.value.push(data.data);
      newMessage.value = "";

      await nextTick();
      scrollToBottom();
    } else {
      alert(data.error || "Failed to send message");
    }
  } catch (err) {
    console.error("Error sending message", err);
  }
};

const blockUser = async () => {
  if (
    !selectedChat.value ||
    !confirm(`Are you sure you want to block ${selectedChat.value.name}?`)
  )
    return;

  try {
    const res = await fetch(`/api/block/${selectedChat.value.receiver_id}`, {
      method: "POST",
      credentials: "include",
    });

    const data = await res.json();

    if (data.success) {
      alert("User blocked");
      selectedChat.value = null;
      messages.value = [];
    } else {
      alert(data.error || "Failed to block user");
    }
  } catch (err) {
    console.error("Error blocking user", err);
  }
};

const reportUser = async () => {
  if (!selectedChat.value) return;

  const reason = prompt("Please provide a reason for reporting:");
  if (!reason || !reason.trim()) return;

  try {
    const res = await fetch(`/api/report/${selectedChat.value.receiver_id}`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        reason: reason.trim(),
      }),
    });

    const data = await res.json();

    if (data.success) {
      alert("User reported");
    } else {
      alert(data.error || "Failed to report user");
    }
  } catch (err) {
    console.error("Error reporting user", err);
  }
};

// ---------- HELPERS ----------
const scrollToBottom = async () => {
  await nextTick();
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
  }
};

const formatTime = (date) => {
  const d = new Date(date);
  const hours = String(d.getUTCHours()).padStart(2, "0");
  const minutes = String(d.getUTCMinutes()).padStart(2, "0");
  return `${hours}:${minutes}`;
};

// ---------- INIT ----------
onMounted(async () => {
  await loadCurrentUser();
  await loadChats();
  await loadMatches();
  await selectMatchFromRoute();

  if (!selectedChat.value && chats.value.length > 0) {
    selectChat(chats.value[0]);
  }
});

onBeforeUnmount(() => {
  stopMessagePolling();
});

// Watchers for polling control
watch(activeTab, (newTab) => {
  if (newTab !== "chats") {
    stopMessagePolling();
  } else if (selectedChat.value) {
    startMessagePolling();
  }
});

watch(selectedChat, (newChat) => {
  if (!newChat) {
    stopMessagePolling();
  } else if (activeTab.value === "chats") {
    startMessagePolling();
  }
});
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  background: var(--bg-primary);
}

/* SIDEBAR */
.sidebar {
  width: 30%;
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  background: var(--bg-card);
}

.tabs {
  display: flex;
}

.tabs button {
  flex: 1;
  padding: 10px;
  border: none;
  background: var(--bg-card);
  color: var(--text-primary);
  cursor: pointer;
  transition: background 0.2s;
}

.tabs button.active {
  background: var(--border-color);
  font-weight: bold;
  color: var(--text-primary);
}

.list {
  flex: 1;
  overflow-y: auto;
}

.list-item {
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  color: var(--text-primary);
  transition: background 0.2s;
}

.list-item:hover {
  background: var(--border-color);
}

.list-item.selected {
  background: var(--like-btn);
  font-weight: bold;
  color: white;
}

.empty {
  padding: 20px;
  text-align: center;
  color: var(--text-secondary);
}

/* CHAT AREA */
.chat-area {
  width: 70%;
  display: flex;
  flex-direction: column;
}

.no-chat {
  margin: auto;
  color: var(--text-secondary);
}

.chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-card);
  color: var(--text-primary);
}

.chat-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: opacity 0.2s;
}

.action-btn:hover {
  opacity: 0.8;
}

.report {
  background: #ff6b6b;
  color: white;
}

.block {
  background: #ffa726;
  color: white;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: var(--bg-primary);
}

.bubble {
  max-width: 60%;
  padding: 10px;
  border-radius: 10px;
  display: inline-block;
  word-wrap: break-word;
}

.sent {
  align-self: flex-end;
  background: var(--like-btn);
  color: white;
  text-align: right;
}

.received {
  align-self: flex-start;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  text-align: left;
}

.time {
  display: block;
  font-size: 10px;
  margin-top: 4px;
  opacity: 0.7;
}

.input-area {
  display: flex;
  padding: 10px;
  border-top: 1px solid var(--border-color);
  position: sticky;
  bottom: 0;
  background: var(--bg-card);
  z-index: 10;
}

.input-area input {
  flex: 1;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.input-area input::placeholder {
  color: var(--text-secondary);
}

.input-area button {
  margin-left: 10px;
  padding: 10px 20px;
  background: var(--like-btn);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}

.input-area button:hover {
  transform: scale(1.02);
}

/* Dark Mode Specific Overrides */
.dark-mode .sent {
  background: var(--like-btn);
}

.dark-mode .received {
  background: var(--bg-card);
  border-color: var(--border-color);
}

.dark-mode .tabs button {
  background: var(--bg-card);
}

.dark-mode .tabs button.active {
  background: var(--border-color);
}

.dark-mode .list-item.selected {
  background: var(--like-btn);
}
</style>