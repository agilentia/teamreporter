var app = angular.module("teamreporterapp")
app.controller('teamTableController', ["$scope","teamService", "$controller", function($scope, teamService, $controller) {
    $scope.teamService = teamService;
    var add_team_view_model = $scope.$new();
    $scope.teams = teamService.get();
    var update_team_controller = $controller("addTeamController", {$scope : add_team_view_model });
    $scope.update = function(team) {
    	update_team_controller.showAddModal(team);
    }
}]);