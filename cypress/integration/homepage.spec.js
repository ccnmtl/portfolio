describe('Home Page Navigation', function() {
    it('Visits the home page', function() {
        cy.visit('/');
        cy.title().should('equal', 'Home -- CTL Portfolio');
    });
});
