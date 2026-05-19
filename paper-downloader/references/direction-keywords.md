# 研究方向关键词库

## 使用说明

本文件包含各研究方向的关键词定义，用于论文检索。每个方向包含：
- 主要关键词（必须包含）
- 次要关键词（可选）
- 排除关键词（避免检索到）
- 相关方法/模型名称

---

## 一、自动驾驶方向

### 1. 纯视觉3D目标检测

**中文名称**: 自动驾驶_纯视觉3D目标检测

**主要关键词**:
```
"3D object detection"
"autonomous driving"
"camera-only"
"monocular"
"multi-view"
"multi-camera"
```

**次要关键词**:
```
"BEV"
"bird's eye view"
"image-only"
"vision-only"
"visual 3D detection"
"pure vision"
```

**排除关键词**:
```
"LiDAR"
"point cloud"
"radar"
"laser"
```

**相关方法**:
```
BEVFormer, BEVDepth, BEVDet, PETR, PETRv2
DETR3D, FCOS3D, MonoDLE, MonoFlex
CenterNet, FCOS, DETR
StreamPETR, Far3D, SparseFusion
```

**搜索语法示例**:
```
arXiv: all:"3D object detection" AND (all:"camera-only" OR all:"monocular" OR all:"multi-view") AND all:"autonomous driving"
```

---

### 2. BEV感知

**中文名称**: 自动驾驶_BEV感知

**主要关键词**:
```
"BEV"
"bird's eye view"
"autonomous driving"
"perception"
```

**次要关键词**:
```
"multi-camera"
"surround view"
"3D detection"
"BEV representation"
"view transform"
```

**排除关键词**:
```
"LiDAR-only"
"point cloud only"
```

**相关方法**:
```
BEVFormer, BEVDepth, BEVDet, BEVStereo
LSS, Lift-Splat-Shoot
BEVFusion, BEVPool
BEVFormerv2, BEVFormat
```

---

### 3. 多模态融合

**中文名称**: 自动驾驶_多模态融合

**主要关键词**:
```
"multi-modal fusion"
"sensor fusion"
"autonomous driving"
"camera LiDAR fusion"
```

**次要关键词**:
```
"multi-sensor"
"fusion detection"
"early fusion"
"late fusion"
"middle fusion"
```

**相关方法**:
```
BEVFusion, TransFusion, CMT
PointPainting, PointAugmenting
MVP, FUTR3D, AutoAlignV2
```

---

### 4. 车道线检测

**中文名称**: 自动驾驶_车道线检测

**主要关键词**:
```
"lane detection"
"lane marking detection"
"autonomous driving"
"lane line"
```

**次要关键词**:
```
"lane instance"
"lane segmentation"
"lane topology"
"road marking"
```

**相关方法**:
```
LaneNet, CLRNet, LaneATT
CondLaneNet, OpenLane
LaneGCN, VectorMapNet
```

---

### 5. 地图构建

**中文名称**: 自动驾驶_在线地图构建

**主要关键词**:
```
"HD map"
"online map construction"
"autonomous driving"
"vectorized map"
```

**次要关键词**:
```
"map learning"
"map element"
"lane graph"
"topology"
```

**相关方法**:
```
VectorMapNet, MapTR, MapTRv2
HDMapNet, VectorMapNet
TopoNet, OpenLane-V2
```

---

### 6. 占用预测

**中文名称**: 自动驾驶_占用预测

**主要关键词**:
```
"occupancy prediction"
"3D occupancy"
"autonomous driving"
"occupancy grid"
```

**次要关键词**:
```
"voxel prediction"
"scene completion"
"semantic occupancy"
"occupancy estimation"
```

**相关方法**:
```
SurroundOcc, Occ3D, TPVFormer
FB-OCC, CTF-Occ
MonoScene, VoxFormer
```

---

### 7. 3D语义分割

**中文名称**: 自动驾驶_3D语义分割

**主要关键词**:
```
"3D semantic segmentation"
"autonomous driving"
"point cloud segmentation"
"voxel segmentation"
```

