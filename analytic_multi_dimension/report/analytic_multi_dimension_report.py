# -*- coding: utf-8 -*-

from openerp import tools
from openerp import models, fields, api


class AnalyticReport(models.Model):
    _name = "analytic.multi.dimension.report"
    _description = "Analytic Multi Dimension Report"
    _auto = False
    _order = 'code, name asc'

    @api.multi
    def _compute_debit_credit_balance(self):
        print 'XXXXXXXXXXXXXx'
        analytic_line_obj = self.env['account.analytic.line']
        domain = [('account_id', 'in', self.mapped('id'))]
        if self._context.get('from_date', False):
            domain.append(('date', '>=', self._context['from_date']))
        if self._context.get('to_date', False):
            domain.append(('date', '<=', self._context['to_date']))
        print 'XXXXXXXXXXXXXYYYy'
        print domain
        account_amounts = analytic_line_obj.search_read(domain, ['account_id', 'amount'])
        account_ids = set([line['account_id'][0] for line in account_amounts])
        data_debit = {account_id: 0.0 for account_id in account_ids}
        data_credit = {account_id: 0.0 for account_id in account_ids}
        for account_amount in account_amounts:
            if account_amount['amount'] < 0.0:
                data_debit[account_amount['account_id'][0]] += account_amount['amount']
            else:
                data_credit[account_amount['account_id'][0]] += account_amount['amount']

        for account in self:
            account.debit = abs(data_debit.get(account.id, 0.0))
            account.credit = data_credit.get(account.id, 0.0)
            account.balance = account.credit - account.debit

    d1 = fields.Many2one('account.analytic.account', string='D1')
    d2 = fields.Many2one('account.analytic.account', string='D2')
    d3 = fields.Many2one('account.analytic.account', string='D3')
    d4 = fields.Many2one('account.analytic.account', string='D4')
    d5 = fields.Many2one('account.analytic.account', string='D5')
    name = fields.Char(string='Analytic Account')
    code = fields.Char(string='Reference')
    account_type = fields.Selection([('normal', 'Normal'), ('view', 'View')], string='Type of Account')
    company_id = fields.Many2one('res.company', string='Company')
    partner_id = fields.Many2one('res.partner', string='Customer')
    balance = fields.Monetary(compute='_compute_debit_credit_balance', string='Balance')
    debit = fields.Monetary(compute='_compute_debit_credit_balance', string='Debit')
    credit = fields.Monetary(compute='_compute_debit_credit_balance', string='Credit')
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency", readonly=True)

    def init(self, cr):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            select a.id, d1, d2, d3, d4, d5,
            a.parent_id, a.name, a.code, a.account_type, a.company_id, a.partner_id
            from account_analytic_account a
            join 
                -- DIMENSIONS --
                (SELECT id, a[1]::int d1, a[2]::int d2, a[3]::int d3, a[4]::int d4, a[5]::int d5 FROM
                (SELECT id, (select a from (select regexp_split_to_array(path, ',')) as dt(a)) from
                (
                WITH RECURSIVE nodes_cte(id, path) AS (
                 SELECT tn.id, tn.id::text AS path FROM account_analytic_account AS tn WHERE tn.parent_id IS NULL
                UNION ALL
                 SELECT c.id, (p.path || ',' || c.id::text) FROM nodes_cte AS p, account_analytic_account AS c WHERE c.parent_id = p.id
                )
                SELECT * FROM nodes_cte AS n ORDER BY n.id ASC
                ) a) b) d
                -- END --
            on a.id = d.id            
        )""" % (self._table, ))
