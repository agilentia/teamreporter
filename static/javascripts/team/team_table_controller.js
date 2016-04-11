var app = angular.module("teamreporterapp")
app.controller('teamTableController', ["$scope","teamService", "$stateParams", function($scope, teamService, $stateParams) {
    $scope.teamService = teamService;
    $scope.team_id = $stateParams.team_id;
    $scope.teams = teamService.get();
}]);