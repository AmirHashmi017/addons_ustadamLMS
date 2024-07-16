# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class addons_uteach/live_sessions(models.Model):
#     _name = 'addons_uteach/live_sessions.addons_uteach/live_sessions'
#     _description = 'addons_uteach/live_sessions.addons_uteach/live_sessions'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

