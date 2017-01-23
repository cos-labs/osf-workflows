import DS from 'ember-data';

export default DS.Model.extend({

    values: DS.attr(),
    inherit: DS.belongsTo('context', { inverse: "heirs" }),
    heirs: DS.hasMany("context", { inverse: "inherit" }),
    workflows: DS.hasMany("workflow"),
    messages: DS.hasMany("message")

});

