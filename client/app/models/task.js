import DS from 'ember-data';

export default DS.Model.extend({

    name: DS.attr('string'),
    description: DS.attr('string'),
    workflow: DS.hasMany('workflow', {inverse: 'tasks'}),
    subtasks: DS.hasMany('task', {inverse: 'parent_task'}),
    parent_task: DS.hasMany('task', {inverse: 'subtasks'}),
    prerequisites: DS.hasMany('task', {inverse: 'prerequisite_for'}),
    prerequisite_for: DS.hasMany('task', {inverse: 'prerequisites'}),
    view: DS.attr('string')

});

