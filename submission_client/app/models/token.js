import DS from 'ember-data';

export default DS.Model.extend({

    color: DS.attr(),
    caxe: DS.belongsTo('case', { inverse: "tokens" }),
    location: DS.belongsTo("location", { inverse: "inherit" }),
    name: DS.attr('string'),
    messages: DS.hasMany("message")

});

