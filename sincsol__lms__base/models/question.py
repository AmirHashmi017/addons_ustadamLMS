from odoo import models, fields

class Question(models.Model):
    _name = "ustadam.question"
    _description = "will hold question info"

    name = fields.Char(string='Name', required=True)
    
    quiz_id = fields.Many2one('ustadam.quiz', string='Quiz')
    option_ids = fields.One2many('ustadam.option', "option_id", string='Option')

    # question_id = fields.Many2one('ustadam.quiz', string='QuestionID')
    def submit_answers(self):
        # Logic to process submitted answers
        for question in self:
            # Here you can access the selected options and process them
            pass
