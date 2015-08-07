(function() {
    var docToolApp = angular.module('docToolApp', [
        'ngRoute',
        'navbar',
        'home',
        'tableView'
    ]);

    "use strict";
    docToolApp.config(['$routeProvider',
        function($routeProvider) {
            $routeProvider.
            when('/home', {
                templateUrl: 'partials/home.html',
                controller: 'HomeController'
            }).
            when('/table', {
                templateUrl: 'partials/table-view.html',
                controller: 'TableViewController'
            }).
            when('/about', {
                templateUrl: 'partials/about.html',
                controller: 'AboutController'
            }).
            otherwise({
                redirectTo: '/home'
            });
        }
    ]);
})();