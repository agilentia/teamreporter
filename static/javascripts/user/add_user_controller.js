var app = angular.module("teamreporterapp")
app.controller('addUserController', ["$scope", "$stateParams", "$uibModal", "userService", function($scope, $stateParams, $uibModal, userService) {
	var self = this;
	$scope.showAddModal = function(){
	  var modalInstance = $uibModal.open({
	      animation: true,
	      templateUrl: '/static/javascripts/common/add_modal.html',
	      controller: "addModalController",
	      //size: size,
	      resolve: {
	      	title: function(){return "Add User"},
	        fields: function () {
	          return [{name: "Email", value: "", type: "email", var_name: "email"}, 
						{name: "First Name", value: "", type: "text", var_name: "first_name"}, 
						{name: "Last Name", value: "", type: "text", var_name: "last_name"}];
	        }
	      }
	    });
		modalInstance.result.then(function (user_info) {
		    userService.save($stateParams.team_id, user_info).then(function(resp){
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
