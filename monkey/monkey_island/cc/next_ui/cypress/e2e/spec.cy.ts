const USERNAME = 'test';
const PASSWORD = 'testtest';

enum Endpoint {
    HOME = '/',
    LOGIN = '/login',
    REGISTER = '/registration'
}

describe('Register Process', () => {
    // Because we don't have a way to unregister a user
    // other than deleting the data dir this test will
    // fail if you run a second time

    describe('on successful registration', () => {
        it('brings the user to home page', () => {
            cy.visit('/');
            cy.location('pathname', { timeout: 10000 }).should(
                'eq',
                Endpoint.REGISTER
            );

            cy.get('input[name="username"]').type(USERNAME);
            cy.get('input[name="password"]').type(PASSWORD);

            cy.get('button').contains('Register').click();

            cy.location('pathname').should('eq', Endpoint.HOME);
        });
    });
});

describe('Login', () => {
    beforeEach(() => {
        cy.visit('/');
    });

    it('prevents unregistered user from logging in', () => {
        cy.location('pathname', { timeout: 10000 }).should(
            'eq',
            Endpoint.LOGIN
        );

        cy.get('input[name="username"]').type('unregistered');
        cy.get('input[name="password"]').type(PASSWORD);

        cy.get('button').contains('Login').click();

        cy.location('pathname').should('eq', Endpoint.LOGIN);
    });

    it('allows registered user to login', () => {
        cy.location('pathname', { timeout: 10000 }).should(
            'eq',
            Endpoint.LOGIN
        );

        cy.get('input[name="username"]').type(USERNAME);
        cy.get('input[name="password"]').type(PASSWORD);

        cy.get('button').contains('Login').click();

        cy.location('pathname').should('eq', Endpoint.HOME);
    });
});
