sdpc_tile_prefix = "http://mdi.hkust-gz.edu.cn/wsi/sdpc/api/sliceInfo/sdpc/" #sdpc信息获取
sdpc_tile_imageURL = "http://mdi.hkust-gz.edu.cn/wsi/sdpc/api/tile/sdpc/"
local_tile_url = "./tiles" #瓦片数据
download_retry = 3 #图片下载重试次数
local_storage  = "/home/mdi/.cache/label-studio/" #sam实时识别预存地址,如果没有该地址请创建
test_tile_storage = "./tile_image/"