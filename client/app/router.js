import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
    location: config.locationType,
    rootURL: config.rootURL
});

Router.map(function() {

    this.route('inbox', function() {
        this.route('event', {path: ':event'});
        this.route('create');
    });

    this.route('workflows', function() {
        this.route('workflow', {path: ':workflow'}, function() {
            this.route('graph', {path: 'graph'});
        });
        this.route('create');
    });

    this.route('tasks', function() {
        this.route('tasks', {path: ':task'});
    });

    this.route('submissions', function() {
        this.route('submission', {path: ':submission'});
    });

    this.route('roles', function() {
        this.route('roles', {path: ':role'});
    });

    this.route('users', function() {
        this.route('users', {path: ':user'});
    });

});

export default Router;
