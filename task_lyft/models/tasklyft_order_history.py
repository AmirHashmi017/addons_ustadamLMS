from odoo import fields, models

class tasklyft_order_history(models.Model):
    _name = 'tasklyft.order_history'
    _description = 'TaskLyft Order History'
    
    user_id = fields.Many2one('res.partner', string='User Id')

