<template>
  <div class="app-container">
    <!-- LEFT PANEL -->
    <div class="sidebar">
      <div class="tabs">
        <button
          :class="{ active: activeTab === 'chats' }"
          @click="activeTab = 'chats'"
        >
          Chats
        </button>
        <button
          :class="{ active: activeTab === 'matches' }"
          @click="activeTab = 'matches'"
        >
          Matches
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

  chats.value.unshift(match);
  matches.value = matches.value.filter((m) => m.match_id !== match.match_id);

  messages.value = [];
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
    }
  } catch (err) {
    console.error("Error sending message", err);
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

  if (chats.value.length > 0) {
    selectChat(chats.value[0]);
  }
});

onBeforeUnmount(() => {
  stopMessagePolling();
});

// Watchers for polling control
watch(activeTab, (newTab) => {
  if (newTab !== 'chats') {
    stopMessagePolling();
  } else if (selectedChat.value) {
    startMessagePolling();
  }
});

watch(selectedChat, (newChat) => {
  if (!newChat) {
    stopMessagePolling();
  } else if (activeTab.value === 'chats') {
    startMessagePolling();
  }
});
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
}

/* SIDEBAR */
.sidebar {
  width: 30%;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
}

.tabs {
  display: flex;
}

.tabs button {
  flex: 1;
  padding: 10px;
  border: none;
  background: #f0f0f0;
}

.tabs button.active {
  background: #ddd;
  font-weight: bold;
}

.list {
  flex: 1;
  overflow-y: auto;
}

.list-item {
  padding: 15px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.list-item:hover {
  background: #f5f5f5;
}

.list-item.selected {
  background: #e0f7fa;
  font-weight: bold;
}

.empty {
  padding: 20px;
  text-align: center;
  color: gray;
}

/* CHAT AREA */
.chat-area {
  width: 70%;
  display: flex;
  flex-direction: column;
}

.no-chat {
  margin: auto;
  color: gray;
}

.chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  padding: 15px;
  border-bottom: 1px solid #ddd;
  font-weight: bold;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
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
  background: #dcf8c6;
  text-align: right;
}

.received {
  align-self: flex-start;
  background: #fff;
  border: 1px solid #eee;
  text-align: left;
}

.time {
  display: block;
  font-size: 10px;
  text-align: right;
}

.input-area {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
  position: sticky;
  bottom: 0;
  background: white;
  z-index: 10;
}

.input-area input {
  flex: 1;
  padding: 10px;
}

.input-area button {
  margin-left: 10px;
}
</style>
