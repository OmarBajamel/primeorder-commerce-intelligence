with item_totals as (
    select order_id, sum(item_revenue_sar - discount_sar) as order_item_revenue_sar
    from {{ ref('stg_order_items') }}
    group by 1
)
select
    i.order_id,
    i.order_date,
    i.product_id,
    coalesce(p.product_name_en, 'Unmapped product') as product_name_en,
    coalesce(p.product_name_ar, 'منتج غير مطابق') as product_name_ar,
    coalesce(p.category, 'Unmapped') as category,
    coalesce(p.brand, 'Unknown') as brand,
    case when p.product_id is null then false else true end as is_product_mapped,
    i.quantity,
    i.item_revenue_sar,
    i.item_cost_sar,
    i.discount_sar,
    case
        when totals.order_item_revenue_sar = 0 then 0
        else o.refund_sar * (i.item_revenue_sar - i.discount_sar) / totals.order_item_revenue_sar
    end as allocated_refund_sar,
    o.anonymous_customer_id,
    o.customer_type,
    o.channel,
    o.source,
    o.medium,
    o.campaign,
    o.device,
    o.city,
    o.payment_method,
    o.coupon_group,
    o.order_status,
    o.refund_sar
from {{ ref('stg_order_items') }} i
inner join {{ ref('stg_orders') }} o using (order_id)
inner join item_totals totals using (order_id)
left join {{ ref('stg_products') }} p using (product_id)
