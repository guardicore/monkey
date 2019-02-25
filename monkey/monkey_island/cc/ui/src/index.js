import 'core-js/fn/object/assign';
import React from 'react';
import ReactDOM from 'react-dom';
import 'babel-polyfill';
import App from './components/Main';
import Bootstrap from 'bootstrap/dist/css/bootstrap.css'; // eslint-disable-line no-unused-vars
import { FilePond, registerPlugin } from 'react-filepond';
import 'filepond/dist/filepond.min.css';

// Render the main component into the dom
ReactDOM.render(<App />, document.getElementById('app'));
