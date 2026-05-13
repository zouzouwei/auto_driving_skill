# LiDAR 感知小型代码阅读报告

## 1. 点云每个点是 4 维还是 5 维

结论：**5 维**。

证据有两处：

1. `config.py`
   - `LoadPointsFromFile(load_dim=5, use_dim=[0, 1, 2, 3, 4])`
   - `LoadPointsFromMultiSweeps(..., use_dim=[0, 1, 2, 3, 4])`
   这说明数据加载时明确读取并使用 5 个通道。

2. `dataset.py`
   - `points = torch.zeros(20000, 5)`
   - 注释写明：`x, y, z, intensity, timestamp_lag`

所以每个点的 5 个维度含义是：
- `x`
- `y`
- `z`
- `intensity`
- `timestamp_lag`

另外，`LoadPointsFromMultiSweeps(sweeps_num=9)` 说明这里还做了多帧 sweep 融合，`timestamp_lag` 也正好对应时序信息。

## 2. voxel / pillar / BEV 特征怎么构造

这份代码的主干是一个 **PointPillars + SECOND + CenterPoint head** 的简化组合。

### 2.1 体素化 / pillar 化

在 `config.py` 中：
- `point_cloud_range = [-54, -54, -5, 54, 54, 3]`
- `voxel_size = [0.075, 0.075, 0.2]`
- `pts_voxel_layer=dict(max_num_points=10, voxel_size=voxel_size, point_cloud_range=point_cloud_range, max_voxels=(90000, 120000))`

这表示：
- 点云先按固定范围裁剪。
- 空间被划分成规则网格。
- 每个 voxel 最多保留 10 个点。
- 这里的 voxel 在实现语义上更接近 **pillar**：因为后面没有 3D sparse conv middle encoder，而是直接用 `PointPillarsScatter` 把柱状特征散到 BEV 平面。

### 2.2 PillarFeatureNet

`pts_voxel_encoder=dict(type='PillarFeatureNet', in_channels=5, feat_channels=[64])`

在 `model.py` 中对应：
```python
voxels, coords, num_points = self.voxel_layer(points)
pillar_feats = self.voxel_encoder(voxels, num_points, coords)
```

作用是：
- 把每个 voxel / pillar 内的点特征编码成一个固定长度的向量。
- 输入是 5 维点特征，输出是 64 维 pillar 特征。

### 2.3 BEV scatter

`pts_middle_encoder=dict(type='PointPillarsScatter', output_shape=[1440, 1440])`

在 `model.py` 中对应：
```python
bev = self.middle_encoder(pillar_feats, coords)
```

这一步把稀疏的 pillar 特征按坐标投到二维 BEV 网格上，形成稠密伪图像。

这里的 `output_shape=[1440,1440]` 与范围和分辨率正好对应：
- x 方向跨度是 `54 - (-54) = 108`
- y 方向跨度也是 `108`
- `108 / 0.075 = 1440`

所以 BEV 特征图是 **1440 x 1440** 的平面网格。

### 2.4 SECOND backbone

`pts_backbone=dict(type='SECOND', in_channels=64)`

在代码里：
```python
feats = self.backbone(bev)
```

这一步是在 BEV 特征图上做 2D 卷积特征提取。这里体现的是 SECOND 风格的 BEV backbone，但由于中间编码已经是 `PointPillarsScatter`，所以它并不是完整的 3D sparse SECOND 流水线，而是更偏 **pillar + BEV CNN**。

## 3. CenterHead 怎么解码 3D box

### 3.1 头部预测了什么

`CenterHead` 在 `model.py` 中定义了这些分支：
- `heatmap`: 类别中心热图
- `reg`: center offset
- `height`: z 方向高度
- `dim`: box 尺寸 `w,l,h`
- `rot`: 朝向 `yaw` 的编码
- `vel`: 速度 `vx, vy`

对应代码：
```python
return dict(
    heatmap=self.heatmap(x),
    reg=self.reg(x),
    height=self.height(x),
    dim=self.dim(x),
    rot=self.rot(x),
    vel=self.vel(x)
)
```

这与 CenterPoint 系列常见的 box 参数化方式一致。

