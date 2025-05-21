from source.app.adapter.fastapi.crud import CrudRouter
from source.app.adapter.fastapi.dependencies import get_repos
from source.app.adapter.token.oauth2 import check_roles
from source.app.domain.product_dto import CreateProductDto, ProductDto

router_v1 = CrudRouter(
    repo_dependency=get_repos,
    role_dependency=check_roles,
    repository="product",
    methods_and_roles={"READ": ["admin", "customer"], "CREATE": ["admin"]},
    response_schema=ProductDto,
    create_schema=CreateProductDto,
    update_schema=ProductDto,
)
