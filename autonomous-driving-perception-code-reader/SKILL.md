---
name: autonomous-driving-perception-code-reader
description: Use this skill whenever the user asks Claude to read, analyze, explain, review, or improve code for autonomous-driving perception systems, including 3D vision, camera-only BEV models, LiDAR/point-cloud perception, lane detection, lane topology, map element perception, occupancy, detection, segmentation, tracking, or multi-sensor fusion. Trigger strongly for prompts about understanding model input/output, dataset pipelines, tensor shapes, BEV transforms, feature extractors, heads/decoders, loss targets, label definitions, paper-to-code mapping, or future research improvements in autonomous-driving perception code, even if the user only says "帮我读这个模型", "解释这个感知代码", "看一下数据流", or "这个网络怎么工作的".
---

# Autonomous-driving perception code reading

Use this skill to turn perception code into a clear technical explanation that connects engineering details, tensor/data flow, algorithm design, and related papers.

Default response style: Chinese explanation with important English terms preserved, such as `dataset`, `pipeline`, `BEV transform`, `decoder`, `query`, `anchor`, `voxel`, `pillar`, `polyline`, `lane topology`, `loss`, and paper/model names.

## Core workflow

1. Identify the perception task and modality before explaining details.
   - Task: 3D object detection, lane detection, lane topology, map element perception, occupancy prediction, segmentation, tracking, prediction, or fusion.
   - Modality: camera/image, LiDAR/point cloud, radar, multi-view camera, camera-LiDAR fusion, temporal BEV, or map prior.
   - Framework family if visible: MMDetection3D/OpenMMLab, Detectron-style, PyTorch Lightning, custom PyTorch, ROS, TensorRT deployment, ONNX, CUDA plugins.

2. Trace data input first. The model architecture explanation is incomplete until the dataset and target construction are understood.
   - Locate dataset classes, annotation loading, transforms/augmentations, collate functions, samplers, and dataloader config.
   - Follow one sample from raw files to model-ready tensors.
   - Record key files and line references when available.
   - State unknowns explicitly instead of guessing.

3. Then trace model flow in order.
   - Input tensors and metadata.
   - Backbone / feature extractor.
   - Neck / FPN / multi-scale feature aggregation.
   - View transform / BEV transform / voxelization / pillarization if present.
   - Temporal fusion, ego-motion compensation, or memory bank if present.
   - Encoder, decoder, transformer blocks, attention, or query update logic.
   - Heads, output parameterization, losses, matching/assignment, and post-processing.

4. Connect code to papers and later work.
   - If the repository includes paper names, configs, README references, citations, or method names, use them first.
   - If not enough information is local and web access is available, search for the model/method and relevant follow-up papers.
   - Explain what the paper contribution is, where it appears in code, what engineering compromises are visible, and what later papers improved.
   - Do not fabricate citations. If a relationship is only likely, label it as likely and explain what evidence would confirm it.

5. Finish with model outputs and practical modification guidance.
   - Explain output tensors, coordinate frames, label meanings, confidence/logit interpretation, post-processing, visualization format, and deployment-facing APIs.
   - Suggest concrete improvement directions tied to the identified bottleneck, not generic ideas.

## Dataset and input checklist

### Camera / 3D vision / BEV perception

When the code is camera-based, multi-view, or 3D vision:

- Dataset identity and class taxonomy:
  - Dataset name: nuScenes, Waymo, KITTI, Argoverse, OpenLane, ONCE, BDD100K, internal dataset, etc.
  - Detection/map/lane class names and class count.
  - Whether background/ignore classes exist.
- Image input details:
  - Number of cameras and camera order, such as front, front-left, front-right, back, back-left, back-right.
  - Raw image size and resized/cropped/padded model input size.
  - Channel order and normalization: RGB/BGR, mean/std, padding divisor.
  - Multi-scale or test-time augmentation behavior.
- Geometry and calibration:
  - Intrinsics, extrinsics, lidar2img, camera2ego, ego2global, post-augmentation matrices.
  - Coordinate frame conventions: camera, LiDAR, ego, global, BEV grid.
  - Whether augmentations correctly update calibration matrices.
- Temporal inputs:
  - Queue length, frame interval, previous BEV, ego-motion alignment, can bus / odometry metadata.
- Target construction:
  - 3D boxes, map vectors, masks, depth supervision, occupancy grids, center heatmaps, anchors, queries, or segmentation labels.

### LiDAR / point cloud perception

When the code uses LiDAR or point cloud data:

- Point dimension and meaning:
  - 4D is commonly `(x, y, z, intensity)`.
  - 5D may add timestamp, elongation, ring index, or other dataset-specific feature. Verify from loader code, do not assume.
  - Note whether features include relative offsets, distance, sweep index, or one-hot sensor id after preprocessing.
- Range and filtering:
  - `point_cloud_range`, voxel size, max points per voxel, max voxels, ground removal, sweep aggregation.
- Representation:
  - Raw points, voxels, pillars, range image, sparse tensor, BEV pseudo-image, or hybrid.
- Coordinate frames:
  - LiDAR frame vs ego/global, sweep alignment, yaw convention, box origin convention.
- Target construction:
  - Anchor assignment, center-based heatmaps, object size/yaw encoding, velocity targets, segmentation masks, occupancy labels.

### Lane / lane topology / map perception

When the code is about lanes, lane lines, lane centerlines, topology, or HD-map elements:

