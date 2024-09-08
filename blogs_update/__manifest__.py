# -*- coding: utf-8 -*-
{
    'name': "./addons_testing/blogs_update",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website_blog'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
         'views/custom_blog_templates.xml',
        #'views/custom_blog_post.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'blogs_update/static/src/js/blogs_sidebar.js',
            'blogs_update/static/src/css/blogs_sidebar.css',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

