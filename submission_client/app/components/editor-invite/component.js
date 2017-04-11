
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';
export default Ember.Component.extend({

    actions: {

        associateResource: async function(operation) {
            let result = await this.get('store').run('operation', operation.id, {
                resource_id: "hello"
            });
            console.log(result);
            this.attrs.refresh();
        }

    }

});