- Lane taxonomy and definitions:
  - Lane line type, boundary type, color, solid/dashed, road edge, stop line, crosswalk, divider, centerline, intersection rules.
  - Whether labels are 2D image lanes, 3D lanes, BEV polylines, graph nodes/edges, or vector map elements.
- Coordinate conversion:
  - Raw annotation to image coordinates, ego coordinates, BEV grid, normalized model coordinates, or spline/polyline control points.
  - Homography/IPM, camera calibration, ground-plane assumption, or learned BEV transform.
- Model input target conversion:
  - Point sampling strategy, ordering of lane points, padding/masks, lane instance ids, positive/negative matching, topology adjacency matrix.
- Output interpretation:
  - Polyline points, lane existence scores, category logits, graph edges, topology scores, NMS/merging, post-fit splines.

## Model explanation checklist

For each major module, explain these five items:

1. What enters and leaves the module: tensor shape, coordinate frame, dtype if relevant.
2. What algorithmic role it plays: feature extraction, view lifting, BEV aggregation, query reasoning, decoding, matching, or loss.
3. What paper idea it likely implements and the evidence from code/config names.
4. Why the design may help: accuracy, geometry consistency, temporal stability, speed, memory, data efficiency.
5. How it could be improved: cite known later directions if verified, or provide code-grounded suggestions.

Common autonomous-driving perception components to look for:

- Image backbone: ResNet, Swin, ConvNeXt, ViT, InternImage, custom CNN.
- Neck: FPN, BiFPN, deformable attention feature aggregation.
- Depth/view transform: Lift-Splat-Shoot, BEVDepth, BEVDet, BEVFormer-style spatial cross-attention, PETR/position embedding, GKT, homography/IPM.
- LiDAR encoder: VoxelNet, SECOND, PointPillars, Dynamic Voxelization, SparseConv, PointNet++, CenterPoint.
- Fusion: BEVFusion, TransFusion, CMT, point-image decoration, attention fusion, late fusion.
- Decoder/head: DETR-style object queries, center heatmap heads, anchor heads, transformer decoder, map vector decoder, lane graph decoder.
- Loss/matching: Hungarian matching, focal loss, L1/GIoU/IoU, direction loss, depth loss, segmentation CE/Dice, topology BCE, Chamfer distance for polylines.
- Post-processing: score threshold, NMS, circle NMS, top-k, box decode, coordinate transform, lane stitching, graph pruning.

## Paper-linking guidance

When linking papers, use a layered approach:

1. Local evidence:
   - Search README, config names, comments, class names, checkpoint names, citation files, paper links, and module names.
2. Code-to-paper mapping:
   - Identify which file implements which paper component.
   - Explain the exact delta if the code modifies the original paper idea.
3. Later improvements:
   - Search for later papers only after the local method is identified.
   - Prefer papers that improve the same bottleneck: view transformation, temporal fusion, depth supervision, sparse representation, decoder design, lane topology, vectorization, deployment speed, or data scaling.
4. Be careful:
   - Do not present paper ancestry as fact without evidence.
   - Use phrases like "从命名和结构看，可能借鉴..." when uncertain.
   - If web search is unavailable, say what keywords the user can search.

## Recommended output structure

Use this structure unless the user asks for something else:

```markdown
## 1. 任务与总体结论
- 任务类型：...
- 输入模态：...
- 代码主路径：...
- 一句话总结：...

## 2. 数据集与输入解构
### 2.1 数据来源与类别定义
### 2.2 原始数据到模型输入的数据流
### 2.3 关键张量 / metadata / 坐标系
### 2.4 目标构造与监督信号

## 3. 模型结构与算法流程
### 3.1 输入接口
### 3.2 Feature extractor / backbone / neck
### 3.3 BEV transform / voxelization / temporal fusion
### 3.4 Encoder / decoder / head
### 3.5 Loss、matching 与 post-processing

## 4. 论文对应关系与改进点
- 原始/相关论文：...
- 代码中对应位置：...
- 这里相比常规方法的改进：...
- 为什么这样改：...
- 后续论文或可改方向：...

## 5. 模型输出解释
- 输出字段 / tensor shape：...
- 坐标系与单位：...
- 类别、score、uncertainty：...
- 后处理和可视化：...

## 6. 工程风险与建议
- shape/坐标/标注定义风险：...
- 训练/部署风险：...
- 建议优先验证：...
```

Keep explanations grounded in files and code. Include `path:line` references for important claims whenever possible.

## Reading strategy for large repos

- Start from configs, training scripts, model registry, dataset registry, and README.
- Use code search for dataset class names, `__getitem__`, `prepare_train_data`, `pipeline`, `collate`, `forward`, `loss`, `decode`, `post_process`, `get_bboxes`, `simple_test`, `predict`, `export`, and `visualize`.
- For OpenMMLab-style repos, trace config `_base_`, `data.train`, `train_pipeline`, `model`, `pts_bbox_head`, `img_backbone`, `view_transformer`, `bbox_coder`, and `test_cfg`.
- For custom PyTorch repos, trace from `train.py`/`main.py` to dataloader, model construction, forward pass, loss, validation, and export/inference.
- If the repo is too large, produce a first-pass map and ask which module to deep-dive next.

## Quality bar

A good answer should help the user answer all of these:

- What exactly is fed into the model?
- What are the label definitions and target conversions?
- What are the core tensors and their shapes across the network?
- Where does camera/LiDAR/lane geometry enter the computation?
- Which parts correspond to known papers, and what changed in this implementation?
- What does the model output mean physically and in code?
- What should be checked first before modifying or improving the model?
