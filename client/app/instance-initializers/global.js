export function initialize(app) {
  // appInstance.inject('route', 'foo', 'service:foo');
    app.store = app.__container__.lookup('service:store');
    window.App = app;
}

export default {
  name: 'global',
  initialize
};
