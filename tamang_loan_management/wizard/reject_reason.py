from odoo import fields, models


class RejectReasonWizard(models.TransientModel):
    """Reject reasons from the company side"""
    _name = 'reject.reason'
    _description = 'Reject Reasons From The Company Side'

    reason = fields.Text(string="Reason", help="Reason Content")
    loan = fields.Char(string="Loan", help="Invisible Field")

    def action_reject_reason_txt(self):
        """Attach Reject Reason"""
        loan_request = self.env['loan.request'].search(
            [('name', '=', self.loan)])
        loan_request.write({
            'state': 'rejected',
            'reject_reason': self.reason
        })