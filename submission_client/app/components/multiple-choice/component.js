
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';
export default Ember.Component.extend({

    choices: Ember.computed("message", function() {
        debugger;
        let content = this.get("message.content");
        return JSON.parse(this.get("message.content"))
    }),

    actions: {

        associateResource: async function(choice) {
            let operation = this.get('message.response');
            let ctx_id = this.get('message.ctx.id');
            let result = await this.get('store').run('operation', operation.get('id'), {
                ctx: ctx_id,
                "chosen": choice
            });
            this.attrs.refresh();
        }

    }

});
