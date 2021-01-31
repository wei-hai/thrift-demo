from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

from services.user import UserService

# Make socket
transport = TSocket.TSocket(host="localhost", port=9090)
# Buffering is critical. Raw sockets are very slow
transport = TTransport.TBufferedTransport(transport)
# Wrap in a protocol
protocol = TBinaryProtocol.TBinaryProtocol(transport)
# Create a client to use the protocol encoder
client = UserService.Client(protocol)
# Connect
transport.open()
request = UserService.GetUserByIdRequest(ids=["1", "2"])
response = client.get_user_by_id(request=request)
if response.users:
    for user in response.users:
        print(user)
else:
    print("empty")
transport.close()
