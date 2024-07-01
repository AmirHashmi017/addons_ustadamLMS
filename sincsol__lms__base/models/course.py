from odoo import models, fields

class Course(models.Model):
    _name = "ustadam.course"
    _description = "will hold course info"

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description', required=True)
    img = fields.Image(string='Image')
    
    quiz_ids = fields.One2many('ustadam.quiz', 'course_id' ,string='Quiz')
    course_content_id = fields.One2many('ustadam.course_content', 'course_id' ,string='Course Content')
    user_ids = fields.Many2one('ustadam.user', string='user_id')
    student_certificate_id = fields.One2many('ustadam.certificate', "course_id" ,string='Student Certificate')
    