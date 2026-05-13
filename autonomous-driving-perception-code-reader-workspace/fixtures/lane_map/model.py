import torch
from torch import nn

class MiniLaneMapNet(nn.Module):
    def __init__(self, img_backbone, view_transform, lane_decoder, topology_head):
        super().__init__()
        self.img_backbone = img_backbone
        self.view_transform = view_transform
        self.lane_decoder = lane_decoder
        self.topology_head = topology_head

    def forward(self, img, cam_intrinsic, cam_extrinsic, lane_points=None, lane_labels=None, lane_adj=None):
        img_feats = self.img_backbone(img)
        bev_feats = self.view_transform(img_feats, cam_intrinsic, cam_extrinsic)
        lane_queries = self.lane_decoder(bev_feats)
        pred_points = lane_queries['points']
        pred_logits = lane_queries['class_logits']
        pred_adj = self.topology_head(lane_queries['query_feats'])
        if self.training:
            return {
                'loss_lane_cls': pred_logits.sum() * 0,
                'loss_lane_points': pred_points.sum() * 0,
                'loss_topology': pred_adj.sum() * 0,
            }
        return {'lane_points': pred_points, 'lane_scores': pred_logits.sigmoid(), 'lane_adj': pred_adj.sigmoid()}

class PolylineTransformerDecoder(nn.Module):
    def __init__(self, num_query=100, num_points=20, num_classes=4):
        super().__init__()
        self.query = nn.Embedding(num_query, 256)
        self.points = nn.Linear(256, num_points * 3)
        self.cls = nn.Linear(256, num_classes)

    def forward(self, bev_feats):
        q = self.query.weight.unsqueeze(0).repeat(bev_feats.size(0), 1, 1)
        return {'query_feats': q, 'points': self.points(q).reshape(bev_feats.size(0), 100, 20, 3), 'class_logits': self.cls(q)}

class LaneTopologyHead(nn.Module):
    def forward(self, query_feats):
        return torch.matmul(query_feats, query_feats.transpose(1, 2))
