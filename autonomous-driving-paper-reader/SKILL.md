---
name: autonomous-driving-paper-reader
description: Use this skill whenever the user asks to read, analyze, explain, or compare autonomous-driving papers. Trigger strongly for prompts about understanding paper methodology, model architecture, technical innovations, ablation studies, experimental results, code implementation, engineering deployment, or batch comparison of papers in the same research direction. Supports single paper deep-dive, folder-level paper comparison, pseudocode explanation with line-by-line commentary, and real-world analogies for complex concepts. Activate for "读论文", "分析论文", "论文解读", "对比论文", "paper analysis", "model architecture", "technical details", "code implementation", or when user provides PDF files of autonomous-driving papers.
version: 1.0.0
---

# Autonomous-Driving Paper Reader

Use this skill to provide deep, structured analysis of autonomous-driving papers with focus on technical details, model innovations, engineering implementation, and easy-to-understand explanations.

Default response style: Chinese explanation with important English technical terms preserved, such as `backbone`, `neck`, `head`, `encoder`, `decoder`, `transformer`, `attention`, `BEV`, `voxel`, `pillar`, `anchor`, `query`, `feature map`, `tensor`, `loss`, `mAP`, `NDS`, `FPS`, `TensorRT`, `ONNX`.

## Core Capabilities

1. **Single Paper Deep-Dive**: Detailed analysis of one paper with technical details, pseudocode, and real-world analogies
2. **Folder-Level Comparison**: Batch analysis and comparison of papers in the same research direction
3. **Code-Paper Mapping**: Connect paper concepts to pseudocode with line-by-line explanation
4. **Engineering Analysis**: Assess deployment feasibility, model complexity, and optimization potential
5. **Output as Markdown**: Save analysis results as structured .md files

## Core Workflow

### Step 1: Paper Source Identification

- Read PDF files provided by the user
- Extract paper title, authors, institution, venue, year
- Identify if open-source code repository exists (GitHub, etc.)
- For folder comparison: scan all PDFs in the specified folder

### Step 2: Technical Deep-Dive Analysis

For each paper, analyze in this order:

1. **Research Motivation**: What problem does it solve? Why existing methods fail?
2. **Overall Architecture**: High-level data flow and module connections
3. **Core Modules**: Detailed analysis of each key component
4. **Technical Innovations**: What's new compared to prior work?
5. **Loss Function & Training**: How is the model optimized?
6. **Experimental Results**: Performance, ablation studies, visualizations
7. **Engineering Assessment**: Deployment feasibility and optimization potential

### Step 3: Pseudocode Explanation Strategy

When explaining technical concepts:

1. **Write pseudocode** (not actual implementation code)
2. **Line-by-line commentary** explaining the thinking behind each step
3. **Connect to paper formulas** showing the mapping from math to code
4. **Use real-world analogies** to make complex concepts accessible

Example format:
```python
# Pseudocode: View Transform Module
# Purpose: Convert image features to BEV representation
# Analogy: Like looking down from a helicopter to create a map

def view_transform(image_features, depth_distribution, camera_params):
    # Step 1: Predict depth for each pixel
    # Think of it as: estimating how far each pixel is from the camera
    depth = depth_net(image_features)  # [B, C, H, W] -> [B, D, H, W]

    # Step 2: Create 3D feature volume
    # Think of it as: lifting 2D image into 3D space using depth
    feature_3d = image_features.unsqueeze(2) * depth.unsqueeze(1)  # [B, C, D, H, W]

    # Step 3: Project to BEV grid
    # Think of it as: looking down from above and summarizing what's at each location
    bev_feature = voxel_pooling(feature_3d, camera_params)  # [B, C, X, Y]

    return bev_feature
```

### Step 4: Real-World Analogy Guidelines

Use **life-like analogies** that are easy to understand:

| Technical Concept | Real-World Analogy |
|-------------------|-------------------|
| Attention Mechanism | Spotlight on a stage - focusing on the most important actor |
| Feature Pyramid | Different magnifying glasses - seeing both fine details and big picture |
| Anchor Boxes | Pre-made templates of different sizes - finding the best match |
| BEV Transform | Looking down from a helicopter to create a map |
| Object Query | Sending out detectives - each one responsible for finding one object |
| NMS | Removing duplicate boxes - keeping only the most confident one |
| Voxelization | Cutting space into small cubes - each cube records point information |
| Transformer Decoder | A team discussion - each member (query) gathers info from others (attention) |

