import DS from 'ember-data';

export default DS.Model.extend({

    net: DS.belongsTo('net', {inverse: 'cases'}),
    messages: DS.hasMany("message"),
    tokens: DS.hasMany('tokens', {inverse: 'caxe'})

});

