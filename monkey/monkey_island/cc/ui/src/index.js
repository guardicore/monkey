import '@babel/polyfill';
import 'core-js/fn/object/assign';
import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/Main';
import './styles/Main.scss';
import './styles/external/fontawesome/css/all.css';

// Render the main component into the dom
ReactDOM.render(<App/>, document.getElementById('app'));
