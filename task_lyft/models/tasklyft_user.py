from odoo import fields, models

class tasklyft_user(models.Model):
    _inherit = 'res.partner'
    

    service_id = fields.One2many('tasklyft.service', 'user_id', string='Service Id')
    order_history_id = fields.One2many('tasklyft.order_history', 'user_id', string='Order History Id')
