var app = angular.module("teamreporterapp")
app.controller('userTableController', ["$scope", "$rootScope", "$stateParams", "userService", function($scope, $rootScope, $stateParams, userService) {
    $scope.team_id = $stateParams.team_id;
    $scope.users = [];
    userService.get($scope.team_id).then(function(resp){
        if("error" in resp) {
            return
        }
        console.log(resp);
        for (var i = 0; i < resp.users.length; i++){
            $scope.users.push(resp.users[i]);
        }

    });

    $rootScope.$on("user_added", function (event, args) {
        $scope.users.push(args.user);
    });

}]);