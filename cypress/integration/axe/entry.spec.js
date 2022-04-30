describe('Entry Page A11Y', function() {
    beforeEach(() => {
        cy.visit('/');
        cy.clear_privacy_notice();
    });

    it('Tests a11y on default entry page', function() {
        cy.visit('/');
        cy.title().should('contain', 'Home -- CTL Portfolio')

        cy.get('a').contains('Default Entry').click();
        cy.title().should('contain', 'Default Entry -- CTL Portfolio');
        cy.injectAxe();
        cy.checkA11y('html', {
            runOnly: {
              type: 'tag',
              values: ['wcag2a']
        }});
    });

    it('Tests a11y on regular entry page', function() {
        cy.visit('/');
        cy.title().should('contain', 'Home -- CTL Portfolio')

        cy.get('a').contains('Entry One').click({force: true});
        cy.title().should('contain', 'Entry One -- CTL Portfolio');
        cy.injectAxe();
        cy.checkA11y('html', {
            runOnly: {
              type: 'tag',
              values: ['wcag2a']
        }});
    });
});

