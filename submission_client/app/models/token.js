import DS from 'ember-data';

export default DS.Model.extend({

    color: DS.attr(),
    caxe: DS.belongsTo('case', {inverse: "tokens"}),
    location: DS.belongsTo('location', {inverse: "tokens"}),
    name: DS.attr('string'),
    requestMessage: DS.belongsTo("message", {inverse: "responseToken"}),
    net: DS.belongsTo('net')

});

