describe('Home Page A11Y', function() {
    beforeEach(() => {
        cy.visit('/');
        cy.clear_privacy_notice();
    });
    it('Tests a11y on the home page', function() {
        cy.visit('/');
        cy.injectAxe();
        cy.checkA11y('html', {
            runOnly: {
              type: 'tag',
              values: ['wcag2a']
        }});
    });
});

