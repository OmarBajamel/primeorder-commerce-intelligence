with ga4 as (
    select channel, source, medium,
           sum(sessions) as sessions,
           sum(users) as active_user_days,
           sum(purchases) as tracked_purchases,
           sum(purchase_revenue_sar) as tracked_purchase_revenue_sar
    from {{ ref('stg_ga4_daily') }}
    group by 1, 2, 3
), spend as (
    select channel, source, medium, sum(ad_spend_sar) as ad_spend_sar
    from {{ ref('stg_google_ads_daily') }}
    group by 1, 2, 3
)
select
    ga4.channel,
    ga4.source,
    ga4.medium,
    concat(ga4.channel, '|', ga4.source, '|', ga4.medium) as acquisition_key,
    ga4.sessions,
    ga4.active_user_days,
    ga4.tracked_purchases,
    ga4.tracked_purchase_revenue_sar,
    spend.ad_spend_sar,
    ga4.tracked_purchases::double / nullif(ga4.sessions, 0) as conversion_rate,
    ga4.tracked_purchase_revenue_sar / nullif(spend.ad_spend_sar, 0) as roas
from ga4
left join spend using (channel, source, medium)
