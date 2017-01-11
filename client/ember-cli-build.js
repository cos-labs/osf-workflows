/*jshint node:true*/
/* global require, module */
var EmberApp = require('ember-cli/lib/broccoli/ember-app');
var path = require('path');

module.exports = function(defaults) {

  var app = new EmberApp(defaults, {
    babel: {
      includePolyfill: true
    }
  });

  // Use `app.import` to add additional libraries to the generated
  // output files.
  //
  // If you need to use different assets in different
  // environments, specify an object as the first parameter. That
  // object's keys should be the environment name and the values
  // should be the asset to use in that environment.
  //
  // If the library that you are including contains AMD or ES6
  // modules that you would like to import into your application
  // please specify an object with the list of modules as keys
  // along with the exports of each module as its value.

  app.import('bower_components/d3/d3.js');
  app.import('bower_components/c3/c3.js');
  app.import('bower_components/freewall/freewall.js');
  app.import('bower_components/packery/dist/packery.pkgd.min.js');
  app.import('bower_components/draggabilly/dist/draggabilly.pkgd.min.js')
  // Import component styles from addon
  app.import(path.join(app.bowerDirectory, 'osf-style/vendor/prism/prism.css'));
  app.import(path.join(app.bowerDirectory, 'osf-style/page.css'));
  app.import(path.join(app.bowerDirectory, 'osf-style/css/base.css'));

  app.import(path.join(app.bowerDirectory, 'osf-style/img/cos-white2.png'), {
  	destDir: 'img'
  });

  app.import('vendor/assets/ember-osf.css');

  return app.toTree();

};
