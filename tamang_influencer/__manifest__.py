# -*- coding: utf-8 -*-
{
    'name': "Tamang Influencer",

    'summary': "Influencer Pathway customized for Tamang",

    'description': """
        influencer Pathway module customized for Tamang project
    """,

    'author': "SincSol",
    'website': "https://www.sincsol.com",
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'website_slides_forum', 'website_profile'],

    'data': [
        'security/ir.model.access.csv',
        # 'security/forum_security.xml',
        'views/views.xml',
        'views/template_extended.xml',
        'views/templates.xml',
    ],
    'license': 'LGPL-3',
}
