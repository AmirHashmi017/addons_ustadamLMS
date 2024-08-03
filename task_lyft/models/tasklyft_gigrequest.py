from odoo import fields, models

class tasklyft_gigrequest(models.Model):
    _name = 'tasklyft.gigrequest'
    _description = 'TaskLyft Gig Request'

    title = fields.Char(string='Title', required=True)
    category = fields.Selection([
        ('Software Developer', 'Software Developer'), 
        ('Web Developer', 'Web Developer'), 
        ('Mobile App Developer', 'Mobile App Developer'), 
        ('Graphic Designer', 'Graphic Designer'), 
        ('UI/UX Designer', 'UI/UX Designer'), 
        ('Data Analyst', 'Data Analyst'), 
        ('Odoo Developer', 'Odoo Developer'), 
        ('Word-Press Developer', 'Word-Press Developer')
    ], string='Category', required=True)
    experience_level = fields.Selection([
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'), 
        ('Professional', 'Professional')
    ], string='Experience Level')
    picture = fields.Image(string='Picture', required=True)    
    price_per_hour = fields.Float(string='Price Per Hour(PKR)', required=True)
    
    user_id = fields.Many2one('res.partner', string="User")
    status = fields.Char(string="Status")

    def action_accept_request(self):
        for record in self:
            self.env['tasklyft.service'].create({
                'title': record.title,
                'category': record.category,
                'experience_level': record.experience_level,
                'picture': record.picture,
                'price_per_hour': record.price_per_hour,
                'user_id': record.user_id.id,
            })
            # Add logic to handle rejection
            record.status = 'accepted'
        
        # redirect('../')



    
    def action_reject_request(self):
        for record in self:
            # Add logic to handle rejection
            record.status = 'rejected'
