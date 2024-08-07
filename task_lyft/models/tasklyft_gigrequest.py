from odoo import fields, models

class tasklyft_gigrequest(models.Model):
    _name = 'tasklyft.gigrequest'
    _description = 'TaskLyft Gig Request'

    title = fields.Char(string='Title', required=True)
    category = fields.Selection([
        ('Matric', 'Matric'), 
        ('FSC(Pre Engineering)', 'FSC(Pre Engineering)'), 
        ('FSC(Pre Medical)', 'FSC(Pre Medical)'), 
        ('ICS', 'ICS'), 
        ('ICOM', 'ICOM'), 
        ('FA', 'FA'), 
        ('Pyhton', 'Pyhton'), 
        ('Web Development', 'Web Development'),
        ('C++', 'C++'),
        ('OOP and C#', 'OOP and C#'),
        ('ODOO Development', 'ODOO Development'),
        ('Graphic Designing', 'Graphic Designing'),
        ('Wordpress', 'Wordpress')
    ], string='Category', required=True)
    experience_level = fields.Selection([
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'), 
        ('Professional', 'Professional')
    ], string='Experience Level')
    Location=fields.Selection([
        ('UET Lahore','UET Lahore'),
        ('Shalamar Garden','Shalamar Garden'),
        ('Model Town','Model Town'),
        ('Gulberg','Gulberg'),
        ('Town Ship','Town Ship'),
        ('Muslim Town','Muslim Town'),
        ('Wahdat Road','Wahdat Road')
        ],string='Location',required=True)
    picture = fields.Image(string='Picture', required=True)

    price_per_month = fields.Float(string='Price Per Month(PKR)', required=True)
    
    user_id = fields.Many2one('res.partner', string="User")
    status = fields.Char(string="Status")

    def action_accept_request(self):
        for record in self:
            self.env['tasklyft.service'].create({
                'title': record.title,
                'category': record.category,
                'experience_level': record.experience_level,
                'Location': record.Location,
                'picture': record.picture,
                'price_per_month': record.price_per_month,
                'user_id': record.user_id.id,
            })
            # Add logic to handle rejection
            record.status = 'accepted'
        
        # redirect('../')



    
    def action_reject_request(self):
        for record in self:
            # Add logic to handle rejection
            record.status = 'rejected'
