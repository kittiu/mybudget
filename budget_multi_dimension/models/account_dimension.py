# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import itertools
from openerp import api, fields, models, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class AccountDimensionGroup(models.Model):
    _name = 'account.dimension.group'
    _description = 'Dimension Group'

    name = fields.Char(
        string='Dimension Group',
        required=True,
    )
    dimension_ids = fields.One2many(
        'account.dimension.group.line',
        'group_id',
        string='Dimensions',
    )

#     @api.one
#     @api.constrains('dimension_ids')
#     def _check_lines(self):
#         lines = self.dimension_ids.filtered(lambda r: r.activity is True)
#         if len(lines) != 1:
#             raise ValidationError(_('A group must have 1 activity dimension'))


class AccountDimensionGroupLine(models.Model):
    _name = 'account.dimension.group.line'
    _description = 'Dimension Group Lines'
    _order = 'sequence, id'

    group_id = fields.Many2one(
        'account.dimension.group',
        string='Dimension',
        ondelete='restrict',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=1,
    )
    dimension_id = fields.Many2one(
        'account.dimension',
        string='Dimension',
        required=True,
    )
#     activity = fields.Boolean(
#         related='dimension_id.activity',
#         string='Activity',
#         readonly='True',
#     )
    _sql_constraints = [
        ('dimension_uniq',
         'unique(group_id, dimension_id)',
         'Dimensions must be unique per group!'),
    ]


class AccountDimension(models.Model):
    _name = 'account.dimension'
    _description = 'Account Dimension'

    DIMENSIONS = [('d01', '01'), ('d02', '02'), ('d03', '03'),
                  ('d04', '04'), ('d05', '05'), ('d06', '06'),
                  ('d07', '07'), ('d08', '08'), ('d09', '09'),
                  ('d10', '10'),
                  ]

    name = fields.Char(
        string='Name',
        required=True,
    )
    ref_model_id = fields.Many2one(
        'ir.model',
        string='Referenced Model',
        ondelete='set null',
    )
    show_in_docline = fields.Boolean(
        string='Show in Document Line',
        default=False,
        help="Allow overwrite this Dimension in document lines, "
        "i.e., Order Lines, Invoice Lines",
    )
    code = fields.Selection(
        DIMENSIONS,
        string='Dimension',
        required=True,
    )
#     activity = fields.Boolean(
#         string='Activity',
#         default=False,
#     )
    item_ids = fields.One2many(
        'account.dimension.item',
        'dimension_id',
        string='Dimension Lines',
    )
    group_ids = fields.Many2many(
        'account.dimension.group',
        string='Used in Groups',
        compute='_compute_group_ids',
    )
    _sql_constraints = [
        ('dimension_code_uniq',
         'unique(code)',
         'Dimension ID must be unique!'),
    ]

    @api.multi
    def _compute_group_ids(self):
        for dimension in self:
            lines = self.env['account.dimension.group.line'].search(
                [('dimension_id', '=', dimension.id)])
            group_ids = [x.group_id.id for x in lines]
            dimension.group_ids = group_ids


class AccountDimensionItem(models.Model):
    _name = 'account.dimension.item'
    _description = 'Account Dimension'

    dimension_id = fields.Many2one(
        'account.dimension',
        string='Dimension',
        ondelete='restrict',
    )
    name = fields.Char(
        string='Dimension',
        required=True,
    )
    value_reference = fields.Char(
        string='Value Reference',
    )
    value = fields.Char(
        string='Value',
        compute='_compute_value',
    )

    @api.multi
    @api.depends('value_reference')
    def _compute_value(self):
        for rec in self:
            if rec.value_reference:
                model, res_id = rec.value_reference.split(',')
                rec.value = self.env[model].browse(int(res_id)).name_get()[0][1]

    @api.multi
    def remove_value_reference(self):
        for item in self:
            item.value_reference = False