---
name: paper-downloader
description: Use this skill whenever the user asks to download, collect, or fetch academic papers. Trigger strongly for prompts like "下载论文", "论文下载", "批量下载", "收集论文", "download papers", "fetch papers", followed by research directions like autonomous driving, embodied AI, computer vision, etc. Supports specifying time range, keywords, conferences, and automatic folder organization with Chinese naming. Activate when user says "帮我下载...论文", "收集...相关论文", "下载最近...年的论文", or provides specific paper search requirements.
version: 1.0.0
---

# Paper Downloader

Use this skill to automatically download academic papers from arXiv based on user-specified research directions, time ranges, and keywords. Organize papers in structured folders with Chinese naming and generate comprehensive summary tables.

Default behavior: Download from arXiv, limit to 50 papers per direction, sort by citation count and open-source availability, use Chinese naming for files and folders.

## Core Capabilities

1. **Smart Paper Search**: Search arXiv with keyword combinations
2. **Automatic Download**: Download PDFs with concurrency control (max 5)
3. **Chinese Naming**: Use Chinese names for easy identification
4. **Sorted Results**: Sort by citation count and open-source availability
5. **Incremental Update**: Support downloading only new papers
6. **Summary Table**: Generate markdown table with Chinese abstracts

## Core Workflow

### Step 1: Parse User Requirements

Parse the user's request to extract:
- **Research Direction**: e.g., "自动驾驶-纯视觉-3D目标检测"
- **Time Range**: e.g., "2022-2026"
- **Keywords**: Extract from direction name
- **Conference Preference**: e.g., "CVPR, ICCV" (optional)

Example parsing:
```
Input: "帮我下载最近2022-2026年自动驾驶-纯视觉-3D目标检测相关的论文"
Output:
- direction: 自动驾驶-纯视觉-3D目标检测
- time_range: 2022-2026
- keywords: ["3D object detection", "autonomous driving", "camera-only", "monocular", "multi-view"]
```

### Step 2: Generate Folder Structure

Create folder with Chinese naming:
```
论文下载/
└── {中文方向名称}_{起始年份}-{结束年份}/
    ├── README.md                    # 论文清单表格（含中文摘要）
    ├── papers/                      # PDF文件夹
    │   ├── {中文标题}_{会议}_{年份}.pdf
    │   └── ...
    └── metadata.json                # 论文元数据（用于增量更新）
```

Example:
```
论文下载/
└── 自动驾驶_纯视觉3D目标检测_2022-2026/
    ├── README.md
    ├── papers/
    │   ├── BEVFormer_通过时空Transformer学习鸟瞰图表示_ECCV_2022.pdf
    │   ├── BEVDepth_多视角3D目标检测的可靠深度获取_AAAI_2023.pdf
    │   └── ...
    └── metadata.json
```

### Step 3: Search Papers from arXiv

Use arXiv API to search papers:
- **API Endpoint**: http://export.arxiv.org/api/query
- **Search Query**: Combine keywords with AND/OR operators
- **Time Filter**: Filter by submission date
- **Max Results**: 50 papers per direction

Search strategy:
1. Primary search: Main keywords combination
2. Secondary search: Related terms
3. Merge and deduplicate
4. Filter by time range

### Step 4: Get Citation and Code Info

For each paper found:
1. **Citation Count**: Query Semantic Scholar API
2. **Open-Source Code**: Search GitHub for implementations
3. **Sort Priority**:
   - Papers with code > Papers without code
   - Higher citation count > Lower citation count

### Step 5: Download PDFs

Download with concurrency control:
- **Max Concurrent**: 5 downloads at a time
- **Retry on Failure**: 3 attempts per paper
- **Progress Display**: Show download progress
- **Error Handling**: Log failed downloads

### Step 6: Generate README Table

Create markdown table with:
- Paper title (Chinese)
- Conference/Year
- Citation count
- Open-source code link
- Chinese abstract summary
- File name

## Output Format Specifications

### README.md Format

