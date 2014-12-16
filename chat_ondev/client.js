var Client = function() {
  self = this;
  var sock = new Sock('ws://localhost:9000');

  sock.onReceived(function(data) {
    console.log(data);

    //Handle connection
    switch (data.type) {
      case 'connect':
        storage.save('connection', {connect: true, ecid: data.employe_id});
        sock.send({type: 'reqcid'});
        break;
      case 'respcid':
        storage.save('own', {cid: data.cid});
        storage.save('conversation', []);
        break;
      case 'message':
        var cvr = storage.load('conversation');
        cvr.push({name: 'employe', content: data.content});
        storage.save('conversation', cvr);
        break;

      default:
        console.log("Unknow message");
        console.log(data);
    }

  });

  sock.onConnected(function() {
    var conn = storage.load('connection');
    if (!conn) {
      sock.send({
        type: 'connect'
      });
    } else {
      var own = storage.load('own');
      sock.send({
        type: 'reconnect',
        content: own.cid
      });
    }
  });

  self.sendMessage = function(message) {
    var conn = storage.load('connection');
    var cvr = storage.load('conversation');
    cvr.push({name: 'me', content: message});
    storage.save('conversation', cvr);
    sock.send({type: 'message', to: conn.ecid, content: message});
  }

  self.sendRaw = function(data) {
    sock.send(data);
  }

  self.getConvensation = function() {
    return storage.load('conversation');
  }

  self.close = function() {
    localStorage.clear();
  }
}


var client = new Client();
