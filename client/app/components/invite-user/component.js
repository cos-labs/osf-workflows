
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';

export default Ember.Component.extend({

    users: [{username: ""}],

    actions: {

        addUser: function() {
            this.get('users').pushObject({username: ""});
        },

        removeUser: function(user) {
            debugger;
            this.get('users').removeObject(user);
        },

        sendInvites: async function(resourceIdentifier) {

            let operation = this.get('operation');
            let ctx = this.get('ctx');
            let users = this.get('users').filter((user)=>{
                return user.username.length > 0
            });

            if (users.length < 1) {
                alert('No users have been added to the list yet!');
                return;
            }

            let result = await this.get('store').run('operation', operation.get('id'), {
                ctx: this.get("ctx.id"),
                editors_to_invite: users
            });

            this.attrs.destroy(this.get('message'));
            this.attrs.refresh();

        }

    }

});
