describe('Our Work A11Y', function() {
    beforeEach(() => {
        cy.clearCookies();
    });

    it('Tests a11y on default entry page', function() {
        cy.visit('/');
        cy.get('#cu-privacy-notice-button').click();
        cy.get('#cu-privacy-notice').should('not.be.visible');

        cy.get('a').contains('Our Work').click();
        cy.title().should('contain', 'Our Work -- CTL Portfolio');
        cy.injectAxe();
        cy.checkA11y('html', {
            runOnly: {
              type: 'tag',
              values: ['wcag2a']
        }});
    });
});

