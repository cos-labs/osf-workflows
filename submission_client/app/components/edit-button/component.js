
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';

export default Ember.Component.extend({

    actions: {

        edit: async function(target) {

            const message = this.get('message');
            const locaxion = this.get('message.response');
            const caxe = this.get('message.caxe');

            this.get('store').findRecord('case', this.get('message.caxe.id')).then(async (caxeo) => {

                const refresh = this.attrs.refresh;
                const store = this.get("store");
                const token = store.createRecord('token');
                token.set('color', {});
                token.set('caxe', caxe);
                token.set('net', caxeo.get('net'));
                token.set('name', message.get('responseTokenName'))
                token.set('location', locaxion);
                token.set('requestMessage', message);
                const response = await token.save();
                this.get('store').findAll('message', {reload: true}).then((messages) => {
                    this.attrs.refresh()
                })

            });

        }

    }

});
