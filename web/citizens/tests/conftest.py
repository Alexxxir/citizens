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
        host_port = "0.0.0.0", 8080
    return Dummy

