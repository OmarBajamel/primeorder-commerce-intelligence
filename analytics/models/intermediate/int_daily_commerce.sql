select
    activity_date,
    sum(purchases) as completed_orders,
    sum(units_sold) as units_sold,
    sum(gross_revenue_sar) as gross_revenue_sar,
    sum(discount_sar) as discount_sar,
    sum(refund_sar) as refund_sar,
    sum(net_revenue_sar) as net_revenue_sar,
    sum(cost_sar) as cost_sar
from {{ ref('stg_commerce_daily') }}
group by 1
