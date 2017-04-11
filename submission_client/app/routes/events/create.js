import Ember from 'ember';
/* global Freewall */
//import 'bower_components/freewall/freewall';
//
export default Ember.Route.extend({

    model: function(params, transition, queryParams) {
        return Ember.RSVP.hash({
            submissions: this.get('store').findAll('submission'),
            tasks: this.get('store').findAll('task'),
            roles: this.get('store').findAll('role'),
            users: this.get('store').findAll('user'),
        });
    },

    setupController: function(controller, model) {

        this._super(controller, model);
        controller.set('submissions', model.submissions)
        controller.set('tasks', model.tasks)
        controller.set('roles', model.roles)
        controller.set('users', model.users)

    }

});
