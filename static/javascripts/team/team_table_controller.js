var app = angular.module("teamreporterapp")
app.controller('teamTableController', ["$scope", "teamService", function($scope, teamService) {
	$scope.teams = [];
	$scope.add_user = function(){
		
	}
	teamService.get().then(function(resp){
		if("error" in resp) {
			return
		}
		console.log(resp);
		for (var i = 0; i < resp.teams.length; i++){
			$scope.teams.push(resp.teams[i]);
		}

	});

}]);