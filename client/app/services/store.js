import DS from 'ember-data';

export default DS.Store.extend({

    run(modelName, id, parameters) {

        let _this = this;
        let adapter = this.adapterFor(modelName)
        let typeClass = this.modelFor(modelName)

        return Ember.RSVP.Promise.resolve({ then: function() {
            return adapter.run(typeClass, id, parameters);
        }});

    }

});

