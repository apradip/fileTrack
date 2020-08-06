from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, BooleanField, EmailField, ListField, EmbeddedDocumentField
from datetime import datetime
import re
import uuid


class NameField(StringField):
    def validate(self, value):
        if len(value) < 5:
            self.error(f"ERROR: `{value}` Is An Invalid Name.")

        if len(value) > 96:
            self.error(f"ERROR: `{value}` Is An Invalid Name.")

        super(NameField, self).validate(value)


class PhoneField(StringField):
    REGEX = re.compile(
        r"(\d{10})")

    def validate(self, value):
        if not PhoneField.REGEX.match(string=value):
            self.error(f"ERROR: `{value}` Is An Invalid Phone Number.")
        super(PhoneField, self).validate(value=value)


class UserDisplayField(EmbeddedDocument):
    name = StringField()
    phone = StringField()
    email = StringField()
    role = StringField()


class UserDetailField(EmbeddedDocument):
    public_id = StringField()
    name = StringField()
    phone = StringField()
    email = StringField()
    role = StringField()
    section_public_id = StringField()
    section = StringField()
    designation_public_id = StringField()
    designation = StringField()


class UserField(Document):
    public_id = StringField(unique=True, required=True,
                            default=str(uuid.uuid4()))
    name = NameField(required=True, max_length=160)
    phone = PhoneField()
    email = EmailField(required=True, max_length=96)
    role = StringField(required=True, max_length=24)
    password = StringField(max_length=96)
    otp = StringField(max_length=96)
    enable = BooleanField(required=True, default=True)

    meta = {
        'db_alias': 'RestAPI',
        'collection': 'users'
    }
