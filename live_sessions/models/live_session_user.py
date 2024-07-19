from odoo import models, fields

class Live_Session_User(models.Model):
    inherit = 'res.users'

    uid = fields.One2many('live.session.info' ,'teacher_id', string="UID")   # for speaker field
