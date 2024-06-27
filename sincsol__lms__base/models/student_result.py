from odoo import models, fields

class Student_Result(models.Model):
    _name = "ustadam.student_result"
    _description = "will hold student_result info"

    marks = fields.Float(string='Marks', required=True)
    
    student_id = fields.Many2one('ustadam.user', string='Student')
    quiz_id = fields.Many2one('ustadam.quiz', string='Quiz')
    course_id = fields.Many2one('ustadam.course', string='Course')
    student_result_id = fields.Many2one('ustadam.user', string='Student Result')
