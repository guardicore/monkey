import React from 'react'
import LoginPageComponent from '../../../src/components/pages/LoginPage'

describe('<LoginPageComponent />', () => {
  it('renders', () => {
    cy.intercept('GET', '/', {
      // Define the mock response data here
      statusCode: 200,
    }).as('mockedRoute');

    cy.intercept('POST', '/api/login').as('loginRequest');
    // Define a variable to track window.location.href changes

    cy.mount(<LoginPageComponent />)
    cy.get('input[type=text]').type("test")
    cy.get('input[type=password]').type("testtest")

    cy.get('.monkey-submit-button').click();

    cy.get('@loginRequest.all').should('have.length',1);

    cy.wait('@mockedRoute').then((intercept) => {
      // Assert that the request was made
      expect(intercept.response.statusCode).to.equal(200); // Modify as needed
    });
  })
})
