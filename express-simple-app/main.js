const express = require('express');
const fetch = require('node-fetch');

const app = express();

const ioHandler = (request, response) => {
  const delay = request.query.delay || '';
  fetch(`http://nginx/${delay}`).then(() => {
    response.send('Request finished!');
  })
};

const cpuHandler = (request, response) => {
  let iterations = parseInt(request.query.iterations || '0', 10);
  for (; iterations > 0; iterations--);
  response.send('Request finished!');

};

app.get('/io', ioHandler);
app.get('/cpu', cpuHandler);

app.listen(5000);
