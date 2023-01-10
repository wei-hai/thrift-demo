from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol


class ConnectionPool:
    def __init__(
        self, host, port, service_cls, pool_size=10, network_timeout=0, is_async=False
    ) -> None:
        self.host = host
        self.port = port
        self.service_cls = service_cls
        self.network_timeout = network_timeout
        self._is_async = is_async
        self._is_closed = False

        if self._is_async:
            import gevent.queue
            from gevent import lock as glock

            self._semaphore = glock.BoundedSemaphore(pool_size)
            self._connection_queue = gevent.queue.LifoQueue(pool_size)
            self._queue_empty_error = gevent.queue.Empty
        else:
            import threading
            import queue

            self._semaphore = threading.BoundedSemaphore(pool_size)
            self._connection_queue = queue.LifoQueue(pool_size)
            self._queue_empty_error = queue.Empty

    def close(self):
        self._is_closed = True
        while not self._connection_queue.empty():
            try:
                conn = self._connection_queue.get(block=False)
                try:
                    self._close_connection(conn)
                except:
                    pass
            except self._queue_empty_error:
                pass

    def _create_connection(self):
        socket = TSocket.TSocket(self.host, self.port)
        if self.network_timeout > 0:
            socket.setTimeout(self.network_timeout)
        transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocolAccelerated(transport)
        connection = self.service_cls(protocol)
        transport.open()
        return connection

    def _close_connection(self, conn):
        try:
            conn._iprot.trans.close()
        except:
            print("failed to close iprot trans on", conn)
        try:
            conn._oprot.trans.close()
        except:
            print("failed to close oprot trans on", conn)

    def get_connection(self):
        self._semaphore.acquire()
        if self._is_closed:
            raise RuntimeError("connection pool is closed")
        try:
            return self._connection_queue.get(block=False)
        except self._queue_empty_error:
            try:
                return self._create_connection()
            except:
                self._semaphore.release()
                raise

    def recycle_connection(self, conn):
        if self._is_closed:
            self._close_connection(conn)
            return
        self._connection_queue.put(conn)
        self._semaphore.release()

    def release_connection(self, conn):
        try:
            self._close_connection(conn)
        except:
            pass
        if not self._is_closed:
            self._semaphore.release()
