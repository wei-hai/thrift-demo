from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket, TTransport

from services.types.ttypes import UserInfo
from services.user import UserService
from services.user.ttypes import GetUserByIdResponse, User
from thrift import transport


class UserServiceImpl:
    def __init__(self):
        print("UserService Created")

    def get_user_by_id(self, ids):
        print("get_user_by_id")
        users = [
            User(id="1", info=UserInfo(first_name="aha", last_name="oho"))
        ]
        return GetUserByIdResponse(users=users)


userServiceImpl = UserServiceImpl()
processor = UserService.Processor(userServiceImpl)
transport = TSocket.TServerSocket(host="localhost", port=9090)
transport_factory = TTransport.TBufferedTransportFactory()
protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()
server = TServer.TSimpleServer(
    processor, transport, transport_factory, protocol_factory)
print("Starting server")
server.serve()
print("Done")
