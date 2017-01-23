import Ember from "ember";

export default Ember.Controller.extend({

    actions: {

        deleteMessage: async function(message) {
            message.destroyRecord();
        },

        refresh() {
            this.set("operations", this.get("store").query("operation", {}));
            return true;
        }
    }

});
