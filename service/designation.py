from typing import List, Optional
import uuid

from model.designations import DesignationField


def all() -> List[DesignationField]:
    try:
        query = DesignationField.objects(enable=True)
        result = list(query)

        return result
    except Exception as e:
        raise Exception(str(e))

    return None


def find(public_id: str) -> DesignationField:
    try:
        item = DesignationField.objects(
            public_id=public_id, enable=True).first()

        return item
    except Exception as e:
        raise Exception(str(e))

    return None


def find_by_name(name: str) -> DesignationField:
    try:
        item = DesignationField.objects(
            name=name, enable=True).first()

        return item
    except Exception as e:
        raise Exception(str(e))

    return None


def create(name: str) -> DesignationField:
    try:
        item = DesignationField()

        item.public_id = str(uuid.uuid4())
        item.name = name
        item.save()

        return item
    except Exception as e:
        raise Exception(str(e))

    return None


def edit(public_id: str, name: str) -> DesignationField:
    try:
        item = find(public_id)

        if item:
            item.name = name
            item.save()

        return item
    except Exception as e:
        raise Exception(str(e))

    return None


def remove(public_id: str) -> DesignationField:
    try:
        item = find(public_id)

        if item:
            item.enable = False
            item.save()

        return item
    except Exception as e:
        raise Exception(str(e))

    return None
