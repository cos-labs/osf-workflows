import DS from 'ember-data';

export default DS.Model.extend({

    submission: DS.belongsTo('submission'),
    task: DS.belongsTo('task'),
    assignee: DS.belongsTo('user'),
    role: DS.belongsTo('role'),
    compoleted: DS.attr('string')

});

