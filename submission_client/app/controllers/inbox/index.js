import Ember from "ember";

export default Ember.Controller.extend({

    sections: [
        "upload",
        "disciplines",
        "basics",
        "authors",
        "submit"
    ],

    actions: {

        deleteMessage: async function(message) {
            message.destroyRecord();
        },

        async refresh() {
            const fetched_messages = await this.get("store").query("message", {});
            const current_messages = this.get("messages")
            fetched_messages.filter((fetched_message) => {
                var exists = false;
                current_messages.forEach((current_message) => {
                    if (fetched_message.id === current_message.id) {
                        exists = true;
                    }
                })
                return !exists;
            }).forEach((new_message) => {
                this.pushObject("messages", message);
            });
            current_messages.filter((current_message) => {
                var exists = false;
                fetched_messages.forEach((fetched_message) => {
                    if (fetched_message.id === current_message.id) {
                        exists = true;
                    }
                })
                return !exists;
            }).forEach((stale_message) => {
                current_messages.removeObject(stale_message);
            });
        }
    }

});
