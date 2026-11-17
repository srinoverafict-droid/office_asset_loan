from odoo import api, fields, models


class OfficeAsset(models.Model):
    _name = 'office.asset'
    _description = 'Office Asset'
    _order = 'code'

    name = fields.Char(string='Asset Name', required=True)
    code = fields.Char(required=True)
    category = fields.Selection(
        [
            ('electronics', 'Electronics'),
            ('furniture', 'Furniture'),
            ('vehicle', 'Vehicle'),
            ('other', 'Other'),
        ],
        default='electronics',
    )
    purchase_date = fields.Date()
    condition = fields.Selection(
        [('good', 'Good'), ('fair', 'Fair'), ('damaged', 'Damaged')],
        default='good',
    )
    note = fields.Text()
    active = fields.Boolean(default=True)
    loan_ids = fields.One2many('office.asset.loan', 'asset_id', string='Loans')
    is_available = fields.Boolean(
        compute='_compute_is_available',
        search='_search_is_available',
    )
    loan_count = fields.Integer(compute='_compute_loan_count')

    _code_unique = models.Constraint(
        'UNIQUE(code)', 'Asset code must be unique!',
    )

    @api.depends('loan_ids.state')
    def _compute_is_available(self):
        for record in self:
            record.is_available = not any(
                loan.state == 'borrowed' for loan in record.loan_ids
            )

    def _search_is_available(self, operator, value):
        borrowed_ids = self.env['office.asset.loan'].search(
            [('state', '=', 'borrowed')]
        ).asset_id.ids
        positive = (operator == '=') == bool(value)
        return [('id', 'not in' if positive else 'in', borrowed_ids)]

    @api.depends('loan_ids')
    def _compute_loan_count(self):
        for record in self:
            record.loan_count = len(record.loan_ids)

    def action_view_loans(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Loans',
            'res_model': 'office.asset.loan',
            'view_mode': 'list,form',
            'domain': [('asset_id', '=', self.id)],
            'context': {'default_asset_id': self.id},
        }
