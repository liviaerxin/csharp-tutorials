from sentiment_analysis.grpc_server import serve, creater_server
from sentiment_analysis.flask_server import WrapperServer


server = creater_server()
server.start()
server.wait_for_termination()