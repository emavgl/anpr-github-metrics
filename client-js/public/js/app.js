
var app = angular.module("github-issue-client-js", ["ngRoute","chart.js"]);

// angular-route confifguration
app.config(function($routeProvider, $httpProvider, $locationProvider) {
    $routeProvider
    .when("/", {
        redirectTo: "/organization"
    })
    .when("/organization", {
        templateUrl : "js/views/organization/organization.html",
        controller: 'OrganizationController',
    })
    .when("/repository/:id", {
        templateUrl : "js/views/repository/repository.html",
        controller: 'RepositoryController'
    })
    .when("/issue", {
        templateUrl : "js/views/issue/issue.html",
        controller: 'IssueController',
    })
    .otherwise({
        redirectTo: '/login'
    });
});


// navigation controller for highlighting the menu field accordingly
app.controller('NavController', function($scope, $location, $http) {

    $scope.repositories = [];

    $scope.getRepos = function(){
        $http.get("http://localhost:5010/repositories").then(function(resp){
            $scope.repositories = resp.data.repositories
        }).catch(function(){
            console.log("error getting repos")
        });
    }

    $scope.switchToRepo = function(id){
        // $http.get("http://www.mocky.io/v2/59d90ef41000006b01caf0de").then(function(resp){
        //     $scope.repositories = resp.data
        // }).catch(function(){
        //     console.log("error getting repos")
        // });

        router

    }
    $scope.getRepos();

});

