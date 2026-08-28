select
    campaign,
    channel,
    concat(campaign, '|', channel) as campaign_key,
    sum(sessions) as sessions,
    sum(purchases) as purchases,
    sum(net_revenue_sar) as attributed_revenue_sar,
    sum(ad_spend_sar) as ad_spend_sar,
    sum(ad_spend_sar) / nullif(sum(purchases), 0) as cost_per_acquisition_sar,
    sum(net_revenue_sar) / nullif(sum(ad_spend_sar), 0) as roas
from {{ ref('stg_commerce_daily') }}
group by 1, 2
