from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags"
    _sql_constraints = [
        ("unique_tag_name","UNIQUE(name)","Nomi tag saranno univoci")
    ]

    name = fields.Char(required=True)