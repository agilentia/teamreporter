var app = angular.module("teamreporterapp")
app.directive('teamTableDirective', function() {
	return {
		templateUrl: "/static/javascripts/team/team_table.html",
		controller:"teamTableController"
	}
});