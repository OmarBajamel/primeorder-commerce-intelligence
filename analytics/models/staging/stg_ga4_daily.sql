select
    cast(date as date) as activity_date,
    cast(channel as varchar) as channel,
    cast(source as varchar) as source,
    cast(medium as varchar) as medium,
    cast(campaign as varchar) as campaign,
    lower(cast(device as varchar)) as device,
    cast(sessions as bigint) as sessions,
    cast(users as bigint) as users,
    cast(product_views as bigint) as product_views,
    cast(add_to_carts as bigint) as add_to_carts,
    cast(begin_checkouts as bigint) as begin_checkouts,
    cast(purchases as bigint) as purchases,
    cast(purchase_revenue_sar as decimal(18, 2)) as purchase_revenue_sar,
    cast(consent_state_coverage as double) as consent_state_coverage
from {{ ref('ga4_daily') }}
