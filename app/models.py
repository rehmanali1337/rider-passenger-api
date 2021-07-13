from pydantic import BaseModel
from typing import List, Optional


class UserRegisterModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserRegisterResponseModel(BaseModel):
    status: int
    message: str


class RidePostModel(BaseModel):
    request_text: str
    pickup_location: str
    destination_location: str
    passengers: int = 1
    packages: int = 0
    payed: bool
    pickup_time: str
    gender: str
    call: bool
    text: bool
    amount: int
    phone: int


class RideAddResponseModel(BaseModel):
    status: int
    ride_id: int
    message: str


class LoginModel(BaseModel):
    username: str
    password: str


class LoginResponseModel(BaseModel):
    status: int
    hashed_password: str


class RideReplyAddModel(BaseModel):
    ride_id: int
    reply_text: str
    amount: int


class RideReplyAddResponseModel(BaseModel):
    status: int
    message: str


class RideReplyModel(BaseModel):
    owner_email: str
    owner_name: str
    reply_text: str
    offered_amount: int


class Ride(BaseModel):
    ride_id: int
    owner_name: str
    owner_email: str
    request_text: str
    timestamp: int
    pickup_time: int
    pickup_location: str
    destination_location: str
    payed: bool
    passengers: int
    packages: int
    reply: RideReplyModel = None
    gender: str
    call: bool
    text: bool
    amount: int
    phone: int


class AllRidesModel(BaseModel):
    status: int
    rides: List[Ride]


class SingleRideResponseModel(BaseModel):
    status: int
    ride: Ride = None


class SingleRideRequestModel(BaseModel):
    ride_id: int


class GetMyRidesRequestModel(BaseModel):
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class RideDeleteRequestModel(BaseModel):
    ride_id: int


class RideDeleteResponseModel(BaseModel):
    status: int
    message: str


class OfferedRide(BaseModel):
    ride_id: int
    owner_name: str
    owner_email: str
    offer_text: str
    timestamp: int
    pickup_time: int
    pickup_location: str
    destination_location: str
    payed: bool
    passengers: int
    packages: int
    gender: str
    call: bool
    text: bool
    amount: int
    phone: int


class AllOfferedRides(BaseModel):
    status: int
    rides: List[OfferedRide]
