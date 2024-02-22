"""
This is not part of the CMS application, so I don't want to confuse things
by using Django's ORM or anything like that, not least because the database
in question is managed externally.
So, we'll just run some lil queries from here.
"""

from ptuweb.settings import env
from sqlalchemy import create_engine
from sqlalchemy import sql, table
from string import ascii_uppercase
from datetime import date


# noinspection PyTypeChecker
class JoinDb:
    USER = env("JOIN_DB_USER")
    PASSWORD = env("JOIN_DB_PASSWORD")
    HOST = env("JOIN_DB_HOST")
    DATABASE = env("JOIN_DB")

    connection_string = (
        f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}"
    )

    def __init__(self):
        self.engine = create_engine(self.connection_string)
        self.db = self.engine.connect()

    def create_person(self, **kwargs):
        people = table("membership.people", autoload=True)
        stm = people.insert().values(**kwargs)
        result = self.db.execute(stm)
        return result.inserted_primary_key[0]

    def create_membership(self, person_id, is_renter=True, rate=600):
        memberships = table("membership.memberships", autoload=True)

        # Generate membership number
        today = date.today()
        month_letter = ascii_uppercase[today.month - 1]
        year_hex = hex(today.year)[2:].upper()
        membership_number = month_letter + year_hex + str(person_id).rjust(5, "0")

        # Decide membership class
        m_class = "ORD"
        if not is_renter:
            m_class = "ASSOC"

        # Doing this because the database has a column 'class'
        # which is a reserved word in python, so using the string keys
        data = {
            "person_id": person_id,
            "membership_number": membership_number,
            "start_date": today,
            "payment_day": today.day,
            "class": m_class,
            "rate": rate,
        }

        stm = memberships.insert().values(**data)
        self.db.execute(stm)
        return membership_number

    def add_subscription_id(self, person_id, subscription_id):
        memberships = table("membership.memberships", autoload=True)
        stm = (
            memberships.update()
            .where(memberships.c.person_id == person_id)
            .where(memberships.c.is_active == True)
            .values(stripe_subscription_id=subscription_id)
        )
        self.db.execute(stm)

    def add_payment_method(self, person_id, payment_method_id):
        memberships = table("membership.memberships", autoload=True)
        stm = (
            memberships.update()
            .where(memberships.c.person_id == person_id)
            .where(memberships.c.is_active == True)
            .values(stripe_payment_method_id=payment_method_id)
        )
        self.db.execute(stm)

    def add_address(self, person_id, uprn=None, **kwargs):
        addresses = table("memberships.addresses", autoload=True)
        addr_base = table("geodata.delivery_addresses", autoload=True)

        address = {}

        if "street" in kwargs and "postcode" in kwargs:
            address["street"] = kwargs["street"]
            address["postcode"] = kwargs["postcode"]

        if "line_1" in kwargs:
            address["line_1"] = kwargs["line_1"]
        if "line_2" in kwargs:
            address["line_2"] = kwargs["line_2"]
        if "district" in kwargs:
            address["district"] = kwargs["district"]
        if "town" in kwargs:
            address["town"] = kwargs["town"]

        if uprn:
            addr_stm = addr_base.select().where(addr_base.c.uprn == uprn)
            addr = self.db.execute(addr_stm).one_or_none()
            if not addr:
                raise Exception("Address not found")

            address = {
                "uprn": addr.uprn,
                "line_1": addr.sao,
                "line_2": addr.pao,
                "street": addr.street,
                "district": addr.locality,
                "town": addr.town_name,
                "postcode": addr.postcode
            }

        # Insert address
        stm = addresses.insert().values(
            person_id=person_id,
            type="HOME",
            **address
        )
        self.db.execute(stm)





