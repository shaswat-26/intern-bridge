from odoo import fields, models

class InternshipDashboard(models.Model):
    _name = 'intern.bridge.dashboard'
    _description = 'Internship Dashboard'

    name = fields.Char(default="Dashboard")

    total_students = fields.Integer(compute="_compute_counts")
    total_internships = fields.Integer(compute='_compute_data')
    total_tasks = fields.Integer(compute="_compute_counts")
    total_weekly_reports = fields.Integer(compute="_compute_counts")
    total_monthly_reports = fields.Integer(compute="_compute_counts")
    total_mentors = fields.Integer(compute="_compute_counts")
    total_guides = fields.Integer(compute="_compute_counts")

    def _compute_counts(self):
        for rec in self:
            rec.total_students = self.env['intern.bridge.student'].search_count([])
            rec.total_internships = self.env['intern.bridge.internship'].search_count([])
            rec.total_tasks = self.env['intern.bridge.task.log'].search_count([])
            rec.total_weekly_reports = self.env['intern.bridge.weekly.report'].search_count([])
            rec.total_monthly_reports = self.env['intern.bridge.monthly.report'].search_count([])
            rec.total_mentors = self.env['intern.bridge.mentor'].search_count([])
            rec.total_guides = self.env['intern.bridge.guide'].search_count([])

    def action_view_students(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'intern.bridge.student',
            'view_mode': 'tree,form',
        }

    def action_view_internships(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Internships',
            'res_model': 'intern.bridge.internship',
            'view_mode': 'tree,form',
        }

    def action_view_tasks(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'res_model': 'intern.bridge.task.log',
            'view_mode': 'tree,form',
        }

    def action_view_weekly_reports(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Weekly Reports',
            'res_model': 'intern.bridge.weekly.report',
            'view_mode': 'tree,form',
        }

    def action_view_monthly_reports(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Monthly Reports',
            'res_model': 'intern.bridge.monthly.report',
            'view_mode': 'tree,form',
        }

    def action_view_mentors(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Mentors',
            'res_model': 'intern.bridge.mentor',
            'view_mode': 'tree,form',
        }

    def action_view_guides(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Guides',
            'res_model': 'intern.bridge.guide',
            'view_mode': 'tree,form',
        }