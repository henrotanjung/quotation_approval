# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Quotation Approval',
    'version': '1.1',
    'category': 'Sales/Sales',
    'summary': 'Implement approval on quotation',
    'description': """
This module contains approval features of Sales Management.
    """,
    'images' : ['images/configuration_1.png','images/quotation_approval_image.png','images/configuration_2.png'],
    'author': 'Henro S Tanjung',
    'maintainer': 'Henro Tanjung',
    'depends': ['sale'],
    'data': [
        # 'security/sale_security.xml',
        'wizard/reject_quotation_view.xml',
        'security/ir.model.access.csv',
        'views/sale_views.xml',
        
    ],
    'demo': [
        # 'data/product_product_demo.xml',
        # 'data/sale_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
}
