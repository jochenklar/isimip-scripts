import json

path = 'ISIMIP3a/InputData/geo_conditions/masks/giorgimask.nc'
codes = [
    'ALA', 'AMZ', 'CAM', 'CAN', 'CAS', 'CSA', 'EAF', 'EAS', 'ENA', 'EQF',
    'GRL', 'MED', 'NAS', 'NAU', 'NEE', 'NEU', 'SAF', 'SAH', 'SAS', 'SAU',
    'SEA', 'SQF', 'SSA', 'TIB', 'WAF', 'WNA',
]

regions = [
    {
        'type': 'mask',
        'specifier': f'giorgi-{code.lower()}',
        'mask_path': path,
        'mask_variable': f'm_{code}'
    } for code in codes
]

print(json.dumps(regions, indent=2))
