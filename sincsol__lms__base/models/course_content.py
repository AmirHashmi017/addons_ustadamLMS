from odoo import models, fields

class Course_Content(models.Model): 
    _name = "ustadam.course_content"
    _description = "will hold course content info"

    text = fields.Char(string='Text')
    video = fields.Char(string='Video')
    
    course_id = fields.Many2one('ustadam.course', string='Course')
    
    # course_content_id = fields.Many2one('ustadam.course', string='Course Content')