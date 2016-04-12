var app = angular.module("teamreporterapp")

app.config(function($stateProvider, $urlRouterProvider) {
	$urlRouterProvider.otherwise("/team/");

	$stateProvider
	.state("user", {
		url: "/team/:team_id/users",
		templateUrl: "/static/javascripts/user/user_list_view.html",
		resolve: {
			userService: 'userService',
			user: function(userService, $stateParams) {
				var team_id = $stateParams.team_id;
				return userService.init(team_id);
			},
			RoleServiceData: function(roleService) {
				return roleService.promise;
			}
		}
	})
	.state("team", {
		url: "/team/",
		templateUrl: "/static/javascripts/team/team_list_view.html",
		resolve: {
			teamService: 'teamService',
			team: function(teamService) {
				return teamService.init();
			}
		}
	})

	.state("report", {
		url: "/team/:team_id/report/questions",
		templateUrl: "/static/javascripts/question/question_list_view.html",
		resolve: {
			reportService: 'reportService',
			report: function(reportService, $stateParams) {
				var team_id = $stateParams.team_id;
				return reportService.init(team_id);
			}
		}
	})

});