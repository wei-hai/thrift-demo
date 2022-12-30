from thrift.protocol import TBinaryProtocol
from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol
from thrift.transport import TSocket, TTransport

from thrift.myapp.services.product import ProductService
from thrift.myapp.services.user import UserService

# Make socket
transport = TSocket.TSocket(host="localhost", port=9090)
# Buffering is critical. Raw sockets are very slow
transport = TTransport.TBufferedTransport(transport)
# Wrap in a protocol
protocol = TBinaryProtocol.TBinaryProtocol(transport)
# register multiple protocols
user_protocol = TMultiplexedProtocol(protocol, "user_service")
product_protocol = TMultiplexedProtocol(protocol, "product_service")
# Create a client to use the protocol encoder
user_client = UserService.Client(user_protocol)
product_client = ProductService.Client(product_protocol)
# Connect
transport.open()
request = UserService.GetUserByIdRequest(ids=["user_id_1", "user_id_2"])
response = user_client.get_user_by_id(request=request)
if response.users:
    for user in response.users:
        print(user)
else:
    print("no user")
request = ProductService.GetProductByIdRequest(ids=["product_id_1"])
response = product_client.get_product_by_id(request=request)
if response.products:
    for product in response.products:
        print(product)
else:
    print("no product")
transport.close()
