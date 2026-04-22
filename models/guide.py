from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
import  re
class Guide(models.Model):
    _name = 'intern.bridge.guide'
    _description = 'company guide'
    _sql_constraints = [('guide_email_unique', 'unique(email)', 'Email must be unique!')]

    name = fields.Char(required=True)
    email = fields.Char(string="Email", required=True)
    user_password = fields.Char(string="Password", required=True)
    user_id = fields.Many2one('res.users', string="Login User")
    internship_ids = fields.Many2many(
        'intern.bridge.internship',
        'internship_guide_rel',
        'guide_id',
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
            raise ValidationError(_("This guide already has a user."))
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
            'groups_id': [(4, self.env.ref('intern_bridge.group_intern_bridge_guide').id)]
        })

        self.user_id = user
        return True