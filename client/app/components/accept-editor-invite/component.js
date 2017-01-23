
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';
export default Ember.Component.extend({


    actions: {

        acceptInvite: async function() {
            let assignment = this.get("assignment");
            let task_id = await assignment.get("task.id");
            this.get('store').run('task', task_id, {
                re_assignment: assignment.id,
                rsvp: "Accept"
            }).then((result) => {
                console.log(result);
                this.attrs.refresh();
            });
        },

        declineInvite: async function() {
            let assignment = this.get("assignment");
            let task_id = await assignment.get("task.id");
            let result = await this.get('store').run('action', task_id, {
                re_assignment: assignment.id,
                rsvp: "Decline"
            });
            console.log(result);
            //this.attrs.refresh();
        }

    }

});
