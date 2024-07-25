from odoo import models, fields

class Live_Session_Coach(models.Model):
    _inherit = 'res.partner'

    qualification = fields.Selection([('Bachelors', 'Bachelors'), ('Masters', 'Masters'), ('PHD', 'PHD')])
    teaching_experience = fields.Char(string="Teaching Experience")
    resume = fields.Binary(string="Resume")
