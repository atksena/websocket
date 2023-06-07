<template>
  <v-app>
    <v-main>
      <v-app-bar app color="grey darken-3" dense dark>
        <v-layout align-center>
          <v-flex>
            <span class="title">CHAT</span>
          </v-flex>
          <v-flex shrink>
            <v-btn color="white" icon size="large" @click="openAddChatRoom">
              <v-icon dark>mdi-plus</v-icon>
            </v-btn>
            <v-menu offset-y>
              <template v-slot:activator="{ on }">
                <v-btn color="white" icon size="large" v-on="on">
                  <v-icon dark>mdi-account</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="logout">
                  <v-list-item-icon>
                    <v-icon>mdi-logout</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Logout</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <span>{{ username }}</span>
          </v-flex>
        </v-layout>
      </v-app-bar>
      <v-container>
        <v-row>
          <v-col
            v-for="(room, index) in rooms"
            :key="room.id"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card>
              <v-card-text @click="openChatRoom(room)">{{
                room.name
              }}</v-card-text>
              <v-card-actions>
                <v-btn @click="deleteRoom(index)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
      <AddChatRoom
        :rooms="rooms"
        @room-added="refreshRooms"
        ref="addChatRoomDialog"
      ></AddChatRoom>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import AddChatRoom from "@/components/AddChatRoom.vue";

export default {
  name: "ChatRoomList",
  components: { AddChatRoom },
  data() {
    return {
      rooms: [],
      username: window.localStorage.getItem("username"),
    };
  },
  methods: {
    getRooms() {
      const token = localStorage.getItem("access");
      fetch("/api/rooms/list/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.rooms = data;
        })
        .catch((error) => {
          console.error("There was a problem with the fetch operation:", error);
        });
    },
    deleteRoom(roomIndex) {
      const roomToDelete = this.rooms[roomIndex];
      fetch("api/rooms/delete/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: roomToDelete.id }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("HTTP error " + response.status);
          }
          this.rooms.splice(roomIndex, 1);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    openChatRoom(room) {
      this.$router.push({
        name: "ChatRoom",
        params: { id: room.id, name: room.name },
      });
    },
    openAddChatRoom() {
      this.$refs.addChatRoomDialog.open();
    },
    refreshRooms(room) {
      this.rooms.push(room);
    },
    logout() {
      const token = localStorage.getItem("access");
      fetch("api/logout/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          localStorage.removeItem("access");
          localStorage.removeItem("username");
          this.$router.push("/loginPage");
        })
        .catch((error) => {
          console.error("There was a problem with the fetch operation:", error);
        });
    },
  },
  created() {
    this.getRooms();
  },
};
</script>
