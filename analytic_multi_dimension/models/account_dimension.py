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

    DIMENSIONS = [('d1', '01'), ('d2', '02'), ('d3', '03'),
                  ('d4', '04'), ('d5', '05'), ('d6', '06'),
                  ('d7', '07'), ('d8', '08'), ('d9', '09'),
                  ('d10', '10'),
                  ]

    name = fields.Char(
        string='Name',
        required=True,
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

#     @api.model
#     def create(self, vals):
#         new_item = super(AccountDimensionItem, self).create(vals)
#         new_item.create_analytic_account_activity()
#         return new_item

#     @api.multi
#     def create_analytic_account_activity(self):
#         """ NOT USED !!!
#             This method create all possible comination in analytic account
#             It is not being used at the moment, and there will be too many
#             combination
#         """
#         for item in self:
#             if not item.dimension_id.activity:
#                 continue
#             dimension_groups = item.dimension_id.group_ids
#             for group in dimension_groups:
#                 comb_list = []
#                 for line in group.dimension_ids:
#                     if line.dimension_id.activity:
#                         continue
#                     comb_list.append(
#                         (line.dimension_id.code,
#                          [x.id for x in line.dimension_id.item_ids]))
#                 # Given dict, i.e., [('d2', [4, 5, 6]), ('d3', [7, 8])]
#                 # Get all possible combinations => [(4, 7), (5, 7), (6, 7)] ...
#                 dimensions, values = zip(*comb_list)   # Split into 2 list
#                 map(lambda x: x.append(False), values)
#                 combinations = list(itertools.product(*values))
#                 # Create analytic account for every possible combination
#                 for comb in combinations:
#                     vals = dict(zip(dimensions, comb))
#                     vals[item.dimension_id.code] = item.id
#                     vals['dimension_group_id'] = group.id
#                     vals['name'] = item.name
#                     self.env['account.analytic.account'].create(vals)
#         return dict
    