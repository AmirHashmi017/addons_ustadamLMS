from odoo import fields, models

class Answer(models.Model):
    _name = "answer"
    _description = "Will hold answer information"

    question_id = fields.Many2one('question', string="Question", required=True, ondelete='cascade')
    content = fields.Text("Content", required=True)
    is_correct = fields.Boolean("Is Correct", default=False)