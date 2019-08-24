from hamcrest import assert_that, calling, is_not, raises


def test_server_connect(socket, Server, socket_error):
    assert_that(calling(socket.connect).with_args((Server.host, Server.port)), is_not(raises(socket_error)))
