select
    activity_date,
    sessions, users, purchases, units_sold,
    gross_revenue_sar, refund_sar, net_revenue_sar, discount_sar, ad_spend_sar,
    net_revenue_sar - cost_sar as gross_margin_sar,
    purchases::double / nullif(sessions, 0) as purchase_conversion_rate,
    net_revenue_sar / nullif(purchases, 0) as average_order_value_sar,
    refund_sar / nullif(gross_revenue_sar, 0) as refund_rate,
    net_revenue_sar / nullif(sessions, 0) as revenue_per_session_sar
from {{ ref('int_daily_commerce') }}
