var app = angular.module("teamreporterapp")
app.directive('addUserDirective', function() {
	return {
		templateUrl: "/static/javascripts/user/add_user.html",
		controller:"addUserController"
	}
});