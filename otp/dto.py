from marshmallow import Schema, fields


class GeolocationSchema(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

class DeviceSchema(Schema):
    device_name = fields.Str(required=True)
    os_version = fields.Str(required=True)
    manufacturer = fields.Str(required=True)
    cpu_info = fields.Str(required=True)
    platform = fields.Str(required=True)

class RequestOtpSchema(Schema):
    phone_number = fields.Str(required=True)
    purpose = fields.Str(required=True)
    ip = fields.Str(required=True)
    package_name = fields.Str(required=True)
    geolocation = fields.Nested(GeolocationSchema, required=True)
    device = fields.Nested(DeviceSchema, required=True)

class ValidateOtpSchema(Schema):
    otp = fields.Str(required=True)
    otp_id = fields.Str(required=True)
    ip = fields.Str(required=True)
    package_name = fields.Str(required=True)
    geolocation = fields.Nested(GeolocationSchema, required=True)
    device = fields.Nested(DeviceSchema, required=True)