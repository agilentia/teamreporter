var app = angular.module("teamreporterapp")
app.controller('questionTableController', ["$scope","reportService", "$stateParams", function($scope, reportService, $stateParams) {
	$scope.reportService = reportService
	$scope.team_id = $stateParams.team_id;
	$scope.questions = reportService.get();
}]);