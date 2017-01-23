
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';
export default Ember.Component.extend({

    actions: {

        associateResource: async function(resourceIdentifier) {
            let operation = this.get('operation');
            let ctx = this.get('ctx');
            let result = await this.get('store').run('operation', operation.get('id'), {
                ctx: this.get("ctx.id"),
                resource_identifier: resourceIdentifier
            });
            this.attrs.destroy(this.get('message'));
            this.attrs.refresh();
        }

    }

});
