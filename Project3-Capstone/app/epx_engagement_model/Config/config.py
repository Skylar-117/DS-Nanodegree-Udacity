# Database info:
DB_USER = 'root'
DB_PASSWORD = '1tism0db'
DB_HOST = 'localhost'
DB_NAME = 'EpxCS'

# Database table used for pulling data out:
DB_TABLE = 'all6_32'

# Specific patient ID:
DB_PID = 1990

# Features:
FEATURES = [
    'patientId', 'dob', 'start_date', 'end_date', 'time_length_d', 'intervention_name',
    'types','calls', 'messages', 'avg_rate', 'avg_communication', 'avg_frequency', 'no_rate', 'no_communication','no_frequency',
    '1_14_rr', '1_14_sc', '1_14_rc', '1_14_avg_respond_duration_s', '1_14_respond_inAdvance_count', '1_14_alert_count', '1_14_isRead_count', '1_14_avg_alert_duration_d',
    '15_28_rr', '15_28_sc', '15_28_rc', '15_28_avg_respond_duration_s', '15_28_respond_inAdvance_count', '15_28_alert_count', '15_28_isRead_count', '15_28_avg_alert_duration_d',
    '29_42_rr', '29_42_sc', '29_42_rc', '29_42_avg_respond_duration_s', '29_42_respond_inAdvance_count', '29_42_alert_count', '29_42_isRead_count', '29_42_avg_alert_duration_d',
    '43_56_rr', '43_56_sc', '43_56_rc', '43_56_avg_respond_duration_s', '43_56_respond_inAdvance_count', '43_56_alert_count', '43_56_isRead_count', '43_56_avg_alert_duration_d',
    '2m1w_rr'
    ]

# Features need to be dropped afterwards:
DROP_FEATURES = ['patientId','dob','start_date','end_date','intervention_name']

# New created features:
NEW_CREATED_FEATURES_AGE = ['age_range','age_isnull']
NEW_CREATED_FEATURES_DURATION = [
    ('1_14_zeroDuration', '1_14_avg_respond_duration_s'),
    ('15_28_zeroDuration', '15_28_avg_respond_duration_s'),
    ('29_42_zeroDuration', '29_42_avg_respond_duration_s'),
    ('43_56_zeroDuration', '43_56_avg_respond_duration_s'),
]
NEW_CREATED_FEATURES_INTERVENTION = [
    'intervention_name_epxasthma',
    'intervention_name_epxcopd',
    'intervention_name_epxdepress',
    'intervention_name_epxdiabetes',
    'intervention_name_epxheart',
    'intervention_name_epxhyper'
]