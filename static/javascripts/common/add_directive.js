var app = angular.module("teamreporterapp")
app.directive('addDirective', function() {
	return {
		templateUrl: "/static/javascripts/common/add.html",
		controller : "addCommonController"
		scope: {
			addType: "@",
			addTitle: "@"
		}
	}
});