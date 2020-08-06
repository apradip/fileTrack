from typing import List, Optional
from werkzeug.security import (generate_password_hash, check_password_hash)
import datetime
import os

from model.users import UserField


def find(public_id: str) -> UserField:
    try:
        item = UserField.objects(
            public_id=public_id, enable=True).first()

        return item
    except Exception as e:
        raise Exception(str(e))


def find_by_phone(phone: str) -> UserField:
    try:
        item = UserField.objects(
            phone=phone, enable=True).first()

        return item
    except Exception as e:
        raise Exception(str(e))


def find_by_email(email: str) -> UserField:
    try:
        item = UserField.objects(
            email=email, enable=True).first()

        return item
    except Exception as e:
        raise Exception(str(e))


def find_by_otp(otp: str) -> UserField:
    try:
        item = UserField.objects(
            otp=otp, enable=True).first()

        return item
    except Exception as e:
        raise Exception(str(e))


def login(user_name: str, password: str) -> UserField:
    try:
        item = find_by_phone(user_name)

        if not item:
            item = find_by_email(user_name)

            if not item:
                return

        if not item.password:
            if not item.otp:
                return

            if not check_password_hash(item.otp, password):
                return
        else:
            if not check_password_hash(item.password, password):
                if not item.otp:
                    return

                if not check_password_hash(item.otp, password):
                    return

        if item:
            return item
    except Exception as e:
        raise Exception(str(e))


def update_otp(user_name: str, otp: str) -> UserField:
    try:
        item = find_by_phone(user_name)

        if not item:
            item = find_by_email(user_name)

            if not item:
                return None

        item.otp = generate_password_hash(otp, method='sha256')
        item.save()

        return item
    except Exception as e:
        raise Exception(str(e))


def update_password(public_id: str, password: str, password_new: str) -> bool:
    try:
        item = find(public_id)

        if not item:
            return False

        if not item.password:
            if not check_password_hash(item.otp, password):
                return False
        else:
            if not check_password_hash(item.password, password):
                if not check_password_hash(item.otp, password):
                    return False

        item.password = generate_password_hash(password_new, method='sha256')
        item.otp = None
        item.save()

        return True
    except Exception as e:
        raise Exception(str(e))


def logout(public_id: str) -> bool:
    try:
        item = find(public_id)

        if not item:
            return False

        item.otp = None
        item.save()

        return True
    except Exception as e:
        raise Exception(str(e))
