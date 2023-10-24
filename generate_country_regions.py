import json

path = 'ISIMIP3a/InputData/geo_conditions/countrymasks/countrymasks.nc'
codes = [
    'AFG', 'ALB', 'DZA', 'AND', 'AGO', 'ATG', 'ARG', 'ARM', 'AUS', 'AUT',
    'AZE', 'BHS', 'BHR', 'BGD', 'BRB', 'BLR', 'BEL', 'BLZ', 'BEN', 'BTN',
    'BOL', 'BIH', 'BWA', 'BRA', 'BRN', 'BGR', 'BFA', 'BDI', 'KHM', 'CMR',
    'CAN', 'CPV', 'CSID', 'CYM', 'CAF', 'TCD', 'CHL', 'CHN', 'COL', 'COM',
    'COG', 'CRI', 'HRV', 'CUB', 'CYP', 'CZE', 'CIV', 'PRK', 'COD', 'DNK',
    'DJI', 'DMA', 'DOM', 'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'EST', 'ETH',
    'FLK', 'FRO', 'FJI', 'FIN', 'FRA', 'GUF', 'PYF', 'ATF', 'GAB', 'GMB',
    'GEO', 'DEU', 'GHA', 'GRC', 'GRL', 'GRD', 'GLP', 'GUM', 'GTM', 'GIN',
    'GNB', 'GUY', 'HTI', 'HMD', 'HND', 'HKG', 'HUN', 'ISL', 'IND', 'IOSID',
    'IDN', 'IRN', 'IRQ', 'IRL', 'IMN', 'ISR', 'ITA', 'JAM', 'JPN',
    'JOR', 'KAZ', 'KEN', 'KIR', 'KWT', 'KGZ', 'LAO', 'LVA', 'LBN', 'LSO',
    'LBR', 'LBY', 'LTU', 'LUX', 'MDG', 'MWI', 'MYS', 'MLI', 'MLT', 'MTQ',
    'MRT', 'MUS', 'MYT', 'MEX', 'FSM', 'MDA', 'MNG', 'MNE', 'MAR', 'MOZ',
    'MMR', 'NAM', 'NPL', 'NLD', 'NCL', 'NZL', 'NIC', 'NER', 'NGA',
    'NIU', 'NOR', 'OMN', 'PSID', 'PAK', 'PLW', 'PSE', 'PAN', 'PNG', 'PRY',
    'PER', 'PHL', 'POL', 'PRT', 'PRI', 'QAT', 'KOR', 'ROU', 'RUS', 'RWA',
    'REU', 'LCA', 'SPM', 'VCT', 'WSM', 'STP', 'SAU', 'SEN', 'SRB', 'SLE',
    'SGP', 'SVK', 'SVN', 'SLB', 'SOM', 'ZAF', 'SGS', 'SSD', 'ESP', 'LKA',
    'SDN', 'SUR', 'SJM', 'SWZ', 'SWE', 'CHE', 'SYR', 'TWN', 'TJK', 'THA',
    'MKD', 'TLS', 'TGO', 'TON', 'TTO', 'TUN', 'TUR', 'TKM', 'GBR', 'UGA',
    'UKR', 'ARE', 'TZA', 'VIR', 'USA', 'URY', 'UZB', 'VUT', 'VEN', 'VNM',
    'ESH', 'YEM', 'ZMB', 'ZWE'
]

regions = [
    {
        'type': 'mask',
        'specifier': f'country-{code.lower()}',
        'mask_path': path,
        'mask_variable': f'm_{code}'
    } for code in codes
]

print(json.dumps(regions, indent=2))
