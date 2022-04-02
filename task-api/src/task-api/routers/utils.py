import json
import os
import datetime
from uuid import UUID
import random
from ..models import *
from ..exceptions import NotFoundException


file_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(file_dir, "./data.json")

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        if isinstance(obj, datetime):
            return str(obj)
        return json.JSONEncoder.default(self, obj)



def load_contracts():
    with open(file_path, "r") as contractFile:
        data = json.load(contractFile)
        contractFile.close()
        return data

def save_contracts(data):
    with open(file_path, "w") as new_contractFile:
        json.dump(data, new_contractFile, cls=UUIDEncoder)
        new_contractFile.close()


def get_or_create_data():
    curr_data = load_contracts()
    if curr_data.get("addressList"):
        return {
            "addressList" : curr_data.get("addressList"),
            "license_info" : curr_data.get("license_info")
        }
    else:
        license_info = License().dict()
        addressList = []
        for _ in range(15):
            tasks = []
            for _ in range(random.randint(5,15)):
                tasks.append(TaskInfo().dict())
            addressList.append(AddressInfo(tasklist=tasks).dict())
        curr_data["addressList"] = addressList
        curr_data["license_info"] = license_info
        save_contracts(curr_data)
    return get_or_create_data()


def get_tasks(address):
    curr_data = load_contracts()
    address_list = curr_data.get("addressList")
    for el in address_list:
        curr_address = el.get("address")
        if curr_address == address:
            return el
    raise NotFoundException("task")


def add_task(address, task):
    curr_data = load_contracts()
    address_list = curr_data.get("addressList")
    for el in address_list:
        curr_address = el.get("address")
        if curr_address == address:
            el.get("tasklist").append(task)
            save_contracts(curr_data)
            return el
    raise NotFoundException("task")


def update_task_status(address, task_id, task_status):
    curr_data = load_contracts()
    address_list = curr_data.get("addressList")
    for el in address_list:
        curr_address = el.get("address")
        if curr_address == address:
            curr_tasks = el.get("tasklist")
            for c in curr_tasks:
                if c.get("id") == task_id:
                    c["status"] = task_status
                    save_contracts(file_path, curr_data)
                    return el
    raise NotFoundException("task")


def check_password(password):
    data = load_contracts()
    return data.get("password") == password


def change_rpc(rpc):
    print("in rpc")
    data = load_contracts()
    data["rpc"] = rpc
    save_contracts(data)
    return load_rpc()


def load_rpc():
    data = load_contracts()
    return data.get("rpc", None)


def signup_create(words, password):
    data = load_contracts()
    data["addressList"] = []
    data["mnemonic"] = words
    data["password"] = password
    save_contracts(data)

