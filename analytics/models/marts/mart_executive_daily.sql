select
    commerce.activity_date,
    ga4.sessions,
    ga4.active_user_days,
    ga4.product_views,
    ga4.add_to_carts,
    ga4.begin_checkouts,
    ga4.tracked_purchases,
    commerce.completed_orders,
    commerce.units_sold,
    commerce.gross_revenue_sar,
    commerce.refund_sar,
    commerce.net_revenue_sar,
    commerce.discount_sar,
    ads.ad_spend_sar,
    commerce.net_revenue_sar - commerce.cost_sar as gross_margin_sar,
    ga4.tracked_purchases::double / nullif(ga4.sessions, 0) as purchase_conversion_rate,
    commerce.net_revenue_sar / nullif(commerce.completed_orders, 0) as average_order_value_sar,
    commerce.refund_sar / nullif(commerce.gross_revenue_sar, 0) as refund_rate,
    ga4.tracked_purchase_revenue_sar / nullif(ga4.sessions, 0) as revenue_per_session_sar
from {{ ref('int_daily_commerce') }} commerce
inner join {{ ref('int_daily_ga4') }} ga4 using (activity_date)
left join (
    select activity_date, sum(ad_spend_sar) as ad_spend_sar
    from {{ ref('stg_google_ads_daily') }} group by 1
) ads using (activity_date)
