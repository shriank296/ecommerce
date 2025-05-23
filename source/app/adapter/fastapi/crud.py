from enum import Enum
from typing import Any, Callable, List, Optional, Type, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.types import DecoratedCallable
from pydantic import BaseModel

from source.app.adapter.db.exception import DbIntegrityError, RecordNotFound
from source.app.ports.db import Repositories, Repository
from source.app.ports.db.repository import ModelDTO


class CrudRouter(APIRouter):
    """
    Dynamically create, read, update and delete methods for our repositories.
    """

    response_schema: Type[ModelDTO]
    create_schema: Type[ModelDTO]
    update_schema: Type[ModelDTO]

    def __init__(
        self,
        repo_dependency: Callable,
        role_dependency: Callable,
        repository: str,
        response_schema: Type[BaseModel],
        methods_and_roles: dict,
        create_schema: Type[BaseModel],
        update_schema: Type[BaseModel],
        partial_schema: Optional[Type[BaseModel]] = None,
        prefix: Optional[str] = None,
        tags: Optional[List[Union[str, Enum]]] = None,
        paginate: Optional[int] = None,
        **kwargs: Any,
    ):
        self.repo_dependency: Callable = repo_dependency
        self.role_dependency: Callable = role_dependency
        self.repository = repository
        self.methods_and_roles = methods_and_roles or []
        self.response_schema: Type[BaseModel] = response_schema
        self.create_schema: Type[BaseModel] = create_schema
        self.update_schema: Type[BaseModel] = update_schema
        self.partial_schema: Optional[Type[BaseModel]] = partial_schema

        prefix = prefix or ""

        super().__init__(prefix=prefix, tags=tags, **kwargs)
        self._setup_routes()

    def _setup_routes(self):
        if "CREATE" in self.methods_and_roles:
            assert self.create_schema
            self.add_api_route(
                "/",
                self._create(),
                methods=["POST"],
                response_model=self.response_schema,
            )
        if "READ" in self.methods_and_roles:
            self.add_api_route(
                "/{id}",
                self._read(),
                methods=["GET"],
                response_model=self.response_schema,
            )
            self.add_api_route(
                "/",
                self._read_multi(),
                methods=["GET"],
                response_model=List[self.response_schema],
            )
        if "UPDATE" in self.methods_and_roles:
            assert self.update_schema
            self.add_api_route(
                "/{id}",
                self._update(),
                methods=["PATCH"],
                response_model=self.response_schema,
            )
        if "DELETE" in self.methods_and_roles:
            #  assert self.delete_schema
            self.add_api_route(
                "/{id}",
                self._delete(),
                methods=["DELETE"],
            )

    @property
    def router(self):
        return self

    def _create(self) -> Callable:
        def create_record(
            obj_in: self.create_schema,  # type: ignore
            repos: Repositories = Depends(self.repo_dependency),
            current_user=Depends(
                self.role_dependency(self.methods_and_roles["CREATE"])
            ),
        ) -> self.response_schema:  # type: ignore
            try:
                repository: Repository = getattr(repos, self.repository)
                result = repository.create(obj_in)
            except RecordNotFound as e:
                raise HTTPException(status_code=404, detail=str(e))
            except DbIntegrityError as e:
                raise HTTPException(status_code=400, detail=str(e))
            else:
                return result

        return create_record

    def _read(self) -> Callable:
        def read_record(
            id: UUID,
            repos: Repositories = Depends(self.repo_dependency),
            current_user=Depends(self.role_dependency(self.methods_and_roles["READ"])),
        ) -> self.response_schema:  # type: ignore
            try:
                repository: Repository = getattr(repos, self.repository)
                result: BaseModel = repository.read(id)
            except RecordNotFound as e:
                raise HTTPException(status_code=404, detail=str(e))
            else:
                return result

        return read_record

    def _read_multi(self) -> Callable:
        def read_multi(
            repos: Repositories = Depends(self.repo_dependency),
            current_user=Depends(self.role_dependency(self.methods_and_roles["READ"])),
        ) -> List[self.response_schema]:  # type: ignore
            try:
                repository: Repository = getattr(repos, self.repository)
                result: BaseModel = repository.read_multi()
            except RecordNotFound as e:
                raise HTTPException(status_code=404, detail=str(e))
            else:
                return result

        return read_multi

    def _update(self) -> Callable:
        def update_record(
            id: UUID,
            obj_in: self.update_schema,  # type: ignore
            repos: Repositories = Depends(self.repo_dependency),
            current_user=Depends(
                self.role_dependency(self.methods_and_roles["UPDATE"])
            ),
        ) -> self.response_schema:  # type: ignore
            try:
                repository: Repository = getattr(repos, self.repository)
                result = repository.update(id, obj_in=obj_in)
            except RecordNotFound as e:
                raise HTTPException(status_code=404, detail=str(e))
            else:
                return result

        return update_record

    def _delete(self) -> Callable:
        def delete_record(
            id: UUID,
            repos: Repositories = Depends(self.repo_dependency),
            current_user=Depends(self.methods_and_roles["DELETE"]),
        ):
            repository: Repository = getattr(repos, self.repository)
            return repository.delete(id)

        return delete_record

    def remove_api_route(self, path: str, methods: List[str]) -> None:
        """
        Used when overriding default routes above, will remove registered
        route to allow a new one to override it.
        """
        methods_ = set(methods)
        for route in self.routes:
            if route.path == f"{self.prefix}{path}" and route.methods == methods_:
                self.routes.remove(route)

    def get(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["GET"])
        return super().get(path, *args, **kwargs)

    def post(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["POST"])
        return super().post(path, *args, **kwargs)

    def patch(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["PATCH"])
        return super().patch(path, *args, **kwargs)

    def put(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["PUT"])
        return super().put(path, *args, **kwargs)

    def delete(
        self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self.remove_api_route(path, ["DELETE"])
        return super().delete(path, *args, **kwargs)
