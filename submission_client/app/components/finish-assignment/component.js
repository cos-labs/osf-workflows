
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';
export default Ember.Component.extend({

    actions: {

        finishAssignment: async function() {

            let operation = this.get('message.response');
            let ctx_id = this.get('message.ctx.id');

            let result = await this.get('store').run('operation', operation.get('id'), {
                finished_assignee: "admin",
                ctx: ctx_id,
            });

            this.attrs.refresh();

        },

    }

});
