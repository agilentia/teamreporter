var app = angular.module("teamreporterapp")
app.controller('userTableController', ["$scope","userService", "$stateParams", function($scope, userService, $stateParams) {
    $scope.userService = userService;
    $scope.team_id = $stateParams.team_id;
    $scope.users = userService.get();
}]);