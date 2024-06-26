from odoo import fields, models

class Quiz(models.Model):
    _name = "quiz"
    _description = "Will hold quiz information"

    title = fields.Char("Title", required=True, translate=True)
    description = fields.Text("Description")
    passing_percentage = fields.Float("Passing Percentage", required=True)
    question_ids = fields.One2many('question', 'quiz_id', string="Questions")