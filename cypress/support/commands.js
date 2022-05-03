// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

Cypress.Commands.add("clear_privacy_notice", () => {
    if (cy.get('body').then($body => {
        if ($body.find('#cu-privacy-notice-button').length > 0) {
            if (cy.get('#cu-privacy-notice-button').then($button => {
                if ($button.is(':visible')) {
                    $button.click();
                    cy.get('#cu-privacy-notice').should('not.be.visible');
                }
            }));
        } else {
            assert.isOk(true,
                'Depending on cookie state, button may not exist');
        }
    }));
});
