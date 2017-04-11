import Ember from 'ember';
/* global Freewall */
//import 'bower_components/freewall/freewall';
//
export default Ember.Route.extend({

    setupController: function(controller, model) {

        this._super(controller, model);
        controller.set('submissions', model.submissions);

    }

});
