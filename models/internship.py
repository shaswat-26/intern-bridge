from odoo import models, fields, api

class Internship(models.Model):
    _name = 'intern.bridge.internship'
    _description = 'Internship'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Internship Name", required=True, tracking=True)
    student_ids = fields.Many2many(
        'intern.bridge.student',
        'internship_student_rel',
        'internship_id',
        'student_id',
        string="Students"
    )
    company_mentor_id = fields.Many2one('res.users', string='Company Mentor', tracking=True)
    college_guide_id = fields.Many2one('res.users', string='College Guide')
    company_name = fields.Many2one('res.partner', string='Company')
    start_date = fields.Date()
    end_date = fields.Date()
    status = fields.Selection([('draft', 'Draft'),('running','Running'),('completed','Completed')],default='draft')
    weekly_report_ids = fields.One2many('intern.bridge.weekly.report', 'internship_id', string='Weekly Reports')
    monthly_report_ids = fields.One2many('intern.bridge.monthly.report', 'internship_id', string='Monthly Reports')
    task_log_ids = fields.One2many('intern.bridge.task.log', 'internship_id', string='Task Logs')
    weekly_report_count = fields.Integer(compute='_compute_counts')
    monthly_report_count = fields.Integer(compute='_compute_counts')
    task_log_count = fields.Integer(compute='_compute_counts')

    @api.depends('weekly_report_ids', 'monthly_report_ids', 'task_log_ids')
    def _compute_counts(self):
        for record in self:
            record.weekly_report_count = len(record.weekly_report_ids)
            record.monthly_report_count = len(record.monthly_report_ids)
            record.task_log_count = len(record.task_log_ids)

    def _add_followers(self):
        for rec in self:
            partners = []

            for student in rec.student_ids:
                if student.user_id:
                    partners.append(student.user_id.partner_id.id)

            if rec.company_mentor_id:
                partners.append(rec.company_mentor_id.partner_id.id)

            if rec.college_guide_id:
                partners.append(rec.college_guide_id.partner_id.id)

            rec.message_subscribe(partner_ids=list(set(partners)))

    def create(self, vals):
        record = super().create(vals)
        record._add_followers()
        return record

    def write(self, vals):
        res = super().write(vals)
        self._add_followers()
        return res



