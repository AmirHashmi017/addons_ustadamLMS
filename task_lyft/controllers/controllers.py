from odoo import http
from odoo.http import request
import base64
import json
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class TasklyftController(http.Controller):

    @http.route('/create_service', type='http', auth='user', website=True, csrf=True)
    def create_service(self, **kwargs):
        # Check if the user has already created 3 services
        user_id = request.env.user.partner_id.id
        service_count = request.env['tasklyft.service'].sudo().search_count([('user_id', '=', user_id)])
        
        if service_count >= 3:
            # If the user has reached the limit, return JSON with an error message
            return request.make_response(
                json.dumps({'error': 'Service limit reached. Max 3 allowed.'}),
                headers={'Content-Type': 'application/json'}
            )

        if request.httprequest.method == 'POST':
            title = kwargs.get('title')
            category = kwargs.get('category')
            experience_level = kwargs.get('experience_level')
            location = kwargs.get('Location')
            price_per_month = kwargs.get('price_per_month')
            
            picture_file = kwargs.get('picture')
            picture = base64.b64encode(picture_file.read()) if picture_file else None
            data = {
                'title': title,
                'category': category,
                'experience_level': experience_level,
                'Location': location,
                'price_per_month': price_per_month,
                'picture': str(picture),  # Convert binary to string for logging
                'user_id': user_id,
            }
            print("Received data:", data)  # This will log the data to the server console

            # Create the service
            request.env['tasklyft.service_request'].sudo().create({
                'title': title,
                'category': category,
                'experience_level': experience_level,
                'Location': location,
                'price_per_month': price_per_month,
                'picture': picture,
                'user_id': user_id,
                'status':'submitted'
            })
            return request.make_response(
                    json.dumps({'success': 'Service Requested successfully!'}),
                    headers={'Content-Type': 'application/json'}
                )
        # Render the service creation page after service is created
        return request.redirect('services')


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
                domain.append(('price_per_month', '>=', float(price_min)))
            if price_max:
                domain.append(('price_per_month', '<=', float(price_max)))

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
