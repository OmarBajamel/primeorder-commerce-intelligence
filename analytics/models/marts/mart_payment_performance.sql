select
    payment_method,
    count(distinct order_id) as orders,
    sum(item_revenue_sar) as gross_revenue_sar,
    sum(discount_sar) as discount_sar,
    sum(allocated_refund_sar) as refund_sar,
    sum(item_revenue_sar - discount_sar - allocated_refund_sar) as net_revenue_sar,
    sum(allocated_refund_sar) / nullif(sum(item_revenue_sar - discount_sar), 0) as refund_rate,
    sum(item_revenue_sar - discount_sar - allocated_refund_sar) / nullif(count(distinct order_id), 0) as average_order_value_sar
from {{ ref('int_orders_enriched') }}
group by 1
