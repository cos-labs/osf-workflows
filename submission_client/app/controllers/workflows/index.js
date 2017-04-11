import Ember from "ember";

export default Ember.Controller.extend({

    actions: {

        beginWorkflow: async function(workflow) {

            let ctx = this.get('store').createRecord('context');
            ctx.get('workflows').pushObject(workflow);
            ctx.set('inherit', workflow.rootContext);
            await ctx.save();
            this.transitionToRoute('inbox.index');

        }

    }

});
