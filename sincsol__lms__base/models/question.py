from odoo import models, fields

class Question(models.Model):
    _name = "ustadam.question"
    _description = "will hold question info"

    content = fields.Text(string='Content', required=True)
    
    option_id = fields.One2many('ustadam.option', "option_id", string='Option')
    quiz_id = fields.Many2one('ustadam.quiz', string='Quiz')
    question_id = fields.Many2one('ustadam.quiz', string='QuestionID')