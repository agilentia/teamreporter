var app = angular.module("teamreporterapp")
app.controller('addQuestionController', ["$scope", "$stateParams", "$uibModal", "reportService", "toastr", function ($scope, $stateParams, $uibModal, reportService, toastr) {
    $scope.showAddModal = function () {
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: '/static/javascripts/common/add_modal.html',
            controller: "addModalController",
            resolve: {
                title: function () {
                    return "Add Question"
                },
                fields: function () {
                    return [{name: "Question", value: "", type: "text", var_name: "question"}];
                }
            }
        });

        modalInstance.result.then(function (question_info) {
            console.log(question_info)
            reportService.save(question_info).then(function (resp) {
                if ("error" in resp) {
                    for (var key in resp.error) {
                        toastr.error(key + ": " + resp.error[key]);
                    }
                } else {
                    toastr.success("Question saved successfully!")
                }
            });
        }, function () {
        });
    }
}]);
