from dotenv import load_dotenv
import os
from pydantic import BaseSettings, Field


load_dotenv()

class Settings(BaseSettings):
    sdpc_tile_prefix: str = Field(..., env="SDPC_TILE_PREFIX")
    sdpc_tile_imageURL: str = Field(..., env="SDPC_TILE_IMAGEURL")
    svs_tile_prefix: str = Field(..., env="SVS_TILE_PREFIX")
    svs_tile_imageURL: str = Field(..., env="SVS_TILE_IMAGEURL")
    download_retry: str = Field(..., env="DOWNLOAD_RETRY")
    local_storage: str = Field(..., env="LOCAL_STORAGE")
    test_tile_storage: str = Field(..., env="TEST_TILE_STORAGE")
    
CONFIG = Settings()
