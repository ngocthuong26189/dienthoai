var Employe = function() {
  self = this;
  var sock = new Sock('ws://localhost:9000/?token=employe');
  var clients = {};

  sock.onReceived(function(data) {
    console.log(data);

    //Handle connection
    switch (data.type) {
      case 'connect':
        var connected_cid = data.cid;
        if (!clients[connected_cid]) {
          clients[connected_cid] = [];
        }
        break;
      case 'message':
        if (clients[data.from]){
          clients[data.from].push({name: 'Client', content: data.content});
        }
        break;

      default:
        console.log("Unknow message");
        console.log(data);
    }

  });

  self.sendRaw = function(data) {
    sock.send(data);
  }

  self.sendMessage = function(to, message) {
    clients[to].push({name: 'me', content: message});
    sock.send({type: 'message', to: to, content: message});
  }

  self.close = function(client_id) {
    sock.send({type: 'close', cids: [client_id]});
  }

  self.getClients = function() {
    return clients;
  }
}

var employe = new Employe();