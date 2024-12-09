import ipaddress
from dataclasses import dataclass

from django.http import HttpRequest


@dataclass
class ClientInfo:
    ip_address: str
    device_name: str


def get_ip_address(request: HttpRequest) -> str:
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if ip_address:
        ip_address = ip_address.split(",")[0]
    else:
        ip_address = request.META.get("REMOTE_ADDR", '').split(",")[0]

    possibles = (ip_address.lstrip("[").split("]")[0], ip_address.split(":")[0])

    for addr in possibles:
        try:
            return str(ipaddress.ip_address(addr))
        except Exception as _:
            pass

    return ip_address


def get_client_info(request: HttpRequest) -> ClientInfo:
    return ClientInfo(
        ip_address=get_ip_address(request=request),
        device_name=request.META.get('HTTP_USER_AGENT', '')
    )
