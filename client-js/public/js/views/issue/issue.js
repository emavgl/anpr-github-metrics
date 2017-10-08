(function()
{
    angular
        .module("github-issue-client-js")
        .controller("IssueController", ['$scope','$routeParams','$http', IssueController]);

    function IssueController($scope, $routeParams, $http, $location, $rootScope){


    };

})();