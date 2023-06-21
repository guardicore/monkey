import 'core-js/stable';
import 'regenerator-runtime/runtime';
import React from 'react';
import {createRoot} from 'react-dom/client';
import App from './components/Main';
import './styles/Main.scss';
import './styles/external/fontawesome/css/all.css';

// Render the main component into the dom
const root = createRoot(document.getElementById('app'));
root.render(
    <React.StrictMode>
            <App />
    </React.StrictMode>
);
