from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, BooleanField, EmailField, ListField, EmbeddedDocumentField
from datetime import datetime
import uuid


# class FileField(EmbeddedDocument):
#     file_public_id = StringField(required=True, nullable=False)
#     in_date_time = DateTimeField(
#         required=True, nullable=False, default=datetime.utcnow())
#     out_date_time = DateTimeField(
#         required=False, null=True)


class PositionField(Document):
    public_id = StringField(unique=True, required=True,
                            default=str(uuid.uuid4()))
    user_public_id = StringField(required=True, nullable=False)
    section_public_id = StringField(required=True, nullable=False)
    designation_public_id = StringField(required=True, nullable=False)
    in_date_time = DateTimeField(
        required=True, nullable=False, default=datetime.utcnow())
    # files = ListField(
    #     EmbeddedDocumentField(FileField))
    # enable = BooleanField(required=True, default=True)

    meta = {
        'db_alias': 'RestAPI',
        'collection': 'positions'
    }
