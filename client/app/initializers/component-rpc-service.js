
// app/initializers/init.js
export function initialize(container, app) {
    app.inject('component', 'rpc', 'service:rpc');
    app.inject('route', 'rpc', 'service:rpc');
}

export default {
    name: 'componet-rpc-service',
    initialize: initialize
};
