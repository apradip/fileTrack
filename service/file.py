from typing import List, Optional
import datetime
import uuid

from model.files import (FileField, LocationField, FileDisplayField,
                         LocationDisplayField, UserDisplayField, FileDetailField)

import service.user as User
import service.section as Section
import service.designation as Designation
import service.position as Position


def all() -> List[FileDetailField]:
    try:
        output = []
        files = FileField.objects(enable=True)

        for file_item in files:
            file = FileDetailField()
            file.public_id = file_item.public_id
            file.name = file_item.name
            file.number = file_item.number
            file.section_public_id = file_item.section_public_id

            section_item = Section.find(file_item.section_public_id)
            if section_item:
                file.section = section_item.name

            output.append(file)

        return output
    except Exception as e:
        raise Exception(str(e))

    return None


def find(public_id: str) -> FileDetailField:
    try:
        item = FileField.objects(public_id=public_id, enable=True).first()

        if item:

            file = FileDetailField()
            file.public_id = item.public_id
            file.name = item.name
            file.number = item.number
            file.section_public_id = item.section_public_id

            section_item = Section.find(item.section_public_id)
            if section_item:
                file.section = section_item.name

            return file
    except Exception as e:
        raise Exception(str(e))

    return None


def find_by_number(number: str) -> FileDetailField:
    try:
        file = FileDetailField()

        item = FileField.objects(
            number=number,
            enable=True).first()

        if item:
            file.public_id = item.public_id
            file.name = item.name
            file.number = item.number
            file.section_public_id = item.section_public_id

            section_item = Section.find(item.section_public_id)
            if section_item:
                file.section = section_item.name

            return file
    except Exception as e:
        raise Exception(str(e))

    return None


def create(name: str,
           number: str,
           section_public_id: str,
           user_public_id: str) -> FileDetailField:

    try:
        file = FileDetailField()
        position_item = Position.find_by_user_public_id(user_public_id)

        location = LocationField()
        location.public_id = str(uuid.uuid4())
        location.position_public_id = position_item.public_id
        location.in_date_time = datetime.datetime.utcnow()

        item = FileField()
        item.public_id = str(uuid.uuid4())
        item.name = name
        item.number = number
        item.section_public_id = section_public_id
        item.locations.append(location)
        item.save()

        file.public_id = item.public_id
        file.name = item.name
        file.number = item.number
        file.section_public_id = item.section_public_id
        file.section = Section.find(item.section_public_id).name

        return file
    except Exception as e:
        raise Exception(str(e))

    return None


def edit(public_id: str,
         name: str,
         number: str,
         section_public_id: str) -> FileDetailField:

    try:
        file = FileDetailField()
        item = FileField.objects(public_id=public_id, enable=True).first()

        if item:
            print(item.name)
            item.name = name
            item.number = number
            item.section_public_id = section_public_id
            item.save()

            file.public_id = item.public_id
            file.name = item.name
            file.number = item.number
            file.section_public_id = item.section_public_id

            section_item = Section.find(item.section_public_id)
            if section_item:
                file.section = section_item.name

            return file
    except Exception as e:
        raise Exception(str(e))

    return None


def remove(public_id: str) -> FileDetailField:
    try:
        file = FileDetailField()
        item = FileField.objects(public_id=public_id, enable=True).first()

        if item:
            item.enable = False
            item.save()

            file.public_id = item.public_id
            file.name = item.name
            file.number = item.number
            file.section_public_id = item.section_public_id

            section_item = Section.find(item.section_public_id)
            if section_item:
                file.section = section_item.name

            return file
    except Exception as e:
        raise Exception(str(e))

    return None


def get_all_location(number: str) -> FileDisplayField:
    try:
        output = FileDisplayField()

        found_file = FileField.objects(
            number=number,
            enable=True).first()

        if not found_file:
            return None

        output.name = found_file.name
        output.number = found_file.number
        output.section = Section.find(found_file.section_public_id).name

        for location_item in found_file.locations:
            location = LocationField()

            location.in_date_time = location_item.in_date_time
            location.out_date_time = location_item.out_date_time

            if location_item.out_date_time:
                time_lag = location_item.out_date_time - location_item.in_date_time
                processing_time = datetime.timedelta(
                    microseconds=time_lag.microseconds)
            else:
                time_lag = datetime.datetime.now() - location_item.in_date_time
                processing_time = datetime.timedelta(
                    microseconds=time_lag.microseconds)

            location.processing_time = processing_time

            found_position = Position.find(location_item.position_public_id)

            if found_position:
                found_user = User.find(found_position.user_public_id)

                if found_user:
                    user = UserDisplayField()
                    user.name = found_user.name
                    user.phone = found_user.phone
                    user.email = found_user.email

                location.user = user

                location.user.section = Section.find(
                    found_position.section_public_id).name

                location.user.designation = Designation.find(
                    found_position.designation_public_id).name

            output.locations.append(location)
        return output
    except Exception as e:
        raise Exception(str(e))

    return None


def update_in(file_public_id: str, user_public_id: str) -> bool:
    found = False

    try:
        item = FileField.objects(
            public_id=file_public_id, enable=True).first()

        if item:
            found = True

            user_last_position = Position.find_by_user_public_id(
                user_public_id)

            location = LocationField()
            location.position_public_id = user_last_position.public_id
            item.locations.append(location)
            item.save()

            # # TODO save file to user document
            # item_user = User.find(user.public_id)

            # if item_user:
            #     file_detail = UserFile()
            #     file_detail.public_id = public_id

            #     file_item = UserFileDetail()
            #     file_item.file_detail = file_detail
            #     file_item.in_date_time = datetime.datetime.utcnow()

            #     item_user.file_handel_list.append(file_item)

            #     item_user.save()
    except Exception as e:
        raise Exception(str(e))

    return found


def update_out(file_public_id: str, user_public_id: str) -> bool:
    found = False

    try:
        user_last_position = Position.find_by_user_public_id(user_public_id)
        item = FileField.objects(public_id=file_public_id, enable=True).first()

        if item:
            for location_item in item.locations:
                if not location_item.out_date_time:
                    if location_item.position_public_id == user_last_position.public_id:
                        found = True
                        location_item.out_date_time = datetime.datetime.utcnow()
                        item.save()

            # # TODO save file to user document
            # item_user = User.find(user.public_id)

            # if item_user:
            #     for file_item in item_user.file_handel_list:
            #         if not file_item.out_date_time:
            #             if file_item.file_detail.public_id == public_id:
            #                 file_item.out_date_time = datetime.datetime.utcnow()

            #                 item_user.save()
    except Exception as e:
        raise Exception(str(e))

    return found
