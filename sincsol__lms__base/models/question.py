from odoo import models, fields

class Question(models.Model):
    _name = "ustadam.question"
    _description = "will hold question info"

    title = fields.Char(string='Title', required=True)
    description = fields.Char(string='Description', required=True)
    passingPercentage = fields.Float(string='Passing Percentage', required=True)
    
    option_id = fields.One2many('ustadam.option', "option_id", string='Option')
    quiz_id = fields.Many2one('ustadam.quiz', string='Quiz')
    question_id = fields.Many2one('ustadam.quiz', string='QuestionID')