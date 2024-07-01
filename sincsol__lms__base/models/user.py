from odoo import models, fields

class User(models.Model):
    # _inherit = "res.users"
    _name = "ustadam.user"
    _description = "will hold user info"

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    password = fields.Char(string='Password', required=True)
    user_type = fields.Selection([('student', 'Student'), ('teacher', 'Teacher')], string='User Type')
    
    course_id = fields.One2many('ustadam.course', "user_ids" ,string='Courses')  
    student_result_id = fields.One2many('ustadam.student_result', "student_id",string='Student Result')
