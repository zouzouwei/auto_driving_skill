# camera_bev 输入流分析报告

## 1. 总体结构

这组 fixture 实现的是一个简化版 camera-only BEV 检测流程：

`dataset.py` 负责把 6 个相机图像和标注整理成模型输入；`config.py` 定义 pipeline 和 model 结构；`model.py` 完成 `backbone -> FPN -> BEV transform -> DETR-style head -> loss / output`。

## 2. 类别与相机顺序

### Classes
代码中类别只有 4 类：
- `car`
- `truck`
- `bus`
- `pedestrian`

它们同时出现在 `config.py` 和 `dataset.py`，并且 `gt_labels_3d` 通过 `CLASSES.index(x)` 映射到类别 id。

### Camera order
相机顺序固定为：
1. `CAM_FRONT`
2. `CAM_FRONT_LEFT`
3. `CAM_FRONT_RIGHT`
4. `CAM_BACK`
5. `CAM_BACK_LEFT`
6. `CAM_BACK_RIGHT`

`dataset.py` 和 `config.py` 使用的是同一顺序，保证多视角张量拼接后索引一致。

## 3. 数据输入流

### Dataset 侧
`MiniNuScenesCameraDataset.__getitem__` 的流程是：
1. `load_annotation(idx)` 读取单个 sample 的标注与多相机元数据。
2. 按固定 `CAMERA_ORDER` 读取 6 张图像。
3. 读取每个相机的：
   - `lidar2img`
   - `cam_intrinsic`
4. 组装初始 data：
   - `img`: `torch.stack(imgs, dim=0)`，形状为 `6 x 3 x 900 x 1600`
   - `lidar2img`: `6 x ...`
   - `cam_intrinsic`: `6 x ...`
   - `gt_bboxes_3d`
   - `gt_labels_3d`
5. 送入 `pipeline(data)`。

### Pipeline 侧
`config.py` 中训练 pipeline 为：
1. `LoadMultiViewImageFromFiles`：按指定 `camera_order` 读取多视角图像。
2. `ResizeCropFlipImage`：把原始图像变换到模型输入分辨率。
3. `NormalizeMultiviewImage`：按 `img_norm_cfg` 标准化。
4. `LoadAnnotations3D`：载入 3D box 和 label。
5. `Collect3D`：收集输入与 meta 信息。

### 原始图像大小 vs 模型输入大小
- 原始图像：`900 x 1600`，这是 `load_image()` 返回的默认尺寸。
- 模型输入：`final_dim=(256, 704)`。

因此，模型真正看到的图像空间分辨率是经过 `ResizeCropFlipImage` 处理后的 `256 x 704`。

## 4. metadata 流

`Collect3D` 保留的 `meta_keys` 是：
- `lidar2img`
- `cam_intrinsic`
- `camera2ego`
- `post_rots`
- `post_trans`

其中：
- `lidar2img` 在 `model.forward()` 中被显式送入 `view_transformer`。
- 其余 meta 虽然在 `model.py` 中没有直接使用，但从 pipeline 看是为几何变换和图像到 BEV 的坐标恢复保留的。

## 5. 模型结构

### 5.1 Backbone + FPN
`MiniBEVFormer.forward()` 中：
1. 输入 `img` 形状为 `B x 6 x 3 x 256 x 704`。
2. reshape 成 `B*6 x 3 x 256 x 704`，把 batch 和 camera 维合并。
3. 送入 `img_backbone`（`ResNet-50`）。
4. 再送入 `img_neck`（`FPN`, `out_channels=256`）。
5. FPN 输出的多层特征被 reshape 回 `B x 6 x ...`。

这说明 backbone/FPN 都是逐相机独立提特征，再在后续做多视角融合。

### 5.2 BEV transform
`view_transformer` 是 `SpatialCrossAttentionBEV(bev_h=128, bev_w=128)`。

代码中它接收：
- `mlvl_feats`
- `img_metas['lidar2img']`

然后返回固定形状的 BEV 特征：
- `2 x (128*128) x 256` 的零张量（fixture 里是占位实现）

这表明它扮演的是“把多相机特征投影 / 聚合到 BEV grid”的角色，接口上与 BEVFormer 风格一致，但当前实现只是 mock。

### 5.3 Decoder / Detection head
`pts_bbox_head` 是 `DETR3DHead`：
- `num_query=300`
- `num_classes=4`

内部结构：
- `query = nn.Embedding(300, 256)`
- `cls = nn.Linear(256, 4)`
- `reg = nn.Linear(256, 10)`

前向过程：
1. 将 query 扩展到 batch 维。
2. 对每个 query 做分类和回归。
3. 输出：
   - `cls_scores`
   - `bbox_preds`

因此这里的检测头是典型的 DETR-style query decoder 接口，但代码里没有显式 transformer decoder 层，只有 query embedding + linear heads。

## 6. loss 与输出

### Training
`self.training == True` 时：
- 调用 `pts_bbox_head.loss(outs, gt_bboxes_3d, gt_labels_3d)`
- 返回：
  - `loss_cls`
  - `loss_bbox`

当前实现中两个 loss 都是 `sum() * 0`，属于占位写法，不表达真实优化目标。

### Inference
推理时：
- 调用 `pts_bbox_head.get_bboxes(outs, img_metas)`
- 直接返回 `outs`

所以 fixture 里的最终输出仍是：
- `cls_scores`
- `bbox_preds`

而不是完整的后处理框集合。

## 7. 与 paper 的关系

代码层面能直接对应到的只有这些名字和接口：
- `MiniBEVFormer` / `SpatialCrossAttentionBEV`：体现 BEV feature aggregation 的思路。
- `DETR3DHead`：体现 query-based 3D detection head。

但当前 fixture 没有实现论文中的完整 attention、decoder、matching 或真实几何投影细节，因此只能说“接口/命名与相关 paper 风格一致”，不能据此断言完整复现。

## 8. 一句话总结

这份代码的输入流是：6 路相机图像按固定顺序读取 -> resize 到 `256 x 704` -> normalize -> 收集多视角 meta -> `ResNet + FPN` 提特征 -> `BEV transform` 聚合到 `128 x 128` BEV -> `DETR3DHead` 做 300-query 分类/回归 -> 训练返回占位 loss，推理返回 `cls_scores` 和 `bbox_preds`。
