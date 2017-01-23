import DS from 'ember-data';

export default DS.Model.extend({

    name: DS.attr("string"),
    description: DS.attr("string"),
    group: DS.belongsTo("group"),
    operation: DS.attr("string"),
    parameters: DS.hasMany("value", {inverse: "operations"}),
    returnValue: DS.belongsTo("value", {inverse: "sourceOperation"}),
    view: DS.attr("string"),
    messages: DS.hasMany("message", {inverse: "origin"}),
    caller: DS.hasMany("message", {inverse: "response"})

});

