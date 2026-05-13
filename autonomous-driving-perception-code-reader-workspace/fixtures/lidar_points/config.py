point_cloud_range = [-54.0, -54.0, -5.0, 54.0, 54.0, 3.0]
voxel_size = [0.075, 0.075, 0.2]
classes = ['car', 'cyclist', 'pedestrian']

train_pipeline = [
    dict(type='LoadPointsFromFile', load_dim=5, use_dim=[0, 1, 2, 3, 4]),
    dict(type='LoadPointsFromMultiSweeps', sweeps_num=9, use_dim=[0, 1, 2, 3, 4]),
    dict(type='PointsRangeFilter', point_cloud_range=point_cloud_range),
    dict(type='ObjectRangeFilter', point_cloud_range=point_cloud_range),
    dict(type='Collect3D', keys=['points', 'gt_bboxes_3d', 'gt_labels_3d'])
]

model = dict(
    type='MiniCenterPoint',
    pts_voxel_layer=dict(max_num_points=10, voxel_size=voxel_size, point_cloud_range=point_cloud_range, max_voxels=(90000, 120000)),
    pts_voxel_encoder=dict(type='PillarFeatureNet', in_channels=5, feat_channels=[64]),
    pts_middle_encoder=dict(type='PointPillarsScatter', output_shape=[1440, 1440]),
    pts_backbone=dict(type='SECOND', in_channels=64),
    pts_bbox_head=dict(type='CenterHead', tasks=[dict(num_class=3, class_names=classes)])
)
