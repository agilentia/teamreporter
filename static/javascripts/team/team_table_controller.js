var app = angular.module("teamreporterapp")
app.controller('teamTableController', ["$scope", "$rootScope", "teamService", function($scope, $rootScope, teamService) {
	$scope.teams = [];
	teamService.get().then(function(resp){
		if("error" in resp) {
			return
		}
		console.log(resp);
		for (var i = 0; i < resp.teams.length; i++){
			$scope.teams.push(resp.teams[i]);
		}

	});
    $rootScope.$on("team_added", function (event, args) {
        $scope.teams.push(args);
    });
}]);