# lane_map 代码阅读报告

## 1. 任务与总体结论

这份 fixture 是一个很小的“单目车道线 / 地图元素矢量化感知”原型，核心目标是把前视图图像中的 lane 以**polyline** 形式预测出来，同时再预测 lane 之间的 **topology graph**。

- 代码主路径：`config.py` 里定义数据流水线和模型骨架，`dataset.py` 负责把原始标注变成训练 target，`model.py` 里串起 backbone、IPM/BEV、polyline decoder 和 topology head。
- 任务类型：更偏向 **lane detection + lane topology prediction**，而不是像素级分割。
- 输入模态：单前视图图像 + 相机标定信息 + 3D lane 标注（ego 坐标系）。
- 一句话总结：这不是一个完整可训练的实现，而是一个**结构非常清楚的教学版 skeleton**；它把“车道类型、点序、BEV 归一化、polyline 输出、topology 矩阵”这些核心概念都摆出来了，但 decoder / loss / resampling 都是简化甚至占位实现。

关键文件：
- `config.py:0-17`
- `dataset.py:0-33`
- `model.py:3-39`

## 2. 数据集与标注

### 2.1 车线类型与 lane definition

`config.py:0-1` 定义了两层 taxonomy：

- `lane_types = ['single_white_solid', 'single_white_dashed', 'double_yellow_solid', 'road_edge']`
- `map_classes = ['lane_divider', 'road_boundary', 'ped_crossing']`

结合 `dataset.py:4-24`，这份代码里真正被用到的是 `lane_types`，也就是每一条 lane instance 都有一个**线型类别**。当前 fixture 中：

- lane 的“实例”不是图像里的像素连通域，而是一个**有序点列** `points_ego`
- 每条 lane 还带一个 `type`
- 另外还有 `topology`，表示 lane 与 lane 之间的连接关系

也就是说，这里的 lane definition 是：

> `lane = { type, ordered polyline points in ego frame, topology relations }`

`map_classes` 更像是未来要扩展到更广义 map element perception 时的类别集合，但在这份最小代码里没有真正接入训练目标。

### 2.2 原始标注长什么样

`dataset.py:5-12` 的 `load_annotation` 返回的原始标注是：

```python
{
  'lanes': [
    {'type': 'single_white_solid', 'points_ego': [[5.0, -1.5, 0.0], [20.0, -1.2, 0.0], [45.0, -1.0, 0.0]]},
    {'type': 'single_white_dashed', 'points_ego': [[4.0, 1.5, 0.0], [25.0, 1.4, 0.0], [55.0, 1.2, 0.0]]},
  ],
  'topology': [[0, 1], [1, 0]],
}
```

这里最重要的三个点：

1. **坐标系是 ego frame**
   - 这通常意味着 `x` 轴朝车前方，`y` 轴朝左，`z` 轴朝上。
   - 代码没有显式写出坐标约定，但从 `pc_range=[0, -30, -2, 60, 30, 4]` 可以看出，模型关心的是前方 0~60m、横向 -30~30m 的 BEV 范围。

2. **点序是有方向的**
   - 例子里的点是从近到远：`x=5 -> 20 -> 45`，说明 lane polyline 的点序应该沿着行驶方向/车前方向排序。
   - 代码里没有额外排序逻辑，所以默认输入标注已经按正确顺序给出。

3. **topology 是 lane-to-lane 的边**
   - `[[0, 1], [1, 0]]` 表示 lane 0 和 lane 1 之间存在双向连接。
   - 这更像一个 adjacency list，而不是 segmentation 标签。

### 2.3 从原始标注到模型 target

真正的 target 构造逻辑在 `dataset.py:14-24`：

#### 第一步：固定长度化

```python
lane_points = torch.zeros(100, 20, 3)
lane_labels = torch.full((100,), -1, dtype=torch.long)
```

含义：

- 最多保留 100 条 lane hypothesis / lane slot
- 每条 lane 固定成 20 个点
- 每个点 3 维 `(x, y, z)`
- 没有被占用的 lane slot 用 `-1` 作为 label

#### 第二步：polyline 重采样

```python
sampled = self.sample_polyline(lane['points_ego'], num_points=20)
```

这里语义上是：

- 把原始稀疏点列重采样成固定 20 点
- 保持点序不变
- 让不同长度、不同采样密度的 lane 进入统一的输出格式

但要注意：`sample_polyline` 在 fixture 里只是 `return torch.zeros(num_points, 3)`，也就是占位实现。真正项目里应该会做线段插值、按弧长均匀采样，或者 spline 采样。

#### 第三步：坐标归一化到 pc range

```python
lane_points[lane_id] = self.normalize_to_pc_range(sampled)
```

归一化公式在 `dataset.py:29-33`：

```python
(points - pc_min) / (pc_max - pc_min)
```

其中：

- `pc_min = [0.0, -30.0, -2.0]`
- `pc_max = [60.0, 30.0, 4.0]`

所以输出点被映射到近似 `[0,1]` 范围，便于网络回归。

