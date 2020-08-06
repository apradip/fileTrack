from typing import List, Optional
import uuid

from model.sections import SectionField


def all() -> List[SectionField]:
    try:
        query = SectionField.objects(enable=True)
        result = list(query)

        return result
    except Exception as e:
        raise Exception(str(e))

    return None


def find(public_id: str) -> SectionField:
    try:
        item = SectionField.objects(public_id=public_id, enable=True).first()

        if item:
            return item
    except Exception as e:
        raise Exception(str(e))

    return None


def find_by_name(name: str) -> SectionField:
    try:
        item = SectionField.objects(
            name=name, enable=True).first()

        if item:
            return item
    except Exception as e:
        raise Exception(str(e))

    return None


def create(name: str) -> SectionField:
    try:
        item = SectionField()
        item.public_id = str(uuid.uuid4())
        item.name = name
        item.save()

        return item
    except Exception as e:
        raise Exception(str(e))

    return None


def edit(public_id: str, name: str) -> SectionField:
    try:
        item = find(public_id)

        if item:
            item.name = name

            item.save()

        return item
    except Exception as e:
        raise Exception(str(e))

    return None


def remove(public_id: str) -> SectionField:
    try:
        item = find(public_id)

        if item:
            item.enable = False

            item.save()

        return item
    except Exception as e:
        raise Exception(str(e))

    return None
