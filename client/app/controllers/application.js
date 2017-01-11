import Ember from 'ember';

import OsfAgnosticAuthControllerMixin from 'ember-osf/mixins/osf-agnostic-auth-controller';

import {
    getAuthUrl
} from 'ember-osf/utils/auth';

export default Ember.Controller.extend(OsfAgnosticAuthControllerMixin,{
    toast: Ember.inject.service(),
    authUrl: getAuthUrl(),
    actions: {
        loginSuccess() {
           // this.transitionToRoute('researcher.grant');
        },
        loginFail(/* err */) {
            this.get('toast').error('Login failed');
        }
    }
});
