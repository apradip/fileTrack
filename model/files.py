from mongoengine import Document, EmbeddedDocument, StringField, LongField, BooleanField, ListField, DateTimeField, EmbeddedDocumentField
from datetime import datetime
import uuid

from model.users import UserDisplayField


class NumberField(StringField):
    def validate(self, value):
        if len(value) < 5:
            self.error(f"ERROR: `{value}` Is An Invalid Name.")

        if len(value) > 100:
            self.error(f"ERROR: `{value}` Is An Invalid Name.")

        super(NumberField, self).validate(value)


class NameField(StringField):
    def validate(self, value):
        if len(value) < 5:
            self.error(f"ERROR: `{value}` Is An Invalid Name.")

        if len(value) > 164:
            self.error(f"ERROR: `{value}` Is An Invalid Name.")

        super(NameField, self).validate(value)


class LocationDisplayField(EmbeddedDocument):
    user = EmbeddedDocumentField(UserDisplayField)
    section = StringField()
    designation = StringField()
    in_date_time = DateTimeField()
    out_date_time = DateTimeField()
    processing_time = StringField()


class FileDisplayField(EmbeddedDocument):
    name = StringField()
    number = StringField()
    section = StringField()
    locations = ListField(EmbeddedDocumentField(LocationDisplayField))


class LocationField(EmbeddedDocument):
    public_id = StringField(unique=True, required=True,
                            default=str(uuid.uuid4()))
    position_public_id = StringField(required=True)
    in_date_time = DateTimeField(
        required=True, nullable=False, default=datetime.utcnow())
    out_date_time = DateTimeField(
        required=False, null=True)


class FileDetailField(EmbeddedDocument):
    public_id = StringField()
    name = StringField()
    number = StringField()
    section_public_id = StringField()
    section = StringField()


class FileField(Document):
    public_id = StringField(unique=True, required=True,
                            default=str(uuid.uuid4()))
    name = NameField(required=True)
    number = NumberField(required=True, null=False)
    section_public_id = StringField(required=True, null=False)
    locations = ListField(EmbeddedDocumentField(LocationField))
    enable = BooleanField(required=True, default=True)

    meta = {
        'db_alias': 'RestAPI',
        'collection': 'files'
    }
