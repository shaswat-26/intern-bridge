import calendar
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MonthlyReport(models.Model):
    _name = 'intern.bridge.monthly.report'
    _description = 'Monthly Reports'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    internship_id = fields.Many2one('intern.bridge.internship', string='Internship')
    student_id = fields.Many2one(
        'intern.bridge.student',
        store=True,
        readonly=True,
        string='Student'
    )

    start_date = fields.Date(string='Start Date',
                                 related='internship_id.start_date',
                                 readonly=True)

    end_date = fields.Date(string='End Date',
                               related='internship_id.end_date',
                               readonly=True)
    report_month = fields.Date(string='Report Month', default=fields.Date.today())
    mentor_id = fields.Many2one(
                                'res.users',
                                string='Mentor',
                                related='internship_id.company_mentor_id',
                                store=True,
                                readonly=True,
                                tracking=True
    )
    guide_id = fields.Many2one('res.users',
                                string='Guide',
                                related='internship_id.college_guide_id',
                                store=True,
                                readonly=True,
                                tracking=True
    )
    weekly_count = fields.Integer(string='Number of Weekly Reports',
                                  compute='_compute_weekly_count',
                                  store=True,
                                  tracking=True)

    total_hours = fields.Float( string="Total Hours Worked",
                                compute='_compute_monthly_summary',
                                store=True,
                                tracking=True
    )
    completed_task = fields.Integer(string='Completed Task',
                                    compute='_compute_monthly_summary',
                                    store=True,
                                    tracking=True)
    pending_task = fields.Integer(string='Pending Task',
                                  compute='_compute_monthly_summary',
                                  store=True,
                                  tracking=True)
    month = fields.Char(string='Month')
    summary = fields.Text()
    progress_percentage = fields.Float(compute="_compute_progress_percentage", store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('mentor_approved', 'Mentor Approved'),
        ('guide_approved', 'Guide Approved')
    ], default='draft', tracking=True)
    remarks = fields.Text()

    can_submit = fields.Boolean(compute="_compute_button_visibility", store=True)
    can_mentor_approve = fields.Boolean(compute="_compute_button_visibility", store=True)
    can_guide_approve = fields.Boolean(compute="_compute_button_visibility", store=True)
    @api.depends()
    def _compute_progress_percentage(self):
        for rec in self:
            user = self.env.user
            
    @api.depends('state', 'mentor_id', 'guide_id', 'student_id.user_id')
    def _compute_button_visibility(self):
        for rec in self:
            user = self.env.user

            rec.can_submit = (
                    rec.state == 'draft' and
                    rec.student_id.user_id == user
            )

            rec.can_mentor_approve = (
                    rec.state == 'submitted' and
                    rec.mentor_id.id == user.id
            )

            rec.can_guide_approve = (
                    rec.state == 'mentor_approved' and
                    rec.guide_id.id == user.id
            )


    @api.depends('internship_id', 'report_month', 'internship_id.weekly_report_ids.hours_worked',
    'internship_id.weekly_report_ids.status')
    def _compute_weekly_count(self):
        for rec in self:
            if not rec.internship_id or not rec.report_month:
                rec.weekly_count = 0
                continue
            month_start=rec.report_month.replace(day=1)
            last_day = calendar.monthrange(rec.report_month.year,rec.report_month.month)[1]
            month_end=rec.report_month.replace(day=last_day)

            weekly_reports = self.env['intern.bridge.weekly.report'].search([
                ('internship_id', '=', rec.internship_id.id),
                ('student_id', '=', rec.student_id.id),
                ('report_date', '>=', month_start),
                ('report_date', '<=', month_end),
            ])
            rec.weekly_count = len(weekly_reports)

    @api.depends('internship_id', 'report_month', 'internship_id.weekly_report_ids')
    def _compute_monthly_summary(self):
        for rec in self:
            rec.total_hours = 0
            rec.completed_task = 0
            rec.pending_task = 0

            if not rec.internship_id or not rec.report_month:
                continue
            month_start = rec.report_month.replace(day=1)
            last_day = calendar.monthrange(rec.report_month.year, rec.report_month.month)[1]
            month_end = rec.report_month.replace(day=last_day)
            weekly_reports = self.env['intern.bridge.weekly.report'].search([
                ('internship_id', '=', rec.internship_id.id),
                ('report_date', '>=', month_start),
                ('report_date', '<=', month_end)
            ])
            rec.total_hours = sum(w.hours_worked for w in weekly_reports if w.hours_worked)
            rec.completed_task = len(weekly_reports.filtered(lambda w: w.status == 'approved'))
            rec.pending_task = len(weekly_reports.filtered(lambda w: w.status != 'approved'))

    @api.model
    def create(self, vals):
        if not vals.get('student_id'):
            student = self.env['intern.bridge.student'].search([
                ('user_id', '=', self.env.user.id)
            ], limit=1)

            if not student:
                raise ValidationError("No student linked to current user.")

            vals['student_id'] = student.id

        return super().create(vals)

    def action_submit(self):
        for rec in self:
            if rec.student_id.user_id != self.env.user:
                raise ValidationError("Only student can submit.")
            rec.state = 'submitted'

    def action_mentor_approve(self):
        for rec in self:
            if self.env.user != rec.mentor_id:
                raise ValidationError("Only mentor can approve.")
            if rec.state != 'submitted':
                raise ValidationError("Must be submitted first.")
            rec.state = 'mentor_approved'

    def action_guide_approve(self):
        for rec in self:
            if self.env.user != rec.guide_id:
                raise ValidationError("Only guide can approve.")
            if rec.state != 'mentor_approved':
                raise ValidationError("Mentor must approve first.")
            rec.state = 'guide_approved'

    @api.depends('internship_id', 'student_id', 'report_month')
    def _compute_progress_percentage(self):
        for rec in self:
            if not rec.internship_id or not rec.student_id or not rec.report_month:
                rec.progress_percentage = 0
                continue
            month_start = rec.report_month.replace(day=1)
            last_day = calendar.monthrange(rec.report_month.year, rec.report_month.month)[1]
            month_end = rec.report_month.replace(day=last_day)
            reports = self.env['intern.bridge.weekly.report'].search([
                ('internship_id', '=', rec.internship_id.id),
                ('student_id', '=', rec.student_id.id),
                ('report_date', '>=', month_start),
                ('report_date', '<=', month_end),
            ])
            unique_weeks = set(reports.mapped('week_number'))
            submitted_weeks = len(unique_weeks)
            total_weeks = len(calendar.monthcalendar(
                rec.report_month.year,
                rec.report_month.month
            ))
            if total_weeks == 0:
                rec.progress_percentage = 0
                continue
            progress = (submitted_weeks / total_weeks) * 100
            rec.progress_percentage = min(progress, 100)