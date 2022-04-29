describe('Home Page A11Y', function() {
    beforeEach(() => {
        cy.clearCookies();
    });

    it('Tests a11y on the home page', function() {
        cy.visit('/');
        cy.get('#cu-privacy-notice-button').click();
        cy.get('#cu-privacy-notice').should('not.be.visible');
        cy.injectAxe();
        cy.checkA11y('html', {
            runOnly: {
              type: 'tag',
              values: ['wcag2a']
        }});
    });
});

