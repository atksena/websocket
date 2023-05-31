<template>
  <v-app>
    <v-main>
      <v-container>
        <v-app-bar app color="grey darken-3" dense dark>
          <v-layout align-center>
            <v-flex>
              <span class="title">CHAT</span>
            </v-flex>
            <v-flex shrink>
              <span>{{ username }}</span>
            </v-flex>
          </v-layout>
        </v-app-bar>
        <v-card>
          <v-btn to="/userList" text>
            <v-card-title>{{ name }}'s Chat Room</v-card-title>
          </v-btn>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="(message, index) in messages"
                :key="message.id"
                :style="{
                  'text-align':
                    message.username === username ? 'left' : 'right',
                }"
              >
                <v-list-item-content>
                  <v-list-item-title>{{ message.username }}</v-list-item-title>
                  <v-list-item-title>{{ message.text }}</v-list-item-title>
                  <v-list-item-subtitle class="grey--text">
                    {{ new Date(message.timestamp).toLocaleTimeString() }}
                    <v-icon
                      v-if="message.username === username && !message.seen"
                      small
                      :color="message.seen ? 'green' : 'grey'"
                    >
                      mdi-check
                    </v-icon>
                    <v-icon small @click="deleteMessages(index)">
                      mdi-delete
                    </v-icon>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card>
            <v-card-title>Send Message</v-card-title>
            <v-card-text>
              <v-text-field
                v-model="newMessage"
                label="Message"
                @keyup.enter="addMessage"
              ></v-text-field>
              <v-btn color="primary" @click="addMessage"
                ><v-icon>mdi-send</v-icon></v-btn
              >
            </v-card-text>
          </v-card>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "ChatRoom",
  props: ["id", "name"],
  data() {
    return {
      message: {
        username: null,
        text: null,
      },
      messages: [],
      newMessage: "",
      username: window.localStorage.getItem("username"),
    };
  },
  mounted() {
    const token = localStorage.getItem("access");
    const url = "ws://localhost/api/ws/chat/" + this.id + "/?token=" + token;
    this.socket = new WebSocket(url);
    this.socket.onopen = () => {
      console.log("WebSocket connection is open");
    };
    this.socket.addEventListener("message", (event) => {
      const message = JSON.parse(event.data);
      const id = message.room.id;
      if (id === this.id) {
        if (!this.messages) {
          this.messages = [];
        }
        this.messages.push(message);
        const index = this.messages.findIndex((msg) => msg.id === message.id);
        if (index !== -1) {
          this.$set(this.messages[index], "seen", true);
        }
      }
    });
  },
  methods: {
    addMessage() {
      const token = localStorage.getItem("access");
      fetch("/api/messages/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
        body: JSON.stringify({
          room: this.id,
          username: this.username,
          text: this.newMessage,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (!this.messages) {
            this.messages = [];
          }
          this.messages.push(data);
          this.newMessage = "";
          const socketMessage = JSON.stringify(data);
          this.socket.send(socketMessage);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    messagesList() {
      const token = localStorage.getItem("access");
      fetch(`/api/messages/list/${this.id}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("HTTP error " + response.status);
          }
          return response.json();
        })
        .then((data) => {
          this.messages = data;
          const users = [];
          data.forEach((message) => {
            if (!users.includes(message.username)) {
              users.push(message.username);
            }
          });
          localStorage.setItem("users", JSON.stringify(users));
        })
        .catch((error) => {
          console.error(error);
        });
    },
    deleteMessages(messageIndex) {
      const messageToDelete = this.messages[messageIndex];
      fetch("/api/messages/delete/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: messageToDelete.id }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("HTTP error " + response.status);
          }
          this.messages.splice(messageIndex, 1);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.messagesList();
  },
};
</script>
