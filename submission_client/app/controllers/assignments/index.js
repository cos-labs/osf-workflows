import Ember from "ember";

export default Ember.Controller.extend({

    //assignmentsController: Ember.inject.controller('assignments'),

    actions: {

        refresh() {
            this.set("assignments", this.get("store").query("assignment", {}));
            return true;
        }

    }

});
