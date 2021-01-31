from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.TMultiplexedProcessor import TMultiplexedProcessor
from thrift.transport import TSocket, TTransport

from services.product import ProductService
from services.product.ttypes import GetProductByIdResponse, Product
from services.types.ttypes import UserInfo
from services.user import UserService
from services.user.ttypes import GetUserByIdResponse, User
from thrift import transport


class UserServiceImpl:
    def __init__(self):
        print("UserService Created")

    def get_user_by_id(self, request: UserService.GetUserByIdRequest):
        print("get_user_by_id")
        users = [
            User(id=user_id, info=UserInfo(first_name=user_id + "_firtst_name", last_name=user_id + "_last_name")) for user_id in request.ids
        ]
        return GetUserByIdResponse(users=users)


class ProductServiceImpl:
    def __init__(self):
        print("ProductService Created")

    def get_product_by_id(self, request: ProductService.GetProductByIdRequest):
        print("get_product_by_id")
        products = [
            Product(id=product_id, name=product_id + "_name") for product_id in request.ids
        ]
        return GetProductByIdResponse(products=products)


userServiceImpl = UserServiceImpl()
productServiceImpl = ProductServiceImpl()
user_processor = UserService.Processor(userServiceImpl)
product_processor = ProductService.Processor(productServiceImpl)
transport = TSocket.TServerSocket(host="localhost", port=9090)
transport_factory = TTransport.TBufferedTransportFactory()
protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()
# Multi processor
processor = TMultiplexedProcessor()
processor.registerProcessor("user_service", user_processor)
processor.registerProcessor("product_service", product_processor)
server = TServer.TSimpleServer(
    processor, transport, transport_factory, protocol_factory)
print("Starting server")
server.serve()
print("Done")
