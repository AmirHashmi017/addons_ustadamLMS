from odoo import models, fields


class ForumNotification(models.Model):
    _name = 'forum.notification'
    _description = 'Forum Notification'

    user_id = fields.Many2one('res.users', string="User")
    post_id = fields.Many2one('forum.post', string="Post")
    message = fields.Char(string="Message")
    is_read = fields.Boolean(string="Read", default=False)
    create_datetime = fields.Datetime(string="Time", default=fields.Datetime.now)

    def get_user_notifications(self):
        return self.search([('user_id', '=', self.env.user.id)], order='create_datetime desc')

    def get_notification_count(self):
        return self.search_count([('user_id', '=', self.env.user.id), ('is_read', '=', False)]) or 0
