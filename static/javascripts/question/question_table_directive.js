var app = angular.module("teamreporterapp")
app.directive('questionTableDirective', function() {
	return {
		templateUrl: "/static/javascripts/question/question_table.html",
		controller:"questionTableController"
	}
});