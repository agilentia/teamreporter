var app = angular.module("teamreporterapp")
app.controller('addQuestionController', ["$scope", "$stateParams", "$uibModal", "reportService", "toastr", function ($scope, $stateParams, $uibModal, reportService, toastr) {
    $scope.$on('edit-question', function (event, question) {
        $scope.showAddModal(question)
    });
    $scope.showAddModal = function (question) {
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: '/static/javascripts/common/add_modal.html',
            controller: "addModalController",
            resolve: {
                title: function () {
                    return "Add Question"
                },
                fields: function () {
                    var text = "";
                    if (question !== undefined) {
                        text = question.text;
                    }
                    return [{name: "Question", value: text, type: "text", var_name: "question"}];
                }
            }
        });

        modalInstance.result.then(function (question_info) {
            if (question === undefined) {
                reportService.save(question_info).then($scope.callback);
            } else {
                reportService.update(question.id, question_info).then($scope.callback);
            }
        }, function () {
        });
    };
    $scope.callback = function (resp) {
        if ("error" in resp) {
            for (var key in resp.error) {
                toastr.error(key + ": " + resp.error[key]);
            }
        } else {
            toastr.success("Question saved successfully!")
        }
    };
}]);
