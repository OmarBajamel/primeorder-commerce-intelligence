select 1
from {{ ref('mart_executive_daily') }}
having count(*) < 365
   or date_diff('day', min(activity_date), max(activity_date)) + 1 <> count(*)
