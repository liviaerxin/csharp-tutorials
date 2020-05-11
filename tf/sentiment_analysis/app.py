from grpc_server import serve, creater_server
from flask_server import WrapperServer


server = creater_server()
server.start()
server.wait_for_termination()