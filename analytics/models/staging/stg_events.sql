select
    cast(date as date) as event_date,
    cast(source as varchar) as source,
    lower(cast(device as varchar)) as device,
    cast(event_name as varchar) as event_name,
    cast(event_count as bigint) as event_count,
    cast(transaction_id_parameter_coverage as double) as transaction_id_parameter_coverage,
    cast(currency_parameter_coverage as double) as currency_parameter_coverage,
    cast(value_parameter_coverage as double) as value_parameter_coverage,
    cast(items_parameter_coverage as double) as items_parameter_coverage,
    cast(item_id_parameter_coverage as double) as item_id_parameter_coverage,
    cast(item_name_parameter_coverage as double) as item_name_parameter_coverage,
    cast(item_category_parameter_coverage as double) as item_category_parameter_coverage,
    cast(price_parameter_coverage as double) as price_parameter_coverage,
    cast(quantity_parameter_coverage as double) as quantity_parameter_coverage,
    cast(promotion_parameter_coverage as double) as promotion_parameter_coverage,
    cast(consent_state_coverage as double) as consent_state_coverage
from {{ ref('events') }}
