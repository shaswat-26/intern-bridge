from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class WeeklyReport(models.Model):
    _name = 'intern.bridge.weekly.report'
    _description = 'Weekly Reports'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    company_id = fields.Many2one(
        'res.partner',
        string="Company",
        related='internship_id.company_name',
        store=True,
        readonly=True,
        tracking=True
    )

    mentor_id = fields.Many2one(
        'res.users',
        string="Mentor",
        related='internship_id.company_mentor_id',
        store=True,
        readonly=True,
        tracking=True
    )

    guide_id = fields.Many2one(
        'res.users',
        string="Guide",
        related="internship_id.college_guide_id",
        store=True,
        readonly=True,
        tracking=True
    )


    start_date = fields.Date(
        related='internship_id.start_date',
        store=True,
        readonly=True
    )
    report_date = fields.Date(
        string="Report Date",
        default=fields.Date.today,
        required=True
    )
    end_date = fields.Date(
        related='internship_id.end_date',
        store=True,
        readonly=True
    )
    internship_id = fields.Many2one('intern.bridge.internship', string='Internship')
    student_id = fields.Many2one('intern.bridge.student', string='Student')
    week_number = fields.Integer(
        string="Week Number",
        compute="_compute_week_number",
        store=True
    )

    work_done = fields.Text()
    challenges = fields.Text()
    learning = fields.Text()
    hours_worked = fields.Float(
        string="Hours Worked",
        required=True
    )
    mentor_feedback = fields.Text()
    guide_feedback = fields.Text()
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('mentor_review', 'Mentor Review'),
        ('approved', 'Approved')
    ], default='draft', tracking=True)

    can_submit = fields.Boolean(string="Can Submit", compute='_compute_button_visibility')
    can_mentor_review = fields.Boolean(string="Can Mentor Review", compute='_compute_button_visibility')
    can_approve = fields.Boolean(string="Can Approve", compute='_compute_button_visibility')

    @api.depends('status')
    def _compute_button_visibility(self):
        for rec in self:
            rec.can_submit = rec.status == 'draft'
            rec.can_mentor_review = rec.status == 'submitted'
            rec.can_approve = rec.status == 'mentor_review'


    def action_print_pdf(self):
        return self.env.ref('intern_bridge.action_weekly_report_pdf').report_action(self)

    def action_submit(self):
        for rec in self:
            if rec.student_id.user_id != self.env.user:
                raise ValidationError("Only the assigned student can submit this report.")
            if rec.status != 'draft':
                raise ValidationError("Only draft reports can be submitted.")
            rec.status = 'submitted'

    def action_mentor_review(self):
        for rec in self:
            if self.env.user != rec.mentor_id:
                raise ValidationError("Only the company mentor can review this report.")
            if rec.status != 'submitted':
                raise ValidationError("Report must be submitted first.")
            rec.status = 'mentor_review'

    def action_approve(self):
        for rec in self:
            if self.env.user != rec.internship_id.college_guide_id:
                raise ValidationError("Only the college guide can approve this report.")
            if rec.status != 'mentor_review':
                raise ValidationError("Report must be reviewed by mentor first.")
            rec.status = 'approved'

    @api.onchange('internship_id')
    def _onchange_internship(self):
        if self.internship_id:
            return {
                'domain': {
                    'student_id': [('id', 'in', self.internship_id.student_ids.ids)]
                }
            }
        return {'domain': {'student_id': []}}


    @api.model
    def create(self, vals):
        if not vals.get('internship_id'):
            raise ValidationError("Internship is required.")

        internship = self.env['intern.bridge.internship'].browse(vals.get('internship_id'))

        student = self.env['intern.bridge.student'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not student:
            raise ValidationError("No student linked to current user.")
        if student not in internship.student_ids:
            raise ValidationError("Only assigned students can create reports.")
        vals['student_id'] = student.id
        record = super().create(vals)
        record._add_followers()
        return record

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        student = self.env['intern.bridge.student'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not student:
            return res
        internships = self.env['intern.bridge.internship'].search([
            ('student_ids', 'in', student.id)
        ])

        if len(internships) == 1:
            res['internship_id'] = internships.id

        return res

    @api.onchange()
    def _onchange_load_filter_internship(self):
        user = self.env.user

        student = self.env['intern.bridge.student'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not student:
            return {'domain': {'internship_id': []}}
        internships = self.env['intern.bridge.internship'].search([
        ('student_ids', 'in', student.id)
        ])

        return {
            'domain': {
                'internship_id': [('id', 'in', internships.ids)]
            }
        }

    def write(self, vals):
        for rec in self:
            if 'internship_id' in vals:
                internship = self.env['intern.bridge.internship'].browse(vals.get('internship_id'))
                student = self.env['intern.bridge.student'].search([('user_id', '=', self.env.user.id)], limit=1)
                if not student:
                    raise ValidationError("No Student linked to current user.")
                if student not in internship.student_ids:
                    raise ValidationError("You can only select your assigned internships.")

        return super().write(vals)

    @api.depends('internship_id.start_date', 'report_date')
    def _compute_week_number(self):
        for rec in self:
            if rec.internship_id and rec.internship_id.start_date:
                start = rec.internship_id.start_date

                delta = (rec.report_date - start).days

                if delta < 0:
                    rec.week_number = 1
                else:
                    rec.week_number = (delta // 7) + 1
            else:
                rec.week_number = 1

    def _add_followers(self):
        for rec in self:
            partners = []

            if rec.student_id:
                partners.append(rec.student_id.user_id.partner_id.id)

            if rec.mentor_id:
                partners.append(rec.mentor_id.partner_id.id)

            if rec.guide_id:
                partners.append(rec.guide_id.partner_id.id)

            rec.message_subscribe(partner_ids=partners)

    def message_post(self, **kwargs):
        user = self.env.user
        if user.has_group('base.group_system'):
            return super().message_post(**kwargs)
        for rec in self:
            allowed_partner_ids = set()
            student = rec.student_id
            mentor = rec.mentor_id
            guide = rec.guide_id

            if student and student.user_id == user:
                if mentor:
                    allowed_partner_ids.add(mentor.partner_id.id)
                if guide:
                    allowed_partner_ids.add(guide.partner_id.id)

            elif mentor and mentor == user:
                if student:
                    allowed_partner_ids.add(student.user_id.partner_id.id)
                if guide:
                    allowed_partner_ids.add(guide.partner_id.id)

            elif guide and guide == user:
                if student:
                    allowed_partner_ids.add(student.user_id.partner_id.id)
                if mentor:
                    allowed_partner_ids.add(mentor.partner_id.id)

            else:
                raise UserError("You are not allowed to send messages on this record.")

            allowed_partner_ids.add(user.partner_id.id)

            if 'partner_ids' in kwargs:
                for pid in kwargs['partner_ids']:
                    if pid not in allowed_partner_ids:
                        raise UserError("You can only message assigned users.")

        return super().message_post(**kwargs)

