import Ember from 'ember';
import DS from 'ember-data';
import ENV from '../config/environment';
import JSONAPIAdapter from 'ember-data/adapters/json-api';

export default JSONAPIAdapter.extend(DS.BuildURLMixin, {
    namespace: 'api',
    host: ENV.apiBaseUrl,
    ajax(url, method, hash) {
        hash = hash || {};
        hash.crossDomain = true;
        hash.xhrFields = { withCredentials: true };
        return this._super(url, method, hash);
    },
    pathForType(type) {
        var inflector = new Ember.Inflector(Ember.Inflector.defaultRules);
        return Ember.String.underscore(inflector.pluralize(type));
    },
    run(type, id, parameters) {
        var url = this.buildURL(type.modelName, id, null, null, null);
        return this.ajax(url, 'RUN', { data: parameters });
    }
});
