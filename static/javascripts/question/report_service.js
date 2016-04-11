var app = angular.module("teamreporterapp")
app.factory("reportService", ["Report", function(Report){
	var questions = [];
	var service = {
		init: function(team_id) {
			query = Report.get({team_id: team_id}, function(data){
				questions = data.questions;
			}, function(error){
				// Deal here
			});
			return query.$promise;
		},

		get: function(){
			return questions;
		},

		save: function(team_id, question_info) {
			save = Report.save({team_id: team_id}, {question: question_info.question}, function(data){
				questions.push(data.question);
			});
			return save.$promise;
		},

		delete: function(team_id, question_id) {
			console.log(question_id)
			Report.delete({team_id: team_id, id: question_id}, function(data){
				for (var i = 0; i < questions.length; i++ ) {
					if (questions[i].id == data.question.id){
						questions.splice(i, 1);
					}
				}
			});
		},

		reportModel: {questions: questions}

	}

	return service
}]);