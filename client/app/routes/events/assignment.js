import Ember from 'ember';
/* global Freewall */
//import 'bower_components/freewall/freewall';
//
export default Ember.Route.extend({


    model: function(params, transition, queryParams) {
        return {
            assignment: {
                test: "hello world"
            }
        };
    },

    setupController: function(controller, model) {

        this._super(controller, model);

        if (controller.get('query') === undefined) { // This will change depending on what default will be in the storage backend.
            controller.set('query', model.dashboard.query);
        }

        controller.set('assignment', model.assignment)

        controller.set('institutionName', "eScholarship @ University of California");
        controller.set('widgets', model.dashboard.widgets);
    }

});
