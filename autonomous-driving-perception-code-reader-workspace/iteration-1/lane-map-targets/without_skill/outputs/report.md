# Lane Map 代码报告

## 1. Lane types / 类别

代码里出现了两套类别定义：

- `config.py`：`lane_types = ['single_white_solid', 'single_white_dashed', 'double_yellow_solid', 'road_edge']`
- `dataset.py`：`LANE_TYPES` 也是同一组顺序

含义上，这四类 lane type 被当作 lane-level 分类标签使用，且**索引顺序就是类别 id**：

- `single_white_solid` -> 0
- `single_white_dashed` -> 1
- `double_yellow_solid` -> 2
- `road_edge` -> 3

`config.py` 里还定义了 `map_classes = ['lane_divider', 'road_boundary', 'ped_crossing']`，但在这三个 fixture 文件中没有进一步参与模型前向或 target 生成。

## 2. Annotation -> target conversion / 标注到训练目标

`LaneDataset.convert_lane_to_target()` 把 annotation 转成三类 target：

- `lane_points`: shape `[100, 20, 3]`
- `lane_labels`: shape `[100]`
- `lane_adj`: shape `[100, 100]`

具体流程：

1. 先初始化 100 个 query 位点的容器：
   - `lane_points = torch.zeros(100, 20, 3)`
   - `lane_labels = torch.full((100,), -1)`
2. 遍历 `anno['lanes']`，每条 lane 使用 `lane_id` 顺序写入对应 slot。
3. `sample_polyline(lane['points_ego'], num_points=20)` 负责把原始 polyline 采样成 20 个点；在这个 fixture 里它直接返回 `torch.zeros(num_points, 3)`，说明这里只保留了接口，不含真实采样逻辑。
4. `normalize_to_pc_range()` 将点归一化到 `[0, 1]`。
5. `lane_labels[lane_id] = LANE_TYPES.index(lane['type'])`，用 lane type 查表得到类别 id。
6. `lane_adj` 根据 `anno['topology']` 构造邻接矩阵：
   - `for src, dst in anno['topology']:`
   - `lane_adj[src, dst] = 1.0`

所以这里的 topology 是**有向边**表示，不是对称矩阵。

`load_annotation()` 的示例标注中：

- lane 0: `single_white_solid`
- lane 1: `single_white_dashed`
- topology: `[[0, 1], [1, 0]]`

即两条 lane 互相连通。

## 3. Coordinate frames / 坐标系

代码里能明确看到两层坐标处理：

### 3.1 Annotation uses ego frame

标注点字段是 `points_ego`，说明原始 lane 点在 **ego frame** 中表达，例如：

- `[x, y, z] = [5.0, -1.5, 0.0]`

### 3.2 pc_range normalization

`normalize_to_pc_range()` 使用：

- `pc_min = [0.0, -30.0, -2.0]`
- `pc_max = [60.0, 30.0, 4.0]`

然后做线性归一化：

- `(points - pc_min) / (pc_max - pc_min)`

这说明 target 点被映射到一个固定的 3D range 内的归一化坐标。

### 3.3 BEV grid range in pipeline

`LaneToBEVPolyline` 使用：

- `xbound=[0, 60, 0.5]`
- `ybound=[-30, 30, 0.5]`
- `num_points=20`

这和 `pc_range` 基本一致，说明训练 target 和 BEV 范围是对齐的。

## 4. BEV / IPM

`model.py` 中的 `MiniLaneMapNet` 前向路径是：

1. `img_backbone(img)` 得到 `img_feats`
2. `view_transform(img_feats, cam_intrinsic, cam_extrinsic)` 得到 `bev_feats`

配置里 `view_transform=dict(type='IPM', use_camera_calibration=True)`，所以这里使用的是 **IPM (Inverse Perspective Mapping)**，并且明确依赖 `camera calibration`：

- `cam_intrinsic`
- `cam_extrinsic`

也就是说，模型是把前视图图像特征通过几何映射投到 BEV，再在 BEV 上做 lane/polyline 预测。

## 5. Decoder / Polyline decoding

`PolylineTransformerDecoder` 是核心 lane decoder：

- `num_query=100`
- `num_points=20`
- `num_classes=4`

实现上：

- `self.query = nn.Embedding(num_query, 256)`
- `self.points = nn.Linear(256, num_points * 3)`
- `self.cls = nn.Linear(256, num_classes)`

forward 里：

- 取 `query.weight` 作为 query features
- 复制到 batch 维度
- 直接回归：
  - `points`: reshape 为 `[B, 100, 20, 3]`
  - `class_logits`: `[B, 100, 4]`

因此这个 decoder 的作用是：

- 每个 query 负责一个候选 lane/polyline
- 同时输出 **geometry** 和 **classification**

## 6. Topology head / 拓扑头

`LaneTopologyHead` 非常简化：

- 输入 `query_feats`
- 输出 `torch.matmul(query_feats, query_feats.transpose(1, 2))`

这等价于对 query 两两做相似度打分，得到 `[B, 100, 100]` 的关系矩阵。

结合 `lane_adj` 的 shape 和训练目标，可以看出它是在做 **lane-to-lane connectivity / adjacency prediction**。

## 7. Outputs / 输出

### 7.1 Training mode

`MiniLaneMapNet.forward()` 在 `self.training` 下返回：

- `loss_lane_cls = pred_logits.sum() * 0`
- `loss_lane_points = pred_points.sum() * 0`
- `loss_topology = pred_adj.sum() * 0`

这说明 fixture 只保留了 loss 的接口形式，**没有实现真实损失**，当前只是占位写法。

### 7.2 Inference mode

推理时返回：

- `lane_points`: `pred_points`
- `lane_scores`: `pred_logits.sigmoid()`
- `lane_adj`: `pred_adj.sigmoid()`

所以最终输出包含：

- lane polyline 点集
- lane 分类概率
- lane 拓扑概率矩阵

## 8. 与常见 lane map pipeline 的对应关系

从代码能直接看到的结构是：

**image -> backbone -> BEV/IPM -> polyline decoder -> topology head**

这说明该 fixture 对应的是一种典型的 lane map 预测范式：

- 用 image features 生成 BEV features
- 用 query-based decoder 预测固定数量的 lane polylines
- 再用单独的 head 预测 lane 之间的拓扑关系

但这份代码只展示了**骨架**：

- 没有完整的 matching / assignment 逻辑
- 没有真实 loss 实现
- `sample_polyline()` 还是占位实现
- 也没有后处理/NMS/阈值筛选

因此，它更像是对论文式 lane map 方法的简化接口示例，而不是完整训练实现。
