from odoo import api, fields, models
from odoo.exceptions import UserError


class ManagerRequest(models.Model):
    _name = 'manager.request'
    _description = 'Manager Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user,
                              readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    request_date = fields.Date(string='Request Date', default=fields.Date.today(), readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)
    message = fields.Text(string='Message', help="Reason for requesting manager role")
    reject_reason = fields.Text(string='Rejection Reason', readonly=True, help="Reason for rejecting the request")

    def action_submit_request(self):
        self.write({'state': 'submitted'})

    def action_approve_request(self):
        self.write({'state': 'approved'})
        user = self.user_id
        user.write({
            'groups_id': [
                (3, self.env.ref('base.group_portal').id),  # Remove Portal group
                (4, self.env.ref('tamang_loan_management.loan_management_group_manager').id),  # Add Loan Manager Group
            ]
        })
        # self._send_email('Your manager request has been approved.')

    def action_reject_request(self):
        if not self.reject_reason:
            raise UserError('Please provide a reason for rejecting the request.')
        self.write({'state': 'rejected'})
        # self._send_email('Your manager request has been rejected.')

    # def _send_email(self, subject):
    #     template = self.env.ref('your_module_name.email_template_manager_request')  # Adjust to your actual module name
    #     self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)