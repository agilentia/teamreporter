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
	      	title: function(){return "Add Team"},
	        fields: function () {
	          return [{name: "Name", value: "", type: "text", var_name: "name"}];
	        }
	      }
	    });
		modalInstance.result.then(function (team_info) {
		    teamService.save(team_info).then(function(resp){
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
