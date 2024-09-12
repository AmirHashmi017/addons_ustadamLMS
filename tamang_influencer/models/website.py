from odoo import models, _

class Website(models.Model):
    _inherit = 'website'

    def _search_get_details(self, search_type, order, options):
        result = super()._search_get_details(search_type, order, options)
        if search_type == 'followers':
            search_details = self.env['res.users']._search_get_detail(self, order, options)
            result.append(search_details)

        return result
