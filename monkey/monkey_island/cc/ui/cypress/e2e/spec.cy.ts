describe('Register Process', () => {
  beforeEach(() =>{
    cy.visit('http://localhost:8000')
  })

  // Because we don't have a way to unregister a user
  // other than deleting the data dir this test will
  // fail if you run a second time

  it('Register', () => {
    cy.location('pathname').should('eq','/register')

    cy.get('input[placeholder="Username"]').type("test")
    cy.get('input[placeholder="Password"]').type("testtest")

    cy.get('.monkey-submit-button').click()

    cy.location('pathname').should('eq','/')

  })
})
