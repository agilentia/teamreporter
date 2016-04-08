var app = angular.module("teamreporterapp")
app.controller('addUserController', ["$scope", "$stateParams", "$uibModal", "userService", function($scope, $stateParams, $uibModal, userService) {
	var self = this;
	$scope.showAddUserModal = function(){
	  var modalInstance = $uibModal.open({
	      animation: true,
	      templateUrl: '/static/javascripts/user/add_user_modal.html',
	      controller: "addUserModalController",
	      //size: size,
	      resolve: {
	        fields: function () {
	          return {};
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

app.controller('addUserModalController', ["$scope", "$uibModalInstance", function($scope, $uibModalInstance) {
	$scope.fields = [{name: "Email", value: "", type: "email", var_name: "email"}, 
	{name: "First Name", value: "", type: "text", var_name: "first_name"}, 
	{name: "Last Name", value: "", type: "text", var_name: "last_name"}];

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

  	$scope.ok = function () {
  		var result = {}
  		console.log($scope.fields)
  		for (var i = 0; i < $scope.fields.length; i++) {
  			result[$scope.fields[i].var_name] = $scope.fields[i].value;
  		}
    	$uibModalInstance.close(result);
  	};
}]);