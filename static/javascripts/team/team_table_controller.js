var app = angular.module("teamreporterapp")
app.controller('teamTableController', ["$scope","teamService", function($scope, teamService) {
    $scope.teamService = teamService;
    $scope.teams = teamService.get();
}]);