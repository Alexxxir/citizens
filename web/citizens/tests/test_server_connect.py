def test_server_connect(socket, Server):
    socket.connect(Server.host_port)
    assert socket
