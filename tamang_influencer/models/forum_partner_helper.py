from odoo import api, models
from odoo.http import request


class ForumPartnerHelper(models.AbstractModel):
    _name = 'forum.partner.helper'

    @api.model
    def get_partners_by_type(self, partner, partner_type):
        partners = []
        #  find the user id of the partner
        user = request.env['res.users'].sudo().search([('partner_id', '=', partner.id)])

        if partner_type == 'follower':
            user_forum = request.env['forum.forum'].search([('create_uid', '=', user.id)])
            temp = user_forum.sudo().message_follower_ids
            partners = list(set(follower.partner_id for follower in temp))

        elif partner_type == 'following':
            forums = request.env['forum.forum'].search([])
            partners = [
                forum.sudo().create_uid.partner_id
                for forum in forums
                if partner in forum.sudo().message_partner_ids.sudo()
            ]

        return partners, len(partners)