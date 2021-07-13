from os import replace
from pydantic.errors import UrlError
from pymongo import MongoClient
from app.vars import Rkeys, UKeys
import json
import urllib


class MongoDB:
    def __init__(self):
        config = json.load(open('./app/config.json'))
        db_username = config.get('MONGODB_USERNAME')
        db_password = config.get("MONGODB_PASSWORD")
        DB_URL = f"mongodb+srv://{urllib.parse.quote_plus(db_username)}:{urllib.parse.quote_plus(db_password)}@cluster0.2lhqy.mongodb.net/main_db?retryWrites=true&w=majority"
        self.client = MongoClient(DB_URL)

        # Uncomment below line for local development..
        # self.client = MongoClient()

        self.db = self.client.main_db
        self.users = self.db.users
        self.ride_requests = self.db.ride_requests
        self.offered_rides = self.db.offered_rides

    def add_user(self, full_name: str, email: str, password: str):
        to_add = {
            UKeys.full_name: full_name,
            UKeys.email: email,
            UKeys.password: password
        }
        self.users.insert_one(to_add)

    def get_user_with_email(self, email):
        return self.users.find_one({
            UKeys.email: email,
        })

    def remove_user_with_email(self, email):
        self.users.find_one_and_delete({
            UKeys.email: email,
        })

    def add_ride_request(self, ride_id: int,
                         request_text: str, timestamp: int, owner_name: str,
                         pickup_location: str, owner_email,
                         destination_location, payed: bool, pickup_time: int,
                         packages: int, passengers: int, gender: str, call: bool,
                         text: bool, amount: int, phone: int):
        self.ride_requests.insert_one({
            Rkeys.ride_id: ride_id,
            Rkeys.timestamp: timestamp,
            Rkeys.request_text: request_text,
            Rkeys.owner_name: owner_name,
            Rkeys.pickup_location: pickup_location,
            Rkeys.destination_location: destination_location,
            Rkeys.payed: payed,
            Rkeys.pickup_time: pickup_time,
            Rkeys.packages: packages,
            Rkeys.passengers: passengers,
            Rkeys.owner_email: owner_email,
            Rkeys.reply: None,
            Rkeys.call: call,
            Rkeys.text: text,
            Rkeys.gender: gender,
            Rkeys.amount: amount,
            Rkeys.phone: phone
        })

    def add_ride_reply(self, ride_id: int, owner_name: str, owner_email: str,
                       reply_text: str, reply_amount: int):
        self.ride_requests.find_one_and_update({Rkeys.ride_id: ride_id},
                                               {'$set': {
                                                   Rkeys.reply: {
                                                       Rkeys.owner_email: owner_email,
                                                       Rkeys.owner_name: owner_name,
                                                       Rkeys.reply_text: reply_text,
                                                       Rkeys.reply_amount: reply_amount
                                                   }
                                               }})

    def get_ride_with_id(self, ride_id):
        return self.ride_requests.find_one({
            Rkeys.ride_id: ride_id
        })

    def get_all_rides(self):
        return self.ride_requests.find({})

    def get_my_rides(self, email):
        res = self.ride_requests.find({
            Rkeys.owner_email: email,
        })
        return res

    def get_ride_by_id(self, ride_id):
        return self.ride_requests.find_one({Rkeys.ride_id: ride_id})

    def delete_ride_by_id(self, ride_id):
        return self.ride_requests.find_one_and_delete({
            Rkeys.ride_id: ride_id
        })

    def add_offered_ride(self, ride_id: int,
                         request_text: str, timestamp: int, owner_name: str,
                         pickup_location: str, owner_email,
                         destination_location, payed: bool, pickup_time: int,
                         packages: int, passengers: int, gender: str, call: bool,
                         text: bool, amount: int, phone: int):
        self.ride_requests.insert_one({
            Rkeys.ride_id: ride_id,
            Rkeys.timestamp: timestamp,
            Rkeys.request_text: request_text,
            Rkeys.owner_name: owner_name,
            Rkeys.pickup_location: pickup_location,
            Rkeys.destination_location: destination_location,
            Rkeys.payed: payed,
            Rkeys.pickup_time: pickup_time,
            Rkeys.packages: packages,
            Rkeys.passengers: passengers,
            Rkeys.owner_email: owner_email,
            Rkeys.call: call,
            Rkeys.text: text,
            Rkeys.gender: gender,
            Rkeys.amount: amount,
            Rkeys.phone: phone
        })

    def get_all_offered_rides(self):
        return self.ride_requests.find({})
