from odoo import models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

_original_methods = {}

def patch_model_operations(env):
    configs = env['model.block.config'].sudo().search([])

    block_map = {}
    for config in configs:
        model = config.model_id.model
        block_map.setdefault(model, {})
        if config.block_create:
            block_map[model]['create'] = True
        if config.block_write:
            block_map[model]['write'] = True
        if config.block_unlink:
            block_map[model]['unlink'] = True

    for model_name in env.registry.models:
        model_cls = env.registry.models[model_name]
        actions = block_map.get(model_name, {})

        def operation_message(model, action):
            return _(
                "❌ The %s operation on model '%s' is not allowed from the Odoo interface.\n"
                "✅ If you want to allow this action, update it in API System settings."
            ) % (action.capitalize(), model)

        # === CREATE ===
        if actions.get('create'):
            if not hasattr(model_cls, '_block_create'):
                _original_methods.setdefault(model_name, {})['create'] = model_cls.create

                def blocked_create(self, vals):
                    if not self.env.context.get('from_ui', True):  # Backend allowed
                        return _original_methods[model_name]['create'](self, vals)
                    raise UserError(operation_message(self._name, 'create'))

                model_cls.create = blocked_create
                model_cls._block_create = True

        elif hasattr(model_cls, '_block_create'):
            model_cls.create = _original_methods[model_name]['create']
            delattr(model_cls, '_block_create')

        # === WRITE ===
        if actions.get('write'):
            if not hasattr(model_cls, '_block_write'):
                _original_methods.setdefault(model_name, {})['write'] = model_cls.write

                def blocked_write(self, vals):
                    if not self.env.context.get('from_ui', True):
                        return _original_methods[model_name]['write'](self, vals)
                    raise UserError(operation_message(self._name, 'write'))

                model_cls.write = blocked_write
                model_cls._block_write = True

        elif hasattr(model_cls, '_block_write'):
            model_cls.write = _original_methods[model_name]['write']
            delattr(model_cls, '_block_write')

        # === UNLINK ===
        if actions.get('unlink'):
            if not hasattr(model_cls, '_block_unlink'):
                _original_methods.setdefault(model_name, {})['unlink'] = model_cls.unlink

                def blocked_unlink(self):
                    if not self.env.context.get('from_ui', True):
                        return _original_methods[model_name]['unlink'](self)
                    raise UserError(operation_message(self._name, 'delete'))

                model_cls.unlink = blocked_unlink
                model_cls._block_unlink = True

        elif hasattr(model_cls, '_block_unlink'):
            model_cls.unlink = _original_methods[model_name]['unlink']
            delattr(model_cls, '_block_unlink')