### Step 5: Folder-Level Comparison Workflow

When comparing papers in a folder:

1. **Scan all PDFs** in the specified folder
2. **Extract key information** from each paper:
   - Core method and innovation
   - Model architecture
   - Experimental results
   - Pros and cons
3. **Build comparison tables**:
   - Basic information comparison
   - Technical approach comparison
   - Performance comparison
   - Innovation comparison
   - Engineering capability comparison
4. **Analyze trends**:
   - Evolution of techniques
   - Common challenges
   - Future directions
5. **Generate recommendation**:
   - Best for different scenarios
   - Suggested reading order
   - Combination possibilities

## Output Format Specifications

### Single Paper Analysis Output

Save as: `{paper_title}_analysis.md`

Structure:
```markdown
# {Paper Title} - 深度技术分析

## 1. 论文基本信息
- **标题**：
- **作者/机构**：
- **发表venue/年份**：
- **开源代码**：
- **一句话总结**：

## 2. 研究动机与问题定义
### 2.1 解决什么问题
### 2.2 现有方法的不足
### 2.3 核心贡献

## 3. 模型架构深度解析

### 3.1 整体架构概览
[架构描述和数据流]

**通俗理解**：
> 生活化类比解释...

### 3.2 核心模块详解

#### 模块A: [名称]

**功能定义**：
- 做什么：
- 为什么需要：

**技术细节**：
- 输入：shape = [...]
- 输出：shape = [...]
- 核心算法：

**伪代码实现**：
```python
# 伪代码：[模块名称]
# 功能：[一句话描述]
# 类比：[生活化例子]

def module_function(input):
    # Step 1: [操作描述]
    # 思想：[为什么这样做]
    result1 = operation1(input)

    # Step 2: [操作描述]
    # 思想：[为什么这样做]
    result2 = operation2(result1)

    return result2
```

**通俗理解**：
> [生活化类比解释]

**设计动机**：
- 为什么这样设计：
- 相比其他方案的优势：

## 4. 关键技术创新点

### 创新点1: [名称]

**改进内容**：
- 原来怎么做：
- 现在怎么做：
- 改进了什么：

**伪代码对比**：
```python
# 原来的方法
def old_method():
    ...

# 本文的改进
def new_method():
    # 改进点：...
    ...
```

**通俗理解**：
> [生活化例子解释为什么这个创新有效]

**效果验证**：
- 消融实验数据：
- 性能提升：

## 5. 损失函数与训练策略

### 5.1 损失函数设计
**总体损失**：L_total = λ1 * L_A + λ2 * L_B

**各损失详解**：
- L_A: [作用、公式、超参数选择]
- L_B: [作用、公式、超参数选择]

**伪代码实现**：
```python
def compute_loss(pred, target):
    # 损失A：[作用描述]
    loss_a = compute_loss_a(pred, target)

    # 损失B：[作用描述]
    loss_b = compute_loss_b(pred, target)

    # 加权组合
    total_loss = weight_a * loss_a + weight_b * loss_b
    return total_loss
```

### 5.2 训练策略
- 优化器：
- 学习率策略：
- 数据增强：

## 6. 实验结果分析

### 6.1 实验设置
- 数据集：
- 评估指标：
- 实现框架：

### 6.2 主实验结果
| 方法 | mAP | NDS | Latency | 备注 |
|------|-----|-----|---------|------|
| Baseline | | | | |
| 本文方法 | | | | |
| 提升 | | | | |

**结果解读**：

### 6.3 消融实验
| 配置 | mAP | NDS | 说明 |
|------|-----|-----|------|
| Baseline | | | |
| +模块A | | | |
| +模块B | | | |
| 全部 | | | |

**消融分析**：

### 6.4 可视化分析
**成功案例**：
**失败案例**：

## 7. 工程化分析

### 7.1 模型复杂度
| 指标 | 数值 | 说明 |
|------|------|------|
| 参数量 | | |
| FLOPs | | |
| 推理延迟 | | |
| 内存占用 | | |

### 7.2 部署友好性
- TensorRT支持：
- ONNX导出：
- INT8量化：

### 7.3 优化建议
- 可优化方向：
- 部署注意事项：

## 8. 优缺点总结

### 8.1 优点
1. 技术层面：
2. 工程层面：

### 8.2 局限性
1. 技术局限：
2. 工程局限：

### 8.3 改进方向
1. 短期改进：
2. 长期方向：

## 9. 相关工作对比
| 方法 | 核心思想 | 优点 | 缺点 | 本文改进 |
|------|----------|------|------|----------|
| 方法A | | | | |
| 方法B | | | | |

## 10. 个人见解与启发
- 对领域的贡献：
- 可借鉴的思路：
- 未来研究方向：
```

