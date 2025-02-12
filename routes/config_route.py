from fastapi import Request, status
from fastapi.responses import JSONResponse

from .base_route import AbstractRoute, APIRoute


class ConfigRoute(AbstractRoute):
    def init(self) -> None:
        self.base_path = "/api/config"
        self.routes = (APIRoute(f"{self.base_path}/reload", self.reload, methods=("POST",)),)

    async def reload(self, request: Request) -> JSONResponse:
        self.config.reload()
        return JSONResponse({"message": "Configuration reloaded successfully."}, status.HTTP_200_OK)
