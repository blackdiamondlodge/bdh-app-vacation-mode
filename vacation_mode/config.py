"""Settings for the vacation_mode app (``BDH_VACATION_MODE_*``).

Legacy un-namespaced names (``BDL_MODES_*``) are still honoured.
"""
from bdh_sdk.settings import app_setting, as_bool

APP_ID = "vacation_mode"


def modes_url():
    """URL of the bdl_modes AppDaemon endpoint; empty disables it."""
    return app_setting(APP_ID, "modes_url", "", legacy=("BDL_MODES_URL",))


def modes_api_key():
    return app_setting(APP_ID, "modes_api_key", "",
                       legacy=("BDL_MODES_API_KEY",))


def preheat_enabled():
    return bool(app_setting(APP_ID, "preheat", False,
                            legacy=("BDL_MODES_PREHEAT",), cast=as_bool))
