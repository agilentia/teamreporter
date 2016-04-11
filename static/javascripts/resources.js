var app = angular.module("teamreporterapp");

app.factory("Report", function($resource){
	return $resource("/team/:team_id/report/questions/:id", null);
})

/*
app.factory("User", function($resource){
	return $resource("/team/:team_id/users/:id", null);
})
*/