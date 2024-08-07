from odoo import http
from odoo.http import request
import base64
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class TasklyftController(http.Controller):

    @http.route('/create_gig', type='http', auth='user', website=True, csrf=True)
    def create_gig(self, **kwargs):
        if request.httprequest.method == 'POST':
            title = kwargs.get('title')
            category = kwargs.get('category')
            experience_level = kwargs.get('experience_level')
            Location = kwargs.get('Location')
            price_per_month = kwargs.get('price_per_month')
            
            picture_file = kwargs.get('picture')
            
            
            picture = base64.b64encode(picture_file.read()) if picture_file else None

            
            request.env['tasklyft.gigrequest'].sudo().create({
                'title': title,
                'category': category,
                'experience_level': experience_level,
                'Location': Location,
                'price_per_month': price_per_month,
                'picture': picture,
                'user_id': request.env.user.partner_id.id,
                'status': 'submitted',
            })
            

        return request.render('task_lyft.services_page')

class TaskLyft(http.Controller):

    @http.route(['/services'], type='http', auth='public', website=True)
    def services_page(self, **kwargs):
        domain = []

        # Get filter parameters
        category = kwargs.get('category')
        title = kwargs.get('title')
        experience_level = kwargs.get('experience_level')
        Location= kwargs.get('Location')
        price_range = kwargs.get('price_range')

        # Apply category filter
        if category:
            domain.append(('category', '=', category))

        # Apply title filter
        if title:
            domain.append(('title', 'ilike', title))

        # Apply experience level filter
        if experience_level:
            domain.append(('experience_level', '=', experience_level))

        if Location:
            domain.append(('Location', '=', Location))

        # Apply price range filter
        if price_range:
            price_min, price_max = price_range.split('-')
            if price_min:
                domain.append(('price_per_hour', '>=', float(price_min)))
            if price_max:
                domain.append(('price_per_hour', '<=', float(price_max)))

        # Fetch filtered services
        services = request.env['tasklyft.service'].sudo().search(domain)

        return request.render('task_lyft.services_page', {
            'services': services
        })

class AuthSignupCustom(AuthSignupHome):

    def get_auth_signup_qcontext(self):
        qcontext = super(AuthSignupCustom, self).get_auth_signup_qcontext()
        qcontext.update({k: v for (k, v) in request.params.items() if k in ['phone']}) 
        return qcontext

    def _prepare_signup_values(self, qcontext): 
        values = super(AuthSignupCustom, self)._prepare_signup_values(qcontext)
        values.update({'phone': qcontext.get('phone')}) 
        return values
