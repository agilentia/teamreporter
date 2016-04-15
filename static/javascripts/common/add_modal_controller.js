app.controller('addModalController', ["$scope", "$uibModalInstance", "fields", "title", function ($scope, $uibModalInstance, fields, title) {
    var cur_date = new Date();
    /*
    for (var i = 0; i < fields.length; i++) {
        if (fields[i].type == "timepicker") {
            fields[i].value = cur_date;
        }
    }
    */
    $scope.hstep = 1;
    $scope.mstep = 5;

    $scope.fields = fields;
    $scope.title = title;
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