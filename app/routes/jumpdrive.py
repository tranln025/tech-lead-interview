import requests
from flask import current_app
from app import db
from app.helpers import api_helper
from app.models import (
    jumpdrive_device,
    jumpdrive_event,
)
from app.routes.auth.decorators import roles_required
from . import util


def get_latest_jumpdrive_events(vin):
    url = "https://www.jumpdrive.com/wsdlv2/getinventorydata.php"
    username = current_app.config.get("JUMPDRIVE_USERNAME")
    password = current_app.config.get("JUMPDRIVE_PASSWORD")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = "username={}&password={}&vin={}&format=json".format(
        username, password, vin
    )

    response = requests.request("GET", url, headers=headers, data=payload)

    # Find all events that have been stored with the same vin
    for event in response.json():
        jumpdrive_events = db.session.query(jumpdrive_event).filter_by(vin=event["vin"])
        event_already_recorded = (
            True
            if jumpdrive_events.filter_by(last_time_in=event["last_time_in"]).first()
            else False
        )

        # Only add an event record if it has not been previously recorded
        if not event_already_recorded:
            new_event = jumpdrive_event(
                serial_number=event["jumpdrive_id"],
                vin=event["vin"],
                last_time_in=event["last_time_in"],
                fuel_percent=event["fuel_percent"],
                battery_level_mV=event["battery"],
                odometer_km=event["odo_current"],
            )
            db.session.add(new_event)
            db.session.commit()

    return response.json()


@util.route("/jumpdrive/inventory-data", methods=["GET"])
@roles_required(["admin"])
def jumpdrive_all_inventory_data(user_):
    device_query = jumpdrive_device.query.filter(
        jumpdrive_device.is_active == True, jumpdrive_device.vin != None
    ).all()

    all_inventory_data = []
    for device in device_query:
        all_inventory_data += get_latest_jumpdrive_events(device.vin)

    return api_helper.return_items(all_inventory_data)


@util.route("/jumpdrive/inventory-data/<vin>", methods=["GET"])
@roles_required(["admin"])
def jumpdrive_inventory_data(user_, vin):
    return api_helper.return_items(get_latest_jumpdrive_events(vin))
