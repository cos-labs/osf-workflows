
import JSONAPIAdapter from 'ember-data/adapters/json-api';
import config from '../config/environment';

export default JSONAPIAdapter.extend({

    host: config.APP.GRANTS_BACKEND,

    buildURL: function(type, id, record) {
        //call the default buildURL and then append a slash
        // return this._super(type, id, record) + '/';
        return this._super(type, id, record) + '/';
    }

});
