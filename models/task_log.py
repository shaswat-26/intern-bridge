from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TaskLog(models.Model):
    _name = 'intern.bridge.task.log'
    _description = 'Task Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Title", required=True)
    date = fields.Date(string="Date", default=fields.Date.today)
    description = fields.Text(string="Work Description")
    student_id = fields.Many2one('intern.bridge.student', string="Student", required=True)
    internship_id = fields.Many2one('intern.bridge.internship', string="Internship", required=True)
    mentor_id = fields.Many2one(
        'res.users',
        string="Mentor",
        related='internship_id.company_mentor_id',
        store=True,
        readonly=True,
        tracking=True
    )
    hours_spent = fields.Float(string="Hours Spent")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Completed'),
    ], string="Status", default='draft', tracking=True)
    mentor_comment = fields.Text(string="Mentor Comment")

    @api.model
    def create(self, vals):
        user = self.env.user
        internship = self.env['intern.bridge.internship'].browse(vals.get('internship_id'))
        if not internship.exists():
            raise ValidationError("Internship not found")
        if internship.company_mentor_id != user:
            raise ValidationError("Only the assigned mentor of this internship can create task logs.")

        student_id = vals.get('student_id')
        if not student_id or student_id not in [s.id for s in internship.student_ids]:
            raise ValidationError("Selected student is not part of this internship")

        vals['mentor_id'] = user.id
        return super().create(vals)

    def write(self, vals):
        for rec in self:
            if 'student_id' in vals:
                raise ValidationError("you can not change student.")
        return super().write(vals)

    @api.onchange()
    def _onchange_filter_internship(self):
        student = self.env['intern.bridge.student'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not student:
            return {'domain': {'internship_id': []}}
        internship = self.env['intern.bridge.internship'].search([
        ('student_ids', 'in', student.id)
        ])
        return {
            'domain': {
                'internship_id': [('id', 'in', internship.ids)]
            }        }

    def action_submit(self):
        for record in self:
            if record.student_id.user_id != self.env.user:
                raise ValidationError("Only assigned student can submit task")
            record.status = 'submitted'

    def action_assign_task(self):
        user = self.env.user
        for record in self:
            if record.internship_id.company_mentor_id != user:
                raise ValidationError("Only the assigned mentor of this internship can assign tasks.")
            record.status = 'assigned'
            record.mentor_id = user.id

    def action_mark_done(self):
        for record in self:
            record.status = 'done'

    def action_approve(self):
        for record in self:
            record.status = 'approved'

    def action_reject(self):
        for record in self:
            record.status = 'rejected'