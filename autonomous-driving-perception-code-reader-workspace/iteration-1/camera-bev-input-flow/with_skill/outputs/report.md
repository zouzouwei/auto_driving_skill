# Camera BEV input flow code reading

## 1. What these three files form

These fixtures describe a very small multi-view camera 3D detection stack:

- `config.py` wires the dataset pipeline and model pieces together.
- `dataset.py` loads six camera views plus 3D labels and camera geometry metadata.
- `model.py` defines a simplified BEVFormer-like model with an image backbone, FPN, a BEV view transformer, and a DETR-style query head.

The implementation is deliberately minimal, so several parts are placeholders rather than full production logic. I will point out where the code is explicit and where the BEVFormer / DETR3D analogy is only approximate.

## 2. Dataset input flow

### 2.1 Category set

`config.py` defines the classes as:

- `car`
- `truck`
- `bus`
- `pedestrian`

`dataset.py` uses the same list in `CLASSES`, and converts string labels to integer class ids with:

```python
torch.tensor([CLASSES.index(x) for x in sample['gt_names']])
```

So the label mapping is fixed by list position:

- `car -> 0`
- `truck -> 1`
- `bus -> 2`
- `pedestrian -> 3`

### 2.2 Camera order

The camera order is fixed in both files and is the same in both places:

1. `CAM_FRONT`
2. `CAM_FRONT_LEFT`
3. `CAM_FRONT_RIGHT`
4. `CAM_BACK`
5. `CAM_BACK_LEFT`
6. `CAM_BACK_RIGHT`

This matters because all per-view tensors are stacked in this exact order, so index `0..5` has a stable semantic meaning across the whole pipeline.

### 2.3 Raw image size vs model input size

`dataset.py` shows the raw image loader stub:

```python
return torch.zeros(3, 900, 1600)
```

So the source image resolution represented in the fixture is:

- channels: `3`
- height: `900`
- width: `1600`

The model comment in `model.py` says:

```python
# img: B x 6 x 3 x 256 x 704 after pipeline resize/crop
```

And `config.py` confirms the preprocessing target:

```python
dict(type='ResizeCropFlipImage', final_dim=(256, 704), resize_lim=(0.38, 0.55), bot_pct_lim=(0.0, 0.0))
```

So the intended model input is:

- 6 views per sample
- each view resized/cropped to `256 x 704`

That means the input tensor passed into the model should be shaped approximately:

- `B x 6 x 3 x 256 x 704`

The raw size is therefore `900 x 1600`, and the model-side working resolution is `256 x 704`.

### 2.4 How metadata enters the dataset output

`dataset.py` returns these fields:

- `img`: stacked multiview images
- `lidar2img`: one transform matrix per camera
- `cam_intrinsic`: one intrinsic matrix per camera
- `gt_bboxes_3d`: 3D boxes
- `gt_labels_3d`: class ids

The code is explicit:

```python
lidar2img = [sample['cams'][name]['lidar2img'] for name in CAMERA_ORDER]
intrinsics = [sample['cams'][name]['cam_intrinsic'] for name in CAMERA_ORDER]
```

So geometry is already attached per camera view before the model sees the sample.

The pipeline in `config.py` additionally asks `Collect3D` to keep these metadata keys:

- `lidar2img`
- `cam_intrinsic`
- `camera2ego`
- `post_rots`
- `post_trans`

Important detail: only `lidar2img` and `cam_intrinsic` are explicitly assembled in `dataset.py`. The other metadata fields are expected to be produced by earlier pipeline transforms, but those transform implementations are not shown in the provided files. So we can say they are intended to flow into the batch metadata, but the exact values are outside the visible code.

## 3. Model architecture and data flow

## 3.1 Top-level wiring

`config.py` instantiates:

- `img_backbone = ResNet-50`
- `img_neck = FPN(out_channels=256)`
- `view_transformer = SpatialCrossAttentionBEV(bev_h=128, bev_w=128)`
- `pts_bbox_head = DETR3DHead(num_query=300, num_classes=4)`

