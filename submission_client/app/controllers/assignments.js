import Ember from "ember";

export default Ember.Controller.extend({

    assignments: [],

    actions: {

        refresh: function() {
            debugger;
            this.set("assignments", this.get("store").query("assignment", {}));
        }

    }

});