**次要关键词**:
```
"panoptic segmentation"
"instance segmentation"
"scene understanding"
```

**相关方法**:
```
MinkUNet, SparseConv
Cylinder3D, PVKD
SphereFormer, FlatFormer
```

---

### 8. 多目标跟踪

**中文名称**: 自动驾驶_多目标跟踪

**主要关键词**:
```
"multi-object tracking"
"MOT"
"autonomous driving"
"3D tracking"
```

**次要关键词**:
```
"object tracking"
"trajectory"
"tracking by detection"
"joint detection and tracking"
```

**相关方法**:
```
AB3DMOT, CenterPoint
MUTR3D, TrackFormer
SparseTrack, QD-3DT
```

---

### 9. 运动预测

**中文名称**: 自动驾驶_运动预测

**主要关键词**:
```
"motion prediction"
"trajectory prediction"
"autonomous driving"
"agent prediction"
```

**次要关键词**:
```
"future prediction"
"behavior prediction"
"path prediction"
"multi-agent prediction"
```

**相关方法**:
```
VectorNet, HiVT, MTR
TNT, DenseTNT
QCNet, MTR++
Wayformer, MotionLM
```

---

### 10. 端到端自动驾驶

**中文名称**: 自动驾驶_端到端

**主要关键词**:
```
"end-to-end autonomous driving"
"end-to-end driving"
"autonomous driving"
"planning"
```

**次要关键词**:
```
"imitation learning"
"behavior cloning"
"world model"
"differentiable planning"
```

**相关方法**:
```
UniAD, VAD, ST-P3
BEV-Planner, PARA-Drive
ThinkTwice, GameFormer
```

---

## 二、具身智能方向

### 1. 机器人抓取

**中文名称**: 具身智能_机器人抓取

**主要关键词**:
```
"grasp planning"
"robot grasping"
"manipulation"
"grasp detection"
```

**次要关键词**:
```
"grasp pose"
"pick and place"
"6-DoF grasp"
"grasp quality"
```

**相关方法**:
```
GraspNet, Contact-GraspNet
AnyGrasp, GIGA
GNFactor, RT-2
```

---

### 2. 视觉导航

**中文名称**: 具身智能_视觉导航

**主要关键词**:
```
"visual navigation"
"embodied navigation"
"robot navigation"
"indoor navigation"
```

**次要关键词**:
```
"point goal navigation"
"object goal navigation"
"vision-language navigation"
"exploration"
```

**相关方法**:
```
Habitat, AI2-THOR, iGibson
PointNav, ObjectNav
VLN, EQA
PIVOT, SayNav
```

---

### 3. 模仿学习

**中文名称**: 具身智能_模仿学习

**主要关键词**:
```
"imitation learning"
"learning from demonstration"
"robot learning"
"behavior cloning"
```

**次要关键词**:
```
"offline reinforcement learning"
"policy learning"
"expert demonstration"
```

**相关方法**:
```
ACT, Diffusion Policy
VQ-BeT, BC-Z
RT-1, RT-2
Octo, OpenVLA
```

---

### 4. 场景理解与重建

**中文名称**: 具身智能_场景理解

**主要关键词**:
```
"3D scene understanding"
"scene reconstruction"
"embodied AI"
"3D vision"
```

**次要关键词**:
```
"scene graph"
"spatial reasoning"
"NeRF"
"3D Gaussian"
```

**相关方法**:
```
NeRF, 3D Gaussian Splatting
SceneNN, ScanNet
EmbodiedScan, LERF
ConceptFusion, ConceptGraphs
```

---

### 5. 具身大模型

**中文名称**: 具身智能_具身大模型

**主要关键词**:
```
"embodied foundation model"
"robot foundation model"
"vision language action"
"embodied AI"
```

**次要关键词**:
```
"multimodal robot"
"robot learning"
"generalist robot"
```

**相关方法**:
```
RT-2, Octo, OpenVLA
SayCan, PaLM-E
RoboFlamingo, RoboMM
π0, SpatialVLM
```

---

## 三、计算机视觉方向

### 1. 2D目标检测

**中文名称**: 计算机视觉_2D目标检测

