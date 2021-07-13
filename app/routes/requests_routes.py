from pymongo import message
from starlette.types import Message
from app.vars import Rkeys, UKeys
from fastapi import APIRouter, Depends
from app.models import *
from app.utils import *
from app.db import MongoDB
from app.authentication import get_current_user
from fastapi import status, HTTPException

router = APIRouter(tags=["Rides"])
db = MongoDB()


@router.post("/add_ride", summary="Add new ride to the Database", response_model=RideAddResponseModel)
async def add_new_ride(request: RidePostModel, user: dict = Depends(get_current_user)):
    ride_id = get_new_ride_id()
    pickup_time = string_to_timestamp(request.pickup_time)
    db.add_ride_request(ride_id=ride_id,
                        timestamp=get_timestamp(),
                        request_text=request.request_text,
                        owner_name=user[UKeys.full_name],
                        owner_email=user[UKeys.email],
                        pickup_location=request.pickup_location,
                        destination_location=request.destination_location,
                        payed=request.payed,
                        pickup_time=pickup_time,
                        passengers=request.passengers,
                        packages=request.packages,
                        gender=request.gender,
                        call=request.call,
                        text=request.text,
                        amount=request.amount,
                        phone=request.phone
                        )
    return RideAddResponseModel(status=status.HTTP_200_OK, ride_id=ride_id, message="success")


@router.post("/add_ride_reply", response_model=RideReplyAddResponseModel, summary="Add reply to ride")
async def add_reply_to_ride(ride: RideReplyAddModel, user: dict = Depends(get_current_user)):
    db.add_ride_reply(owner_name=user[UKeys.full_name], owner_email=user[UKeys.email],
                      reply_text=ride.reply_text, ride_id=ride.ride_id, reply_amount=ride.amount)
    return RideReplyAddResponseModel(status=status.HTTP_200_OK, message="success")


@ router.get("/get_all_rides", response_model=AllRidesModel)
async def get_all_rides(user: dict = Depends(get_current_user)):
    rides = db.get_all_rides()
    rides_models = list()
    for ride in rides:
        if ride[Rkeys.reply]:
            reply = RideReplyModel(owner_name=ride[Rkeys.reply][Rkeys.owner_name],
                                   owner_email=ride[Rkeys.reply][Rkeys.owner_email],
                                   reply_text=ride[Rkeys.reply][Rkeys.reply_text],
                                   offered_amount=ride[Rkeys.reply][Rkeys.reply_amount])
        else:
            reply = None
        rides_models.append(Ride(ride_id=ride[Rkeys.ride_id],
                                 owner_email=ride[Rkeys.owner_email],
                                 owner_name=ride[Rkeys.owner_name],
                                 request_text=ride[Rkeys.request_text],
                                 timestamp=ride[Rkeys.timestamp],
                                 pickup_time=ride[Rkeys.pickup_time],
                                 pickup_location=ride[Rkeys.pickup_location],
                                 destination_location=ride[Rkeys.destination_location],
                                 payed=ride[Rkeys.payed],
                                 passengers=ride[Rkeys.passengers],
                                 packages=ride[Rkeys.packages],
                                 reply=reply,
                                 amount=ride[Rkeys.amount],
                                 call=ride[Rkeys.call],
                                 text=ride[Rkeys.text],
                                 gender=ride[Rkeys.gender],
                                 phone=ride[Rkeys.phone]
                                 ))

    return AllRidesModel(status=status.HTTP_200_OK, rides=rides_models)


@router.get("/get_my_rides", response_model=AllRidesModel)
async def get_all_rides(user: dict = Depends(get_current_user)):
    rides = db.get_my_rides(user[UKeys.email])
    rides_models = list()
    for ride in rides:
        if ride[Rkeys.reply]:
            reply = RideReplyModel(owner_name=ride[Rkeys.reply][Rkeys.owner_name],
                                   owner_email=ride[Rkeys.reply][Rkeys.owner_email],
                                   reply_text=ride[Rkeys.reply][Rkeys.reply_text],
                                   offered_amount=ride[Rkeys.reply][Rkeys.reply_amount])
        else:
            reply = None
        rides_models.append(Ride(ride_id=ride[Rkeys.ride_id],
                                 owner_email=ride[Rkeys.owner_email],
                                 owner_name=ride[Rkeys.owner_name],
                                 request_text=ride[Rkeys.request_text],
                                 timestamp=ride[Rkeys.timestamp],
                                 pickup_time=ride[Rkeys.pickup_time],
                                 pickup_location=ride[Rkeys.pickup_location],
                                 destination_location=ride[Rkeys.destination_location],
                                 payed=ride[Rkeys.payed],
                                 passengers=ride[Rkeys.passengers],
                                 packages=ride[Rkeys.packages],
                                 reply=reply,
                                 amount=ride[Rkeys.amount],
                                 call=ride[Rkeys.call],
                                 text=ride[Rkeys.text],
                                 gender=ride[Rkeys.gender],
                                 phone=ride[Rkeys.phone]
                                 ))

    return AllRidesModel(status=status.HTTP_200_OK, rides=rides_models)


