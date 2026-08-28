select
    cast(date as date) as activity_date,
    cast(channel as varchar) as channel,
    cast(source as varchar) as source,
    cast(medium as varchar) as medium,
    cast(campaign as varchar) as campaign,
    lower(cast(device as varchar)) as device,
    cast(city as varchar) as city,
    lower(cast(payment_method as varchar)) as payment_method,
    cast(purchases as bigint) as purchases,
    cast(units_sold as bigint) as units_sold,
    cast(gross_revenue_sar as decimal(18, 2)) as gross_revenue_sar,
    cast(discount_sar as decimal(18, 2)) as discount_sar,
    cast(refund_sar as decimal(18, 2)) as refund_sar,
    cast(net_revenue_sar as decimal(18, 2)) as net_revenue_sar,
    cast(cost_sar as decimal(18, 2)) as cost_sar
from {{ ref('commerce_daily') }}