### Folder Comparison Output

Save as: `{research_direction}_comparison.md`

Structure:
```markdown
# {研究方向} 论文对比分析报告

## 分析概述
- **论文数量**：N篇
- **研究主题**：
- **时间范围**：
- **主要会议**：

## 1. 论文基本信息汇总

| 序号 | 标题 | 会议/年份 | 核心方法 | 开源代码 |
|------|------|-----------|----------|----------|
| 1 | | | | |
| 2 | | | | |
| ... | | | | |

## 2. 技术路线对比

### 2.1 问题建模方式对比

| 论文 | 输入表示 | 输出表示 | 建模思路 |
|------|----------|----------|----------|
| A | | | |
| B | | | |
| C | | | |

**分析**：
- 主流趋势：
- 关键差异：

### 2.2 模型架构对比

#### Backbone设计对比

| 论文 | Backbone类型 | 参数量 | 特点 |
|------|--------------|--------|------|
| A | | | |
| B | | | |
| C | | | |

#### 核心模块对比

| 论文 | 模块名称 | 功能 | 技术要点 |
|------|----------|------|----------|
| A | | | |
| B | | | |
| C | | | |

**伪代码对比**：
```python
# 论文A的核心实现
def method_a():
    # 思想：...
    ...

# 论文B的核心实现
def method_b():
    # 思想：...
    ...

# 对比分析
# 差异：...
# 优势：...
```

### 2.3 关键创新点对比

| 论文 | 创新点1 | 创新点2 | 创新点3 |
|------|---------|---------|---------|
| A | | | |
| B | | | |
| C | | | |

**创新点分析**：
- 共同关注的问题：
- 不同的解决思路：
- 谁的方法更优雅：

### 2.4 损失函数对比

| 论文 | 主要损失 | 辅助损失 | 损失权重策略 |
|------|----------|----------|--------------|
| A | | | |
| B | | | |
| C | | | |

## 3. 性能对比分析

### 3.1 主实验结果对比

#### nuScenes数据集

| 方法 | mAP | NDS | Latency | 参数量 |
|------|-----|-----|---------|--------|
| A | | | | |
| B | | | | |
| C | | | | |

#### 其他数据集（如有）

| 方法 | 指标1 | 指标2 | 指标3 |
|------|-------|-------|-------|
| A | | | |
| B | | | |
| C | | | |

### 3.2 速度-精度Trade-off分析

**分析**：
- Pareto最优方法：
- 各方法定位：

### 3.3 消融实验对比

| 论文 | 消融内容 | 关键发现 |
|------|----------|----------|
| A | | |
| B | | |
| C | | |

## 4. 工程化能力对比

### 4.1 部署友好性

| 论文 | TensorRT | ONNX | INT8量化 | 动态shape |
|------|----------|------|----------|-----------|
| A | | | | |
| B | | | | |
| C | | | | |

### 4.2 模型效率对比

| 论文 | 参数量 | FLOPs | 推理延迟 | 内存占用 |
|------|--------|-------|----------|----------|
| A | | | | |
| B | | | | |
| C | | | | |

### 4.3 代码质量评估

| 论文 | 模块化 | 可读性 | 文档 | 测试 |
|------|--------|--------|------|------|
| A | | | | |
| B | | | | |
| C | | | | |

## 5. 各论文改进点分析

### 5.1 论文A的改进点
**相对前人工作**：
- 改进了什么：
- 如何改进的：
- 改进效果：

**伪代码展示改进**：
```python
# 前人方法
def previous_method():
    ...

# 论文A的改进
def paper_a_method():
    # 改进点：...
    ...
