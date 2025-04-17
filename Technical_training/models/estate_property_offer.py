from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class EstateOffer(models.Model):
    _name =  "estate.property.offer"
    _description = "Offerta"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accettato", "Accettato"),
            ("respinto", "Respinto"),
        ],
        copy=False,
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse = "_inverse_date_deadline")
   

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one("estate.property.type", required=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for property in self:
            property.date_deadline = fields.Date.today() + relativedelta(days=property.validity)    

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for property in self:
            property.validity = (property.date_deadline - fields.Date.today()).days

    def action_accept(self):
        self.ensure_one()
        if "accettato" in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("Error"))
        else:
            self.status= "accettato"
            self.property_id.selling_price = self.price
            

    def action_refuse(self):
        self.ensure_one()
        if self.status == "accettato":
            raise UserError(_("Error"))
        else:
            self.status="respinto" 
            self.property_id.selling_price = self.price

    _sql_constraints = [
        ("offer_price", "CHECK(price > 0)", "Offer price positive")
    ]

    @api.constrains("price")
    def _check_constrains(self):
        for offer in self:
            if offer.price < 0.9* self.property_id.expected_price:
                raise ValidationError(_("ok offer"))
            
    
    @api.model
    def create(self, vals_list):
        if self.price <= self.property_id.best_offer: 
            raise UserError(_("Esiste già un'offerta più alta"))
        else:
            res = super().create(vals_list)
            self.env['estate.property'].browse(vals_list['property_id']).state = "received"
            return res