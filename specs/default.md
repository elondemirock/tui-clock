  Add optional tracking for water consumption achievements: daily record (highest single-day drink count) and
  streak (consecutive days meeting a configurable goal).

  Track consecutive days where the user meets their daily drink count goal - goal should be set by the user in a config file
  Display in the water stats pop-up, underneath water emoji + count (use similar emoji + metric count format)
  If enabled, water counter should should "x/y" where x is daily count and y is daily goal
  
  Also track the highest drink count logged in a single day, computed from existing history in .water_stats - no new persistence needed
  Display in the water stats popup, underneath the streak display (if enabled)

  Both features are opt-in (disabled by default)


