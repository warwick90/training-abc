from odoo import models, fields


class Real_estate(models.Model):
    
    _name = "estate.property"
    _description = "casa_vacanza"

    active = fields.Boolean(
        string = "Active",
        default = True, 
        invisible=True
    )



    name = fields.Char(
        string = "Nome",
        default="House", 
        required=True
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Received"),
            ("accepted", "Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new"
    )
    price = fields.Float()
    postcode = fields.Char()
    description = fields.Text()
    offers = fields.tag_ids()

    def _default_date(self):
        return fields.Date.today()
    
    date = fields.Date(default=_default_date)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    garage = fields.Boolean()
    facades = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='orientation',
        selection=
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
      
    )
    property_type_id = fields.Many2one("estate.property.type")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    tag_ids = fields.Many2many("estate.property.tag")