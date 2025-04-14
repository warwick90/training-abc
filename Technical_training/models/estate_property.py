from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



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
    postcode = fields.Char()
    description = fields.Text()
    best_offer = fields.Float(compute="_best_offer")
    Salesman = fields.Text()
    Buyer = fields.Text()
    def _default_date(self):
        return fields.Date.today()
    date_available = fields.Date(default = _default_date)
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
    total_area = fields.Float(compute="_compute_total_area")

    
    
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _best_offer(self):
        for record in self:
            if len(record.offer_ids) > 0:
                record.best_offer = max(record.offer_ids.mapped("price"))   
            else:
                record.best_offer = 0 

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0

    @api.onchange("date_available")       
    def onchange_date_available(self):
        for record in self:
            if (record.date_available - fields.Date.today()).days <0:
                return {
                    "Warning":{
                        "title": _("Warning"),
                        "message": _("Errore")
                    }
            }   

    def Venduto(self):
        if self.state == "sold":
            raise UserError("Già venduto") 
        else:
            self.state= "sold"

    def Cancellato(self):
        if self.state == "canceled" or self.state =="sold":
            raise UserError("Impossibile")
        else:
            self.state= "canceled"
    @api.constrains("selling_price")
    def _check_constrains(self):
        for estate in self:
            if estate.selling_price < 5000:
                raise ValidationError(_("Error selling"))      
                
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)","Positive"),
        ("selling_check_price", "CHECK(selling_price > 0)","Selling price positive" )
    ]

    
   
             
                  
        