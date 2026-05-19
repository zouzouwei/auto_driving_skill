# 自动驾驶核心论文清单

## 经典基础论文

### 点云处理
- **PointNet**: Deep Learning on Point Sets for 3D Classification and Segmentation (CVPR 2017)
- **PointNet++**: Deep Hierarchical Feature Learning on Point Sets in a Metric Space (NeurIPS 2017)
- **DGCNN**: Dynamic Graph CNN for Learning on Point Clouds (TOG 2019)

### 3D目标检测
- **VoxelNet**: End-to-End Learning for Point Cloud Based 3D Object Detection (CVPR 2018)
- **SECOND**: Sparsely Embedded Convolutional Detection (Sensors 2018)
- **PointPillars**: Fast Encoders for Object Detection from Point Clouds (CVPR 2019)
- **CenterPoint**: Center-based 3D Object Detection and Tracking (CVPR 2021)

### BEV感知
- **LSS**: Lift, Splat, Shoot: Encoding Images from Arbitrary Camera Rigs by Implicitly Unprojecting to 3D (ECCV 2020)
- **BEVDet**: High-Performance Multi-Camera 3D Object Detection in Bird-Eye-View (arXiv 2021)
- **BEVDepth**: Acquisition of Reliable Depth for Multi-view 3D Object Detection (AAAI 2023)
- **BEVFormer**: Learning Bird's-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers (ECCV 2022)

### Transformer检测
- **DETR**: End-to-End Object Detection with Transformers (ECCV 2020)
- **Deformable DETR**: Deformable Transformers for End-to-End Object Detection (ICLR 2021)
- **DETR3D**: 3D Object Detection from Multi-view Images via 3D-to-2D Queries (CoRL 2021)
- **PETR**: Position Embedding Transformation for Multi-View 3D Object Detection (ECCV 2022)

### 多模态融合
- **BEVFusion**: Multi-Task Multi-Sensor Fusion with Unified Bird's-Eye View Representation (ICRA 2023)
- **TransFusion**: Robust LiDAR-Camera Fusion for 3D Object Detection with Transformers (CVPR 2022)
- **CMT**: Cross-Modal Transformer for End-to-End Multimodal Detection (NeurIPS 2022)

## 车道线/地图感知

### 车道线检测
- **LaneNet**: Towards End-to-End Lane Detection (IV 2018)
- **CLRNet**: Cross Layer Refinement Network for Lane Detection (CVPR 2022)
- **OpenLane**: Urban Scene Topology Reasoning (CVPR 2023)

### 地图元素感知
- **VectorMapNet**: End-to-End Vectorized HD Map Learning (ICML 2023)
- **MapTR**: Structured Modeling and Learning for Online Vectorized HD Map Construction (ICLR 2023)
- **MapTRv2**: An End-to-End Framework for Online Vectorized HD Map Construction (arXiv 2023)

## 运动预测

### 轨迹预测
- **VectorNet**: Encoding HD Maps and Agent Dynamics from Vectorized Representation (CVPR 2020)
- **TNT**: Target-driveN Trajectory Prediction (CoRL 2020)
- **HiVT**: Hierarchical Vector Transformer for Multi-Agent Motion Prediction (CVPR 2022)
- **MTR**: Motion Transformer with Global Intention Localization and Local Movement Refinement (NeurIPS 2022)

## 占用网格预测

### 3D占用预测
- **SurroundOcc**: Multi-camera 3D Occupancy Prediction for Autonomous Driving (ICCV 2023)
- **Occ3D**: A Large-Scale 3D Occupancy Prediction Benchmark for Autonomous Driving (NeurIPS 2023)
- **TPVFormer**: Tri-perspective View for Vision-Based 3D Semantic Occupancy Prediction (CVPR 2023)

## 最新进展 (2024-2025)

### CVPR 2024
- **StreamPETR**: Exploring Object-Centric Temporal Modeling for Efficient Multi-View 3D Object Detection
- **Far3D**: Expanding the Horizon for Surround-view 3D Object Detection
- **SparseFusion**: Fusing Multi-Modal Sparse Representations for Multi-Sensor 3D Object Detection

### ICCV 2023
- **BEVFormer v2**: Adapting Modern Image Backbones to Bird's-Eye-View Recognition via Perspective Supervision
- **UniAD**: Planning-oriented Autonomous Driving (Best Paper)

### ECCV 2022
- **BEVFormer**: Learning Bird's-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers
- **PETR**: Position Embedding Transformation for Multi-View 3D Object Detection

## 综述论文

### 3D检测综述
- **3D Object Detection for Autonomous Driving: A Comprehensive Survey** (IJCV 2023)
- **Deep Learning for 3D Point Clouds: A Survey** (TPAMI 2021)

### BEV感知综述
- **Vision-Centric BEV Perception: A Survey** (arXiv 2022)
- **BEV Perception for Autonomous Driving: A Survey** (arXiv 2023)

### 自动驾驶综述
- **Autonomous Driving: A Comprehensive Survey** (IEEE 2023)
- **Deep Learning for Autonomous Driving: A Survey** (arXiv 2023)

## 按任务分类

### 纯视觉3D检测
- DETR3D, PETR, BEVFormer, BEVDet, BEVDepth, StreamPETR, Far3D

### LiDAR 3D检测
- PointPillars, CenterPoint, Part-A2, PV-RCNN, Voxel-RCNN

### 多模态融合
- BEVFusion, TransFusion, CMT, PointPainting, PointAugmenting

### 车道线检测
- LaneNet, CLRNet, OpenLane, LaneATT, CondLaneNet

### 地图构建
- VectorMapNet, MapTR, MapTRv2, HDMapNet, VectorMapNet

### 运动预测
- VectorNet, TNT, HiVT, MTR, QCNet, MTR++

### 占用预测
- SurroundOcc, Occ3D, TPVFormer, FB-OCC, CTF-Occ

## 推荐阅读路线

### 入门路线
1. PointNet → PointNet++ → VoxelNet → PointPillars
2. DETR → Deformable DETR → DETR3D
3. LSS → BEVDet → BEVDepth → BEVFormer

### 进阶路线
1. CenterPoint → BEVFusion → TransFusion
2. PETR → StreamPETR → Far3D
3. VectorNet → HiVT → MTR

### 研究前沿
1. 关注CVPR/ICCV/ECCV/NeurIPS最新论文
2. 关注nuScenes/Waymo排行榜最新方法
3. 关注arXiv上的最新预印本
