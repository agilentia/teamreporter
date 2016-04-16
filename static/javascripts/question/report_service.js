var app = angular.module("teamreporterapp")
app.factory("reportService", ["Report", function(Report){
	var questions = [];
	var team_id = "";
	var self = this;
	var service = {
		init: function(team_id) {
			self.team_id = team_id;
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

		save: function(question_info) {
			save = Report.save({team_id: self.team_id}, {question: question_info.question}, function(data){
				if ("question" in data)
					questions.push(data.question);

			});
			return save.$promise;
		},

		delete: function(question_id) {
			console.log(self.team_id, question_id);
			Report.delete({team_id: self.team_id, id: question_id}, function(data){
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