namespace py thrifts.services.user
namespace java thrifts.services.user
namespace go thrifts.services.user

include "./types.thrift"

struct User {
    10: types.UserID id
    20: types.UserInfo info
}

struct GetUserByIdRequest {
    10: list<types.UserID> ids
}

struct GetUserByIdResponse {
    10: optional list<User> users
}

service UserService {
    GetUserByIdResponse get_user_by_id(1: GetUserByIdRequest request)
}