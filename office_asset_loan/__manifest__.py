{
    'name': 'Office Asset Loan',
    'version': '19.0.1.0.0',
    'summary': 'Catat inventaris kantor dan peminjamannya',
    'category': 'Tools',
    'author': 'Sri Wulan Novera',
    'website': 'https://github.com/srinoverafict-droid/office_asset_loan',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/office_asset_loan_security.xml',
        'data/office_asset_loan_sequence.xml',
        'views/office_asset_views.xml',
        'views/office_asset_loan_views.xml',
        'views/office_asset_menus.xml',
    ],
    'demo': [
        'demo/office_asset_loan_demo.xml',
    ],
    'application': True,
    'installable': True,
}