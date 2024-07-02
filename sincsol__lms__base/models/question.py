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
    def open_related_options(self):
        self.ensure_one()
        return {
        'type': 'ir.actions.act_window',
        'name': 'Options',
        'view_mode': 'tree',
        'res_model': 'ustadam.option',
        'domain': [('id', 'in', self.option_ids.ids)],
        'context': {'default_question_id': self.id},
        'target': 'new',
    }
    def submit_all_answers(self):
        session_key = 'quiz_answers'
        if session_key in http.request.session:
            answers = http.request.session[session_key]
            correct_answers = sum(answers.values())
            # Assuming methods to get current student and quiz IDs
            current_student_id = self._get_current_student_id()
            current_quiz_id = self._get_current_quiz_id()
            # Store the result
            self.env['ustadam.student_result'].create({
                'marks': correct_answers,
                'student_id': current_student_id,
                'quiz_id': current_quiz_id,
            })
            # Clear the session data for this quiz
            del http.request.session[session_key]
            # Add logic for redirection or response as needed