```markdown
# {中文方向名称} 论文下载清单

## 下载信息
- **研究方向**：{方向描述}
- **时间范围**：{起始年份}-{结束年份}
- **下载时间**：{当前日期}
- **论文数量**：{N}篇
- **排序方式**：引用量优先，有开源代码优先

## 论文列表

| 序号 | 论文标题 | 会议/年份 | 引用量 | 开源代码 | 中文摘要 |
|------|----------|-----------|--------|----------|----------|
| 1 | {中文标题} | {会议}/{年份} | {数量} | [代码]({链接}) | {中文摘要} |
| 2 | {中文标题} | {会议}/{年份} | {数量} | 无 | {中文摘要} |
| ... | ... | ... | ... | ... | ... |

## 详细信息

### 1. {中文标题}
- **英文标题**：{English Title}
- **会议/年份**：{Conference}/{Year}
- **作者**：{Authors}
- **引用量**：{Citations}
- **arXiv链接**：{URL}
- **开源代码**：{GitHub Link or "无"}
- **中文摘要**：
  {详细中文摘要，200-300字}

### 2. {中文标题}
...

## 下载统计

| 年份 | 论文数量 | 主要会议 |
|------|----------|----------|
| {年份} | {数量} | {会议列表} |
| **总计** | {总数} | - |
```

### metadata.json Format

```json
{
  "query": {
    "direction": "自动驾驶_纯视觉3D目标检测",
    "direction_en": "autonomous_driving_camera_3d_detection",
    "time_range": {
      "start": 2022,
      "end": 2026
    },
    "keywords": ["3D object detection", "autonomous driving", "camera-only"],
    "max_papers": 50,
    "last_download": "2025-01-15T10:30:00Z"
  },
  "papers": [
    {
      "id": 1,
      "title_en": "BEVFormer: Learning Bird's-Eye-View Representation...",
      "title_cn": "BEVFormer: 通过时空Transformer学习鸟瞰图表示",
      "authors": ["Zhiqi Li", "Wenhai Wang", "..."],
      "venue": "ECCV",
      "year": 2022,
      "arxiv_id": "2203.17270",
      "arxiv_url": "https://arxiv.org/abs/2203.17270",
      "pdf_url": "https://arxiv.org/pdf/2203.17270",
      "abstract_en": "...",
      "abstract_cn": "...",
      "citations": 500,
      "github_url": "https://github.com/zhiqi-li/BEVFormer",
      "has_code": true,
      "file_name": "BEVFormer_通过时空Transformer学习鸟瞰图表示_ECCV_2022.pdf",
      "download_status": "success",
      "download_date": "2025-01-15"
    }
  ],
  "statistics": {
    "total_papers": 50,
    "download_success": 48,
    "download_failed": 2,
    "with_code": 30,
    "without_code": 20,
    "venue_distribution": {
      "CVPR": 15,
      "ICCV": 10,
      "ECCV": 8
    },
    "year_distribution": {
      "2024": 20,
      "2023": 18,
      "2022": 12
    }
  }
}
```

## Incremental Update Workflow

When user requests update:

1. **Read existing metadata.json**
2. **Search for new papers** since last download
3. **Compare and identify new papers**
4. **Download only new papers**
5. **Update metadata.json** with new entries
6. **Update README.md table** with new entries
7. **Report update statistics**

## Research Direction Keywords

### Autonomous Driving (自动驾驶)

```
纯视觉3D检测:
├── Primary: "3D object detection", "autonomous driving", "camera-only", "monocular", "multi-view"
├── Secondary: "BEV", "bird's eye view", "image-only", "vision-only"
└── Exclude: "LiDAR", "point cloud", "radar"

BEV感知:
├── Primary: "BEV", "bird's eye view", "autonomous driving", "perception"
├── Secondary: "multi-camera", "surround view", "3D detection"
└── Related: "BEVFormer", "BEVDepth", "BEVDet"

车道线检测:
├── Primary: "lane detection", "lane marking", "autonomous driving"
├── Secondary: "lane line", "road marking", "lane instance"
└── Related: "LaneNet", "CLRNet", "OpenLane"

占用预测:
├── Primary: "occupancy prediction", "3D occupancy", "autonomous driving"
├── Secondary: "occupancy grid", "voxel prediction", "scene completion"
└── Related: "SurroundOcc", "Occ3D", "TPVFormer"

运动预测:
├── Primary: "motion prediction", "trajectory prediction", "autonomous driving"
├── Secondary: "agent prediction", "future prediction", "behavior prediction"
└── Related: "VectorNet", "HiVT", "MTR"
```

### Embodied AI (具身智能)

