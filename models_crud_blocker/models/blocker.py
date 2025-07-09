from odoo import _, api
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

    for model_name, actions in block_map.items():
        model_cls = env.registry.models.get(model_name)
        if not model_cls:
            continue

        def operation_message(model, action):
            return _(
                f"❌ The {action.capitalize()} operation on model '{model}' is not allowed from the Odoo interface.\n"
                "✅ If you want to allow this action, update it From the API Only."
            )

        # === CREATE ===
        if actions.get('create') and not hasattr(model_cls, '_block_create'):
            _original_methods.setdefault(model_name, {})['create'] = model_cls.create

            def make_blocked_create(model_name=model_name):
                @api.model_create_multi
                def blocked_create(self, vals_list):
                    if self.env.context.get('from_api'):
                        return _original_methods[model_name]['create'](self, vals_list)
                    raise UserError(operation_message(self._name, 'create'))
                return blocked_create

            model_cls.create = make_blocked_create()
            model_cls._block_create = True

        # === WRITE ===
        if actions.get('write') and not hasattr(model_cls, '_block_write'):
            _original_methods.setdefault(model_name, {})['write'] = model_cls.write

            def make_blocked_write(model_name=model_name):
                def blocked_write(self, vals):
                    if self.env.context.get('from_api'):
                        return _original_methods[model_name]['write'](self, vals)
                    raise UserError(operation_message(self._name, 'write'))
                return blocked_write

            model_cls.write = make_blocked_write()
            model_cls._block_write = True

        # === UNLINK ===
        if actions.get('unlink') and not hasattr(model_cls, '_block_unlink'):
            _original_methods.setdefault(model_name, {})['unlink'] = model_cls.unlink

            def make_blocked_unlink(model_name=model_name):
                def blocked_unlink(self):
                    if self.env.context.get('from_api'):
                        return _original_methods[model_name]['unlink'](self)
                    raise UserError(operation_message(self._name, 'delete'))
                return blocked_unlink

            model_cls.unlink = make_blocked_unlink()
            model_cls._block_unlink = True
