from odoo import http
from odoo.http import request
from odoo.addons.website_profile.controllers.main import WebsiteProfile

class CustomWebsiteProfile(WebsiteProfile):

    @http.route('/profile/user/<int:user_id>', type='http', auth='public', website=True)
    def view_user_profile(self, user_id, **post):
        # Call the original method to get the initial data
        user_sudo, denial_reason = self._check_user_profile_access(user_id)
        if denial_reason:
            return request.render('website_profile.profile_access_denied', {'denial_reason': denial_reason})

        # Prepare the values using the existing method
        values = self._prepare_user_values(**post)
        params = self._prepare_user_profile_parameters(**post)
        values.update(self._prepare_user_profile_values(user_sudo, **params))

        user = values['user']

        # Get followers and following counts
        _, followers_count = request.env['forum.partner.helper'].get_partners_by_type(user.partner_id, 'follower')
        _, following_count = request.env['forum.partner.helper'].get_partners_by_type(user.partner_id, 'following')

        # Update the context with the new data
        values.update({
            'followers_count': followers_count,
            'following_count': following_count,
        })

        # Render the profile template with the updated context
        return request.render("website_profile.user_profile_main", values)