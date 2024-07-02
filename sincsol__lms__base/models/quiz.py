from odoo import models, fields

class Quiz(models.Model):
    _name = "ustadam.quiz"
    _description = "will hold quiz info"

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description', required=True)
    passing_percentage = fields.Float(string='Passing Percentage', required=True)
    
    course_id = fields.Many2one('ustadam.quiz', string='quiz_ids')
    question_ids = fields.One2many('ustadam.question', "quiz_id" ,string='Questions')
    # student_result_id = fields.Many2one('ustadam.user', string='Student Result')


    
    def open_related_questions(self):
        self.ensure_one()
        return {
        'type': 'ir.actions.act_window',
        'name': 'Questions to attempt',
        'view_mode': 'tree',
        'res_model': 'ustadam.question',
        'domain': [('quiz_id', '=', self.id)],
        'context': {'default_quiz_id': self.id},
        'target': 'new',
    }

    def submit_quiz(self):
        # Logic to submit the quiz
        pass