```

### 5.2 论文B的改进点
...

### 5.3 论文C的改进点
...

### 5.4 改进点对比总结

| 论文 | 改进对象 | 改进方式 | 改进效果 | 改进难度 |
|------|----------|----------|----------|----------|
| A | | | | |
| B | | | | |
| C | | | | |

## 6. 发展趋势分析

### 6.1 技术演进路线
```
时间线：
2023: 方法A → 方法B
2024: 方法C → 方法D
2025: 方法E → 方法F
```

### 6.2 关键趋势
1. 趋势1：
2. 趋势2：
3. 趋势3：

### 6.3 未来方向预测
- 短期（1年内）：
- 中期（1-3年）：
- 长期（3年以上）：

## 7. 综合推荐

### 7.1 各论文适用场景

| 场景 | 推荐论文 | 理由 |
|------|----------|------|
| 追求最高精度 | | |
| 追求实时性 | | |
| 工程部署优先 | | |
| 研究学习参考 | | |

### 7.2 方法组合建议
- 可以组合的模块：
- 组合后的预期效果：

### 7.3 推荐阅读顺序
1. 入门：论文X（基础概念）
2. 进阶：论文Y（关键技术）
3. 深入：论文Z（最新进展）

## 8. 总结
- 核心结论：
- 关键发现：
- 研究建议：
```

## Autonomous Driving Domain Knowledge

### Perception Task Analysis Framework

#### 3D Object Detection
- **Representation**: point cloud / voxel / pillar / BEV
- **Feature Extraction**: backbone / neck design
- **Detection Head**: anchor-based / anchor-free / query-based
- **Post-processing**: NMS / voting / aggregation
- **Multi-modal Fusion**: early / mid / late fusion

#### BEV Perception
- **View Transform**: LSS / BEVFormer / Transformer
- **Temporal Fusion**: alignment / memory mechanism
- **BEV Representation**: grid / query / hybrid
- **Multi-task Learning**: detection + segmentation + mapping

#### Lane/Map Perception
- **Representation**: 2D / 3D / BEV / vectorized
- **Topology**: lane connection / traffic rules
- **Online Construction**: real-time mapping / map prior

### Prediction Task Analysis Framework

- **Input Representation**: history trajectory / HD map / traffic signal
- **Model Architecture**: RNN / GNN / Transformer / MLP
- **Output Representation**: trajectory points / probability distribution / multi-modal
- **Interaction Modeling**: vehicle-vehicle / vehicle-road

### Planning & Control Analysis Framework

- **Planning**: A* / RRT / Lattice / optimization / learning-based
- **Control**: PID / MPC / LQR
- **Safety**: collision detection / traffic rules / robustness

### Common Components Checklist

When analyzing papers, look for these components:

- **Image Backbone**: ResNet, Swin, ConvNeXt, ViT, InternImage
- **Neck**: FPN, BiFPN, deformable attention
- **Depth/View Transform**: LSS, BEVDepth, BEVDet, BEVFormer, PETR
- **LiDAR Encoder**: VoxelNet, SECOND, PointPillars, SparseConv
- **Fusion**: BEVFusion, TransFusion, CMT
- **Decoder/Head**: DETR queries, center heatmap, anchor head, transformer decoder
- **Loss**: Hungarian matching, focal loss, L1/GIoU, Chamfer distance
- **Post-processing**: NMS, circle NMS, top-k, box decode

## Reading Strategy for Large Repos

- Start from configs, training scripts, model registry, dataset registry, and README
- Use code search for dataset class names, `__getitem__`, `prepare_train_data`, `pipeline`, `collate`, `forward`, `loss`, `decode`, `post_process`, `get_bboxes`, `simple_test`, `predict`, `export`, and `visualize`
- For OpenMMLab-style repos, trace config `_base_`, `data.train`, `train_pipeline`, `model`, `pts_bbox_head`, `img_backbone`, `view_transformer`, `bbox_coder`, and `test_cfg`
- For custom PyTorch repos, trace from `train.py`/`main.py` to dataloader, model construction, forward pass, loss, validation, and export/inference
- If the repo is too large, produce a first-pass map and ask which module to deep-dive next

## Quality Bar

A good answer should:

1. **Technical Depth**: Not just describe what, but explain why and how
2. **Code Connection**: Show pseudocode with line-by-line explanation
3. **Easy Understanding**: Use real-world analogies for complex concepts
4. **Engineering Focus**: Assess deployment feasibility and optimization potential
5. **Structured Output**: Save as well-organized Markdown files

## File Output Guidelines

- Always save analysis results as .md files in the user's working directory
- Use descriptive filenames: `{paper_title}_analysis.md` or `{direction}_comparison.md`
- Include proper Markdown formatting with tables, code blocks, and headers
- Preserve important English technical terms in Chinese explanations
