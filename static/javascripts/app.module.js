var teamreporterapp = angular.module('teamreporterapp', ['ui.router', 'ui.bootstrap', 'smart-table', 'ui.multiselect'])
.config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});