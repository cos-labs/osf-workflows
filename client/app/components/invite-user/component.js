
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';

export default Ember.Component.extend({

    users: null,

    didReceiveAttrs() {
        this.set('users', [{username: ""}])
    },

    actions: {

        addUser: function() {
            this.get('users').pushObject({username: ""});
        },

        removeUser: function(user) {
            this.get('users').removeObject(user);
        },

        sendInvites: async function(resourceIdentifier) {

            let operation = this.get('message.response');
            let ctx_id = this.get('message.ctx.id');
            let users = this.get('users').filter((user) => {
                return user.username.length > 0
            });

            if (users.length < 1) {
                alert('No users have been added to the list yet!');
                return;
            }

            let result = await this.get('store').run('operation', operation.get('id'), {
                ctx: ctx_id,
                users_to_invite: users
            });

            this.attrs.refresh();
        }

    }

});
