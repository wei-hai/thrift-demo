namespace py thrift.myapp.services.types
namespace java thrift.myapp.services.types
namespace go thrift.myapp.services.types

typedef string UserID

struct UserInfo {
    10: string first_name
    20: string last_name
}
