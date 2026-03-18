"""Mock streamlit so app.py functions can be imported without a running Streamlit server."""
import sys
from unittest.mock import MagicMock

st_mock = MagicMock()

# selectbox must return a real string so dict lookups in app.py don't crash
st_mock.sidebar.selectbox.return_value = "Normal"

# columns/tabs etc. need to return real iterables of the right length
st_mock.columns.side_effect = lambda n, **kw: [MagicMock() for _ in range(n)]

# session_state needs to behave like a namespace/dict
class _FakeSessionState(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)
    def __setattr__(self, key, value):
        self[key] = value
    def __contains__(self, item):
        return dict.__contains__(self, item)

st_mock.session_state = _FakeSessionState()

sys.modules["streamlit"] = st_mock