**主要关键词**:
```
"object detection"
"2D detection"
"visual detection"
"image detection"
```

**次要关键词**:
```
"anchor-free"
"anchor-based"
"transformer detection"
"real-time detection"
```

**相关方法**:
```
DETR, Deformable DETR
YOLO系列, FCOS
DINO, CO-DETR
RT-DETR, YOLO-World
```

---

### 2. 语义分割

**中文名称**: 计算机视觉_语义分割

**主要关键词**:
```
"semantic segmentation"
"image segmentation"
"scene parsing"
"pixel classification"
```

**次要关键词**:
```
"dense prediction"
"panoptic segmentation"
"universal segmentation"
```

**相关方法**:
```
DeepLab, SegFormer
Mask2Former, OneFormer
SAM, GroundedSAM
DINOv2, EVA-02
```

---

### 3. 图像生成

**中文名称**: 计算机视觉_图像生成

**主要关键词**:
```
"image generation"
"text-to-image"
"diffusion model"
"generative model"
```

**次要关键词**:
```
"image synthesis"
"GAN"
"stable diffusion"
"controllable generation"
```

**相关方法**:
```
Stable Diffusion, DALL-E
ControlNet, IP-Adapter
SDXL, Flux
DiT, PixArt
```

---

### 4. 视觉Transformer

**中文名称**: 计算机视觉_视觉Transformer

**主要关键词**:
```
"Vision Transformer"
"ViT"
"visual transformer"
"self-attention"
```

**次要关键词**:
```
"image classification"
"pre-training"
"foundation model"
```

**相关方法**:
```
ViT, DeiT, Swin
BEiT, MAE, DINO
DINOv2, EVA, InternImage
SigLIP, CLIP
```

---

## 四、常用会议列表

### 顶级会议（Tier 1）
```
CVPR: IEEE/CVF Conference on Computer Vision and Pattern Recognition
ICCV: IEEE/CVF International Conference on Computer Vision
ECCV: European Conference on Computer Vision
NeurIPS: Neural Information Processing Systems
ICML: International Conference on Machine Learning
ICLR: International Conference on Learning Representations
```

### 机器人/自动驾驶会议
```
ICRA: IEEE International Conference on Robotics and Automation
IROS: IEEE/RSJ International Conference on Intelligent Robots and Systems
CoRL: Conference on Robot Learning
RSS: Robotics: Science and Systems
ITSC: IEEE International Conference on Intelligent Transportation Systems
IV: IEEE Intelligent Vehicles Symposium
```

### AAAI/IJCAI
```
AAAI: Association for the Advancement of Artificial Intelligence
IJCAI: International Joint Conference on Artificial Intelligence
```

---

## 五、搜索策略模板

### 基础搜索模板
```
{主要关键词1} AND {主要关键词2} AND {时间过滤}
```

### 进阶搜索模板
```
({主要关键词1} OR {次要关键词1}) AND ({主要关键词2} OR {次要关键词2}) NOT {排除关键词}
```

### 会议限定模板
```
{关键词} AND (journal:{会议缩写} OR booktitle:{会议缩写})
```

---

## 六、中文翻译参考

### 常见术语翻译
```
3D Object Detection → 3D目标检测
Autonomous Driving → 自动驾驶
BEV → 鸟瞰图
Transformer → Transformer
Attention → 注意力机制
Feature Extraction → 特征提取
Backbone → 骨干网络
Neck → 颈部网络
Head → 检测头
Loss Function → 损失函数
Ablation Study → 消融实验
State-of-the-Art → 最先进的
```

### 标题翻译示例
```
"BEVFormer: Learning Bird's-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers"
→ "BEVFormer: 通过时空Transformer从多相机图像学习鸟瞰图表示"

"BEVDepth: Acquisition of Reliable Depth for Multi-view 3D Object Detection"
→ "BEVDepth: 多视角3D目标检测的可靠深度获取"

"PETR: Position Embedding Transformation for Multi-View 3D Object Detection"
→ "PETR: 用于多视角3D目标检测的位置嵌入变换"
```
