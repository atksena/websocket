<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <v-card>
      <v-card-title class="headline">New Room</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            v-model="room.name"
            label="Room Name"
            required
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="close">Close</v-btn>
        <v-btn color="primary" @click="addRoom">Add Room</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "AddChatRoom",
  data() {
    return {
      dialog: false,
      room: {
        id: null,
        name: null,
      },
      rooms: [],
    };
  },
  methods: {
    open() {
      this.dialog = true;
    },
    close() {
      this.dialog = false;
    },
    addRoom() {
      fetch("/api/rooms/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.room),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.rooms.push(data);
          this.$emit("room-added", data);
          this.close();
        })
        .catch((error) => {
          console.error("There was a problem with the fetch operation:", error);
        });
    },
  },
};
</script>
