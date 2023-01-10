from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

from thrifts.services.user import UserService
from pool import ConnectionPool
import operator
import inspect

class Client:
    def __init__(self, iface_cls,
                 host, port,
                 pool_size=10,
                 retries = 3,
                 is_async = False,
                 network_timeout = 0,
                 debug = True):
        self.host = host
        self.port = port
        self.debug = debug
        self.retries = retries
        self._connection_pool = ConnectionPool(host, port, iface_cls, is_async=is_async, pool_size=pool_size, network_timeout=network_timeout)
        self._iface_cls = iface_cls
        #inject all methods defined in the thrift Iface class
        for m in inspect.getmembers(self._iface_cls, predicate=lambda x: inspect.isfunction(x) or inspect.ismethod(x)):
            setattr(self, m[0], self.__create_thrift_proxy__(m[0]))

    def close(self):
        self._connection_pool.close()

    def __create_thrift_proxy__(self, methodName):
        def __thrift_proxy(*args):
            return self.__thrift_call__(methodName, *args)
        return __thrift_proxy

    def __thrift_call__(self, method, *args):
        attempts_left = self.retries #self._connection_pool.size + 1
        result = None
        while True:
            conn = self._connection_pool.get_connection()
            try:
                if self.debug:
                    print("Thrift Call:%s Args:%s" % (method, args))
                result = getattr(conn, method)(*args)
            except TTransport.TTransportException as e:
                #broken connection, release it
                self._connection_pool.release_connection(conn)
                if attempts_left > 0:
                    attempts_left -= 1
                    continue
                raise e
            except Exception as e:
                #data exceptions, return connection and don't retry
                self._connection_pool.recycle_connection(conn)
                raise

            #call completed succesfully, return connection to pool
            self._connection_pool.recycle_connection(conn)
            return result

# Make socket
transport = TSocket.TSocket(host="localhost", port=9090)
# Buffering is critical. Raw sockets are very slow
transport = TTransport.TBufferedTransport(transport)
# Wrap in a protocol
protocol = TBinaryProtocol.TBinaryProtocol(transport)
# Create a client to use the protocol encoder
client = UserService.Client(protocol)
c = Client(UserService.Client, "localhost", 9090)
# Connect
# transport.open()
request = UserService.GetUserByIdRequest(ids=["1", "2"])

response = c.get_user_by_id(request)
if response.users:
    for user in response.users:
        print(user)
else:
    print("empty")

# transport.close()
