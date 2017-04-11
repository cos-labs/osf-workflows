
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';
export default Ember.Component.extend({

    actions: {

        associateResource: async function(resourceIdentifier) {
            let operation = this.get('message.response');
            let ctx_id = this.get('message.ctx.id');
            let result = await this.get('store').run('operation', operation.get('id'), {
                ctx: ctx_id,
                resource_identifier: resourceIdentifier
            });
            this.attrs.refresh();
        }

    }

});
