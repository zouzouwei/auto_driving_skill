# 自动驾驶论文常用术语表

## 感知相关术语

### 数据表示
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| BEV | 鸟瞰图 (Bird's Eye View) | 从上往下看的视角表示 |
| Voxel | 体素 | 3D空间中的小方块 |
| Pillar | 柱体 | 垂直方向的柱状体素 |
| Point Cloud | 点云 | 3D空间中的点集合 |
| Feature Map | 特征图 | 卷积网络的输出 |
| Tensor | 张量 | 多维数组 |

### 检测相关
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Anchor | 锚框 | 预定义的参考框 |
| Query | 查询 | Transformer中的查询向量 |
| Bounding Box | 边界框 | 包围物体的框 |
| IoU | 交并比 | 两个框的重叠程度 |
| NMS | 非极大值抑制 | 去除重叠框的方法 |
| mAP | 平均精度均值 | 检测性能指标 |
| NDS | nuScenes检测分数 | nuScenes数据集的综合指标 |

### 模型架构
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Backbone | 骨干网络 | 特征提取网络 |
| Neck | 颈部网络 | 特征融合网络 |
| Head | 检测头 | 预测输出网络 |
| Encoder | 编码器 | 特征编码模块 |
| Decoder | 解码器 | 特征解码模块 |
| Transformer | Transformer | 自注意力机制网络 |
| Attention | 注意力 | 关注重要信息的机制 |
| FPN | 特征金字塔网络 | 多尺度特征融合 |

## 预测规划术语

### 预测相关
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Trajectory | 轨迹 | 物体运动的路径 |
| Waypoint | 路径点 | 轨迹上的点 |
| Prediction | 预测 | 预测未来状态 |
| Multi-modal | 多模态 | 多种可能的预测 |
| ADE | 平均位移误差 | 轨迹预测精度指标 |
| FDE | 最终位移误差 | 终点预测精度指标 |

### 规划控制
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Planning | 规划 | 路径规划 |
| Control | 控制 | 车辆控制 |
| MPC | 模型预测控制 | 优化控制方法 |
| PID | 比例-积分-微分控制 | 经典控制方法 |
| LQR | 线性二次调节器 | 最优控制方法 |
| Lattice | 格点搜索 | 路径搜索方法 |

## 工程部署术语

### 模型优化
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Inference | 推理 | 模型前向计算 |
| Latency | 延迟 | 推理时间 |
| Throughput | 吞吐量 | 每秒处理样本数 |
| FLOPs | 浮点运算次数 | 计算量指标 |
| Parameters | 参数量 | 模型参数数量 |
| TensorRT | TensorRT | NVIDIA推理优化引擎 |
| ONNX | 开放神经网络交换格式 | 模型交换格式 |
| INT8 | 8位整数量化 | 模型量化方法 |
| FP16 | 16位浮点 | 半精度浮点 |

### 部署相关
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| CUDA | CUDA | NVIDIA并行计算平台 |
| GPU | 图形处理器 | 并行计算硬件 |
| Edge Device | 边缘设备 | 嵌入式计算设备 |
| Real-time | 实时 | 满足时间约束 |
| Batch Size | 批大小 | 一次处理的样本数 |

## 数据集术语

### 数据集名称
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| nuScenes | nuScenes | 大规模自动驾驶数据集 |
| Waymo | Waymo | Waymo开放数据集 |
| KITTI | KITTI | 经典自动驾驶数据集 |
| Argoverse | Argoverse | Argoverse数据集 |
| OpenLane | OpenLane | 车道线数据集 |
| ONCE | ONCE | 大规模点云数据集 |
| BDD100K | BDD100K | 驾驶视频数据集 |

### 数据标注
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Ground Truth | 真实标注 | 人工标注的真值 |
| Annotation | 标注 | 数据标签 |
| Label | 标签 | 类别标签 |
| Calibration | 标定 | 传感器参数 |
| Intrinsic | 内参 | 相机内部参数 |
| Extrinsic | 外参 | 相机外部参数 |

## 评估指标术语

### 检测指标
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| Precision | 精确率 | 预测为正样本中真正为正的比例 |
| Recall | 召回率 | 真正为正样本中被预测为正的比例 |
| AP | 平均精度 | Precision-Recall曲线下面积 |
| mAP | 平均精度均值 | 所有类别的AP平均值 |
| APH | 平均精度-heading | 包含朝向的AP |
| IoU | 交并比 | 预测框与真值框的重叠度 |

### 分割指标
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| mIoU | 平均交并比 | 分割性能指标 |
| Dice | Dice系数 | 分割相似度指标 |
| CE | 交叉熵 | 分割损失函数 |

### 效率指标
| 英文术语 | 中文翻译 | 说明 |
|----------|----------|------|
| FPS | 每秒帧数 | 处理速度 |
| ms | 毫秒 | 时间单位 |
| GFLOPs | 十亿浮点运算 | 计算量单位 |
| M | 百万 | 参数量单位 |
| GB | 千兆字节 | 内存/存储单位 |

## 常用缩写

| 缩写 | 全称 | 中文 |
|------|------|------|
| CNN | Convolutional Neural Network | 卷积神经网络 |
| RNN | Recurrent Neural Network | 循环神经网络 |
| LSTM | Long Short-Term Memory | 长短期记忆网络 |
| GNN | Graph Neural Network | 图神经网络 |
| ViT | Vision Transformer | 视觉Transformer |
| DETR | Detection Transformer | 检测Transformer |
| FPN | Feature Pyramid Network | 特征金字塔网络 |
| RPN | Region Proposal Network | 区域提议网络 |
| ROI | Region of Interest | 感兴趣区域 |
| BN | Batch Normalization | 批归一化 |
| LN | Layer Normalization | 层归一化 |
| ReLU | Rectified Linear Unit | 修正线性单元 |
| SGD | Stochastic Gradient Descent | 随机梯度下降 |
| Adam | Adaptive Moment Estimation | 自适应矩估计 |
