app.controller('addModalController', ["$scope", "$uibModalInstance", "fields", function($scope, $uibModalInstance, fields) {
	$scope.fields = fields;

	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

  	$scope.ok = function () {
  		var result = {};
  		for (var i = 0; i < $scope.fields.length; i++) {
  			result[$scope.fields[i].var_name] = $scope.fields[i].value;
  		}
    	$uibModalInstance.close(result);
  	};
}]);