var app = angular.module("teamreporterapp")

    .factory("Report", function ($resource) {
        return $resource("/team/:team_id/report/questions/:id", null,
            {
                'update': {method: 'PUT'}
            });
    })


    .factory("User", function ($resource) {
        return $resource("/team/:team_id/users/:id", null);
    })

    .factory("Team", function ($resource) {
        return $resource("/team/:id", null,
            {
                'update': {method: 'PUT'}
            });
    });
