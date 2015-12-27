# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import UserError


class DimensionSelectValueReference(models.TransientModel):
    _name = "dimension.select.value.reference"
    _description = "Dimension Select Value Reference"

    @api.model
    def _get_records(self):
        active_model = self._context.get('active_model')
        active_id = self._context.get('active_id')
        if not active_model or not active_id:
            return False
        dimension_item = self.env[active_model].browse(active_id)
        model = dimension_item.dimension_id.ref_model_id
        records = []
        if model:
            res = self.env[model.model].search([])
            records = [('%s,%s' % (model.model, str(r.id)), r.name_get()[0][1])
                       for r in res]
        return records

    value_reference = fields.Selection(
        _get_records,
        string='Value Reference',
    )

    @api.multi
    def assign_value_reference(self):
        active_model = self._context.get('active_model')
        active_id = self._context.get('active_id')
        dimension_item = self.env[active_model].browse(active_id)
        dimension_item.value_reference = self.value_reference
        return {'type': 'ir.actions.act_window_close'}
