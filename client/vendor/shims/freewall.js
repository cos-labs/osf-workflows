(function() {
  function vendorModule() {
    'use strict';

    return { 'default': self['freewall'] };
  }

  define('freewall', [], vendorModule);
})();
