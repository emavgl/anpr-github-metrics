(function() {
    angular
        .module("github-issue-client-js")
        .controller("RepositoryController", ['$scope', '$routeParams', '$http', RepositoryController]);

    function RepositoryController($scope, $routeParams, $http, $location, $rootScope) {

        var backendEndpoint = "http://localhost:5010"
        var dataIssues = {};



        $scope.repo = {};

        $scope.getRepo = function(evento_id) {
            console.log(backendEndpoint + "/repositories/" + evento_id);
            $http.get(backendEndpoint + "/repositories/" + evento_id, { timeout: 100000 }).then(function(response) {
                dataIssues = response.data;
                $scope.repo = response.data.repository;

                var dataMaxMax = 432000; // 5 Days Timeouts
                //var dataActualMax = Math.max(...dataIssues.repository.issues.first_response_times);

                var dataActualMax = Math.max.apply(Math, (dataIssues.repository.issues.first_response_times));
                dataActualMax += 100;

                var maxColumns = 10;

                if (dataIssues.repository.issues.first_response_times.length < maxColumns) {
                    maxColumns = dataIssues.repository.issues.first_response_times.length;
                }

                var bucketLenght = dataActualMax / maxColumns;

                var finalData = [];
                var finalLabels = [];

                var lastBucket = 0

                for (var i = 0; i < dataIssues.repository.issues.first_response_times.length; i++) {

                    var indexFinalData = parseInt(dataIssues.repository.issues.first_response_times[i] / bucketLenght);

                    finalData[indexFinalData] = finalData[indexFinalData] + 1 || 1;
                    finalLabels.push(parseInt(lastBucket / 60) + "m - " + parseInt((lastBucket + bucketLenght) / 60) + "m")
                    lastBucket += bucketLenght

                    console.log("array: ", finalData)

                }


                $scope.labels_first_response = finalLabels;
                $scope.data_first_response = finalData;

                //#############################

                var dataMaxMax = 432000; // 5 Days Timeouts
                //var dataActualMax = Math.max(...dataIssues.repository.issues.first_response_times);

                var dataActualMax = Math.max.apply(Math, (dataIssues.repository.issues.closing_times));
                dataActualMax += 100;

                var maxColumns = 10;

                if (dataIssues.repository.issues.closing_times.length < maxColumns) {
                    maxColumns = dataIssues.repository.issues.closing_times.length;
                }

                var bucketLenght = dataActualMax / maxColumns;

                var finalData = [];
                var finalLabels = [];

                var lastBucket = 0

                for (var i = 0; i < dataIssues.repository.issues.closing_times.length; i++) {

                    var indexFinalData = parseInt(dataIssues.repository.issues.closing_times[i] / bucketLenght);

                    finalData[indexFinalData] = finalData[indexFinalData] + 1 || 1;
                    finalLabels.push(parseInt(lastBucket / 60) + "m - " + parseInt((lastBucket + bucketLenght) / 60) + "m")
                    lastBucket += bucketLenght

                    console.log("array: ", finalData)

                }

                $scope.labels_closing_times = finalLabels;
                $scope.data_closing_times = finalData;


                // $scope.series = ['Series A'];
                // $scope.colors = ['blue'];

                // ###############################
                $scope.labels_number_total = ["Open Issues", "Closed Issues"];
                $scope.data_number_total = [dataIssues.repository.issues.number_open, dataIssues.repository.issues.number_closed];
                $scope.colors_number_total = ["#ff0000", "#00ff00"];

            }).catch(function(data) {
                console.log(data);
                console.log("repository: errore nella richiesta al server");
            });

        };

        $scope.getRepo($routeParams.id);

    };

})();