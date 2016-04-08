var app = angular.module("teamreporterapp")
app.directive('addDirective', function() {
	return {
		templateUrl: "/static/javascripts/common/add.html",
		controller : "@",
		name: "controllerName",
		scope: {
			addType: "@"
		}
	}
});