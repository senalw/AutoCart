import base64
import uuid
from typing import Optional


def get_page_number(next_page_token: str) -> int:
    """
    Convert valid page_token string into page_numer.

    :param next_page_token: String page token
    :return:              : Integer page numer
    """
    try:
        if not next_page_token:
            return 0
        token_byte = base64.b64decode(next_page_token)
        decoded_page = token_byte.decode("utf-8")
        return int(decoded_page)
    except ValueError:
        return 0


def get_next_page_token(page_numer: int, page_size: int, total_records: int) -> str:
    """
    Get next page toke for given page_number, page_size, and total_record_count
    :param page_numer: current page number
    :param page_size: expected page size
    :param total_records: total number of records in the table
    :return: next page token
    """
    next_record_offset: int = page_numer + page_size
    next_page_token: str = ""

    if total_records > next_record_offset:
        next_page_token = _convert_offset_to_page_token(next_record_offset)

    return next_page_token


def _convert_offset_to_page_token(record_offset: int) -> Optional[str]:
    """
    Convert record offset to page_token.

    :param record_offset: Integer record offset
    :return:            : String next_page_token
    """
    if not isinstance(record_offset, int) or record_offset < 0:
        raise ValueError(f"Invalid page number: {record_offset}")
    token_byte = str(record_offset).encode("utf-8")
    token_string = base64.b64encode(token_byte).decode("utf-8")
    return token_string


def is_valid_uuid(uuid_str: str) -> bool:
    try:
        uuid_obj = uuid.UUID(uuid_str)
        return str(uuid_obj) == uuid_str
    except ValueError:
        return False
