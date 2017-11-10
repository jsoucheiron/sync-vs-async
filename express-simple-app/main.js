const cluster = require('cluster');
const express = require('express');
const fetch = require('node-fetch');

const PORT = 80;
const NUM_WORKERS = 4;

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

const app = express();
app.get('/io', ioHandler);
app.get('/cpu', cpuHandler);

if (cluster.isMaster) {
  for (let i = 0; i < NUM_WORKERS; i++) {
    cluster.fork();
  }
} else {
  app.listen(PORT);
  console.log(`Worker ${process.pid} started`);
}

