import torch

class MiniLidarDataset:
    def load_points(self, path):
        # x, y, z, intensity, timestamp_lag
        points = torch.zeros(20000, 5)
        points[:, 4] = torch.linspace(0, -0.5, 20000)
        return points

    def prepare_train_data(self, idx):
        points = self.load_points('sample.bin')
        gt_bboxes_3d = torch.zeros(32, 9)  # x,y,z,w,l,h,yaw,vx,vy in LiDAR frame
        gt_labels_3d = torch.zeros(32, dtype=torch.long)
        return {'points': points, 'gt_bboxes_3d': gt_bboxes_3d, 'gt_labels_3d': gt_labels_3d}