这一步很关键，因为它说明了 target 并不是直接回归米制坐标，而是回归**归一化后的 BEV/pc-range 坐标**。

#### 第四步：类别标签与拓扑矩阵

```python
lane_labels[lane_id] = LANE_TYPES.index(lane['type'])
```

- `lane_labels` 是每条 lane 的类别 id
- 类别空间就是 4 个 lane type

拓扑矩阵：

```python
lane_adj = torch.zeros(100, 100)
for src, dst in anno['topology']:
    lane_adj[src, dst] = 1.0
```

- `lane_adj[i, j] = 1` 表示 lane i 与 lane j 有连接关系
- 这里是一个 dense adjacency matrix
- 在这个 fixture 中，`topology` 是监督信号，最终 target 变成 `100 x 100` 的矩阵

#### 第五步：送入训练 batch

`config.py:3-9` 的 pipeline 最终收集：

- `img`
- `lane_points`
- `lane_labels`
- `lane_adj`

这里有一个值得注意的工程缺口：`model.py:11` 的 `forward` 其实还需要 `cam_intrinsic` 和 `cam_extrinsic`，但 `config.py` 的 `Collect` 并没有把这些 metadata 明确收集出来。也就是说，**IPM 需要标定，但当前 pipeline 没把标定流完整接上**。

## 3. 模型结构与数据流

### 3.1 image backbone

`config.py:11-17` 里 backbone 是 `SwinTransformer`，对应 `model.py:12`：

```python
img_feats = self.img_backbone(img)
```

作用很直接：

- 输入是前视图图像 `img`
- backbone 提取多尺度图像特征
- 这一步还在 image space，没有进入 BEV

从配置看，这里是**单目 front view**，不是多相机环视。

### 3.2 IPM / BEV

`config.py:14` 里是：

```python
view_transform=dict(type='IPM', use_camera_calibration=True)
```

`model.py:13`：

```python
bev_feats = self.view_transform(img_feats, cam_intrinsic, cam_extrinsic)
```

这表示它想做的是 **Inverse Perspective Mapping / BEV transform**：

- 利用相机内参和外参，把透视图特征投影到地面 BEV 平面
- 这样 lane 的几何关系更接近欧式空间，便于 polyline 回归和 topology 预测

从命名上看，这个模块依赖真实标定，因此 `cam_intrinsic` / `cam_extrinsic` 是必需输入。

不过要特别指出：在当前 `PolylineTransformerDecoder` 的简化实现里，`bev_feats` 只是传进去了，但 decoder 并没有真正使用它做 attention 或 sampling。这说明 fixture 里的 BEV 只是**结构占位**，不是完整算法实现。

### 3.3 polyline decoder

`config.py:15`：

```python
lane_decoder=dict(type='PolylineTransformerDecoder', num_query=100, num_points=20)
```

`model.py:26-35` 是 decoder 的实现：

```python
self.query = nn.Embedding(num_query, 256)
self.points = nn.Linear(256, num_points * 3)
self.cls = nn.Linear(256, num_classes)
```

forward 时：

```python
q = self.query.weight.unsqueeze(0).repeat(bev_feats.size(0), 1, 1)
return {
    'query_feats': q,
    'points': self.points(q).reshape(bev_feats.size(0), 100, 20, 3),
    'class_logits': self.cls(q)
}
```

这表示：

- 100 个 learnable queries
- 每个 query 代表一条 lane hypothesis
- 每个 query 回归 20 个点，每点 3 维
- 同时输出 4 类 logits

所以这个 decoder 的输出本质上是：

- **polyline geometry**：`[B, 100, 20, 3]`
- **lane class logits**：`[B, 100, 4]`
- **query embedding**：`[B, 100, 256]`

这里有两个非常重要的理解点：

1. **这是 query-based vectorized representation**
   - 每个 query 对应一个 lane proposal
   - 不是逐像素预测
   - 和 DETR / MapTR 风格的 vectorized map perception 思路很接近

2. **当前实现没有真正利用 BEV 特征**
   - 正常 decoder 应该用 BEV features 去更新 query
   - 这里却直接把 `query.weight` 复制出来并线性回归
   - 所以它更像“接口骨架”，而不是可工作的 decoder

### 3.4 topology head

`config.py:16`：

```python
topology_head=dict(type='LaneTopologyHead')
```

`model.py:37-39`：

```python
def forward(self, query_feats):
    return torch.matmul(query_feats, query_feats.transpose(1, 2))
```

它做的是 query 之间的两两相似度：

- 输入：`[B, 100, 256]`
- 输出：`[B, 100, 100]`

含义上可以解释为：

- `pred_adj[i, j]` 越大，lane i 与 lane j 越可能存在拓扑关系
- 经过 `sigmoid` 后可视作边存在概率

但这里也有一个明显限制：

- `q @ q^T` 天然是**对称矩阵**
- 因此它不擅长表达严格的有向拓扑
- 如果真实任务需要 `predecessor -> successor` 这种方向性关系，当前 head 还不够

