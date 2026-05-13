import torch

CAMERA_ORDER = ['CAM_FRONT', 'CAM_FRONT_LEFT', 'CAM_FRONT_RIGHT', 'CAM_BACK', 'CAM_BACK_LEFT', 'CAM_BACK_RIGHT']
CLASSES = ['car', 'truck', 'bus', 'pedestrian']

class MiniNuScenesCameraDataset:
    def __init__(self, ann_file, pipeline):
        self.ann_file = ann_file
        self.pipeline = pipeline

    def __getitem__(self, idx):
        sample = self.load_annotation(idx)
        imgs = [self.load_image(sample['cams'][name]['data_path']) for name in CAMERA_ORDER]
        lidar2img = [sample['cams'][name]['lidar2img'] for name in CAMERA_ORDER]
        intrinsics = [sample['cams'][name]['cam_intrinsic'] for name in CAMERA_ORDER]
        data = {
            'img': torch.stack(imgs, dim=0),
            'lidar2img': torch.tensor(lidar2img),
            'cam_intrinsic': torch.tensor(intrinsics),
            'gt_bboxes_3d': sample['gt_boxes'],
            'gt_labels_3d': torch.tensor([CLASSES.index(x) for x in sample['gt_names']]),
        }
        return self.pipeline(data)

    def load_annotation(self, idx):
        raise NotImplementedError

    def load_image(self, path):
        return torch.zeros(3, 900, 1600)
