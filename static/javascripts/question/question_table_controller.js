var app = angular.module("teamreporterapp")
app.controller('questionTableController', ["$scope", "reportService", "$rootScope", "$stateParams", function ($scope, reportService, $rootScope, $stateParams) {
    $scope.reportService = reportService;
    $scope.team_id = $stateParams.team_id;
    $scope.questions = reportService.get();
    $scope.update = function (question) {
        $rootScope.$broadcast('edit-question', question);
    }
}]);