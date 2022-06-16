import hashlib

""" Generates an id by concatenating, normalizing and hasing """
def get_person_id(prefix:str, firstname:str, lastname:str):
    normalized = normalize(prefix + firstname + lastname)
    return hash(normalized)

""" Generates an id by concatenating, normalizing and hasing """
def get_corporate_id(prefix:str, corporation:str):
    normalized = normalize(prefix + corporation)
    return hash(normalized)

def get_trade_id(date:str, issuerid: str, personid: str):
    normalized = normalize(date + issuerid + personid)
    return hash(normalized)

def get_announcement_id(rb_id:int, state: str):
    normalized = normalize(str(rb_id) + state)
    return hash(normalized)

""" Removes special characters from a string"""
def normalize(s:str):
    s = s.lower()
    return ''.join(e for e in s if e.isalnum())

""" Hashes a string and returns it """
def hash(s: str):
    return hashlib.md5(s.encode('utf-8')).hexdigest()