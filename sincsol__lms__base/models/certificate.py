from odoo import models, fields

class Certificate(models.Model):
    _name = "ustadam.certificate"
    _description = "will hold certificate info"

    certificate_name = fields.Char(string='Certificate Name', required=True)
    img = fields.Image(string='Image')
    
    course_id = fields.Many2one('ustadam.course', string='Course')