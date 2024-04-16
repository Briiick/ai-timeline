const functions = require('firebase-functions');
const app = require('./main').app;

exports.app = functions.https.onRequest(app);