var app = angular.module("teamreporterapp")
app.controller('addTeamController', ["$scope", "$stateParams", "$uibModal", "teamService", "toastr", function ($scope, $stateParams, $uibModal, teamService, toastr) {
    var self = this;
    $scope.self = self;
    $scope.update = function (team) {
        $scope.showAddModal(team);
    };
    $scope.$on('edit-team', function (event, team) {
        $scope.showAddModal(team)
    });
    $scope.showAddModal = function (team) {
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: '/static/javascripts/common/add_modal.html',
            controller: "addModalController",
            //size: size,
            resolve: {
                title: function () {
                    return "Add Team"
                },

                fields: function () {
                    var name = "";
                    var summary_send_time = new Date();
                    var survey_send_time = new Date();
                    var days_of_week = {};
                    if (team !== undefined) {
                        name = team.name;
                        var summary_time_arr = team.report.summary_send_time.split(":");
                        var survey_time_arr = team.report.survey_send_time.split(":");
                        summary_send_time.setHours(summary_time_arr[0]);
                        summary_send_time.setMinutes(summary_time_arr[1]);
                        survey_send_time.setHours(survey_time_arr[0]);
                        survey_send_time.setMinutes(survey_time_arr[1]);
                        for (var i = 0; i < team.report.days_of_week.length; i++)
                            days_of_week[team.report.days_of_week[i]] = true
                    }

                    return [{name: "Name", value: name, type: "text", var_name: "name"},
                        {
                            name: "Days of Week",
                            value: days_of_week,
                            type: "checkbox",
                            var_name: "days_of_week",
                            options: [{"id": 0, name: "Monday"}, {id: 1, name: "Tuesday"}, {
                                id: 2,
                                name: "Wednesday"
                            }, {id: 3, name: "Thursday"}, {id: 4, name: "Friday"}]
                        },
                        {name: "Survey Issue Time", value: survey_send_time, type: "timepicker", var_name: "send_time"},
                        {
                            name: "Report Summary Time",
                            value: summary_send_time,
                            type: "timepicker",
                            var_name: "summary_time"
                        }];
                }
            }
        });
        modalInstance.result.then(function (team_info) {
            var days_of_week = [];
            for (var week in team_info.days_of_week) {
                if (!team_info.days_of_week.hasOwnProperty(week)) continue;

                if (team_info.days_of_week[week]) {
                    days_of_week.push(parseInt(week))
                }
            }
            team_info.days_of_week = days_of_week;
            if (team === undefined) {
                teamService.save(team_info).then($scope.callback);
            } else {
                teamService.update(team.id, team_info).then($scope.callback);
            }

        }, function () {
            //$log.info('Modal dismissed at: ' + new Date());
        });
    }
    $scope.callback = function (resp) {
        if ("error" in resp) {
            var error_string = ""
            for (var key in resp.error) {
                error_string += key + ": " + resp.error[key] + "\n"
            }
            toastr.error(error_string)
            return
        } else {
            toastr.success("Team saved successfully!")
        }

    }
}]);
