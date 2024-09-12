from odoo import fields, models


class RepaymentLine(models.Model):
    """Loan repayments """
    _name = "repayment.line"
    _description = "Repayment Line"

    name = fields.Char(string="Loan ", default="/", readonly=True,
                       help="Repayment no: of loan")
    partner_id = fields.Many2one('res.partner', string="Partner",
                                 required=True, readonly=True,
                                 help="Partner")
    company_id = fields.Many2one('res.company', string='Company',
                                 readonly=True, help="Company",
                                 default=lambda self: self.env.company)
    date = fields.Date(string="Payment Date", required=True,
                       default=fields.Date.today(),
                       readonly=True, help="Date of the payment")
    amount = fields.Float(string="Amount", required=True, help="Amount",
                          digits=(16, 2), readonly=True)
    interest_amount = fields.Float(string="Interest Amount", required=True,
                                   help="Interest Amount", digits=(16, 2), readonly=True)
    total_amount = fields.Float(string="Total Amount", required=True,
                                help="Total Amount", digits=(16, 2), readonly=True)
    loan_id = fields.Many2one('loan.request', string="Loan Ref.",
                              help="Loan", readonly=True, ondelete='cascade')
    state = fields.Selection(string="State",
                             selection=[('unpaid', 'Unpaid'),
                                        ('invoiced', 'Invoiced'),
                                        ('paid', 'Paid')], copy=False,
                             default='unpaid',
                             help="Includes paid and unpaid states for each "
                                  "repayments", )
    journal_loan_id = fields.Many2one('account.journal',
                                      string="Journal",
                                      store=True, default=lambda self: self.
                                      env['account.journal'].
                                      search([('code', 'like', 'CSH1')]),
                                      help="Journal Record")
    interest_account_id = fields.Many2one('account.account',
                                          string="Interest",
                                          store=True,
                                          help="Account For Interest")
    repayment_account_id = fields.Many2one('account.account',
                                           string="Repayment",
                                           store=True,
                                           help="Account For Repayment")
    invoice = fields.Boolean(string="invoice", default=False,
                             help="For monitoring the record")

    def action_pay_emi(self):
        """Creates invoice for each EMI"""
        time_now = self.date
        interest_product_id = self.env['ir.config_parameter'].sudo().get_param(
            'tamang_loan_management.interest_product_id')
        repayment_product_id = self.env['ir.config_parameter'].sudo().get_param(
            'tamang_loan_management.repayment_product_id')
        for rec in self:
            loan_lines_ids = self.env['repayment.line'].search(
                [('loan_id', '=', rec.loan_id.id)], order='date asc')
            for line in loan_lines_ids:
                if line.date < rec.date and line.state in \
                        ('unpaid', 'invoiced'):
                    message_id = self.env['message.popup'].create(
                        {'message': (
                            "You have pending amounts")})
                    return {
                        'name': 'Repayment',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form',
                        'res_model': 'message.popup',
                        'res_id': message_id.id,
                        'target': 'new'
                    }

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'invoice_date': time_now,
            'partner_id': self.partner_id.id,
            'currency_id': self.company_id.currency_id.id,
            'payment_reference': self.name,
            'invoice_line_ids': [
                (0, 0, {
                    'price_unit': self.amount,
                    'product_id': repayment_product_id,
                    'name': 'Repayment',
                    'account_id': self.repayment_account_id.id,
                    'quantity': 1,
                }),
                (0, 0, {
                    'price_unit': self.interest_amount,
                    'product_id': interest_product_id,
                    'name': 'Interest amount',
                    'account_id': self.interest_account_id.id,
                    'quantity': 1,
                }),
            ],
        })
        if invoice:
            invoice.action_post()
            self.invoice = True
            self.write({'state': 'invoiced'})
        return {
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
        }

    def action_view_invoice(self):
        """To view the invoices"""
        invoices = self.env['account.move'].search([
            ('payment_reference', '=', self.name)
        ])

        self.invoice = True

        if len(invoices) == 1:
            return {
                'name': 'Invoice',
                'res_model': 'account.move',
                'res_id': invoices.id,
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
            }
        elif len(invoices) > 1:
            return {
                'name': 'Invoices',
                'res_model': 'account.move',
                'domain': [('id', 'in', invoices.ids)],
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
            }
        else:
            return {
                'type': 'ir.actions.act_window_close',
            }
