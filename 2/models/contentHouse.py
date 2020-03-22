from marshmallow import Schema, fields

class ContentHouse(object):
    def __init__(self, _id, name, owner, phone_num, addr, house_type, house_status, gender):
        self.id = _id
        self.name = name
        self.owner = owner
        self.phone_num = phone_num
        self.addr = addr
        self.house_type = house_type
        self.house_status = house_status
        self.gender = gender

class HouseSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    owner = fields.Str()
    phone_num = fields.Str()
    addr = fields.Str()
    house_type = fields.Str()
    house_status = fields.Str()
    gender = fields.Str()
