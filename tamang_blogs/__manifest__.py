{
    'name': 'Tamang Blogs Update',
    'version': '17.0.1.0.0',

    'summary': 'Helps You To Manage Loan Requests/Disbursement/Repayments/Amortization Operations',
    'description': """
        This module allows you to create different types of loans,
        manage loan requests and amortization operations simply,
        and create invoices for each repayment amount.
    """,

    'author': 'SincSol',
    'depends': ['website_blog'],

    'data': [
         'views/custom_blog_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'tamang_blogs/static/src/js/blogs_sidebar.js',
            'tamang_blogs/static/src/css/blogs_sidebar.css',
        ],
    },
}
