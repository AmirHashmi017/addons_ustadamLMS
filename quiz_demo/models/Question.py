from odoo import fields, models

class Question(models.Model):
    _name = "question"
    _description = "Will hold question information"

    quiz_id = fields.Many2one('quiz', string="Quiz", required=True, ondelete='cascade')
    content = fields.Text("Content", required=True)
    answer_ids = fields.One2many('answer', 'question_id', string="Answers")