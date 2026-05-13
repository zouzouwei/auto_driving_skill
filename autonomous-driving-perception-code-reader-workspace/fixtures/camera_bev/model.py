import torch
from torch import nn

class MiniBEVFormer(nn.Module):
    def __init__(self, img_backbone, img_neck, view_transformer, pts_bbox_head):
        super().__init__()
        self.img_backbone = img_backbone
        self.img_neck = img_neck
        self.view_transformer = view_transformer
        self.pts_bbox_head = pts_bbox_head

    def forward(self, img, img_metas, gt_bboxes_3d=None, gt_labels_3d=None):
        # img: B x 6 x 3 x 256 x 704 after pipeline resize/crop
        b, n, c, h, w = img.shape
        img = img.reshape(b * n, c, h, w)
        feats = self.img_neck(self.img_backbone(img))
        feats = [x.reshape(b, n, *x.shape[1:]) for x in feats]
        bev = self.view_transformer(feats, img_metas['lidar2img'])
        outs = self.pts_bbox_head(bev)
        if self.training:
            return self.pts_bbox_head.loss(outs, gt_bboxes_3d, gt_labels_3d)
        return self.pts_bbox_head.get_bboxes(outs, img_metas)

class SpatialCrossAttentionBEV(nn.Module):
    def forward(self, mlvl_feats, lidar2img):
        return torch.zeros(2, 128 * 128, 256)

class DETR3DHead(nn.Module):
    def __init__(self, num_query=300, num_classes=4):
        super().__init__()
        self.query = nn.Embedding(num_query, 256)
        self.cls = nn.Linear(256, num_classes)
        self.reg = nn.Linear(256, 10)

    def forward(self, bev):
        query_feat = self.query.weight.unsqueeze(0).repeat(bev.size(0), 1, 1)
        return {'cls_scores': self.cls(query_feat), 'bbox_preds': self.reg(query_feat)}

    def loss(self, outs, gt_bboxes_3d, gt_labels_3d):
        return {'loss_cls': outs['cls_scores'].sum() * 0, 'loss_bbox': outs['bbox_preds'].sum() * 0}

    def get_bboxes(self, outs, img_metas):
        return outs