这也是 lane topology 里常见的难点：

- 几何相邻不等于拓扑相连
- 交叉口、分叉、合流都需要显式关系建模

### 3.5 loss 与训练逻辑

`model.py:18-23` 里的 loss 是纯占位：

```python
return {
    'loss_lane_cls': pred_logits.sum() * 0,
    'loss_lane_points': pred_points.sum() * 0,
    'loss_topology': pred_adj.sum() * 0,
}
```

这意味着：

- 没有真实的 Hungarian matching
- 没有 polyline Chamfer / L1 loss
- 没有 topology BCE / focal loss
- 只是为了保持接口形式完整

所以这份代码最适合用来理解**数据流和张量语义**，不适合直接推断训练效果。

## 4. 模型输出分别表示什么

`model.py:24` 的推理输出是：

```python
{
  'lane_points': pred_points,
  'lane_scores': pred_logits.sigmoid(),
  'lane_adj': pred_adj.sigmoid()
}
```

### 4.1 `lane_points`

- 形状：`[B, 100, 20, 3]`
- 含义：每个 query 对应一条 polyline 候选
- 20 个点表示一条 lane 的固定采样序列
- 3 维坐标通常可理解为 `(x, y, z)` 的归一化形式

如果做完整系统，一般需要再把它反归一化回 ego/BEV 米制坐标，再做可视化和后处理。

### 4.2 `lane_scores`

- 形状：`[B, 100, 4]`
- 含义：每条 lane query 的类别置信度
- 这里是对 4 个 `lane_types` 做 sigmoid 后的结果

所以它不是单一 scalar score，而是**类别概率向量**。

### 4.3 `lane_adj`

- 形状：`[B, 100, 100]`
- 含义：lane query 两两之间的拓扑连接概率
- 适合表示 lane graph / adjacency graph

在这份实现里，它更像“关系矩阵”而不是精细的 graph decoder 输出。

## 5. 论文与相关方向：lane topology / vectorized map perception

下面这部分因为当前环境没有成功启用 web search，所以我只能基于已知文献记忆给出**代表性方向**。这些名字和分类建议再人工检索确认，但方向本身是对的。

### 5.1 专门做 lane topology 的代表性方向

- **TopoNet**：强调 lane geometry 之外的 topology 关系建模，是“lane topology prediction”里很典型的一类工作。
- **Topology-aware lane detection 系列**：核心思想是把 lane 之间的连接、前驱后继、分叉合流显式纳入模型，而不是只输出单条线。
- **Lane graph / lane GNN 类方法**：通过图结构在 lane instance 之间做消息传递，用于提升交叉口和复杂道路场景下的拓扑一致性。

如果你后续要继续查，关键词建议直接搜：

- `lane topology prediction`
- `topology-aware lane detection`
- `lane graph reasoning`
- `lane adjacency matrix`

### 5.2 vectorized map perception 的代表性方向

- **MapTR**：非常典型的 vectorized HD map perception 方法，用 query + ordered points 表示地图元素。
- **MapTRv2**：在 MapTR 基础上的改进版，通常会增强匹配、表征或训练稳定性。
- **VectorMapNet**：把 HD map 元素作为 vector / polyline 来建模，强调矢量化输出。
- **StreamMapNet**：更偏在线/时序地图构建，但仍是 vectorized map perception 的重要方向。

这些工作的共同点是：

- 不输出像素 mask，而是输出**有序点列 / polyline**
- 用 query-based decoder 表示多个 map instance
- 更适合后续做 lane stitching、graph reasoning、规划接口对接

## 6. 这份代码的工程风险与建议

### 6.1 关键风险

1. **标定信息缺失**
   - `IPM` 明确需要 `cam_intrinsic` / `cam_extrinsic`
   - 但 pipeline 的 `Collect` 没把这些 metadata 明确传出来

2. **decoder 没有真正用 BEV 特征**
   - 当前只是 learnable queries + linear head
   - 所以无法体现“image -> BEV -> lane”的真实信息流

3. **topology head 只能输出对称关系**
   - `q @ q^T` 无法表达方向性 edge
   - 对真实 lane graph 不够强

4. **sample_polyline 是空实现**
   - 这意味着点序、插值、等弧长采样等关键细节都没有真的落地

### 6.2 优先建议验证的点

- 先确认 raw annotation 的坐标系定义：ego 原点、x/y 方向、z 轴方向
- 确认 lane 点序是否总是从近到远，还是需要按弧长重排
- 把相机标定 metadata 接入 pipeline，确保 IPM 真正可用
- 如果要做 lane topology，建议把 topology head 从纯相似度改成显式 relation decoder
- 如果要接近 MapTR / vectorized map 的范式，decoder 应该真正基于 BEV features 做 query update，而不是只读 embedding

---

如果你愿意，我可以下一步把这份报告再压缩成一页“数据流总览图”，或者把 `dataset -> target -> model output` 画成表格版，方便你直接拿去讲解。