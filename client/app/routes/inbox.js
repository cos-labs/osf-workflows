import Ember from 'ember';
/* global Freewall */
//import 'bower_components/freewall/freewall';
//
export default Ember.Route.extend({

    model: function(params, transition, queryParams) {
        return Ember.RSVP.hash({
            events: this.get('store').findAll('event')
        });
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('events', model.events)
    }


});
