import Ember from 'ember';

export default Ember.Service.extend({

    init() {
        this._super(...arguments);
        $.jsonRPC.setup({
            endPoint: 'http://localhost:8000/rpc/',
            namespace: ''
        });
    },

    invoke(key, parameters) {
        return Ember.RSVP.Promise.resolve({ then: function(resolve, reject) {
            $.jsonRPC.request(key, {
                params: parameters,
                success: function(result) { resolve(result.result); },
                error: function(result) { reject(result.error); }
            });
        }});
    },

});
