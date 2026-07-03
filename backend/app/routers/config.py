from fastapi import APIRouter, Request

router = APIRouter(tags=["config"])


@router.get("/config")
def get_config(request: Request):
    return request.state.tenant
