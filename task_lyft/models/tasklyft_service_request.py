from odoo import fields, models

class tasklyft_service_request(models.Model):
    _name = 'tasklyft.service_request'
    _description = 'TaskLyft Service Request'

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
        ('Allama Iqbal Town','Allama Iqbal Town'),
        ('Anarkali','Anarkali'),
        ('Bharia Town','Bharia Town'),
        ('Bund Road','Bund Road'),
        ('Cantt Lahore','Cantt Lahore'),
        ('Davis Road','Davis Road'),
        ('DHA Phase-1','DHA Phase-1'),
        ('DHA Phase-2','DHA Phase-2'),
        ('DHA Phase-3','DHA Phase-3'),
        ('DHA Phase-4','DHA Phase-4'),
        ('DHA Phase-5','DHA Phase-5'),
        ('DHA Phase-6','DHA Phase-6'),
        ('DHA Phase-7','DHA Phase-7'),
        ('DHA Phase-8','DHA Phase-8'),
        ('DHA Phase-9','DHA Phase-9'),
        ('Etihad Town','Etihad Town'),
        ('Faisal Town','Faisal Town'),
        ('Fateh Garh','Fateh Garh'),
        ('Ferozpur Road','Ferozpur Road'),
        ('Gulberg','Gulberg'),
        ('Gardern Town','Gardern Town'),
        ('Ghaziabad','Ghaziabad'),
        ('Harbanspura','Harbanspura'),
        ('Iqbal Town','Iqbal Town'),
        ('Johar Town','Johar Town'),
        ('Jail Road','Jail Road'),
        ('Khan Colony','Khan Colony'),
        ('Lal Pul','Lal Pul'),
        ('Lawrence Road','Lawrence Road'),
        ('Model Town','Model Town'),
        ('Muslim Town','Muslim Town'),
        ('Mall Road','Mall Road'),
        ('Mughalpura','Mughalpura'),
        ('NFC Society','NFC Society'),
        ('Nishat Colony','Nishat Colony'),
        ('Outfall Road','Outfall Road'),
        ('Peer Colony','Peer Colony'),
        ('Qaddafi Stadium','Qaddafi Stadium'),
        ('Ramgarh','Ramgarh'),
        ('Rajput Town','Rajput Town'),
        ('Revenue Society','Revenue Society'),
        ('Shalamar Garden','Shalamar Garden'),
        ('Town Ship','Town Ship'),
        ('UET Lahore','UET Lahore'),
        ('Valencia','Valencia'),
        ('Wahdat Road','Wahdat Road'),
        ('Wapda House','Wapda House'),
        ('Yasrab Colony','Yasrab Colony'),
        ('Zaman Park','Zaman Park'),
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
