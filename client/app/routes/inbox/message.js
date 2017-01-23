import Ember from 'ember';
/* global Freewall */
//import 'bower_components/freewall/freewall';
//
export default Ember.Route.extend({

    model: function(params, transition, queryParams) {
        return Ember.RSVP.hash({
            message: this.get('store').findRecord('message', params.message)
        });
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('message', model.message)
        controller.set('messages', model.messages)
    }


});
