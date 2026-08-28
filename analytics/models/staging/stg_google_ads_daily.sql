select
    cast(date as date) as activity_date,
    cast(channel as varchar) as channel,
    cast(source as varchar) as source,
    cast(medium as varchar) as medium,
    cast(campaign as varchar) as campaign,
    cast(clicks as bigint) as clicks,
    cast(conversions as double) as conversions,
    cast(conversion_value_sar as decimal(18, 2)) as conversion_value_sar,
    cast(ad_spend_sar as decimal(18, 2)) as ad_spend_sar
from {{ ref('google_ads_daily') }}
