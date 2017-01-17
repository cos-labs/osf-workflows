import DS from 'ember-data';

export default DS.Model.extend({

    name: DS.attr("string"),
    description: DS.attr("string"),
    type: DS.attr("string"),
    value: DS.attr("string"),
    operations: DS.hasMany("operation"),
    contexts: DS.hasMany("value")

});

