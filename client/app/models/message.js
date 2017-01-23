import DS from 'ember-data';

export default DS.Model.extend({

    messageType: DS.attr('string'),
    timestamp: DS.attr('date'),
    origin: DS.hasMany('operation', {inverse: 'messages'}),
    response: DS.belongsTo('operation', {inverse: "caller"}),
    ctx: DS.belongsTo('context', {inverse: "messages"}),
    content: DS.attr('string')

});

