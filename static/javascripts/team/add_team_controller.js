var app = angular.module("teamreporterapp")
app.controller('addTeamController', ["$scope", "$stateParams", "$uibModal", "teamService", "toastr", function($scope, $stateParams, $uibModal, teamService, toastr) {
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
	          return [{name: "Name", value: "", type: "text", var_name: "name"},
	          		  {name: "Days of Week", type: "checkbox", var_name: "days_of_week", options: 
	          		  		[{"id": 0, name: "Monday"}, {id: 1, name: "Tuesday"}, {id: 2, name: "Wednesday"}, {id:3, name: "Thursday"}, {id: 4, name: "Friday"}]},
	          		  {name: "Survey Issue Time", type: "timepicker", var_name: "send_time"},
	          		  {name: "Report Summary Time", type: "timepicker", var_name: "summary_time"}];
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

		    teamService.save(team_info).then(function(resp){
		      	if ("error" in resp) {
		      		var error_string = ""
		      		for (var key in resp.error) {
		      			error_string += key + ": " + resp.error[key] + "\n"
		      		}
		      		toastr.error(error_string)
		      		return
		      	} else{
		      		toastr.success("Team saved successfully!")
		      	}

		      	
	      	});
	    }, function () {
	      //$log.info('Modal dismissed at: ' + new Date());
	    });
	}
}]);
