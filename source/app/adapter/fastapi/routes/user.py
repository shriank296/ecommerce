from source.app.domain.user_dto import UserDTO, CreateUserDTO
from source.app.adapter.fastapi.crud import CrudRouter
from source.app.adapter.fastapi.dependencies import get_repos


router_v1 = CrudRouter(
    repo_dependency=get_repos,
    repository="user",
    methods=["READ", "CREATE"],
    response_schema=UserDTO,
    create_schema=CreateUserDTO,
    update_schema=UserDTO
)
