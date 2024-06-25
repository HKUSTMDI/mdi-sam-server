# mdi-ml-sam
MDI annotation platform SAM real-time recognition server ⚡ .
Current support:
- (1) 🌟 Real time annotation: multi-point annotation, single rectangle annotation
- (2) 🔥 Prompt with different positive and negative values
- (3) 🐬 the Whole Llide Image recognition

### WSI segmentation annotation
<img src="./docs/wsi_segmentation.gif" width="75%"/>

### point & rectangle模式
<p float="left">
  <br>
  <img src="./docs/demo_point1.jpg" width="37.25%" />
  <img src="./docs/demo_point2.jpg" width="37.25%" />
  <br>
  <img src="./docs/demo_rectangle1.jpg" width="37.25%" /> <img src="./docs/demo_rectangle2.jpg" width="37.25%" />
</p>

### Supporting models:
  - 1.**[Meta SAM](https://github.com/facebookresearch/segment-anything)** (default service)
  - 2.**[mobile_sam](https://github.com/ChaoningZhang/MobileSAM)**
  - 3.**ONNX** mode
## Installation
The Python used in the development process of this version is 3.10.12. Please use this version or an updated version.
### [API Docs](./docs/接口文档.md)
+ Explanation: The request body adopts JSON mode, and the request header contains a token for verification
Request header: Content Type: application/JSON; token:xxxx
