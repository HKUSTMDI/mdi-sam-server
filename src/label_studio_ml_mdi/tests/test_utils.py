import aiohttp
import asyncio
from PIL import Image, ImageOps
from io import BytesIO
import logging
import time
from functools import wraps
import requests

logger = logging.getLogger(__name__)

def cost_time(func):
    @wraps(func)
    def decrated(*args, **kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        cost_time = round(time.time() - start_time, 3) * 1000
        print(f"[function:{func.__name__}] cost {cost_time} ms")
        return result
    return decrated

@cost_time
async def download_image(session, image):
    url = image['tile_url']
    max_retry = 3  # 最大重试次数
    retry_count = 0
    print("url:",url)

    while retry_count < max_retry:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image['content'] = Image.open(BytesIO(image_data))
                    file_name = "./" + str(int(time.time()*1000)) + '.jpeg'
                    image['content'].save(file_name)
                else:
                    logger.error("Failed to download image")
                    raise Exception("Failed to download image")
            
            # 下载成功则跳出循环
            break
        except Exception as e:
            # 失败时进行延时并增加重试计数
            print(e)
            retry_count += 1
            if retry_count < max_retry:
                delay_seconds = 2  # 延时时间（秒）
                await asyncio.sleep(delay_seconds)
                continue
            else:
                print(e)
                raise e
@cost_time
def get_tile_info():
    url_info = "http://mdi.hkust-gz.edu.cn/wsi/sdpc/api/sliceInfo/sdpc/20211025_065925_0%238_11"
    try:
        response = requests.get(url_info)
        if response.status_code == 200:
            tile_info = response.json()
            print(tile_info)
        else:
            print(f"status code:{response.status_code}")
    except Exception as err:
        print(err)

image_url_list = [
        {
            "tile_url": "http://mdi.hkust-gz.edu.cn/wsi/sdpc/api/tile/sdpc/20211025_065925_0%238_11/3/0/0",
            "content" :  None,
            "file_url": str(int(time.time()*1000))},
        {
            "tile_url": "http://mdi.hkust-gz.edu.cn/wsi/sdpc/api/tile/sdpc/20211025_065925_0%238_11/3/0/1",
            "content" :  None,
            "file_url": str(int(time.time()*1000))}
    ]

tasks = []
@cost_time
async def process_urls():
    async with aiohttp.ClientSession() as session:
        for url in image_url_list:
            task = asyncio.ensure_future(download_image(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)

#获取信息
get_tile_info()
#获取图片
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(process_urls())
loop.close()



