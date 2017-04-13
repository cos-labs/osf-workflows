import DS from 'ember-data';

export default DS.Model.extend({

    name: DS.attr("string"),
    description: DS.attr("string"),
    type: DS.attr("string"),
    sources: DS.hasMany("transitions", {inverse: "outputs"}),
    tokens: DS.hasMany('tokens', {inverse: 'location'}),
    targets: DS.hasMany("transitions", {inverse: "inputs"}),
    sourceOperation: DS.belongsTo("operation"),
    caller: DS.hasMany("message", {inverse: "response"}),
    net: DS.belongsTo("net", {inverse: "locations"})

});

