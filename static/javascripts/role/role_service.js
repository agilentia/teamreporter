var app = angular.module("teamreporterapp")
app.factory("roleService", ["$http", function($http){
	var roles = null;
	var promise = $http({
				method: 'GET',
				url: "/role/",
				headers: {
    				'Content-Type': 'application/json'
				}
			}).success(function(data) {
				roles = data.roles;
			});
	var service = {
		promise: promise,
		get: function(){
			return roles;
		},
	}

	return service
}]);