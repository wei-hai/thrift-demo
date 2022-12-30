namespace py thrift.myapp.services.product
namespace java thrift.myapp.services.product
namespace go thrift.myapp.services.product

struct Product {
    10: string id
    20: string name
}

struct GetProductByIdRequest {
    10: list<string> ids
}

struct GetProductByIdResponse {
    10: optional list<Product> products
}

service ProductService {
    GetProductByIdResponse get_product_by_id(1: GetProductByIdRequest request)
}