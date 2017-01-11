import Ember from 'ember';

export default Ember.Controller.extend({

    queryParams: ['id', 'scholar', 'query', 'q', 'institution', 'tag', 'topic'],

    updateParams: Ember.observer('queryParams', function() {
        this.set("parameters", Ember.computed.apply(this, this.get('queryParams').concat(() => {
            return this.get('queryParams').map((param) => {
                return this.get(param);
            })
        })));
    }),

    wall: false,

    currentUser: Ember.inject.service(),

    // Initialize the dashboard with no widgets.
    widgets: [],

    // Initialize the list of additional charts that the user can add
    addableList: [],
    storedDashboards: [],

    configureQuery: function()  {
    }.on('init'),

    createWall: function() {
        Ember.run.schedule('afterRender', this, () => {
           // var wall =  new Freewall('#freewall');
           // wall.reset({
           //     draggable: true,
           //     selector: '.widget',
           //     animate: true,
           //     cellW: 150,
           //     cellH: 150,
           //     fixSize: 0,
           //     cacheSize: true,
           //     onResize: function() {
           //         wall.refresh();
           //     },
           //     onBlockMove: function() {
           //         console.log(this);
           //     }
           // });
           // wall.fitWidth();
           // Ember.$(window).trigger('resize');
           // controller.set('wall', wall);
        });
    }.on('init'),

    init() {
        let ret = this._super();
                return ret;
    },

    actions: {

        changeQ: function(query) {
            this.set('q',query);
        },

        changeGte: function(g) {
            g = new Date(g);
            this.set('gte', g.toISOString().split('T')[0]); // Elasticsearch doesn't accept timezone information.
        },

        changeLte: function(l) {
            l = new Date(l);
            this.set('lte',l.toISOString().split('T')[0]);
        },

        sortEndAction: function() {

        },

        removeChart: function(targetWidget) {
            this.set('widgets', this.get('widgets').filter(function(widget) {
                return widget !== targetWidget;
            }).slice());
        },

        addChart: function(widget) {
            this.set('widgets', this.get('widgets').concat({isPlaceholder: true}));
        },

        refreshWall: function() {
            console.log('refreshing wall');
            let wall = this.get('wall');
            wall && wall.refresh();
        },

        dashboardSaveWidget: function(widget) {
            this.get('currentUser').load().then((c) => {
                widget.author = c.get('fullName');
                this.set('widgets', this.get('widgets').addObject(widget));
                widget = this.store.createRecord('widget', widget);
                widget.save();
                // TODO: This should not be an alert, but a growl-style notification.
                // alert("Chart has been successfully saved!");
            }, function(r){
                // TODO: This should not be an alert, but a growl-style notification.
                alert("Widgets may not be saved anonymously. Log in to save a widget.");
            });
        }

    },

});