### 3.2 但这个 fixture 里没有真正实现解码

这里最关键的一点是：
```python
def decode_heatmap(self, preds):
    return {'boxes_3d': torch.zeros(100, 9), 'scores_3d': torch.zeros(100), 'labels_3d': torch.zeros(100, dtype=torch.long)}
```

也就是说：
- **没有真正从 heatmap peak 解出 box**
- **没有把 reg / height / dim / rot / vel 组合成真实框**
- **直接返回固定的 100 个零框**

所以，这份小型代码里 CenterHead 的“解码”只是接口占位，并不是完整实现。

### 3.3 按这个 head 的设计，理论上的解码逻辑

如果按 CenterPoint 的常规逻辑，通常会做：
1. 在 `heatmap` 上找每类 top-k 峰值
2. 根据峰值位置加上 `reg` 的亚像素偏移，恢复中心点的 BEV 坐标
3. 结合 `height` 得到 z
4. 用 `dim` 恢复 `w,l,h`
5. 用 `rot` 恢复 `yaw`
6. 结合 `vel` 得到速度
7. 组装成最终 3D box

但这些步骤在当前 fixture 中都没有写出来。

## 4. 输出坐标系和后处理是什么

### 4.1 坐标系

从数据标注可以直接看到：
```python
gt_bboxes_3d = torch.zeros(32, 9)  # x,y,z,w,l,h,yaw,vx,vy in LiDAR frame
```

这说明训练标注和目标框定义都在 **LiDAR 坐标系** 下。

因此，这个模型输出的 box 也应理解为 **LiDAR frame 的 3D box**。

### 4.2 后处理

这个 fixture 里真正的后处理也没有实现。

`forward()` 在推理时直接返回：
```python
return self.bbox_head.decode_heatmap(preds)
```

而 `decode_heatmap()` 只是返回零张量，所以：
- 没有 NMS
- 没有 score threshold
- 没有旋转框去重
- 没有任何坐标变换

因此，**代码里目前的后处理是占位式的空实现**。

如果按 CenterPoint 的标准流程，后处理通常会包含：
- heatmap top-k 选点
- 解码出 3D box
- class-wise NMS 或 circle NMS / rotated NMS
- 输出 `boxes_3d / scores_3d / labels_3d`

但这份代码只保留了接口，没有保留这些细节。

## 5. CenterPoint / SECOND / PointPillars 的论文思路在代码里有没有体现

有，而且很明显，但都是**简化版**。

### 5.1 PointPillars 的体现

最明显的是：
- `PillarFeatureNet`
- `PointPillarsScatter`
- 先柱状编码，再散到 BEV

这就是典型 PointPillars 思路。

### 5.2 SECOND 的体现

`pts_backbone=dict(type='SECOND', in_channels=64)` 体现了 SECOND 风格的 backbone 命名和 BEV 特征提取思路。

但这里没有出现 SECOND 经典的 3D sparse convolution middle encoder，而是直接用了 pillar scatter，所以它不是完整 SECOND，而是 **借用了 SECOND 的 2D BEV backbone 概念**。

### 5.3 CenterPoint 的体现

`pts_bbox_head=dict(type='CenterHead', ...)` 明确体现了 CenterPoint 的中心点检测范式：
- heatmap 预测中心点
- 回归 center offset / height / size / rotation / velocity
- 最终由中心点解码出 3D boxes

不过在这份代码中，CenterPoint 的核心后处理和真实 decode 逻辑并未实现，只保留了结构。

## 6. 总结

- 点云是 **5 维**：`x, y, z, intensity, timestamp_lag`
- voxel/pillar 流程是：**voxelize -> PillarFeatureNet -> PointPillarsScatter -> BEV CNN(SECOND) -> CenterHead**
- 这里的 BEV 特征是 **1440 x 1440** 的二维平面特征图
- `CenterHead` 的真实 3D box 解码和后处理在这份 fixture 中**没有实现**，只是返回零框占位
- 输出和标注都应理解为 **LiDAR 坐标系**
- 代码明显融合了 **PointPillars、SECOND、CenterPoint** 的核心思想，但都是极简骨架，不是完整论文实现
