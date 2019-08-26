import pytest
import socket as s


@pytest.yield_fixture
def socket():
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    yield _socket
    _socket.close()


@pytest.fixture(scope="module")
def Server():
    class Dummy:
        host = "0.0.0.0"
        port = 8080
        uri = f"http://{host}:{port}/"

    return Dummy


@pytest.fixture(scope="module")
def socket_error():
    return s.error
