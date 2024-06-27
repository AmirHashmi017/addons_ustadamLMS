from odoo import models, fields

class Student_Certificate(models.Model):
    _name = "ustadam.student_certificate"
    _description = "will hold student certificate info"

    img = fields.Image(string='Image')
    
    student_id = fields.Many2one('ustadam.user', string='Student')
    student_certificate_id = fields.Many2one('ustadam.user', string='Certificate')