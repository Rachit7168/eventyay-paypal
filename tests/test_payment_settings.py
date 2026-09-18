from eventyay_paypal.payment import Paypal


class FakeSettings:
    """Stand-in for SettingsSandbox that needs no database."""

    def __init__(self, **values):
        self._values = values

    def __getattr__(self, item):
        return self._values.get(item, "")

    def get(self, key, default=None, as_type=str):
        return self._values.get(key, default)


def provider_with_settings(**values):
    provider = Paypal.__new__(Paypal)
    provider.settings = FakeSettings(**values)
    return provider


def test_settings_form_fields_are_hidden_until_the_account_is_connected():
    provider = provider_with_settings(connect_client_id="client", connect_secret_key="secret", connect_user_id="")
    assert provider.settings_form_fields == {}


def test_is_enabled_is_false_while_onboarding_is_unfinished():
    provider = provider_with_settings(
        _enabled=True,
        connect_client_id="client",
        connect_secret_key="secret",
        connect_user_id="",
    )
    assert not provider.is_enabled


def test_is_enabled_follows_the_setting_once_paypal_can_be_used():
    connected = provider_with_settings(
        _enabled=True,
        connect_client_id="client",
        connect_secret_key="secret",
        connect_user_id="MERCHANT1",
    )
    assert connected.is_enabled

    own_credentials = provider_with_settings(_enabled=True, client_id="client", secret="secret")
    assert own_credentials.is_enabled

    switched_off = provider_with_settings(_enabled=False, client_id="client", secret="secret")
    assert not switched_off.is_enabled
