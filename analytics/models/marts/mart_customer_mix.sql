select
    customer_type,
    count(distinct anonymous_customer_id) as anonymous_customers,
    count(distinct order_id) as orders,
    sum(item_revenue_sar - discount_sar - allocated_refund_sar) as net_revenue_sar,
    count(distinct order_id)::double / nullif(count(distinct anonymous_customer_id), 0) as orders_per_customer,
    sum(item_revenue_sar - discount_sar - allocated_refund_sar) / nullif(sum(sum(item_revenue_sar - discount_sar - allocated_refund_sar)) over (), 0) as revenue_share
from {{ ref('int_orders_enriched') }}
group by 1
