//
// Main OPAL Referrals plugin application!
//
var opalshim = OPAL.module('opal', [])

var pathway = OPAL.module('opal.multistage', []);

var app = OPAL.module('opal.pathway', [
    'ngRoute',
    'ngProgressLite',
    'ngCookies',
    'opal.filters',
    'opal.services',
    'opal.directives',
    'opal.controllers',
    'opal.multistage',
    'opal.controllers',
    'opal.services'
]);

OPAL.run(app);

app.config(function($routeProvider){
    $routeProvider
        .when('/', {
            controller: 'PathwayRedirectCtrl',
            resolve: {},
            templateUrl: '/templates/loading_page.html'
        })
        .when('/:pathway/:patient_id?/:episode_id?', {
            controller: 'PathwayCtrl',
            resolve: {
              	referencedata: function(Referencedata) { return Referencedata.load(); },
              	metadata: function(Metadata) { return Metadata.load(); },
                recordLoader: function(recordLoader){ return recordLoader.load(); },
                episode: function($route, episodeLoader){
                  if($route.current.params.episode_id){
                    if(!$route.current.params.episode_id){
                        return null;
                    }
                    return episodeLoader($route.current.params.episode_id);
                  }
                },
                pathwayDefinition: function($route, pathwayLoader){
                  return pathwayLoader.load(
                    $route.current.params.pathway,
                    $route.current.params.patient_id,
                    $route.current.params.episode_id
                  );
                }
            },
            templateUrl: function(params){
                return '/pathway/templates/' + params.pathway + '.html';
            }
        });
});