@router.get("/get_ride_by_id", response_model=SingleRideResponseModel)
async def get_ride_by_id(ride_id: int, user: dict = Depends(get_current_user)):
    ride = db.get_ride_by_id(ride_id)
    if ride:
        if ride[Rkeys.reply]:
            reply = RideReplyModel(owner_name=ride[Rkeys.reply][Rkeys.owner_name],
                                   owner_email=ride[Rkeys.reply][Rkeys.owner_email],
                                   reply_text=ride[Rkeys.reply][Rkeys.reply_text])
        else:
            reply = None
        ride_model = Ride(ride_id=ride[Rkeys.ride_id],
                          owner_email=ride[Rkeys.owner_email],
                          owner_name=ride[Rkeys.owner_name],
                          request_text=ride[Rkeys.request_text],
                          timestamp=ride[Rkeys.timestamp],
                          pickup_time=ride[Rkeys.pickup_time],
                          pickup_location=ride[Rkeys.pickup_location],
                          destination_location=ride[Rkeys.destination_location],
                          payed=ride[Rkeys.payed],
                          passengers=ride[Rkeys.passengers],
                          packages=ride[Rkeys.packages],
                          reply=reply,
                          amount=ride[Rkeys.amount],
                          call=ride[Rkeys.call],
                          text=ride[Rkeys.text],
                          gender=ride[Rkeys.gender],
                          phone=ride[Rkeys.phone]
                          )
        return SingleRideResponseModel(status=status.HTTP_200_OK, ride=ride_model)
    raise HTTPException(status=status.HTTP_404_NOT_FOUND,
                        message="Ride not found!")


@router.delete("/delete_ride", response_model=RideDeleteResponseModel)
async def delete_ride(ride_id: int, user: dict = Depends(get_current_user)):
    db.delete_ride_by_id(ride_id)
    return RideDeleteResponseModel(status=status.HTTP_200_OK, message="success")


@router.post("/add_offered_ride", response_model=RideAddResponseModel)
async def add_new_ride(request: RidePostModel, user: dict = Depends(get_current_user)):
    ride_id = get_new_ride_id()
    pickup_time = string_to_timestamp(request.pickup_time)
    db.add_ride_request(ride_id=ride_id,
                        timestamp=get_timestamp(),
                        request_text=request.request_text,
                        owner_name=user[UKeys.full_name],
                        owner_email=user[UKeys.email],
                        pickup_location=request.pickup_location,
                        destination_location=request.destination_location,
                        payed=request.payed,
                        pickup_time=pickup_time,
                        passengers=request.passengers,
                        packages=request.packages,
                        gender=request.gender,
                        call=request.call,
                        text=request.text,
                        amount=request.amount,
                        phone=request.phone
                        )
    return RideAddResponseModel(status=status.HTTP_200_OK, ride_id=ride_id, message="success")


@ router.get("/get_all_offered_rides", response_model=AllOfferedRides)
async def get_all_rides(user: dict = Depends(get_current_user)):
    rides = db.get_all_rides()
    rides_models = list()
    for ride in rides:
        rides_models.append(OfferedRide(ride_id=ride[Rkeys.ride_id],
                                        owner_email=ride[Rkeys.owner_email],
                                        owner_name=ride[Rkeys.owner_name],
                                        offer_text=ride[Rkeys.request_text],
                                        timestamp=ride[Rkeys.timestamp],
                                        pickup_time=ride[Rkeys.pickup_time],
                                        pickup_location=ride[Rkeys.pickup_location],
                                        destination_location=ride[Rkeys.destination_location],
                                        payed=ride[Rkeys.payed],
                                        passengers=ride[Rkeys.passengers],
                                        packages=ride[Rkeys.packages],
                                        amount=ride[Rkeys.amount],
                                        call=ride[Rkeys.call],
                                        text=ride[Rkeys.text],
                                        gender=ride[Rkeys.gender],
                                        phone=ride[Rkeys.phone]
                                        ))

    return AllOfferedRides(status=status.HTTP_200_OK, rides=rides_models)
