app.controller('addModalController', ["$scope", "$uibModalInstance", "fields", "title", function($scope, $uibModalInstance, fields, title) {
	$scope.fields = fields;
	$scope.title = title;
	$scope.cancel = function () {
		$uibModalInstance.dismiss('cancel');
	};

  $scope.clicked = function () {
    console.log($scope.fields[1].value);
  }

  	$scope.ok = function () {
  		var result = {};
  		for (var i = 0; i < $scope.fields.length; i++) {
  			result[$scope.fields[i].var_name] = $scope.fields[i].value;
  		}
    	$uibModalInstance.close(result);
  	};
}]);