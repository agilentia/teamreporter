var app = angular.module("teamreporterapp")
app.controller('addQuestionController', ["$scope", "$stateParams", "$uibModal", "reportService", "toastr", function($scope, $stateParams, $uibModal, reportService, toastr) {
	var self = this;
	$scope.showAddModal = function(){
	  var modalInstance = $uibModal.open({
	      animation: true,
	      templateUrl: '/static/javascripts/common/add_modal.html',
	      controller: "addModalController",
	      //size: size,
	      resolve: {
	      	title: function(){return "Add Question"},
	        fields: function () {
	          return [{name: "Question", value: "", type: "text", var_name: "question"}];
	        }
	      }
	    });
	  
		modalInstance.result.then(function (question_info) {
		    reportService.save($stateParams.team_id, question_info).then(function(resp){
 				if ("error" in resp) {
		      		var error_string = ""
		      		for (var key in resp.error) {
		      			error_string += key + ": " + resp.error[key] + "\n"
		      		}
		      		toastr.error(error_string)
		      	} else{
		      		toastr.success("Question saved successfully!")
		      	}
	      	});
	    }, function () {
	      //$log.info('Modal dismissed at: ' + new Date());
	    });
	}
}]);
