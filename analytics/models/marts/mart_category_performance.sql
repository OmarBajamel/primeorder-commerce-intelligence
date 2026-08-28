select
    category,
    sum(quantity) as units_sold,
    sum(item_revenue_sar) as gross_revenue_sar,
    sum(discount_sar) as discount_sar,
    sum(allocated_refund_sar) as refund_sar,
    sum(item_revenue_sar - discount_sar - allocated_refund_sar) as revenue_sar,
    sum(item_revenue_sar - discount_sar - allocated_refund_sar - item_cost_sar) as gross_margin_sar,
    sum(item_revenue_sar - discount_sar - allocated_refund_sar) / nullif(sum(sum(item_revenue_sar - discount_sar - allocated_refund_sar)) over (), 0) as revenue_share
from {{ ref('int_orders_enriched') }}
group by 1
