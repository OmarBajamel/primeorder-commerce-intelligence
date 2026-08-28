select *
from {{ ref('mart_search_performance') }}
where clicks > impressions or ctr < 0 or ctr > 1 or average_position <= 0
