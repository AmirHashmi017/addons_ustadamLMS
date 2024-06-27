from odoo import models, fields

class Quiz(models.Model):
    _name = "ustadam.quiz"
    _description = "will hold quiz info"

    title = fields.Char(string='Title', required=True)
    description = fields.Char(string='Description', required=True)
    passingPercentage = fields.Float(string='Passing Percentage', required=True)
    
    course_id = fields.Many2one('ustadam.quiz', string='quiz_id')
    question_id = fields.One2many('ustadam.question', "question_id" ,string='Questions')