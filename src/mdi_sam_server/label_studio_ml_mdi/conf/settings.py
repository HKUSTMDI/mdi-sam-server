from dotenv import load_dotenv
import os
from pydantic import BaseSettings, Field
import logging

load_dotenv()
# sdpc_tile_prefix = os.getenv("SDPC_TILE_PREFIX") #sdpc信息获取
# sdpc_tile_imageURL = os.getenv("SDPC_TILE_IMAGEURL") 
# svs_tile_prefix = os.getenv("SVS_TILE_PREFIX")
# svs_tile_imageURL =os.getenv("SVS_TILE_IMAGEURL")
# download_retry = os.getenv("DOWNLOAD_RETRY") #图片下载重试次数
# local_storage  = os.getenv("LOCAL_STORAGE") #sam实时识别预存地址,如果没有该地址请创建
# test_tile_storage = os.getenv("TEST_TILE_STORAGE")

logger = logging.getLogger(__name__)
class Settings(BaseSettings):
    sdpc_tile_prefix: str = os.getenv("SDPC_TILE_PREFIX") 
    sdpc_tile_imageURL: str = os.getenv("SDPC_TILE_IMAGEURL")
    svs_tile_prefix: str = os.getenv("SVS_TILE_PREFIX")
    svs_tile_imageURL: str = os.getenv("SVS_TILE_IMAGEURL")
    download_retry: str = os.getenv("DOWNLOAD_RETRY") 
    local_storage: str = os.getenv("LOCAL_STORAGE") 
    test_tile_storage: str = os.getenv("TEST_TILE_STORAGE")
    
CONFIG = Settings()
logger.debug(f"CONFIG:{CONFIG}")
