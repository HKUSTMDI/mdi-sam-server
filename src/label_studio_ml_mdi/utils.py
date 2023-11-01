import logging

from PIL import Image, ImageOps
from collections import OrderedDict

from label_studio_tools.core.utils.params import get_env
from label_studio_tools.core.utils.io import get_local_path

from typing import List, Dict, Optional
from .conf.settings import *
import requests
import math
import re
import os
import concurrent.futures
from io import BytesIO
import threading
import os
import aiohttp
import asyncio
import time

from functools import wraps

DATA_UNDEFINED_NAME = '$undefined$'

logger = logging.getLogger(__name__)

def cost_time(func):
    @wraps(func)
    def decrated(*args, **kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        cost_time = round(time.time() - start_time, 3) * 1000
        logger.info(f"[function:{func.__name__}] cost {cost_time} ms")
        return result
    return decrated


def get_single_tag_keys(parsed_label_config, control_type, object_type):
    """
    Gets parsed label config, and returns data keys related to the single control tag and the single object tag schema
    (e.g. one "Choices" with one "Text")
    :param parsed_label_config: parsed label config returned by "label_studio.misc.parse_config" function
    :param control_type: control tag str as it written in label config (e.g. 'Choices')
    :param object_type: object tag str as it written in label config (e.g. 'Text')
    :return: 3 string keys and 1 array of string labels: (from_name, to_name, value, labels)
    """
    assert len(parsed_label_config) == 1
    from_name, info = list(parsed_label_config.items())[0]
    assert info['type'] == control_type, 'Label config has control tag "<' + info['type'] + '>" but "<' + control_type + '>" is expected for this model.'  # noqa

    assert len(info['to_name']) == 1
    assert len(info['inputs']) == 1
    assert info['inputs'][0]['type'] == object_type
    to_name = info['to_name'][0]
    value = info['inputs'][0]['value']
    return from_name, to_name, value, info['labels']


def get_first_tag_keys(parsed_label_config, control_type, object_type):
    """
    Reads config and returns the first control tag and the first object tag that match the given types
    :param parsed_label_config:
    :param control_type:
    :param object_type:
    :return:
    """
    for from_name, info in parsed_label_config.items():
        if info['type'] == control_type:
            for input in info['inputs']:
                if input['type'] == object_type:
                    return from_name, info
    return None, None


def is_skipped(completion):
    if len(completion['annotations']) != 1:
        return False
    completion = completion['annotations'][0]
    return completion.get('skipped', False) or completion.get('was_cancelled', False)


def get_choice(completion):
    return completion['annotations'][0]['result'][0]['value']['choices'][0]


def get_image_local_path(url, image_cache_dir=None, project_dir=None, image_dir=None,
                         label_studio_host=None, label_studio_access_token=None):
    image_local_path = get_local_path(
        url=url,
        cache_dir=image_cache_dir,
        project_dir=project_dir,
        hostname=label_studio_host or get_env('HOSTNAME'),
        image_dir=image_dir,
        access_token=label_studio_access_token
    )
    logger.debug(f'Image stored in the local path: {image_local_path}')
    return image_local_path


def get_image_size(filepath):
    img = Image.open(filepath)
    img = ImageOps.exif_transpose(img)
    return img.size

@cost_time
async def download_image(session, image):
    url = image['tile_url']
    max_retry = download_retry  # 最大重试次数
    retry_count = 0

    while retry_count < max_retry:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image['content'] = Image.open(BytesIO(image_data))
                    local_tile_storage = test_tile_storage + image['file_name'] + ".jpg"
                    image['content'].save(local_tile_storage)
                else:
                    logger.error("Failed to download image")
                    raise Exception("Failed to download image")
            
            # 下载成功则跳出循环
            break
        except Exception as e:
            # 失败时进行延时并增加重试计数
            retry_count += 1
            if retry_count < max_retry:
                delay_seconds = 2  # 延时时间（秒）
                await asyncio.sleep(delay_seconds)
                continue
            else:
                raise e
        
class InMemoryLRUDictCache:
    def __init__(self, capacity=1):
        self.cache = OrderedDict()
        self.capacity = capacity

    def __contains__(self, item):
        return item in self.cache

    def get(self, key):
        if key in self.cache:
            # Move the accessed item to the end
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            # Move the updated item to the end
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Pop the first item if cache reached its capacity
            self.cache.popitem(last=False)

        self.cache[key] = value

    def __str__(self):
        return str(self.cache)


class sdpcHanler:
    def __init__(self) -> None:
        self.cache = InMemoryLRUDictCache(50)

    def convert(self,tasks:List[Dict], context: Optional[Dict] = None, **kwargs):
        #获取图片信息，请求SDPC_INFO_PREFIX
        image_info_url = tasks[0]['data']['image']
        pattern = re.escape(sdpc_tile_prefix)
        image_filename = re.sub(pattern, '', image_info_url)

        #查看是否有缓存
        if not image_info_url in self.cache:
            logger.info(f"no info in cache,ready to request:{image_info_url}")
            start_time = time.time()
            resp = requests.get(image_info_url)
            if resp.status_code == 200:
                image_info = resp.json()
                self.cache.put(image_info_url,image_info)
                
            else:
                logger.debug(f"get sdpc image[{image_info_url}]info faild,status code:[{resp.status_code}]")
                raise Exception(f"get sdpc image[{image_info_url}]info faild,status code:[{resp.status_code}]")
            cost_time = (time.time() - start_time) * 1000
            logger.info(f"request url_info cost_time:{cost_time} ms")
        else:
            logger.info("use image_info_url in cache")
            image_info = self.cache.get(image_info_url) 
        
        #计算layer位置
        cur_scale        = context["result"][0]['value']['cur_scale']
        layer_size       = image_info['basisInfo']['layerSize']
        basisInfo_width  = image_info['basisInfo']['tileWidth']
        basisInfo_height = image_info['basisInfo']['tileHeight']
        sliceLayerInfo   = image_info['originalInfo']['sliceLayerInfo']
        current_layer    = self.get_layer_level(sliceLayerInfo, cur_scale)
        logger.debug("current_layer:",current_layer)
        current_layer_info = sliceLayerInfo[current_layer-1]

        #拼接、保存图片
        current_layer_sliceX = current_layer_info['sliceNumX']
        current_layer_sliceY = current_layer_info['sliceNumY']
        logger.debug("current_layer_info:",current_layer_info)
        
        input_data  =  context['result'][0]
        point_x     = input_data['value']['x'] / 100
        point_y     = input_data['value']['y'] / 100
        box_width   = input_data['value']['width'] / 100 
        box_height  = input_data['value']['height'] / 100
        
        logger.debug(f"point_x:{point_x},point_y:{point_y},box_width:{box_width},box_height:{box_height}")
        #左上角tile瓦片位置
        layer_x_min = math.floor( point_x * current_layer_sliceX ) #计算所需要的layer块x方向的位置
        layer_y_min = math.floor( point_y * current_layer_sliceY ) #计算所需要的layer块y方向的位置
        layer_x_max = math.floor( (point_x + box_width) * current_layer_sliceX )
        layer_y_max = math.floor( (point_y + box_height) * current_layer_sliceY )

        slice_width_num  = layer_x_max - layer_x_min + 1
        slice_height_num = layer_y_max - layer_y_min + 1
        tile_size        = ( basisInfo_width , basisInfo_height)
        slice_size_num   = ( slice_width_num, slice_height_num )

        logger.debug("layer_x_min:",layer_x_min,"layer_x_max:",layer_x_max)
        logger.debug("layer_y_min:",layer_y_min,"layer_y_max:",layer_y_max)
        box_point_list = []
        for i in range(layer_y_min, layer_y_max + 1):
            for j in range(layer_x_min, layer_x_max + 1):
                box_point_list.append([j,i])

        logger.debug("box_point_list:",box_point_list)
        #图片下载、拼接
        #tile_image_url:瓦片图前缀
        tile_image_url = sdpc_tile_imageURL + image_filename
        #判断图片收集否存在(优化)

        slice_url, slice_width, slice_height = self.create_image(tile_size, slice_size_num, current_layer, 
                                      box_point_list, tile_image_url, image_filename)
        
        #修改tasks,contex的值,x,y,width,height都要改
        tasks[0]['data']['image']     = slice_url
        input_data['original_width']  = slice_width
        input_data['original_height'] = slice_height

        #x,y,width,height位置变换:在拼接的slice中，输入点相对于参考点的坐标位置
        x_relative          = (point_x * current_layer_sliceX - layer_x_min) / slice_width_num * 100
        y_relative          = (point_y * current_layer_sliceY - layer_y_min) / slice_height_num * 100
        box_width_relative  = box_width * current_layer_sliceX / slice_width_num * 100
        box_height_relative = box_height * current_layer_sliceY / slice_height_num * 100

        input_data['value']['x'] = x_relative
        input_data['value']['y'] = y_relative
        input_data['value']['width'] = box_width_relative
        input_data['value']['height'] = box_height_relative

        logger.debug(f"x_relative:{x_relative},y_relative:{y_relative},box_width_relative:{box_width_relative}, box_height_relative:{box_height_relative}")


    def get_layer_level(self, layerInfo, curScale):
        level = 0
        for item in range(len(layerInfo)):
            if curScale < layerInfo[item]['curScale']:
                level = item + 1
            else:
                level += 1
                break
        return level
    
    @cost_time
    def create_image(self, tile_size, slice_size_num, layer, point_list:list, prefix_url, image_filename):
        """
        description:tile瓦片拼接出图片
        """
        url_layer = layer - 1
        image_url_list= []
        for item in point_list:
            logger.debug(f"prefix_url:{prefix_url}")
            tile_url = prefix_url + '/' + str(url_layer) + '/' + str(item[0]) + '/' + str(item[1])
            file_name = image_filename + '_'  + str(url_layer) + '_' + str(item[0]) + '_' + str(item[1])
            logger.debug(f"tile_url:[{tile_url}],file_name:[{file_name}]")

            image_url_list.append(
                {
                    "tile_url"      : tile_url,
                    "file_name"     : file_name,
                    "layer"         : layer,
                    "x"             : item[0],
                    "y"             : item[1],
                    "content"       : None,
                    file_name       : True
                }
            )
        #download_images(image_url_list)
        tasks = []
        logger.debug(f"image_url_list:{image_url_list}")
        start_time = time.time()
        async def process_urls():
            async with aiohttp.ClientSession() as session:
                for url in image_url_list:
                    task = asyncio.ensure_future(download_image(session, url))
                    tasks.append(task)
                await asyncio.gather(*tasks)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process_urls())
        loop.close()
        cost_time = (time.time() - start_time) * 1000
        logger.info(f"download tile images cost time:{cost_time}")
        #拼接
        slice_width  = tile_size[0] * slice_size_num[0]
        slice_height = tile_size[1] * slice_size_num[1]

        logger.debug(f"slice_size_num:{slice_size_num}")
        logger.debug(f"new slice size:[{slice_width},{slice_height}]")

        slice_image = Image.new('RGB', (slice_width, slice_height))
        logger.debug(f"image_url_list:{image_url_list}")
        for item, image in enumerate(image_url_list):
            slice_x = int(item % slice_size_num[0] * tile_size[0])
            slice_y = int(item // slice_size_num[0] * tile_size[1])
            slice_image.paste(image["content"], (slice_x, slice_y))
        
        #url文件名:/data/5cf58b__CMWGTUhghiTnTpwd.jpg?d=home/mdi/.cache/label-studio;
        #本地文件名:/home/mdi/.cache/label-studio/5cf58b__CMWGTUhghiTnTpwd.jpg
        #保存在本地，本地文件名:原文件名+时间戳(ms)

        slice_filename = image_filename  + "_" + str(int(time.time() * 1000)) + '.jpeg'
        url_slice_filename = "/data/" + slice_filename + '?d=' + local_storage
        local_slice_filename = os.path.join(local_storage, slice_filename)
        slice_image.save(local_slice_filename)

        return url_slice_filename, slice_width, slice_height


if __name__ == "__main__":
    c = InMemoryLRUDictCache(2)
    c.put(1, 1)
    c.put(2,2)
    c.put("test",{"a":1})
    print(c.get("test"))
    logger.debug(c.cache)