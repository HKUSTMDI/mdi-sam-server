# MDI SAM Server

**[Medical Data Inteligence Lab](https://mdi.hkust-gz.edu.cn/)**

[Cheng ZHANG](https://zachczhang.github.io/)

![architechture](https://mdi.hkust-gz.edu.cn/images/data-manager/architecture.jpg)

MDI annotation platform [SAM1](https://github.com/facebookresearch/segment-anything) &  [SAM2](https://github.com/facebookresearch/segment-anything-2) (and other SAM Family models) real-time recognition server ⚡ . You can use this server to generate the mask of image that you post with points (negative, positive), box, or both. You can install the server as **label studio** machine learning backend.

**Currently support:**

- (1) Real time annotation: multi-point annotation, single rectangle annotation
- (2) Prompt with different positive and negative values
- (3) the Whole Slide Image recognition

## 

### WSI segmentation annotation

<img src="https://mdi.hkust-gz.edu.cn/images/data-manager/wsi_segmentation.gif" width="75%"/>

### point & rectangle模式

<p float="left">
  <br>
  <img src="https://mdi.hkust-gz.edu.cn/images/data-manager/demo_point1.jpg" width="37.25%" />
  <img src="https://mdi.hkust-gz.edu.cn/images/data-manager/demo_point2.jpg" width="37.25%" />
  <br>
  <img src="https://mdi.hkust-gz.edu.cn/images/data-manager/demo_rectangle1.jpg" width="37.25%" /> <img src="https://mdi.hkust-gz.edu.cn/images/data-manager/demo_rectangle2.jpg" width="37.25%" />
</p>

### Supporting models:

  - 1.**[Meta SAM](https://github.com/facebookresearch/segment-anything)**
  - 2.**[Meta SAM2](https://github.com/facebookresearch/segment-anything-2)** 
  - 3.**[mobile_sam](https://github.com/ChaoningZhang/MobileSAM)**
  - 4.**ONNX** mode

## Installation

The Python used in the development process of this version is 3.10. Please use this version or an updated version.
```shell
# install the package
pip install -e .

# init .env and download models
sh init.sh
```

### How to use
- .env file
Please pay attention to .env file if you can't run the server.
```shell
#!/bin/bash
# if you wan't to predict WSI file, please fill in the blank variables.
SAM_CHOICE=SAM2
SDPC_TILE_PREFIX=  
SDPC_TILE_IMAGEURL=
SVS_TILE_PREFIX=
SVS_TILE_IMAGEURL=
LOCAL_TILE_URL="./tiles" 
DOWNLOAD_RETRY="3"
LOCAL_STORAGE="~/.cache/label-studio/"
TEST_TILE_STORAGE="../tile_image/"
```

- Use server command, please `run pip install -e .`  firstly.
```shell
# Parameter explanation:
# SAM_CHOICE: SAM model type chioce
# SAM2_CHECKPOINT: SAM model checkpoint
# SAM2_CONFIG: SAM2 config
# --env-path: enviroment value config
#...

SAM_CHOICE=SAM2 \
  SAM2_CHECKPOINT=./models/sam2_hiera_base_plus.pt \
  SAM2_CONFIG=sam2_hiera_b+.yaml  \
  mdi_sam_server run --port 9011 --log-level INFO --env-path /home/mdi/zhangcheng-dev/mdi-sam-server/.env

```

- Use shell
```shell
cd src/

SAM_DRAW_MODE=true \
SAM_CHOICE=SAM2 \
SAM2_CHECKPOINT=../models/sam2_hiera_large.pt \
SAM2_CONFIG=sam2_hiera_l.yaml \
python run_server.py run  --port 9014 --log-level INFO --env-path
```

### [API Docs](./docs/api.md)

+ Explanation: The request body adopts JSON mode, and the request header contains a token for verification
Request header: Content Type: application/JSON; token:xxxx

## Contact
If you find this project helpful, please give it a ⭐, and for any questions or issues, feel free to create an issue or email czhangcn@connect.ust.hk.

## License
This project is released under the [Apache-2.0 license](./LICENSE)

## Acknowledgement

We extend my heartfelt thanks to the developers and contributors of [Label-Studio](https://github.com/HumanSignal/label-studio), [playgroud](https://github.com/open-mmlab/playground/tree/main), [SAM](https://github.com/facebookresearch/segment-anything-2).

## Citation

If you use this software in your research, please cite it as below:
```
@misc{mdi-sam-server,
  year = {2023-2024}
  author = {Cheng ZHANG},
  publisher = {Github},
  journal = {Github repository},
  title = {{MDI SAM Server}: MDI machine learning SAM model service},
  url = {https://github.com/HKUSTMDI/mdi-sam-server},
  organization = {HKUSTMDI}
}
```