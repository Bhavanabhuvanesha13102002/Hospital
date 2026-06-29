DATASETS = [
    {
        "name": "general_info",
        "url": "https://data.cms.gov/provider-data/dataset/xubh-q36u",
        "filename": "general_info.csv",
        "raw_table": "raw_general_info",
        "bronze_table": "bronze_general_info",
    
    },
    {
        "name": "readmissions",
        "url": "https://data.cms.gov/provider-data/dataset/9n3s-kdb3",
        "filename": "readmissions.csv",
        "raw_table": "raw_readmissions",
        "bronze_table": "bronze_readmissions",
    },
    {
        "name": "infections",
        "url": "https://data.cms.gov/provider-data/dataset/77hc-ibv8",
        "filename": "infections.csv",
        "raw_table": "raw_infections",
        "bronze_table": "bronze_infections",
        "primary_key": "infections_id"
    },
    {
        "name": "complications",
        "url": "https://data.cms.gov/provider-data/dataset/ynj2-r877",
        "filename": "complications.csv",
        "raw_table": "raw_complications",
        "bronze_table": "bronze_complications",
        "primary_key": "complications_id"
    },
    {
        "name": "hcahps",
        "url": "https://data.cms.gov/provider-data/dataset/dgck-syfz",
        "filename": "hcahps.csv",
        "raw_table": "raw_hcahps",
        "bronze_table": "bronze_hcahps",
        "primary_key": "hcahps_id"
    }
]
   