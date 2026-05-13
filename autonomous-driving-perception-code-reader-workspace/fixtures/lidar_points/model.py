import torch
from torch import nn

class MiniCenterPoint(nn.Module):
    def __init__(self, voxel_layer, voxel_encoder, middle_encoder, backbone, bbox_head):
        super().__init__()
        self.voxel_layer = voxel_layer
        self.voxel_encoder = voxel_encoder
        self.middle_encoder = middle_encoder
        self.backbone = backbone
        self.bbox_head = bbox_head

    def forward(self, points, gt_bboxes_3d=None, gt_labels_3d=None):
        voxels, coords, num_points = self.voxel_layer(points)
        pillar_feats = self.voxel_encoder(voxels, num_points, coords)
        bev = self.middle_encoder(pillar_feats, coords)
        feats = self.backbone(bev)
        preds = self.bbox_head(feats)
        if self.training:
            return self.bbox_head.loss(preds, gt_bboxes_3d, gt_labels_3d)
        return self.bbox_head.decode_heatmap(preds)

class CenterHead(nn.Module):
    def __init__(self, num_classes=3):
        super().__init__()
        self.heatmap = nn.Conv2d(128, num_classes, 3, padding=1)
        self.reg = nn.Conv2d(128, 2, 3, padding=1)
        self.height = nn.Conv2d(128, 1, 3, padding=1)
        self.dim = nn.Conv2d(128, 3, 3, padding=1)
        self.rot = nn.Conv2d(128, 2, 3, padding=1)
        self.vel = nn.Conv2d(128, 2, 3, padding=1)

    def forward(self, feats):
        x = feats[0]
        return dict(heatmap=self.heatmap(x), reg=self.reg(x), height=self.height(x), dim=self.dim(x), rot=self.rot(x), vel=self.vel(x))

    def decode_heatmap(self, preds):
        return {'boxes_3d': torch.zeros(100, 9), 'scores_3d': torch.zeros(100), 'labels_3d': torch.zeros(100, dtype=torch.long)}

    def loss(self, preds, gt_bboxes_3d, gt_labels_3d):
        return {'loss_heatmap': preds['heatmap'].sum() * 0, 'loss_bbox': preds['reg'].sum() * 0}
