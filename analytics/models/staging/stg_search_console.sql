select
    cast(date as date) as search_date,
    cast(query as varchar) as query,
    cast(page as varchar) as page,
    upper(cast(country as varchar)) as country,
    lower(cast(device as varchar)) as device,
    cast(clicks as bigint) as clicks,
    cast(impressions as bigint) as impressions,
    cast(ctr as double) as reported_ctr,
    cast(average_position as double) as average_position,
    cast(is_branded as boolean) as is_branded
from {{ ref('search_console') }}
