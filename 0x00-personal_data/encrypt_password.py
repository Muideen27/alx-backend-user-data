#!/usr/bin/env python3
""" module for tasks 5 and 6 """
import bcrypt


def hash_password(password: str) -> bytes:
    """ method to convert plain text password to hash """
    encoded = password.encode()
    return bcrypt.hashpw(encoded, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ method that checks if a given password is valid """
    pass_encoded = password.encode()
    return bcrypt.checkpw(pass_encoded, hashed_password)
