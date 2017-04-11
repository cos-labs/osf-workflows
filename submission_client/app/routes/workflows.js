import Ember from 'ember';
/* global Freewall */
//import 'bower_components/freewall/freewall';
//
export default Ember.Route.extend({

    model: async function(params, transition, queryParams) {
        let workflows = await this.get('store').findAll('workflow');
        return Ember.RSVP.hash({
            workflows: workflows
        });
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('workflows', model.workflows)
    }

});
