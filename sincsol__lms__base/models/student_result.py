from odoo import models, fields

class Student_Result(models.Model):
    _name = "ustadam.student_result"
    _description = "will hold student_result info"

    marks = fields.Float(string='Marks', required=True)
    
    # student_id = fields.Many2one('ustadam.user', string='Student')
    # quiz_id = fields.One2many('ustadam.quiz', 'student_result_id', string='Quiz')
