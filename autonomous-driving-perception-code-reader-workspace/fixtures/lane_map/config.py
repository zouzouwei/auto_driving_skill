lane_types = ['single_white_solid', 'single_white_dashed', 'double_yellow_solid', 'road_edge']
map_classes = ['lane_divider', 'road_boundary', 'ped_crossing']

train_pipeline = [
    dict(type='LoadFrontViewImage', final_dim=(320, 800)),
    dict(type='LoadLaneAnnotations3D', with_topology=True),
    dict(type='LaneToBEVPolyline', xbound=[0, 60, 0.5], ybound=[-30, 30, 0.5], num_points=20),
    dict(type='NormalizeLanePoints', pc_range=[0, -30, -2, 60, 30, 4]),
    dict(type='Collect', keys=['img', 'lane_points', 'lane_labels', 'lane_adj'])
]

model = dict(
    type='MiniLaneMapNet',
    img_backbone=dict(type='SwinTransformer'),
    view_transform=dict(type='IPM', use_camera_calibration=True),
    lane_decoder=dict(type='PolylineTransformerDecoder', num_query=100, num_points=20),
    topology_head=dict(type='LaneTopologyHead')
)
