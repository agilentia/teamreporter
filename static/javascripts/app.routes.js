var app = angular.module("teamreporterapp")

app.config(function($stateProvider, $urlRouterProvider) {
	$urlRouterProvider.otherwise("/team/");

	$stateProvider
	.state("user", {
		url: "/team/:team_id/users",
		templateUrl: "/static/javascripts/user/user_list_view.html"
	})
	.state("team", {
		url: "/team/",
		templateUrl: "/static/javascripts/team/team_list_view.html"
	})

	.state("question", {
		url: "/team/:team_id/questions",
		templateUrl: "/static/javascripts/question/question_list_view.html"
	})

});