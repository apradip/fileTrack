import service.designation as Designation
import service.section as Section
import service.position as Position
from model.positions import PositionField
from model.users import UserField, UserDetailField
from typing import List, Optional
import uuid
import datetime


def all() -> List[UserDetailField]:
    try:
        output = []
        users = UserField.objects(enable=True)

        for user_item in users:
            position_item = Position.find_by_user_public_id(
                user_item.public_id)

            user = UserDetailField()
            user.public_id = user_item.public_id
            user.name = user_item.name
            user.phone = user_item.phone
            user.email = user_item.email
            user.role = user_item.role

            if position_item:
                user.section_public_id = position_item.section_public_id
                user.section = Section.find(
                    position_item.section_public_id).name
                user.designation_public_id = position_item.designation_public_id
                user.designation = Designation.find(
                    position_item.designation_public_id).name

            output.append(user)

        return output
    except Exception as e:
        raise Exception(str(e))


def find(public_id: str) -> UserDetailField:
    try:
        user = UserDetailField()
        item = UserField.objects(public_id=public_id, enable=True).first()

        if item:
            position_item = Position.find_by_user_public_id(
                item.public_id)

            user.public_id = item.public_id
            user.name = item.name
            user.phone = item.phone
            user.email = item.email
            user.role = item.role

            if position_item:
                user.section_public_id = position_item.section_public_id
                user.section = Section.find(
                    position_item.section_public_id).name
                user.designation_public_id = position_item.designation_public_id
                user.designation = Designation.find(
                    position_item.designation_public_id).name

            return user
    except Exception as e:
        raise Exception(str(e))


def find_by_phone(phone: str) -> UserDetailField:
    try:
        user = UserDetailField()

        item = UserField.objects(
            phone=phone, enable=True).first()

        if item:
            position_item = Position.find_by_user_public_id(
                item.public_id)

            user.public_id = item.public_id
            user.name = item.name
            user.phone = item.phone
            user.email = item.email
            user.role = item.role
            user.section_public_id = position_item.section_public_id
            user.section = Section.find(position_item.section_public_id).name
            user.designation_public_id = position_item.designation_public_id
            user.designation = Designation.find(
                position_item.designation_public_id).name

            return user
    except Exception as e:
        raise Exception(str(e))


def find_by_email(email: str) -> UserDetailField:
    try:
        user = UserDetailField()

        item = UserField.objects(
            email=email, enable=True).first()

        if item:
            position_item = Position.find_by_user_public_id(
                item.public_id)

            user.public_id = item.public_id
            user.name = item.name
            user.phone = item.phone
            user.email = item.email
            user.role = item.role
            user.section_public_id = position_item.section_public_id
            user.section = Section.find(position_item.section_public_id).name
            user.designation_public_id = position_item.designation_public_id
            user.designation = Designation.find(
                position_item.designation_public_id).name

            return user
    except Exception as e:
        raise Exception(str(e))


def create(name: str,
           phone: str,
           email: str,
           role: str,
           section_public_id: str,
           designation_public_id: str) -> UserDetailField:
    try:
        user = UserDetailField()
        item = UserField()
        item.public_id = str(uuid.uuid4())
        item.name = name
        item.phone = phone
        item.email = email
        item.role = role
        item.save()

        position_item = Position.create(item.public_id,
                                        section_public_id,
                                        designation_public_id)

        item.section_public_id = section_public_id
        item.section = Section.find(section_public_id).name
        item.designation_public_id = designation_public_id
        item.designation = Designation.find(designation_public_id).name

        return item
    except Exception as e:
        raise Exception(__name__ + ":create:" + str(e))


def edit(public_id: str,
         name: str,
         phone: str,
         email: str,
         role: str,
         section_public_id: str,
         designation_public_id: str) -> UserDetailField:
    try:
        user = UserDetailField()
        item = UserField.objects(public_id=public_id, enable=True).first()

        if item:
            item.name = name
            item.phone = phone
            item.email = email
            item.role = role
            item.save()

            position_item = Position.create(item.public_id,
                                            section_public_id,
                                            designation_public_id)

            user.public_id = item.public_id
            user.name = item.name
            user.phone = item.phone
            user.email = item.email
            user.role = item.role
            user.section_public_id = position_item.section_public_id
            user.section = Section.find(position_item.section_public_id).name
            user.designation_public_id = position_item.designation_public_id
            user.designation = Designation.find(
                position_item.designation_public_id).name

        return user
    except Exception as e:
        raise Exception(str(e))


def remove(public_id: str) -> UserDetailField:
    user = UserDetailField()

    try:
        item = UserField.objects(public_id=public_id, enable=True).first()

        if item:
            item.enable = False
            item.save()

            position_item = Position.find_by_user_public_id(
                item.public_id)

            user.public_id = item.public_id
            user.name = item.name
            user.phone = item.phone
            user.email = item.email
            user.role = item.role
            user.section_public_id = position_item.section_public_id
            user.section = Section.find(position_item.section_public_id).name
            user.designation_public_id = position_item.designation_public_id
            user.designation = Designation.find(
                position_item.designation_public_id).name

        return user
    except Exception as e:
        raise Exception(str(e))
