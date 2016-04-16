var app = angular.module("teamreporterapp")
app.controller('teamTableController', ["$scope","teamService",  "$rootScope", "$controller", function($scope, teamService, $rootScope, $controller) {
    $scope.teamService = teamService;
    $scope.teams = teamService.get();
    $scope.update = function(team) {
        $rootScope.$broadcast('edit-team', team);
    }
}]);