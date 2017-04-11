import Ember from 'ember';
/* global Freewall */
//import 'bower_components/freewall/freewall';
//
export default Ember.Route.extend({

    model() {
        return this.get('store').findRecord("net", "1a85108c-387d-47cd-8b47-ca831248bc4c");
    },

    setupController: async function(controller, model) {
        controller.set("workflow", model);
        console.log(model)
    }

});
