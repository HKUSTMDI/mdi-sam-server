# mdi-ml-sam
mdi machine learning  SAM model service

# 接口文档
+ 说明:请求体采用json方式，请求头中包含token进行验证 
请求头:Content-Type:application/json;token:xxxx
## 1.pre_download 
- 接口说明:在使用sam模型进行自动标注前，前端加载过程中，调用后端提前下载图片。
- method:**POST,GET**
- URL:```${prefix_url}/pre_download```
- body

参数名|类型|出现要求|描述
---|---|---|---
url|string|是|需要预下载图片的url

### request
Headers:
Content-Type:application/json;token:test
```
{
  "url":"xxxx"
}
```
### response
```
{
  "code": 200,
  "msg": "ok"
}
```
## 2.predict
- 接口说明: 使用sam模型获取指定url图片的mas。如果url中的图片为经过pre_download下载，将会在本接口重新下载，届时将增加时耗，请先调用pre_download接口下载图片。
- method:**POST**
- URL:```${prefix_url}/predict```
- body

参数名|类型|出现要求|描述
---|---|---|---
url|string|是|指定的图片
model_version|string|否|sam模型类型,默认使用mobile_sam
task_id|string|是|任务id，同一个task id需要串行调用
[params](#params参数)|json|是|参数

### params参数


```
原生接口:
keypoint:
{   "login": null,
    "password": null,
    "context": {
        "result": [
            {
                "original_width": 3840,
                "original_height": 2160,
                "image_rotation": 0,
                "value": {
                    "x": 80.3072625698324,
                    "y": 43.67245657568238,
                    "width": 0.27932960893854747,
                },
                "is_positive": true,
                "id": "Gi5wQhzp-f",
                "from_name": "KeyPointLabels",
                "to_name": "image",
                "type": "keypointlabels", #类型1:keypointlabels点标注,2:rectanglelabels方框标注
                "origin": "manual"
            }
        ]
    }
}

rectangle:
{
    "login": null,
    "password": null,
    "context": {
        "result": [
            {
                "original_width": 1200,
                "original_height": 800,
                "image_rotation": 0,
                "value": {
                    "x": 4.463040446304045,
                    "y": 60.25104602510462,
                    "width": 19.107391910739192,
                    "height": 12.343096234309623,
                    "rotation": 0,
                    "rectanglelabels": [
                        "person"
                    ]
                },
                "id": "xtiVfciBUc",
                "from_name": "RectangleLabels",
                "to_name": "image",
                "type": "rectanglelabels",
                "origin": "manual"
            }
        ]
    }
}

原参数参考:
 "lead_time": 31.06, "was_postponed": false, "created_at": "2023-10-10T05:51:52.918761Z", "updated_at": "2023-10-10T05:52:45.101563Z", "task": 2, "annotation": null}], "predictions": [], "data": {"image": "/data/upload/1/b8c2e0a4-cat.jpg"}, "meta": {}, "created_at": "2023-09-22T07:39:29.196959Z", "updated_at": "2023-09-22T08:00:55.258384Z", "inner_id": 2, "total_annotations": 1, "cancelled_annotations": 0, "total_predictions": 0, "comment_count": 0, "unresolved_comment_count": 0, "last_comment_updated_at": null, "project": 1, "updated_by": 1, "comment_authors": []}], "model_version": "1696915632", "project": "1.1695368091", "label_config": "<View>\n  <Image name=\"image\" value=\"$image\" zoom=\"true\"/>\n  <KeyPointLabels name=\"KeyPointLabels\" toName=\"image\">\n    <Label value=\"cat\" smart=\"true\" background=\"#e51515\" showInline=\"true\"/>\n    <Label value=\"person\" smart=\"true\" background=\"#412cdd\" showInline=\"true\"/>\n  </KeyPointLabels>\n  <RectangleLabels name=\"RectangleLabels\" toName=\"image\">\n  \t<Label value=\"cat\" background=\"#FF0000\"/>\n  \t<Label value=\"person\" background=\"#0d14d3\"/>\n  </RectangleLabels>\n  <PolygonLabels name=\"PolygonLabels\" toName=\"image\">\n  \t<Label value=\"cat\" background=\"#FF0000\"/>\n  \t<Label value=\"person\" background=\"#0d14d3\"/>\n  </PolygonLabels>\n  <BrushLabels name=\"BrushLabels\" toName=\"image\">\n  \t<Label value=\"cat\" background=\"#FF0000\"/>\n  \t<Label value=\"person\" background=\"#0d14d3\"/>\n  </BrushLabels>\n</View>", "params": {"login": null, "password": null, "context": {"result": [{"original_width": 1200, "original_height": 800, "image_rotation": 0, "value": {"x": 4.463040446304045, "y": 60.25104602510462, "width": 19.107391910739192, "height": 12.343096234309623, "rotation": 0, "rectanglelabels": ["person"]}, "id": "xtiVfciBUc", "from_name": "RectangleLabels", "to_name": "image", "type": "rectanglelabels", "origin": "manual"}]}}}

 图片路径:
 ./home/mdi/.local/share/label-studio/media/upload/1/b8c2e0a4-cat.jpg
```
### request
Headers:
Content-Type:application/json;token:test
```
{
  "url":"xxxx"
}
```
### response
```
{
  "code": 200,
  "msg": "ok",
  "data": {
    "rle":[],
    "bbox":[]
  }
}
```

## 3.health_check
method:**GET**
URL:```${prefix_url}/health_check```


