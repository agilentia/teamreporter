var teamreporterapp = angular.module('teamreporterapp', ["ngResource", 'ui.router', 'ui.bootstrap', 'smart-table', 'ui.multiselect', 'toastr'])
.config(function($httpProvider, $resourceProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $resourceProvider.defaults.stripTrailingSlashes = false;
});