'use strict'

angular.module('admin_chat_app', [
  'ui.router',
  'btford.socket-io'
]).
config(['$urlRouterProvider','$stateProvider', function($urlRouterProvider, $stateProvider) {
    $urlRouterProvider.otherwise("/");
    $stateProvider.state('index',{
        url:'/',
        templateUrl:'/static/partials/index.html',
        controller:'index'
    });
}])
.controller('index', ['$scope','chatSocket', function ($scope,chatSocket) {
    chatSocket.forward('message', $scope);
    chatSocket.forward('connect', $scope);
    chatSocket.forward('error', $scope);
    chatSocket.forward('employee_disconnected', $scope);
    $scope.$on('socket:connect',function (ev,data) {
        var sid = getCookie('sid');
        var userId = getCookie('userId');
        chatSocket.emit('login',{sid:sid,userId:userId});
    });
    $scope.$on('socket:message',function (ev,data) {
        alert(JSON.stringify(data));
    });
    $scope.$on('socket:error',function (ev,data) {
        alert(JSON.stringify(data));
    });
    $scope.$on('socket:employee_disconnected',function (ev,data) {
        alert(JSON.stringify(data));
    });
    $scope.closeChat=function (id) {
        var isClose = confirm("Are you want close chat with this customer ?");
        if(isClose){
           
        }
    }
    $scope.send=function () {
        if($scope.message){
           alert($scope.message); 
        } 
    }
    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i=0; i<ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1);
            if (c.indexOf(name) != -1) return c.substring(name.length,c.length);
        }
        return "";
    }
}])
.factory('chatSocket', function (socketFactory) {
    var myIoSocket = io.connect('http://' + document.domain + ':' + 8080 + '/employee');
    var chatSocket = socketFactory({
      ioSocket: myIoSocket
    });
    return chatSocket;
})
;