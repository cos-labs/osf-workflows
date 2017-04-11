
import Ember from 'ember';
import ENV from 'analytics-dashboard/config/environment';

function getToken() {
    var token;
    var session = window.localStorage['ember_simple_auth:session'];
    if (session) {
        token = JSON.parse(session)['authenticated'];
        if ('attributes' in token) {
            return token['attributes']['accessToken'];
        }
        return token;
    }
}

export default Ember.Component.extend({

    actions: {

        uploadFile: function(target) {
            const reader = new FileReader();
            const f = event.target.files[0];
            const uri = "https://files.osf.io/v1/resources/h8d72/providers/osfstorage/?kind=file&name=" + f.name;
            const operation = this.get('message.response');
            const ctx_id = this.get('message.ctx.id');
            const refresh = this.attrs.refresh;
            const store = this.get("store");

            reader.onloadend = function(e) {
                const xhr = new XMLHttpRequest();
                console.log(f);
                debugger;
                xhr.open("PUT", uri, true);
                xhr.setRequestHeader("Authorization", "Bearer " + getToken());
                xhr.withCredentials = false;
                xhr.onreadystatechange = async function() {
                    if (xhr.readyState == 4 && xhr.status >= 200 && xhr.status < 300) {
                        const result = await store.run('operation', operation.get('id'), {
                            ctx: ctx_id,
                            file_url: JSON.parse(xhr.responseText).data.links.download 
                        });
                        refresh();
                    }
                };
                xhr.send(e.target.result);
            };

            reader.readAsBinaryString(f);
        },

        associateResource: async function(resourceIdentifier) {
        }

    }

});
