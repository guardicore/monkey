import React from 'react';
import { ThemeMode } from './ThemeMode';

describe('<ThemeMode />', () => {
    it('renders', () => {
        // see: https://on.cypress.io/mounting-react
        cy.document().its('fonts.status').should('equal', 'loaded');
        cy.mount(<ThemeMode />);
    });
});
