import Ember from 'ember';
/* global Freewall */
//import 'bower_components/freewall/freewall';
//
export default Ember.Route.extend({


    model: function(params, transition, queryParams) {
        return Ember.RSVP.hash({
            workflow: this.get('store').find('workflow', params.workflow),
        });
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('workflow', model.workflow)
        controller.set('workflows', model.workflows)
    }

});