```
机器人抓取:
├── Primary: "grasp planning", "robot grasping", "manipulation"
├── Secondary: "grasp detection", "grasp pose", "pick and place"
└── Related: "GraspNet", "Contact-GraspNet", "AnyGrasp"

视觉导航:
├── Primary: "visual navigation", "embodied navigation", "robot navigation"
├── Secondary: "point goal", "object goal", "vision-language navigation"
└── Related: "Habitat", "AI2-THOR", "iGibson"

模仿学习:
├── Primary: "imitation learning", "learning from demonstration", "robot learning"
├── Secondary: "behavior cloning", "offline RL", "policy learning"
└── Related: "ACT", "Diffusion Policy", "VQ-BeT"

场景理解:
├── Primary: "3D scene understanding", "scene reconstruction", "embodied AI"
├── Secondary: "scene graph", "spatial reasoning", "3D vision"
└── Related: "NeRF", "3D Gaussian", "SceneNN"
```

### Computer Vision (计算机视觉)

```
目标检测:
├── Primary: "object detection", "2D detection", "visual detection"
├── Secondary: "anchor-free", "anchor-based", "transformer detection"
└── Related: "DETR", "YOLO", "FCOS"

语义分割:
├── Primary: "semantic segmentation", "image segmentation", "scene parsing"
├── Secondary: "pixel classification", "dense prediction"
└── Related: "DeepLab", "SegFormer", "Mask2Former"

图像生成:
├── Primary: "image generation", "text-to-image", "diffusion model"
├── Secondary: "generative model", "image synthesis", "GAN"
└── Related: "Stable Diffusion", "DALL-E", "Midjourney"
```

## Chinese Translation Guidelines

### Title Translation Rules
1. Keep technical terms in English: BEV, Transformer, CNN, etc.
2. Translate descriptive parts to Chinese
3. Keep acronyms as-is: DETR, BEVFormer, PointNet

Examples:
- "BEVFormer: Learning Bird's-Eye-View Representation..." → "BEVFormer: 通过时空Transformer学习鸟瞰图表示"
- "BEVDepth: Acquisition of Reliable Depth..." → "BEVDepth: 多视角3D目标检测的可靠深度获取"
- "PETR: Position Embedding Transformation..." → "PETR: 用于多视角3D目标检测的位置嵌入变换"

### Abstract Translation Rules
1. Translate to natural Chinese
2. Keep technical terms in English where appropriate
3. Maintain academic tone
4. Length: 200-300 Chinese characters

## Error Handling

### Download Failures
- Log failed papers in metadata.json
- Continue downloading other papers
- Report failures at the end
- Suggest manual download for failed papers

### API Rate Limits
- arXiv: 3 second delay between requests
- Semantic Scholar: Respect rate limits
- GitHub: Use authenticated requests if available

### Network Issues
- Retry 3 times with exponential backoff
- Check PDF integrity after download
- Resume interrupted downloads

## Quality Checklist

### Search Quality
□ Keywords cover all relevant papers
□ Time range is correct
□ No important papers missed
□ No duplicate papers

### Download Quality
□ All PDFs are valid and readable
□ Chinese naming is accurate
□ Folder structure is correct
□ metadata.json is complete

### README Quality
□ Table is properly formatted
□ Chinese abstracts are accurate
□ Citation counts are up-to-date
□ Code links are working

## Usage Examples

### Example 1: Autonomous Driving Papers
```
User: "帮我下载最近2022-2026年自动驾驶-纯视觉-3D目标检测相关的论文"

Skill:
1. Parse: direction=自动驾驶-纯视觉-3D目标检测, time=2022-2026
2. Create folder: 论文下载/自动驾驶_纯视觉3D目标检测_2022-2026/
3. Search arXiv with keywords
4. Sort by citations and code availability
5. Download top 50 papers
6. Generate README with Chinese abstracts
```

### Example 2: Embodied AI Papers
```
User: "下载2023-2025年具身智能-机器人抓取相关的最新论文"

Skill:
1. Parse: direction=具身智能-机器人抓取, time=2023-2025
2. Create folder: 论文下载/具身智能_机器人抓取_2023-2025/
3. Search and download
4. Generate summary table
```

### Example 3: Update Existing Collection
```
User: "帮我更新一下自动驾驶3D检测的论文"

Skill:
1. Read existing metadata.json
2. Search for new papers since last download
3. Download only new papers
4. Update metadata.json and README.md
5. Report: "新增X篇论文"
```
