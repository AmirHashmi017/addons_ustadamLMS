from odoo import models, fields

class Course(models.Model):
    _name = "ustadam.course"
    _description = "will hold course info"

    title = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description', required=True)
    img = fields.Image(string='Image')
    
    quiz_id = fields.One2many('ustadam.quiz', 'course_id' ,string='Quiz')
    course_content_id = fields.One2many('ustadam.course_content', 'course_content_id' ,string='Course Content')
    course_id = fields.Many2one('ustadam.user', string='user_id')