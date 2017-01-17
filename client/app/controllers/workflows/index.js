import Ember from "ember";

export default Ember.Controller.extend({

    actions: {

        beginWorkflow: function(workflow) {

            this.get('store').run('operation', workflow.get('origin.id'), {
                test: 'TEST'
            }).then((result) => {
                this.transitionToRoute('inbox.index');
            });

        }

    }

});
