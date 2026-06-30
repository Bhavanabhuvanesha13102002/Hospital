BASE_VOLUME_PATH = "/Volumes/hospitalchecks/default/hospital_quality_volume"


DATASETS = [
    {
        "name": "general_info",
        "url": "https://data.cms.gov/provider-data/dataset/xubh-q36u",
        "filename": "general_info.csv",

        "raw_table": "raw_general_info",
        "bronze_table": "bronze_general_info",
        "archive_table": "archive_general_info",

        "raw_path": f"{BASE_VOLUME_PATH}/raw/general_info/general_info.csv",
        "bronze_path": f"{BASE_VOLUME_PATH}/bronze/general_info",
        "archive_path": f"{BASE_VOLUME_PATH}/archive/general_info",

        "required_columns": [
            "facility_id",
            "facility_name",
            "address",
            "city_town",
            "state",
            "zip_code",
            "county_parish",
            "telephone_number",
            "hospital_type",
            "hospital_ownership",
            "emergency_services",
            "hospital_overall_rating"
        ],

        "dedup_columns": ["facility_id"],

        "compare_columns": [
            "facility_name",
            "address",
            "city_town",
            "state",
            "zip_code",
            "county_parish",
            "telephone_number",
            "hospital_type",
            "hospital_ownership",
            "emergency_services",
            "hospital_overall_rating"
        ]
    },

    {
        "name": "readmissions",
        "url": "https://data.cms.gov/provider-data/dataset/9n3s-kdb3",
        "filename": "readmissions.csv",

        "raw_table": "raw_readmissions",
        "bronze_table": "bronze_readmissions",
        "archive_table": "archive_readmissions",

        "raw_path": f"{BASE_VOLUME_PATH}/raw/readmissions/readmissions.csv",
        "bronze_path": f"{BASE_VOLUME_PATH}/bronze/readmissions",
        "archive_path": f"{BASE_VOLUME_PATH}/archive/readmissions",

        "required_columns": [
            "facility_id",
            "facility_name",
            "number_of_discharges",
            "number_of_readmissions",
            "measure_name",
            "excess_readmission_ratio",
            "state"
        ],

        "dedup_columns": ["facility_id", "measure_name"],

        "compare_columns": [
            "facility_name",
            "number_of_discharges",
            "number_of_readmissions",
            "measure_name",
            "excess_readmission_ratio",
            "state"
        ]
    },

    {
        "name": "infections",
        "url": "https://data.cms.gov/provider-data/dataset/77hc-ibv8",
        "filename": "infections.csv",

        "raw_table": "raw_infections",
        "bronze_table": "bronze_infections",
        "archive_table": "archive_infections",

        "raw_path": f"{BASE_VOLUME_PATH}/raw/infections/infections.csv",
        "bronze_path": f"{BASE_VOLUME_PATH}/bronze/infections",
        "archive_path": f"{BASE_VOLUME_PATH}/archive/infections",

        "required_columns": [
            "facility_id",
            "facility_name",
            "address",
            "compared_to_national",
            "measure_id",
            "measure_name",
            "score",
            "state"
        ],

        "dedup_columns": ["facility_id", "measure_id"],

        "compare_columns": [
            "facility_name",
            "measure_name",
            "score",
            "state"
        ]
    },

    {
        "name": "complications",
        "url": "https://data.cms.gov/provider-data/dataset/ynj2-r877",
        "filename": "complications.csv",

        "raw_table": "raw_complications",
        "bronze_table": "bronze_complications",
        "archive_table": "archive_complications",

        "raw_path": f"{BASE_VOLUME_PATH}/raw/complications/complications.csv",
        "bronze_path": f"{BASE_VOLUME_PATH}/bronze/complications",
        "archive_path": f"{BASE_VOLUME_PATH}/archive/complications",

        "required_columns": [
            "facility_id",
            "facility_name",
            "address",
            "compared_to_national",
            "denominator",
            "measure_id",
            "measure_name",
            "score",
            "state"
        ],

        "dedup_columns": ["facility_id", "measure_id"],

        "compare_columns": [
            "facility_name",
            "measure_name",
            "compared_to_national",
            "denominator",
            "score",
            "state"
        ]
    },

    {
        "name": "hcahps",
        "url": "https://data.cms.gov/provider-data/dataset/dgck-syfz",
        "filename": "hcahps.csv",

        "raw_table": "raw_hcahps",
        "bronze_table": "bronze_hcahps",
        "archive_table": "archive_hcahps",

        "raw_path": f"{BASE_VOLUME_PATH}/raw/hcahps/hcahps.csv",
        "bronze_path": f"{BASE_VOLUME_PATH}/bronze/hcahps",
        "archive_path": f"{BASE_VOLUME_PATH}/archive/hcahps",

        "required_columns": [
            "facility_id",
            "facility_name",
            "hcahps_measure_id",
            "hcahps_question",
            "hcahps_answer_description",
            "patient_survey_star_rating",
            "survey_response_rate_percent",
            "state"
        ],

        "dedup_columns": ["facility_id", "hcahps_measure_id"],

        "compare_columns": [
            "facility_name",
            "hcahps_measure_id",
            "hcahps_question",
            "patient_survey_star_rating",
            "survey_response_rate_percent",
            "state"
        ]
    }
]
