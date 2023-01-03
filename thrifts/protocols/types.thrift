namespace py thrifts.services.types
namespace java thrifts.services.types
namespace go thrifts.services.types

typedef string UserID

struct UserInfo {
    10: string first_name
    20: string last_name
}
