
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';

export default Ember.Component.extend({

    users: [{username: ""}],

    actions: {

        acceptInvite: async function(user) {

            let operation = this.get('message.response');
            let ctx_id = this.get('message.ctx.id');

            let result = await this.get('store').run('operation', operation.get('id'), {
                ctx: ctx_id,
                invitee: "admin",
                rsvp: "Accept"
            });

            this.attrs.refresh();

        },

        declineInvite: async function(resourceIdentifier) {

            let operation = this.get('message.response');
            let ctx_id = this.get('message.ctx.id');

            let result = await this.get('store').run('operation', operation.get('id'), {
                ctx: ctx_id,
                invitee: "admin",
                rsvp: "Decline"
            });

            this.attrs.refresh();

        }

    }

});
