import Ember from 'ember';

import OsfTokenLoginRouteMixin from 'ember-osf/mixins/osf-token-login-route';

export default Ember.Route.extend(OsfTokenLoginRouteMixin, {

    store: Ember.inject.service(),
    session: Ember.inject.service(),

    model() {
        //if (this.get('session.isAuthenticated')) {
        //    return this.get('store').findRecord('user', 'me');
        //}
    }
});
