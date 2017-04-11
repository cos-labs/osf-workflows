import Ember from "ember";

export default Ember.Controller.extend({

    actions: {

        beginWorkflow: async function(net) {
            let wfcase = this.get('store').createRecord('case');
            wfcase.set("net", net)
            await wfcase.save();
            this.transitionToRoute('inbox.index');
        }

    }

});
