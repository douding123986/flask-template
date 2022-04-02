from wtforms import Form
from wtforms.fields import StringField, IntegerField
from wtforms.validators import Regexp, IPAddress, DataRequired, AnyOf, Optional
from . import Config


class BaseAccountForm(Form):
    place = StringField(validators=[
        DataRequired(message='The place cannot be empty'),
        AnyOf(values=Config.places(), message='The entered place is not within the specified range')
    ])
    device_name = StringField(validators=[DataRequired(message='The device name cannot be empty')])
    manage_ip = StringField(validators=[
        DataRequired(message='The manage ip cannot be empty'),
        IPAddress(message='The manage ip does not meet the specification')
    ])
    room_name = StringField(validators=[DataRequired(message='The room name cannot be empty')])
    manufacture = StringField(validators=[
        DataRequired(message='The manufacture cannot be empty'),
        AnyOf(values=Config.manufactures(), message='The entered manufacturer is not within the specified range')
    ])
    remark = StringField(validators=[Optional()])


class AddSwitchAccountForm(BaseAccountForm):
    device_type = StringField(validators=[
        DataRequired(message='The device type cannot be empty'),
        Regexp(regex=r'^Switch$', message='The device type must be Bras or Switch')
    ])
    full_name = StringField(validators=[
        DataRequired(message='The full_name cannot be empty'),
        Regexp(regex=r'^s\d-[a-z]-gdzj-[a-z]+$',
               message='The device full name does not conform to specification')
    ])
    loop_port = StringField(validators=[
        Optional(),
        Regexp(regex=r'[a-zA-Z0-9/、]+',
               message='The loop port does not conform to specification')
    ])


class AddBrasAccountFrom(BaseAccountForm):
    device_type = StringField(validators=[
        DataRequired(message='The device type cannot be empty'),
        Regexp(regex=r'^Bras$', message='The device type must be Bras')
    ])
    full_name = StringField(validators=[
        DataRequired(message='The full_name cannot be empty'),
        Regexp(regex=r'^(b\d-[a-z]-gdzj-[a-z]+|r\d-[a-z]-gdzj-[a-z]+|s\d-[a-z]-gdzj-[a-z]+)$',
               message='The device full name does not conform to specification')
    ])
    register_port = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(Eth-Trunk\d+\.\d+|smartgroup\d+\.\d+|xgei-[0-9|/|\.]+)$',
               message='The register port does not conform to specification')
    ])
    band_port = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(Eth-Trunk\d+\.\d+|smartgroup\d+\.\d+|xgei-[0-9|/|\.]+)$',
               message='The band port does not conform to specification')
    ])
    iptv_port = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(Eth-Trunk\d+\.\d+|smartgroup\d+\.\d+|xgei-[0-9|/|\.]+)$',
               message='The iptv port does not conform to specification')
    ])


class DeleteDeviceAccountForm(Form):
    device_id = IntegerField(validators=[DataRequired(message='The device id cannot be empty')])


class ModifyBrasAccountForm(AddBrasAccountFrom):
    device_id = IntegerField(validators=[DataRequired(message='The device id cannot be empty')])


class ModifySwitchAccountForm(AddSwitchAccountForm):
    device_id = IntegerField(validators=[DataRequired(message='The device id cannot be empty')])


class SearchDeviceAccountForm(Form):
    device_type = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(Bras|Switch)$', message='The device type must be Bras or Switch')
    ])
    device_name = StringField(validators=[Optional()])
    full_name = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(b\d-[a-z]-gdzj-[a-z]+|r\d-[a-z]-gdzj-[a-z]+|s\d-[a-z]-gdzj-[a-z]+)$',
               message='The device full name does not conform to specification')
    ])
    manage_ip = StringField(validators=[
        Optional(),
        IPAddress(message='The manage ip does not meet the specification')
    ])
    room_name = StringField(validators=[Optional()])
    manufacture = StringField(validators=[
        Optional(),
        AnyOf(values=Config.manufactures(), message='The entered manufacturer is not within the specified range')
    ])
    place = StringField(validators=[
        Optional(),
        AnyOf(values=Config.places(), message='The entered place is not within the specified range')
    ])
    page = IntegerField(validators=[
        Optional(),
        DataRequired(message='The number of pages must be an integer')
    ])
