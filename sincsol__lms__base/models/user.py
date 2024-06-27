from odoo import models, fields

class User(models.Model):
    _name = "ustadam.user"
    _description = "will hold user info"

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    password = fields.Char(string='Password', required=True)
    user_type = fields.Selection([('student', 'Student'), ('teacher', 'Teacher')], string='User Type')
    
    course_id = fields.One2many('ustadam.course', "course_id" ,string='Courses')  
    student_certificate_id = fields.One2many('ustadam.student_certificate', "student_certificate_id" ,string='Student Certificate')
    student_result_id = fields.One2many('ustadam.student_result', "student_result_id",string='Student Result')
