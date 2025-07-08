# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from .blocker import patch_model_operations

class ModelBlockConfig(models.Model):
    _name = 'model.block.config'
    _description = 'Model Operation Blocking Configuration'
    _order = 'model_id'
    _rec_name = 'display_name'

    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        required=True,
        ondelete='cascade',
        help="Select the model to block operations for."
    )

    block_create = fields.Boolean(
        string='Block Create',
        help="Block creation of new records in this model."
    )
    block_write = fields.Boolean(
        string='Block Write',
        help="Block editing/updating existing records in this model."
    )
    block_unlink = fields.Boolean(
        string='Block Delete',
        help="Block deletion of records in this model."
    )

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=False
    )

    _sql_constraints = [
        (
            'unique_model_id',
            'UNIQUE(model_id)',
            _('Each model can only be configured once.')
        )
    ]

    @api.depends('model_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.model_id.name or _('Unnamed Model')

    @api.model
    def create(self, vals):
        record = super().create(vals)
        patch_model_operations(self.env)
        return record

    def write(self, vals):
        result = super().write(vals)
        patch_model_operations(self.env)
        return result

    def unlink(self):
        result = super().unlink()
        patch_model_operations(self.env)
        return result
