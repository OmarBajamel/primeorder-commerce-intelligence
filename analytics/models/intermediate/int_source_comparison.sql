with salla as (
    select activity_date, sum(purchases) as salla_purchases, sum(net_revenue_sar) as salla_revenue_sar
    from {{ ref('stg_commerce_daily') }} group by 1
),
ga4 as (
    select activity_date, sum(purchases) as ga4_purchases, sum(purchase_revenue_sar) as ga4_revenue_sar
    from {{ ref('stg_ga4_daily') }} group by 1
)
select
    s.activity_date,
    s.salla_purchases,
    g.ga4_purchases,
    s.salla_revenue_sar,
    g.ga4_revenue_sar,
    abs(s.salla_purchases - g.ga4_purchases) / nullif(s.salla_purchases, 0) as transaction_variance_rate,
    abs(s.salla_revenue_sar - g.ga4_revenue_sar) / nullif(s.salla_revenue_sar, 0) as revenue_variance_rate
from salla s inner join ga4 g using (activity_date)
