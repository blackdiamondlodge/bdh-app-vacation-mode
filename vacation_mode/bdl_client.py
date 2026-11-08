"""Client for the bdl_modes AppDaemon app, which runs vacation / preheat /
home in the background (retries, scheduling, failure notifications)."""

import requests
from . import config

COMMANDS = ("vacation", "home", "preheat", "update_arrival", "arrive_now",
            "cancel")


def enabled():
    return bool(config.modes_url())


def call(cmd, **fields):
    """POST a command. Returns (payload, error, http_status)."""
    body = {"cmd": cmd}
    body.update({k: v for k, v in fields.items() if v is not None})
    try:
        r = requests.post(
            config.modes_url(), json=body, timeout=15,
            headers={"X-API-Key": config.modes_api_key()})
    except requests.RequestException as exc:
        return None, "Lodge controller unreachable: %s" % exc, 502
    try:
        data = r.json()
    except ValueError:
        return None, "Bad response from lodge controller (HTTP %s)" % (
            r.status_code), 502
    if r.status_code != 200:
        msg = data.get("error") if isinstance(data, dict) else None
        return None, msg or "HTTP %s" % r.status_code, (
            r.status_code if r.status_code in (400, 401) else 502)
    return data, None, 200