This is a camera-only 3D detection pipeline that follows the common multi-view image -> BEV -> query head pattern.

## 3.2 Forward pass in `MiniBEVFormer`

The forward flow is:

1. Input image tensor comes in as `B x 6 x 3 x 256 x 704`.
2. The model flattens batch and camera dimensions:
   ```python
   img = img.reshape(b * n, c, h, w)
   ```
3. It runs the image backbone and FPN:
   ```python
   feats = self.img_neck(self.img_backbone(img))
   ```
4. It reshapes feature maps back to per-batch, per-camera form.
5. It calls the BEV view transformer with feature maps and `lidar2img`:
   ```python
   bev = self.view_transformer(feats, img_metas['lidar2img'])
   ```
6. It passes the BEV features into the detection head:
   ```python
   outs = self.pts_bbox_head(bev)
   ```

### 3.3 Backbone and FPN

The backbone is only specified as `ResNet(depth=50)` in the config. The code does not show stage names or feature map scales, but the neck is an FPN with `out_channels=256`, so the intended effect is:

- extract multi-scale image features from each camera
- unify channel dimension to 256
- preserve different spatial resolutions for downstream fusion

This matches standard practice in BEVFormer/DETR3D-style camera perception pipelines, but the exact internal feature pyramid layout is not shown here.

### 3.4 BEV / spatial cross-attention stage

The class is named `SpatialCrossAttentionBEV`, which is a strong hint toward BEVFormer-style spatial cross-attention.

However, the actual implementation is a stub:

```python
return torch.zeros(2, 128 * 128, 256)
```

So in this fixture it does not really project image features into BEV. It only reveals the intended tensor shape:

- BEV grid size: `128 x 128`
- BEV token count: `128 * 128 = 16384`
- BEV embedding dim: `256`

This is enough to infer the design intent:

- each BEV cell is represented by a 256-d vector
- the BEV canvas is a flat sequence of 16,384 queries/tokens
- `lidar2img` is supposed to control how image features are sampled or projected into BEV space

### 3.5 How `lidar2img` is used

The only metadata passed into `view_transformer` in this fixture is:

```python
img_metas['lidar2img']
```

So the geometric bridge from image space to BEV is explicitly intended to use `lidar2img`.

What is not visible here:

- whether `cam_intrinsic` is used inside the transformer
- whether `camera2ego` / `post_rots` / `post_trans` are consumed
- whether the implementation does depth sampling, point projection, or deformable attention

Because those details are absent, the safest reading is:

- `lidar2img` is the only geometry input that definitely reaches the model in this fixture
- the other meta fields are prepared by the pipeline but not consumed in the shown model code

### 3.6 DETR-style head

`DETR3DHead` is query-based:

```python
self.query = nn.Embedding(num_query, 256)
self.cls = nn.Linear(256, num_classes)
self.reg = nn.Linear(256, 10)
```

This gives it the key DETR-like ingredients:

- a fixed set of learnable object queries: `300`
- per-query classification logits: `4` classes
- per-query box regression: `10` outputs

The forward method ignores the BEV tensor content and simply repeats the learned queries for the batch:

```python
query_feat = self.query.weight.unsqueeze(0).repeat(bev.size(0), 1, 1)
return {'cls_scores': self.cls(query_feat), 'bbox_preds': self.reg(query_feat)}
```

So the current fixture does **not** implement the full DETR decoder block. There is no visible transformer decoder, cross-attention to BEV tokens, self-attention among queries, or iterative refinement.

What it does show is a DETR-style output head structure:

- fixed query set
- classification per query
- regression per query

That is enough to label it as DETR-like, but not as a faithful DETR3D implementation.

## 4. Loss and training behavior

The `loss` method is a placeholder:

```python
return {
    'loss_cls': outs['cls_scores'].sum() * 0,
    'loss_bbox': outs['bbox_preds'].sum() * 0
}
```

So both losses are always zero-valued tensors.

This means:

- there is no real matching between predictions and ground truth
- there is no classification supervision actually applied
- there is no box regression supervision actually applied
- this code is not trainable in its current form

