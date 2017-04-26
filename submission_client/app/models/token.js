import DS from 'ember-data';

export default DS.Model.extend({

    color: DS.attr(),
    caxe: DS.belongsTo('case', {inverse: "tokens"}),
    location: DS.belongsTo('location', {inverse: "tokens"}),
    name: DS.attr('string'),
    requestMessages: DS.hasMany("message", {inverse: "responseTokens"}),
    net: DS.belongsTo('net')

});

