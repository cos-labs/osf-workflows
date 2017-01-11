import DS from 'ember-data';

export default DS.Model.extend({

    identifier: DS.attr('string'),
    uploader: DS.belongsTo('user'),
    workflow: DS.belongsTo('workflow'),

});

