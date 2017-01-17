import DS from 'ember-data';

export default DS.Model.extend({

    name: DS.attr("string"),
    description: DS.attr("string"),
    group: DS.belongsTo("group"),
    operation: DS.attr("string"),
    parameters: DS.hasMany("parameter", {inverse: "operations"}),
    view: DS.attr("string")

});

