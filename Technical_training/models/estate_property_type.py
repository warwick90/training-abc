from odoo import fields, models, api, _

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "tipo"
    _order = "sequence desc"

    sequence = fields.Integer(default=1)
    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    property_count = fields.Integer(compute="_compute_property_count")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_offer_count")

    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        if "name" in vals_list:
            self.env["estate.property.tag"].create(
                {
                    "name": vals_list.get("name"),
                }
            )
        return res
    
    def unlink(self):
        self.property_ids.state = "canceled"
        return super().unlink()

    @api.depends("property_ids") 
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)


    def action_open_property_ids(self):
        return {
            "name": _("Related_Proprties"),
            "type": "ir.actions.act_window",
            "view_mode":"list,form",
            "res_model":"estate.property",
            "target":"current",
            "domain":[("property_type_id", "=", self.id)],
            "context":{"default_property_type_id": self.id}
        }
    def action_open_offer_ids(self):
        return {
            "name": _("Related Proprties offers"),
            "type": "ir.actions.act_window",
            "view_mode":"list,form",
            "res_model":"estate.property.offer",
            "target":"current",
            "domain":[("property_type_id", "=", self.id)],
            "context":{"default_property_type_id": self.id}
        }    
    
    def _offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)



    
