var app = angular.module("teamreporterapp")
app.directive('userTableDirective', function() {
	return {
		templateUrl: "/static/javascripts/user/user_table.html",
		controller:"userTableController"
	}
});