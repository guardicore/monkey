const USERNAME = 'test';
const PASSWORD = 'testtest';

enum Endpoint {
    HOME = '/',
    LOGIN = '/signin',
    REGISTER = '/signup'
}

describe('template spec', () => {
    it('passes', () => {
        cy.visit('https://example.cypress.io');
    });
});

describe('Register Process', () => {
    // Because we don't have a way to unregister a user
    // other than deleting the data dir this test will
    // fail if you run a second time

    it('Register', () => {
        cy.visit('https://localhost:8443');
        cy.location('pathname').should('eq', Endpoint.REGISTER);

        cy.get('input[placeholder="username"]').type(USERNAME);
        cy.get('input[placeholder="Password"]').type(PASSWORD);

        cy.get('button[text="Sign Up"]').click();

        cy.location('pathname').should('eq', Endpoint.HOME);
    });
});

describe('Login', () => {
    beforeEach(() => {
        cy.visit('https://localhost:8443');
    });

    it('prevents unregistered user from logging in', () => {
        cy.location('pathname').should('eq', Endpoint.LOGIN);

        cy.get('input[placeholder="username"]').type('unregistered');
        cy.get('input[placeholder="Password"]').type(PASSWORD);

        cy.get('button[text="Sign In"]').click();

        cy.location('pathname').should('eq', Endpoint.LOGIN);
    });

    it('allows registered user to login', () => {
        cy.location('pathname').should('eq', Endpoint.LOGIN);

        cy.get('input[placeholder="username"]').type(USERNAME);
        cy.get('input[placeholder="Password"]').type(PASSWORD);

        cy.get('button[text="Sign In"]').click();

        cy.location('pathname').should('eq', Endpoint.HOME);
    });
});
