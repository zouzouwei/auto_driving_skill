import torch

LANE_TYPES = ['single_white_solid', 'single_white_dashed', 'double_yellow_solid', 'road_edge']

class LaneDataset:
    def load_annotation(self, idx):
        return {
            'lanes': [
                {'type': 'single_white_solid', 'points_ego': [[5.0, -1.5, 0.0], [20.0, -1.2, 0.0], [45.0, -1.0, 0.0]]},
                {'type': 'single_white_dashed', 'points_ego': [[4.0, 1.5, 0.0], [25.0, 1.4, 0.0], [55.0, 1.2, 0.0]]},
            ],
            'topology': [[0, 1], [1, 0]],
        }

    def convert_lane_to_target(self, anno):
        lane_points = torch.zeros(100, 20, 3)
        lane_labels = torch.full((100,), -1, dtype=torch.long)
        for lane_id, lane in enumerate(anno['lanes']):
            sampled = self.sample_polyline(lane['points_ego'], num_points=20)
            lane_points[lane_id] = self.normalize_to_pc_range(sampled)
            lane_labels[lane_id] = LANE_TYPES.index(lane['type'])
        lane_adj = torch.zeros(100, 100)
        for src, dst in anno['topology']:
            lane_adj[src, dst] = 1.0
        return lane_points, lane_labels, lane_adj

    def sample_polyline(self, points, num_points):
        return torch.zeros(num_points, 3)

    def normalize_to_pc_range(self, points):
        pc_min = torch.tensor([0.0, -30.0, -2.0])
        pc_max = torch.tensor([60.0, 30.0, 4.0])
        return (points - pc_min) / (pc_max - pc_min)
