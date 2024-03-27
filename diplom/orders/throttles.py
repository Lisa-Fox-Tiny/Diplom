from rest_framework.throttling import ScopedRateThrottle


class AllThrottle(ScopedRateThrottle):
    scope = 'all_throttle'
    rate = '5/minute'