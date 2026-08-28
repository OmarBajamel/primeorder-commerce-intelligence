with ga4 as (
    select campaign, channel,
           sum(sessions) as sessions,
           sum(purchases) as tracked_purchases,
           sum(purchase_revenue_sar) as tracked_purchase_revenue_sar
    from {{ ref('stg_ga4_daily') }}
    group by 1, 2
), spend as (
    select campaign, channel, sum(ad_spend_sar) as ad_spend_sar
    from {{ ref('stg_google_ads_daily') }}
    group by 1, 2
)
select
    ga4.campaign,
    ga4.channel,
    concat(ga4.campaign, '|', ga4.channel) as campaign_key,
    ga4.sessions,
    ga4.tracked_purchases,
    ga4.tracked_purchase_revenue_sar,
    spend.ad_spend_sar,
    spend.ad_spend_sar / nullif(ga4.tracked_purchases, 0) as cost_per_acquisition_sar,
    ga4.tracked_purchase_revenue_sar / nullif(spend.ad_spend_sar, 0) as roas
from ga4
left join spend using (campaign, channel)
