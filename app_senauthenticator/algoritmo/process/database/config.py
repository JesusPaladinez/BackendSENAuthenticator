from pydantic import BaseModel
from app_senauthenticator.algoritmo.process.database.users_path import (users_path, users_check_path)
from app_senauthenticator.algoritmo.process.database.faces_path import faces_path


class DataBasePaths(BaseModel):
    # paths
    faces: str = faces_path
    users: str = users_path
    check_users: str = users_check_path
