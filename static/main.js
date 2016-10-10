// Enable pusher logging - don't include this in production
Pusher.logToConsole = true;

var pusher = new Pusher('09a9be90c83a82b77a1a', {
  cluster: 'eu',
  encrypted: true
});

var channel = pusher.subscribe('stream_shannel');
channel.bind('new_message', function(data) {
  console.log(data.message);
});
