select
    query,
    page,
    is_branded,
    concat(query, '|', page) as search_key,
    sum(clicks) as clicks,
    sum(impressions) as impressions,
    sum(clicks)::double / nullif(sum(impressions), 0) as ctr,
    sum(average_position * impressions) / nullif(sum(impressions), 0) as average_position,
    max(search_date) as fresh_through
from {{ ref('stg_search_console') }}
group by 1, 2, 3
