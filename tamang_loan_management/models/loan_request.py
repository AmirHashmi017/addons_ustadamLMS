from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class LoanRequest(models.Model):
    """Can create new loan requests and manage records"""
    _name = 'loan.request'
    _description = 'Loan Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Loan Reference', readonly=True,
                       copy=False, default=lambda self: 'New')
    applicant_id = fields.Many2one('res.users', string='Applicant',
                                   default=lambda self: self.env.user, readonly=True, help="Applicant")
    company_id = fields.Many2one('res.company', string='Company',
                                 readonly=True, help="Company Name",
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True, help="Currency",
                                  default=lambda self: self.env.user.company_id.
                                  currency_id)
    loan_type_id = fields.Many2one('loan.type', string='Loan Type', required=True,
                                   help="Can choose different loan types suitable")
    # Changed from computed to related fields
    loan_amount = fields.Float(string="Loan Amount", related='loan_type_id.loan_amount', readonly=True, store=True,
                               help="Total loan amount")
    disbursal_amount = fields.Float(string="Disbursal Amount", related='loan_type_id.disbursal_amount', readonly=True,
                                    store=True, help="Total loan amount available to disburse")
    tenure = fields.Integer(string="Tenure", related='loan_type_id.tenure', readonly=True, store=True,
                            help="Installment period")
    interest_rate = fields.Float(string="Interest Rate", related='loan_type_id.interest_rate', readonly=True,
                                 store=True, help="Interest percentage")
    documents_ids = fields.Many2many('loan.documents', string="Documents", readonly=True, store=True,
                                     compute='_compute_documents_ids', help="Documents as proof")

    date = fields.Date(string="Request Date", default=fields.Date.today(),
                       readonly=True, help="Date on which loan is requested")

    partner_id = fields.Many2one('res.partner', string="Partner", related='loan_type_id.creator_id.partner_id',
                                 store=True, readonly=True, help="Partner")

    repayment_lines_ids = fields.One2many('repayment.line',
                                          'loan_id',
                                          string="Loan Line", index=True,
                                          help="Repayment lines")
    img_attachment_ids = fields.Many2many('ir.attachment',
                                          relation="m2m_ir_identity_card_rel",
                                          column1="documents_ids",
                                          string="Images", required=True,
                                          help="Image proofs")
    journal_id = fields.Many2one('account.journal',
                                 string="Journal",
                                 help="Journal types",
                                 domain="[('type', '=', 'purchase'),"
                                        "('company_id', '=', company_id)]",
                                 )
    debit_account_id = fields.Many2one('account.account',
                                       string="Debit account",
                                       help="Choose account for "
                                            "disbursement debit")
    credit_account_id = fields.Many2one('account.account',
                                        string="Credit account",
                                        help="Choose account for "
                                             "disbursement credit")
    reject_reason = fields.Text(string="Reason", help="Displays "
                                                      "rejected reason")
    request = fields.Boolean(string="Request",
                             help="For monitoring the record")
    state = fields.Selection(string='State',
                             selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'),
                                        ('waiting', 'Waiting For Approval'), ('wait', 'Waiting For Closing'),
                                        ('approved', 'Approved'), ('disbursed', 'Disbursed'),
                                        ('rejected', 'Rejected'), ('closed', 'Closed')],
                             copy=False, tracking=True, default='draft', help="Loan request states")

    @api.model
    def create(self, vals):
        """create  auto sequence for the loan request records"""
        if 'partner_id' not in vals:
            loan_type = self.env['loan.type'].browse(vals.get('loan_type_id'))
            if loan_type:
                vals['partner_id'] = loan_type.creator_id.partner_id.id
            else:
                raise UserError(_('Loan Type must be selected to fetch the Partner.'))

        loan_count = self.env['loan.request'].search(
            [('partner_id', '=', vals['partner_id']),
             ('state', 'not in', ('draft', 'rejected', 'closed'))])
        if loan_count:
            for rec in loan_count:
                if rec.state != 'closed':
                    raise UserError(
                        _('The partner has already an ongoing loan.'))
        else:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('increment.loan.ref') or 'New'
            res = super().create(vals)
            return res

    @api.depends('loan_type_id')
    def _compute_documents_ids(self):
        for record in self:
            record.documents_ids = record.loan_type_id.documents_ids

    @api.onchange('loan_type_id')
    def _onchange_loan_type_id(self):
        """Changing field values based on the chosen loan type"""
        type_id = self.loan_type_id
        self.loan_amount = type_id.loan_amount
        self.disbursal_amount = type_id.disbursal_amount
        self.tenure = type_id.tenure
        self.interest_rate = type_id.interest_rate
        self.documents_ids = type_id.documents_ids
        self.partner_id = self.loan_type_id.creator_id.partner_id.id

    def action_loan_request(self):
        """Changes the state to confirmed and send confirmation mail"""
        self.write({'state': "confirmed"})
        self.loan_type_id.applicants_count += 1
        partner = self.partner_id
        loan_no = self.name
        subject = 'Loan Confirmation'
        message = (f"Dear {partner.name},<br/> This is a confirmation mail "
                   f"for your loan{loan_no}. We have submitted your loan "
                   f"for approval.")
        outgoing_mail = self.company_id.email
        mail_values = {
            'subject': subject,
            'email_from': outgoing_mail,
            'author_id': self.env.user.partner_id.id,
            'email_to': partner.email,
            'body_html': message,
        }
        mail = self.env['mail.mail'].sudo().create(mail_values)
        mail.send()

    def action_request_for_loan(self):
        """Change the state to waiting for approval"""
        existing_loan = self.env['loan.request'].search([
            ('state', 'in', ['disbursed']),
            ('applicant_id', '=', self.applicant_id.id)
        ])

        if existing_loan:
            raise ValidationError(_('You have already have an active loan'))
        else:
            if self.request:
                self.write({'state': "waiting"})
            else:
                message_id = self.env['message.popup'].create(
                    {'message': _("Compute the repayments before requesting")}
                )
                return {
                    'name': _('Repayment'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.popup',
                    'res_id': message_id.id,
                    'target': 'new'
                }

    def action_loan_approved(self):
        """Change to Approved state"""
        self.write({'state': "approved"})

    def action_disburse_loan(self):
        """Disbursing the loan to customer and creating journal
         entry for the disbursement"""
        self.write({'state': "disbursed"})
        for loan in self:
            amount = loan.disbursal_amount
            loan_name = loan.partner_id.name
            reference = loan.name
            journal_id = loan.journal_id.id
            debit_account_id = loan.debit_account_id.id
            credit_account_id = loan.credit_account_id.id
            date_now = loan.date

            # Fetch currency from the partner
            partner_currency_id = loan.partner_id.property_product_pricelist.currency_id.id
            if not partner_currency_id:
                # Fallback to company currency if partner currency is not set
                partner_currency_id = self.env.user.company_id.currency_id.id

            # Prepare debit and credit values with currency_id
            debit_vals = {
                'name': loan_name,
                'account_id': debit_account_id,
                'journal_id': journal_id,
                'date': date_now,
                'debit': amount > 0.0 and amount or 0.0,
                'credit': amount < 0.0 and -amount or 0.0,
                'currency_id': partner_currency_id,  # Include currency_id
            }
            credit_vals = {
                'name': loan_name,
                'account_id': credit_account_id,
                'journal_id': journal_id,
                'date': date_now,
                'debit': amount < 0.0 and -amount or 0.0,
                'credit': amount > 0.0 and amount or 0.0,
                'currency_id': partner_currency_id,  # Include currency_id
            }

            # Create the account move
            vals = {
                'name': f'DIS / {reference}',
                'narration': reference,
                'ref': reference,
                'journal_id': journal_id,
                'date': date_now,
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)],
                'currency_id': partner_currency_id,  # Set currency_id for the move
            }
            move = self.env['account.move'].create(vals)
            move.action_post()
        return True

    def action_request_close_loan(self):
        """Requesting to close the loan"""
        demo = []
        for check in self.repayment_lines_ids:
            if check.state == 'unpaid':
                demo.append(check)
        if len(demo) >= 1:
            message_id = self.env['message.popup'].create(
                {'message': _("Pending Repayments")})
            return {
                'name': _('Repayment'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'message.popup',
                'res_id': message_id.id,
                'target': 'new'
            }
        self.write({'state': "wait"})

    def action_close_loan(self):
        """Closing the loan"""
        demo = []
        for check in self.repayment_lines_ids:
            if check.state == 'unpaid':
                demo.append(check)
        if len(demo) >= 1:
            message_id = self.env['message.popup'].create(
                {'message': _("Pending Repayments")})
            return {
                'name': _('Repayment'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'message.popup',
                'res_id': message_id.id,
                'target': 'new'
            }
        self.write({'state': "closed"})

    def action_loan_rejected(self):
        """You can add reject reasons here"""
        return {'type': 'ir.actions.act_window',
                'name': 'Loan Rejection',
                'res_model': 'reject.reason',
                'target': 'new',
                'view_mode': 'form',
                'context': {'default_loan': self.name}
                }

    def action_compute_repayment(self):
        """This automatically create the installment the employee need to pay to
        company based on payment start date and the no of installments.
            """
        self.request = True
        for loan in self:
            loan.repayment_lines_ids.unlink()
            date_start = datetime.strptime(str(loan.date), '%Y-%m-%d') + relativedelta(months=1)
            amount = loan.loan_amount / loan.tenure
            interest = loan.loan_amount * loan.interest_rate
            interest_amount = interest / loan.tenure
            total_amount = amount + interest_amount
            partner = self.partner_id
            for rand_num in range(1, loan.tenure + 1):
                self.env['repayment.line'].create({
                    'name': f"{loan.name}/{rand_num}",
                    'partner_id': partner.id,
                    'date': date_start,
                    'amount': amount,
                    'interest_amount': interest_amount,
                    'total_amount': total_amount,
                    'interest_account_id': self.env.ref('tamang_loan_management.'
                                                        'loan_management_'
                                                        'inrst_accounts').id,
                    'repayment_account_id': self.env.ref('tamang_loan_management.'
                                                         'demo_'
                                                         'loan_accounts').id,
                    'loan_id': loan.id})
                date_start += relativedelta(months=1)
        return True
