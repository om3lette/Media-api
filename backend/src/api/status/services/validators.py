from backend.src.api.common.io.requests_repository import RequestsRepository
from backend.src.api.status.constants import ValidationStatusCode
from backend.src.api.status.schemas.status import StatusEventSchema


def validate_subscription(rid: str, req_repo: RequestsRepository):
    is_subscribable, is_present = req_repo.is_subscribable(rid)
    if not is_present:
        return ValidationStatusCode.REQUEST_NOT_FOUND, True
    if not is_subscribable:
        return ValidationStatusCode.SUB_NOT_ACCEPTED, False
    return ValidationStatusCode.OK, False


def validate_sub(
    payload: StatusEventSchema, subscribed: set[str], req_repo: RequestsRepository
) -> tuple[ValidationStatusCode, bool]:
    if payload.rid in subscribed:
        return ValidationStatusCode.ALREADY_SUBSCRIBED, False
    return validate_subscription(payload.rid, req_repo)


def validate_unsub(
    payload: StatusEventSchema, subscribed: set[str], req_repo: RequestsRepository
) -> tuple[ValidationStatusCode, bool]:
    if payload.rid not in subscribed:
        return ValidationStatusCode.NOT_SUBSCRIBED, False
    return validate_subscription(payload.rid, req_repo)


def validate_sync(
    payload: StatusEventSchema, subscribed: set[str], req_repo: RequestsRepository
) -> tuple[ValidationStatusCode, bool]:
    return ValidationStatusCode.OK, False
