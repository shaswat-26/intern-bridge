from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

class Student(models.Model):
    _name = 'intern.bridge.student'
    _description = 'Student'

    _sql_constraints = [
        ('enrollment_no_unique', 'unique(enrollment_no)', 'Enrollment No must be unique!')
    ]

    name = fields.Char(required=True)
    enrollment_no = fields.Char(
        string="Enrollment No",
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )
    email = fields.Char(string="Email", required=True)
    user_password = fields.Char(string="Password", required=True)
    user_id = fields.Many2one('res.users', string="Login User")
    internship_ids = fields.Many2many(
        'intern.bridge.internship',
        'internship_student_rel',
        'student_id',
        'internship_id',
        string="Internships"
    )

    @api.constrains('email')
    def _check_email(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        for rec in self:
            if rec.email and not re.match(pattern, rec.email):
                raise ValidationError("Please enter a valid email address!")
    def action_create_user(self):
        self.ensure_one()

        if self.user_id:
            raise ValidationError(_("This student already has a user."))
        if not self.email:
            raise ValidationError(_("Please enter an email for login."))
        if not self.user_password:
            raise ValidationError(_("Please enter a password."))

        user = self.env['res.users'].sudo().create({
            'name': self.name,
            'login': self.email,
            'password': self.user_password,

            })
        user.write({
            'groups_id': [(4, self.env.ref('intern_bridge.group_intern_bridge_student').id)]
        })

        self.user_id = user
        return True

    @api.model
    def create(self, vals):
        if vals.get('enrollment_no', 'New') == 'New':
            vals['enrollment_no'] = self.env['ir.sequence'].next_by_code(
                'intern.bridge.student'
            ) or 'New'
        return super(Student, self).create(vals)