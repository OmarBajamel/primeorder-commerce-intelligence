select
    channel,
    source,
    medium,
    concat(channel, '|', source, '|', medium) as acquisition_key,
    sum(sessions) as sessions,
    sum(users) as users,
    sum(purchases) as purchases,
    sum(net_revenue_sar) as net_revenue_sar,
    sum(ad_spend_sar) as ad_spend_sar,
    sum(purchases)::double / nullif(sum(sessions), 0) as conversion_rate,
    sum(net_revenue_sar) / nullif(sum(ad_spend_sar), 0) as roas
from {{ ref('stg_commerce_daily') }}
group by 1, 2, 3