In a real BEVFormer / DETR3D pipeline, this part would normally contain Hungarian matching and losses such as classification loss plus box regression loss. None of that is present here.

## 5. Final output

### Training mode

If `self.training` is true, the model returns the loss dict:

- `loss_cls`
- `loss_bbox`

Both are zero placeholders in this fixture.

### Inference mode

Otherwise, it returns:

```python
return self.pts_bbox_head.get_bboxes(outs, img_metas)
```

But `get_bboxes` simply returns the raw network outputs unchanged:

```python
return outs
```

So the final inference output is just:

- `cls_scores`: shape roughly `B x 300 x 4`
- `bbox_preds`: shape roughly `B x 300 x 10`

The code does not decode boxes into a geometric 3D box structure, does not threshold scores, and does not apply NMS.

## 6. Relation to BEVFormer and DETR3D

### 6.1 Evidence for BEVFormer-like design

Strong evidence:

- model name is `MiniBEVFormer`
- there is an explicit `SpatialCrossAttentionBEV` module
- the pipeline is multi-view camera based
- the model uses geometry metadata, especially `lidar2img`
- the spatial abstraction is a BEV grid of size `128 x 128`

This is consistent with the high-level BEVFormer idea: convert multi-view image features into BEV features using geometric cross-attention.

### 6.2 Evidence for DETR3D-like design

Strong evidence:

- `DETR3DHead` name
- learnable queries (`num_query=300`)
- per-query classification and regression heads

That matches the DETR family pattern used by DETR3D-style detectors.

### 6.3 Uncertainty and what is missing

The fixture is not a full reproduction of either paper.

Missing compared with real BEVFormer / DETR3D systems:

- actual transformer decoder stack
- attention between queries and image/BEV features
- multi-scale deformable attention or real spatial cross-attention logic
- real use of all geometry metadata
- temporal fusion / history BEV, if expected from BEVFormer
- proper box decoding and training losses
- query-to-ground-truth matching

So the safest conclusion is:

- this is a BEVFormer-inspired skeleton with DETR3D-style query heads
- it is structurally similar to the papers, but algorithmically much simpler

## 7. Recommended follow-up improvements

1. **Implement a real annotation loader**
   - Make `load_annotation()` return real samples.
   - Verify camera files, box coordinates, and class names are consistent with `CAMERA_ORDER`.

2. **Clarify and document metadata flow**
   - Confirm how `camera2ego`, `post_rots`, and `post_trans` are created.
   - Ensure they are all synchronized with the resized/cropped image tensors.

3. **Replace the placeholder BEV transformer**
   - Use `lidar2img` plus the full camera geometry to project or sample image features into BEV.
   - If aiming for BEVFormer behavior, add BEV queries and real spatial cross-attention.

4. **Add a real DETR-style decoder**
   - Put a transformer decoder between BEV features and the prediction heads.
   - Let object queries attend to BEV tokens iteratively.

5. **Use proper losses and matching**
   - Replace zero losses with Hungarian matching.
   - Add actual classification and 3D box regression objectives.

6. **Decode predictions into 3D boxes**
   - Convert `bbox_preds` into structured 3D boxes with scores.
   - Add thresholding and optional NMS for inference.

7. **Verify input-shape consistency**
   - The dataset stub returns `900 x 1600`, while the model expects `256 x 704`.
   - Make sure the resize/crop pipeline is applied before the forward pass.

## 8. Short conclusion

This fixture is a compact multi-view camera 3D detection prototype. The data path is clear: six cameras are loaded in a fixed order, labels are mapped to four classes, raw images start at `900 x 1600`, and the pipeline reduces them to `256 x 704`. Geometry metadata, especially `lidar2img`, is intended to drive the transition into BEV space. The model then uses a ResNet+FPN image encoder, a BEV transformer stub, and a query-based DETR-style head. However, the BEV attention, decoder, loss, and bbox decoding are all placeholders, so the code is best understood as a structural sketch of BEVFormer/DETR3D rather than a faithful implementation.
