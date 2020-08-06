from typing import List, Optional
import datetime

from model.positions import PositionField


def all() -> List[PositionField]:
    try:
        query = PositionField.objects()
        result = list(query)

        return result
    except Exception as e:
        raise Exception(str(e))

    return None


def find(public_id: str) -> PositionField:
    try:
        item = PositionField.objects(
            public_id=public_id).first()

        return item
    except Exception as e:
        raise Exception(str(e))

    return None


def find_by_user_public_id(user_public_id: str) -> PositionField:
    try:
        item = PositionField.objects(
            user_public_id=user_public_id)

        if item.count() > 0:
            item = item[len(item) - 1]

            return item
    except Exception as e:
        raise Exception(str(e))

    return None


def create(user_public_id: str,
           section_public_id: str,
           designation_public_id: str) -> PositionField:

    try:
        item = PositionField()
        item.user_public_id = user_public_id
        item.section_public_id = section_public_id
        item.designation_public_id = designation_public_id
        item.in_date_time = datetime.datetime.utcnow()
        item.save()

        return item
    except Exception as e:
        raise Exception(__name__ + ":create:" + str(e))

    return None


def edit(public_id: str,
         user_public_id: str,
         section_public_id: str,
         designation_public_id: str) -> PositionField:

    try:
        item = item = find(public_id)

        if item:
            item.user_public_id = user_public_id
            item.section_public_id = section_public_id
            item.designation_public_id = designation_public_id
            item.save()

        return item
    except Exception as e:
        raise Exception(str(e))

    return None
