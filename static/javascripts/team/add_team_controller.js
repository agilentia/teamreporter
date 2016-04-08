var app = angular.module("teamreporterapp")
app.controller('addTeamController', ["$scope", "$stateParams", "$uibModal", "teamService", function($scope, $stateParams, $uibModal, teamService) {
	var self = this;
	$scope.showAddModal = function(){
	  var modalInstance = $uibModal.open({
	      animation: true,
	      templateUrl: '/static/javascripts/common/add_modal.html',
	      controller: "addModalController",
	      //size: size,
	      resolve: {
	        fields: function () {
	          return [{name: "Email", value: "", type: "email", var_name: "email"}, 
						{name: "First Name", value: "", type: "text", var_name: "first_name"}, 
						{name: "Last Name", value: "", type: "text", var_name: "last_name"}];
	        }
	      }
	    });
		modalInstance.result.then(function (user_info) {
		    teamService.save(user_info).then(function(resp){
		      	if ("error" in resp) {
		      		alert("error while saving")
		      		return
		      	}
	      	});
	    }, function () {
	      //$log.info('Modal dismissed at: ' + new Date());
	    });
	}
}]);
