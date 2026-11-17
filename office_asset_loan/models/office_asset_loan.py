from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class OfficeAssetLoan(models.Model):
    _name = 'office.asset.loan'
    _description = 'Office Asset Loan'
    _order = 'id desc'

    name = fields.Char(string='Loan Number', readonly=True, copy=False,
                       default='New')
    asset_id = fields.Many2one('office.asset', string='Asset', required=True,
                               ondelete='restrict')
    borrower_id = fields.Many2one('res.users', string='Borrower',
                                  required=True,
                                  default=lambda self: self.env.user)
    loan_date = fields.Date(required=True, default=fields.Date.context_today)
    due_date = fields.Date(required=True)
    return_date = fields.Date(readonly=True, copy=False)
    purpose = fields.Char()
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('borrowed', 'Borrowed'),
            ('returned', 'Returned'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        copy=False,
    )
    duration_days = fields.Integer(compute='_compute_duration_days')
    is_overdue = fields.Boolean(compute='_compute_is_overdue')

    @api.depends('loan_date', 'due_date')
    def _compute_duration_days(self):
        for record in self:
            if record.loan_date and record.due_date:
                record.duration_days = (record.due_date - record.loan_date).days
            else:
                record.duration_days = 0

    @api.depends('state', 'due_date')
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for record in self:
            record.is_overdue = bool(
                record.state == 'borrowed'
                and record.due_date
                and record.due_date < today
            )

    @api.constrains('loan_date', 'due_date')
    def _check_dates(self):
        for record in self:
            if (record.loan_date and record.due_date
                    and record.due_date < record.loan_date):
                raise ValidationError(
                    'Due date cannot be earlier than loan date.'
                )

    @api.onchange('loan_date')
    def _onchange_loan_date(self):
        if self.loan_date and (
            not self.due_date or self.due_date < self.loan_date
        ):
            self.due_date = self.loan_date + timedelta(days=7)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'office.asset.loan'
                ) or 'New'
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_loans(self):
        for record in self:
            if record.state in ('borrowed', 'returned'):
                raise UserError(
                    'You cannot delete a loan that is Borrowed or Returned.'
                )

    def action_borrow(self):
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft loans can be borrowed.')
            if record.asset_id.condition == 'damaged':
                raise UserError('This asset is damaged and cannot be loaned.')
            clash = self.search_count([
                ('asset_id', '=', record.asset_id.id),
                ('state', '=', 'borrowed'),
                ('id', '!=', record.id),
            ])
            if clash:
                raise UserError('This asset is currently borrowed.')
            record.state = 'borrowed'

    def action_return(self):
        for record in self:
            if record.state != 'borrowed':
                raise UserError('Only borrowed loans can be returned.')
            record.write({
                'return_date': fields.Date.context_today(record),
                'state': 'returned',
            })

    def action_cancel(self):
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft loans can be cancelled.')
            record.state = 'cancelled'
