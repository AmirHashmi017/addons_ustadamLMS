from odoo import api, fields, models


class LoanTypes(models.Model):
    """Create different types of Loans, And can wisely choose while requesting
     for loan"""
    _name = 'loan.type'
    _inherit = ['mail.thread']
    _description = 'Loan Type'

    name = fields.Char(string='Name', required=True, help="Loan Type Name")
    loan_amount = fields.Float(string='Loan Amount', required=True, help="Loan Amount")
    tenure = fields.Integer(string='Tenure (monthly)', default=1, help="Amortization period")
    tenure_plan = fields.Char(string="Tenure Plan", default='monthly', readonly=True, help="EMI payment plan")
    interest_rate = fields.Float(string='Interest Rate', help="Loan Interest Rate")
    disbursal_amount = fields.Float(string='Disbursal Amount', compute='_compute_disbursal_amount',
                                    help="Total Amount To Be Disbursed")
    documents_ids = fields.Many2many('loan.documents', string="Documents", help="Personal Proofs")
    processing_fee = fields.Integer(string="Processing Fee", help="Amount For Initializing The Loan")
    note = fields.Text(string="Criteria", help="Criteria for approving loan requests")
    company_id = fields.Many2one('res.company', string='Company', readonly=True, help="Company Name",
                                 default=lambda self: self.env.company)
    creator_id = fields.Many2one('res.users', string='Creator', default=lambda self: self.env.user, readonly=True)
    applicants_count = fields.Integer(string='Applicants', default=0)

    @api.depends('processing_fee')
    def _compute_disbursal_amount(self):
        """Calculating amount for disbursing"""
        for record in self:
            record.disbursal_amount = record.loan_amount - record.processing_fee

    def apply_loan_action(self):
        """Handle loan application action"""
        for record in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Loan Request',
                'res_model': 'loan.request',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_loan_type_id': record.id,
                    'default_loan_amount': record.loan_amount,
                    'default_disbursal_amount': record.disbursal_amount,
                    'default_tenure': record.tenure,
                    'default_interest_rate': record.interest_rate,
                    'default_documents_ids': [(6, 0, record.documents_ids.ids)],
                    'default_partner_id': record.creator_id.partner_id.id,
                    'default_applicant_id': self.env.user.id,
                    'readonly_fields': ['loan_type_id', 'loan_amount', 'disbursal_amount', 'tenure', 'interest_rate',
                                        'documents_ids', 'partner_id', 'applicant_id'],
                }
            }
