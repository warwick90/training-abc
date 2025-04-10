from odoo import fields, models

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
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)