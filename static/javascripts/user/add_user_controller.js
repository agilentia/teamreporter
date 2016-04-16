var app = angular.module("teamreporterapp")
app.controller('addUserController', ["$scope", "$stateParams", "$uibModal", "userService", "roleService", "toastr", function($scope, $stateParams, $uibModal, userService, roleService, toastr) {
	var self = this;
	$scope.self = self;
	var roles = roleService.get();
	self.showAddModal = function(){
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
						{name: "Last Name", value: "", type: "text", var_name: "last_name"},
						{name: "Roles", value: [], type: "multiselect", var_name: "roles", options: roles}];
	        }
	      }
	    });
	  
		modalInstance.result.then(function (user_info) {
		    userService.save(user_info).then(function(resp){
		      	if ("error" in resp) {
		      		var error_string = ""
		      		for (var key in resp.error) {
		      			error_string += key + ": " + resp.error[key] + "\n"
		      		}
		      		toastr.error(error_string)
		      	} else{
		      		toastr.success("User saved successfully!")
		      	}
	      	});
	    }, function () {
	      //$log.info('Modal dismissed at: ' + new Date());
	    });
	}
}]);
