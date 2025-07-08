# -*- coding: utf-8 -*-
{
    'name': 'Models Operation Blocker',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Block create, write, or delete operations on specific models dynamically.',
    'description': """
        Models Operation Blocker
        ========================
        
        This module allows administrators to dynamically block create, write, or delete operations 
        on any Odoo model through a configuration interface in Paramétrage.
        
        Features:
        - Block creation of products, categories, UoMs, or any model.
        - Flexible operation blocking: create, write, delete.
        - Configuration accessible via backend settings (Paramétrage).
    """,
    'author': 'Rida Louchachha',
    'maintainer': 'Rida Louchachha',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/config_view.xml',
        'data/model_block_config_data.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
