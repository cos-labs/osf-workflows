import DS from 'ember-data';

export default DS.Model.extend({

    event_type: DS.attr('string'),
    timestamp: DS.attr('date'),
    context: DS.hasMany('context', {inverse: "messages"}),
    responses: DS.hasMany('event', {inverse: "context"}),
    operation: DS.belongsTo('operation'),
    content: DS.attr()

});

