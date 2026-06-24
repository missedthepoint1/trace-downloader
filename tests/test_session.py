from trace_grabber.session import api_logged_in


class _Resp:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status = status

    def json(self):
        return self._payload


class _Req:
    """Minimal stand-in for Playwright's APIRequestContext."""
    def __init__(self, resp_or_exc):
        self._r = resp_or_exc

    def get(self, url, timeout=None):
        if isinstance(self._r, Exception):
            raise self._r
        return self._r


def test_api_logged_in_valid():
    ok, detail = api_logged_in(_Req(_Resp({"success": True, "data": {"user_id": 42}})))
    assert ok is True
    assert "42" in detail


def test_api_logged_in_expired():
    ok, detail = api_logged_in(_Req(_Resp({"success": False,
                                           "error": {"id": "user_not_logged_in"}})))
    assert ok is False
    assert detail == "user_not_logged_in"


def test_api_logged_in_success_without_user_id_is_not_logged_in():
    ok, detail = api_logged_in(_Req(_Resp({"success": True, "data": {}})))
    assert ok is False


def test_api_logged_in_unreachable():
    ok, detail = api_logged_in(_Req(RuntimeError("boom")))
    assert ok is False
    assert detail.startswith("api unreachable")
