var app = angular.module("teamreporterapp")
function UserCache(){
	this.user_cache = {}
	this.init_team = function(team) {
		this.user_cache[team] = [];
	}
	this.add = function(team, user){
		if (!(team in this.user_cache)) {
			init_team();
		}

		this.user_cache[team].push(user)
	}

	this.get = function(team){
		if (!(team in this.user_cache)) {
			init_team();
		}
		return this.user_cache[team]
	}

}
app.factory("userService", ["$http", "$rootScope", function($http, $rootScope){

	var service = {
		get: function(team) {
			return $http({
				method: 'GET',
				url: "/team/" + team + "/users/", 
				headers: {
    				'Content-Type': 'application/json'
				}
			}).then(function(resp) {
				var user_obj = {users: resp.data.users};
				return user_obj
			}, function(error){
				return {error: error}
			});
		},

		save: function(team, user_info) {
			return $http({
				method: 'POST',
				url: "/team/" + team + "/users/",
				data: user_info,
				headers: {
    				'Content-Type': 'application/json'
				}
			}).then(function(resp) {
				var user_obj = {user: resp.data.user};
				console.log(user_obj)
				$rootScope.$broadcast('user_added', user_obj)
				return user_obj

			}, function(error){
				return {error: error}
			});
		},
	}

	return service
}]);