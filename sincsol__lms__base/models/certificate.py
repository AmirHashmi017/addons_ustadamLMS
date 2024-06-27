from odoo import models, fields

class Certificate(models.Model):
    _name = "ustadam.certificate"
    _description = "will hold certificate info"

    title = fields.Char(string='Title', required=True)