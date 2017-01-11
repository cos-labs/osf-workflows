import Ember from 'ember';
/* global Freewall */
//import 'bower_components/freewall/freewall';
//
export default Ember.Route.extend({

    model: function(params, transition, queryParams) {
        return Ember.RSVP.hash({
            workflows: this.get('store').findAll('workflow'),
        });
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('workflows', model.workflows)
    }

});
