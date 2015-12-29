# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from lxml import etree
from openerp import api, fields, models, _
from openerp.osv.orm import setup_modifiers
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class AccountBudgetPost(models.Model):
    _inherit = 'account.budget.post'

    activity_ids = fields.One2many(
        'account.activity',
        'budget_post_id',
        string='Activities',
    )

    @api.constrains('account_ids', 'activity_ids')
    def _check_account_id(self):
        account_ids = [x.account_id.id for x in self.activity_ids]
        print account_ids
        print self.account_ids.ids
        if not (set(account_ids) <= set(self.account_ids.ids)):
            raise ValidationError(_('Activity account must be within '
                                    'accounts of budgetary position'))


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    dimension_group_id = fields.Many2one(
        'account.dimension.group',
        string='Dimension Group',
    )
    # Active Flag
    d01_active = fields.Boolean(compute='_compute_dimension_active')
    d02_active = fields.Boolean(compute='_compute_dimension_active')
    d03_active = fields.Boolean(compute='_compute_dimension_active')
    d04_active = fields.Boolean(compute='_compute_dimension_active')
    d05_active = fields.Boolean(compute='_compute_dimension_active')
    d06_active = fields.Boolean(compute='_compute_dimension_active')
    d07_active = fields.Boolean(compute='_compute_dimension_active')
    d08_active = fields.Boolean(compute='_compute_dimension_active')
    d09_active = fields.Boolean(compute='_compute_dimension_active')
    d10_active = fields.Boolean(compute='_compute_dimension_active')
    # --
    d01 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 1',
        domain="[('dimension_id.code', '=', 'd01')]",
        ondelete='set null',
    )
    d02 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 2',
        domain="[('dimension_id.code', '=', 'd02')]",
        ondelete='set null',
    )
    d03 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 3',
        domain="[('dimension_id.code', '=', 'd03')]",
        ondelete='set null',
    )
    d04 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 4',
        domain="[('dimension_id.code', '=', 'd04')]",
        ondelete='set null',
    )
    d05 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 5',
        domain="[('dimension_id.code', '=', 'd05')]",
        ondelete='set null',
    )
    d06 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 6',
        domain="[('dimension_id.code', '=', 'd06')]",
        ondelete='set null',
    )
    d07 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 7',
        domain="[('dimension_id.code', '=', 'd07')]",
        ondelete='set null',
    )
    d08 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 8',
        domain="[('dimension_id.code', '=', 'd08')]",
        ondelete='set null',
    )
    d09 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 9',
        domain="[('dimension_id.code', '=', 'd09')]",
        ondelete='set null',
    )
    d10 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 10',
        domain="[('dimension_id.code', '=', 'd10')]",
        ondelete='set null',
    )
    _sql_constraints = [
        ('dimension_uniq',
         'unique(creating_user_id, d01, d02, d03, d04, d05, d06, d07, d08, d09, d10)',
         'Analytic Account Dimensions must be unique!'),
    ]

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(CrossoveredBudget, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(result['arch'])
        dimensions = [(x.code, x.name) for x in
                      self.env['account.dimension'].search([])]
        for d in dimensions:
            nodes = doc.xpath("//field[@name='%s']" % d[0])
            if nodes:
                node = nodes[0]
                node.set('string', d[1])
                setup_modifiers(node, result['fields'][d[0]])
        result['arch'] = etree.tostring(doc)
        return result

    @api.onchange('dimension_group_id')
    def onchange_dimension_group_id(self):
        for d in self.env['account.dimension'].DIMENSIONS:
            self[d[0]] = False

    @api.multi
    @api.depends('dimension_group_id')
    def _compute_dimension_active(self):
        for rec in self:
            codes = [(line.dimension_id.code, line.dimension_id.name) for
                     line in rec.dimension_group_id.dimension_ids]
            for d in self.env['account.dimension'].DIMENSIONS:
                rec[d[0] + '_active'] = False
            for d in codes:
                rec[d[0] + '_active'] = True

    @api.multi
    def budget_validate(self):
        self.crossovered_budget_line.create_analytic_account_activity()
        return super(CrossoveredBudget, self).budget_validate()


class CrossoveredBudgetLines(models.Model):
    _inherit = 'crossovered.budget.lines'

    activity_id = fields.Many2one(
        'account.activity',
        string='Activity',
        required=True,
    )

    @api.onchange('activity_id')
    def onchange_activity_id(self):
        self.general_budget_id = self.activity_id.budget_post_id

#     @api.model
#     def create(self, vals):
#         res = super(CrossoveredBudgetLines, self).create(vals)
#         res.create_analytic_account_activity()
#         return res

    @api.multi
    def create_analytic_account_activity(self):
        """ Create analytic account for those not been created """
        analytic_obj = self.env['account.analytic.account']
        dimension_obj = self.env['account.dimension']
        for line in self:
            # Populate Domain
            group_id = line.crossovered_budget_id.dimension_group_id.id
            budget_post_id = line.budget_post_id.id
            activity_id = line.activity_id.id
            domain = [('dimension_group_id', '=', group_id),
                      ('activity_id', '=', activity_id),
                      ('budget_post_id', '=', budget_post_id)]
            for d in dimension_obj.DIMENSIONS:
                domain.append((d[0], '=', line.crossovered_budget_id[d[0]].id))
            # Check existing analytic account
            analytics = self.env['account.analytic.account'].search(domain)
            # Create and assign
            if len(analytics) == 0:
                vals = dict((x[0], x[2]) for x in domain)
                vals['name'] = line.activity_id.name
                vals['activity_id'] = line.activity_id.id
                line.analytic_account_id = analytic_obj.create(vals)
            else:
                line.analytic_account_id = analytics[0].id
        return
