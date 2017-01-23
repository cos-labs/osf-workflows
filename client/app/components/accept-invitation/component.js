
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';

export default Ember.Component.extend({

    users: [{username: ""}],

    actions: {

        acceptInvite: async function(user) {

            let operation = this.get('operation');
            let ctx = this.get('ctx');

            let result = await this.get('store').run('operation', operation.get('id'), {
                ctx: this.get("ctx.id"),
                invitee: "Bob The Builder"
            });

            this.attrs.destroy(this.get('message'));
            this.attrs.refresh();

        },

        declineInvite: async function(resourceIdentifier) {

            let operation = this.get('operation');
            let ctx = this.get('ctx');

            let result = await this.get('store').run('operation', operation.get('id'), {
                ctx: this.get("ctx.id"),
                editors_to_invite: users
            });

            this.attrs.destroy(this.get('message'));
            this.attrs.refresh();

        }

    }

});
