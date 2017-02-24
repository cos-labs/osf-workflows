import Ember from "ember";

export default Ember.Controller.extend({

    actions: {

        deleteMessage: async function(message) {
            message.destroyRecord();
        },

        refresh() {
            this.set("messages", this.get("store").query("message", {}));
            return true;
        }
    }

});
