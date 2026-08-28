select
    cast(date as date) as activity_date,
    lower(cast(device as varchar)) as device,
    upper(cast(country as varchar)) as country,
    cast(sessions as bigint) as sessions,
    cast(dead_clicks as bigint) as dead_clicks,
    cast(rage_clicks as bigint) as rage_clicks,
    cast(excessive_scrolls as bigint) as excessive_scrolls,
    cast(javascript_errors as bigint) as javascript_errors
from {{ ref('clarity_daily') }}
