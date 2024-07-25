from odoo import models, fields

class Live_Session_Info(models.Model):
    _name = 'live.session.info'
    _description = 'Live Sessions Information'

    meeting_type = fields.Selection([('Online', 'Online'), ('In-Person', 'In-Person')])
    meet_url = fields.Char(string='Meet URL')
    img = fields.Image(string='Image', required=True)
    lesson_name = fields.Char(string='Lesson Name', required=True)
    lesson_description = fields.Text(string='Lesson Description', required=True)
    learning_objectives = fields.Text(string='Learning Objectives')
    
    isFree = fields.Boolean(string='Is Free')
    price = fields.Float(string='Price')
    old_price = fields.Float(string='Old Price')
    number_of_participants = fields.Integer(string='Number of Participants')
    knowledge_level = fields.Selection([('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], string='Knowledge Level')
    hide_dates = fields.Boolean(string='Hide Dates')
    
    visibility = fields.Selection([('public', 'public'), ('private', 'private')], string='Visibility')

    frequency_ids = fields.One2many('live.session.frequency', 'session_id', string='FrequencyIds')
    teacher_id = fields.Many2one('res.users', string="TeacherID", required=True)   # for speaker field

    def action_view_teacher(self):
        self.ensure_one()
        if self.teacher_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Teacher Info',
                'view_mode': 'form',
                'res_model': 'res.users',
                'res_id': self.teacher_id.id,
                'target': 'new',
            }
        else:
            return {
                'type': 'ir.actions.act_window_close'
            }
    def truncate_text(self, text, word_limit):
        words = text.split()
        if len(words) > word_limit:
            return ' '.join(words[:word_limit]) + '...'
        return text

    def modal_form_coach(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Teacher Info',
            'view_mode': 'form',
            'res_model': 'res.users',
            'res_id': self.teacher_id.id,
            'target': 'new',
        }
    def action_view_session_dates(self):
        self.ensure_one()
        action = self.env.ref('your_module.action_live_session_frequency').read()[0]
        action['domain'] = [('session_id', '=', self.id)]
        return action


    