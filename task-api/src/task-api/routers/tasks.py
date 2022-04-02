from fastapi import APIRouter
from fastapi.params import Body, Path

from ..exceptions import *
from ..models import *
from .utils import add_task, get_tasks, update_task_status, change_rpc

DEFAULT_RESPONSE = {
    404: {
        "description": "Not found"
    },
    500: {
        "description": "Internal Error"
    }
}

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses=DEFAULT_RESPONSE,
)


@router.post("/create", response_model=AddressInfo)
def create_task(
    data : CreateTask = Body(..., embed=False)
):
    curr_data = data.dict()
    address = curr_data.get("address")
    task = curr_data.get("task")
    return add_task(address, task)


@router.get("/{address_id}/get-tasks-info", response_model=AddressInfo)
def get_tasks_info(
    address_id : str = Path(..., title="The unique address ID")
):
    return get_tasks(address_id)


@router.post("/{address_id}/update-task", response_model=AddressInfo)
def update_task(
    address_id : str = Path(..., title="The unique address ID"),
    data : ChangeTaskStatus = Body(..., embed=False)
):
    return update_task_status(
        address_id, str(data.id), data.status
        )
