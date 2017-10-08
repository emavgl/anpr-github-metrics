(function()
{
    angular
        .module("github-issue-client-js")
        .controller("RepositoryController", ['$scope','$routeParams','$http', RepositoryController]);

    function RepositoryController($scope, $routeParams, $http, $location, $rootScope){

        $scope.labels = ['2006', '2007', '2008', '2009', '2010', '2011', '2012'];
        $scope.series = ['Series A', 'Series B'];

        $scope.data = [
            [65, 59, 80, 81, 56, 55, 40],
            [28, 48, 40, 19, 86, 27, 90]
        ];

        $scope.repo = {};

        $scope.getRepo = function(evento_id){
            $http.get("/").then(function(response){
                $console.log(response.data);
                $scope.repo = response.data;
            }).catch(function(data){
                console.log("errore nella richiesta al server");
            });
        };
    };

})();