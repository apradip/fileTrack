from mongoengine import Document, StringField, BooleanField
import uuid


class NameField(StringField):
    def validate(self, value):
        if len(value) < 3:
            self.error(f"ERROR: `{value}` Is An Invalid Name.")

        if len(value) > 96:
            self.error(f"ERROR: `{value}` Is An Invalid Name.")

        super(NameField, self).validate(value)


class SectionField(Document):
    public_id = StringField(unique=True, required=True,
                            nullable=False, default=str(uuid.uuid4()))
    name = NameField(required=True, nullable=False)
    enable = BooleanField(required=True, nullable=False, default=True)

    meta = {
        'db_alias': 'RestAPI',
        'collection': 'sections'
    }
