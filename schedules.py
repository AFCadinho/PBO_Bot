# schedules.py
from datetime import datetime

BUG_CATCHING_SCHEDULE = [
    {"day": "Monday", "hour": 19, "role_id": 1310224429669679184},
    {"day": "Wednesday", "hour": 3, "role_id": 1310224429669679184},
    {"day": "Wednesday", "hour": 19, "role_id": 1310224429669679184},
    {"day": "Thursday", "hour": 3, "role_id": 1310224429669679184},
    {"day": "Friday", "hour": 3, "role_id": 1310224429669679184},
    {"day": "Saturday", "hour": 19, "role_id": 1310224429669679184},
    {"day": "Sunday", "hour": 17, "role_id": 1310224429669679184},
]

FISHING_COMPETITION_SCHEDULE = [
    {"day": "Monday", "hour": 3, "role_id": 1310224290196623501},
    {"day": "Tuesday", "hour": 3, "role_id": 1310224290196623501},
    {"day": "Tuesday", "hour": 19, "role_id": 1310224290196623501},
    {"day": "Thursday", "hour": 19, "role_id": 1310224290196623501},
    {"day": "Friday", "hour": 19, "role_id": 1310224290196623501},
    {"day": "Saturday", "hour": 3, "role_id": 1310224290196623501},
    {"day": "Sunday", "hour": 11, "role_id": 1310224290196623501},
]

DYNAMAX_INVASION_SCHEDULE = [
    {"day": "Wednesday", "hour": 11, "role_id": 1310224206637830206},
    {"day": "Wednesday", "hour": 19, "role_id": 1310224206637830206},
    {"day": "Friday", "hour": 2, "role_id": 1310224206637830206},
    {"day": "Friday", "hour": 19, "role_id": 1310224206637830206},
    {"day": "Saturday", "hour": 11, "role_id": 1310224206637830206},
    {"day": "Saturday", "hour": 17, "role_id": 1310224206637830206},
    {"day": "Sunday", "hour": 4, "role_id": 1310224206637830206},
    {"day": "Sunday", "hour": 19, "role_id": 1310224206637830206},  
]

CREW_WARS_SCHEDULE = [
    {"day": "Saturday", "hour": 4, "role_id": 1310224095228465214, "tier": "OU"},
    {"day": "Sunday", "hour": 1, "role_id": 1310224095228465214, "tier": "OU"},
    {"day": "Sunday", "hour": 19, "role_id": 1310224095228465214, "tier": "OU"},
    {"day": "Monday", "hour": 17, "role_id": 1310224095228465214, "tier": "UU"},
    {"day": "Wednesday", "hour": 11, "role_id": 1310224095228465214, "tier": "UU"},
    {"day": "Wednesday", "hour": 20, "role_id": 1310224095228465214, "tier": "OU"},
    {"day": "Thursday", "hour": 20, "role_id": 1310224095228465214, "tier": "UU"},
]

RUBBING_ADINHOS_BELLY = [
    {"day": datetime.now().strftime("%A"),  # Today's day
     "hour": datetime.now().hour,          # Current hour
     "minute": (datetime.now().minute + 2) % 60,  # 2 minutes from now
     "role_id": 1310224206637830206},      # Replace with a valid role ID in your server
]
