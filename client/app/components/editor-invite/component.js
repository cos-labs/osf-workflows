
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';
export default Ember.Component.extend({

    actions: {

        sendInvite: async function() {
            let assignment = this.get("assignment");
            let task_id = await assignment.get("task.id");
            let result = await this.get('store').run('task', task_id, {
                re_assignment: assignment.id,
                string: "hello"
            });
            console.log(result);
        }

    }

});
