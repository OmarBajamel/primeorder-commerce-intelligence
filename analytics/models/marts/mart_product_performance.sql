select
    product_id,
    product_name_en,
    product_name_ar,
    category,
    brand,
    is_product_mapped,
    sum(quantity) as units_sold,
    sum(item_revenue_sar) as gross_revenue_sar,
    sum(discount_sar) as discount_sar,
    sum(allocated_refund_sar) as refund_sar,
    sum(item_revenue_sar - discount_sar - allocated_refund_sar) as revenue_sar,
    sum(item_revenue_sar - discount_sar - allocated_refund_sar - item_cost_sar) as gross_margin_sar,
    sum(item_revenue_sar - discount_sar - allocated_refund_sar - item_cost_sar) / nullif(sum(item_revenue_sar - discount_sar - allocated_refund_sar), 0) as gross_margin_rate
from {{ ref('int_orders_enriched') }}
group by 1, 2, 3, 4, 5, 6
