import '@babel/polyfill';
import 'core-js/fn/object/assign';
import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/Main';
import Bootstrap from 'bootstrap/dist/css/bootstrap.css'; // eslint-disable-line no-unused-vars

// Render the main component into the dom
ReactDOM.render(<App/>, document.getElementById('app'));
