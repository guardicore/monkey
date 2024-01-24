import React from 'react';
import MonkeyDrawer from './Drawer';

describe('<MonkeyDrawer />', () => {
    it('renders', () => {
        // see: https://on.cypress.io/mounting-react
        cy.mount(<MonkeyDrawer />);
    });
});
