
////var socket = io('/', 8001);
//var ws = new WebSocket("ws://localhost:9000/chat?token=1234&lmao=123");
//ws.onopen = function() {
    //// Web Socket is connected, send data using send()
    //ws.send(JSON.stringify({
        //type: 'connect'			
    //}));
    //console.log("Message is sent...");
//};
//ws.onmessage = function (evt) {
    //var received_msg = evt.data;
    //console.log("Message is received:" + received_msg);
//};
//ws.onclose = function() {
    //// websocket is closed.
    //console.log("Connection is closed...");
/*};*/

var Sock = function(url) {
  var ws = new WebSocket(url);
  var self = this;
  
  self.received = self.close = self.open = function(e) {
    if (e) console.log(e);
  }
  
  ws.onopen = function() {
    self.open();
  }

  ws.onmessage = function(e) {
    var data = e.data;
    self.received(JSON.parse(data));
  }

  ws.onclose = function() {
    self.close();
  }
 
  //Set up
  self.onReceived = function(next) {
    self.received = next;
  }

  self.onClose = function(next) {
    self.close = next;
  }

  self.onConnected = function(next) {
    self.open = next;
  }

  self.send = function(data) {
    ws.send(JSON.stringify(data));
  }
}


var storage = {
  save: function(key, data) {
    localStorage.setItem(key, JSON.stringify(data));
  },
  load: function(key) {
    return JSON.parse(localStorage.getItem(key));
  }
}
