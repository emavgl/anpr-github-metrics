(function()
{
    angular
        .module("github-issue-client-js")
        .controller("OrganizationController", ['$scope','$routeParams','$http', OrganizationController]);

    function OrganizationController($scope, $routeParams, $http, $location, $rootScope){

        $scope.testo = "placeholder"

        $scope.getData = function(evento_id){
            // $http.get("/").then(function(response){
            //     $console.log(response.data);
            //     $scope.testo = response.data;
            // }).catch(function(data){
            //     console.log("errore nella richiesta al server");
            // });
        };

        $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
        $scope.series = ['Series A', 'Series B'];
        $scope.data = [
            [65, 59, 80, 81, 56, 55, 40],
            [28, 48, 40, 19, 86, 27, 90]
        ];

        $scope.onClick = function (points, evt) {
            console.log(points, evt);
        };

        $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
        $scope.options = {
        scales: {
          yAxes: [
            {
              id: 'y-axis-1',
              type: 'linear',
              display: true,
              position: 'left'
            },
            {
              id: 'y-axis-2',
              type: 'linear',
              display: true,
              position: 'right'
            }
          ]
        }
        };
    };

})();