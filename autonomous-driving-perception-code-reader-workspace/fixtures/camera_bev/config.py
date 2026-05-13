dataset_type = 'MiniNuScenesCameraDataset'
classes = ['car', 'truck', 'bus', 'pedestrian']
img_norm_cfg = dict(mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)

train_pipeline = [
    dict(type='LoadMultiViewImageFromFiles', camera_order=['CAM_FRONT', 'CAM_FRONT_LEFT', 'CAM_FRONT_RIGHT', 'CAM_BACK', 'CAM_BACK_LEFT', 'CAM_BACK_RIGHT']),
    dict(type='ResizeCropFlipImage', final_dim=(256, 704), resize_lim=(0.38, 0.55), bot_pct_lim=(0.0, 0.0)),
    dict(type='NormalizeMultiviewImage', **img_norm_cfg),
    dict(type='LoadAnnotations3D', with_bbox_3d=True, with_label_3d=True),
    dict(type='Collect3D', keys=['img', 'gt_bboxes_3d', 'gt_labels_3d'], meta_keys=['lidar2img', 'cam_intrinsic', 'camera2ego', 'post_rots', 'post_trans'])
]

model = dict(
    type='MiniBEVFormer',
    img_backbone=dict(type='ResNet', depth=50),
    img_neck=dict(type='FPN', out_channels=256),
    view_transformer=dict(type='SpatialCrossAttentionBEV', bev_h=128, bev_w=128),
    pts_bbox_head=dict(type='DETR3DHead', num_query=300, num_classes=len(classes))
)
