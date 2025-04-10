from odoo import fields, models

class PropertyType(models.Model):
    _name="estate.property.type"
    _description="tipo"

    name = fields.Char(string="Name")

    
