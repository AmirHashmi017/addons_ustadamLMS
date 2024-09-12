from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request


class LoanController(http.Controller):

    @http.route('/loans', auth='user', website=True)
    def loan_types_list(self, **kw):
        # Fetch all loan types
        loan_types = request.env['loan.type'].search([])
        return request.render('tamang_loan_management.loan_types_list', {
            'loan_types': loan_types,
        })

    @http.route('/get_loan', type='http', auth='user', website=True)
    def get_loan(self, **kwargs):
        # Logic to handle 'Get Loan' request
        request.env['user.request'].create({
            'user_id': request.env.user.id,
            'company_id': request.env.company.id,
            'message': 'Request to become a loan user',
        }).action_submit_request()
        return request.redirect('/loans')

    @http.route('/become_loan_manager', type='http', auth='user', website=True)
    def become_loan_manager(self, **kwargs):
        if request.env.user.has_group('tamang_loan_management.loan_management_group_user'):
            active_loan = request.env['loan.request'].search([
                ('applicant_id', '=', request.env.user.id),
                ('state', 'not in', ['close', 'draft', 'confirmed'])
            ])

            if active_loan:
                raise ValidationError('You have an active loan request. Please close it before applying for a new one.')

        # Logic to handle 'Become Loan Manager' request
        manager_request = request.env['manager.request'].create({
            'user_id': request.env.user.id,
            'company_id': request.env.company.id,
            'message': 'Request to become a loan manager',
        })
        manager_request.action_submit_request()

        return request.redirect('/loans')

