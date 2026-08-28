select
    event_date,
    event_name,
    sum(event_count) as event_count,
    sum(event_count * transaction_id_parameter_coverage) / nullif(sum(event_count), 0) as transaction_id_parameter_completeness,
    sum(event_count * currency_parameter_coverage) / nullif(sum(event_count), 0) as currency_parameter_completeness,
    sum(event_count * value_parameter_coverage) / nullif(sum(event_count), 0) as value_parameter_completeness,
    sum(event_count * items_parameter_coverage) / nullif(sum(event_count), 0) as items_parameter_completeness,
    sum(event_count * item_id_parameter_coverage) / nullif(sum(event_count), 0) as item_id_parameter_completeness,
    sum(event_count * item_name_parameter_coverage) / nullif(sum(event_count), 0) as item_name_parameter_completeness,
    sum(event_count * item_category_parameter_coverage) / nullif(sum(event_count), 0) as item_category_parameter_completeness,
    sum(event_count * price_parameter_coverage) / nullif(sum(event_count), 0) as price_parameter_completeness,
    sum(event_count * quantity_parameter_coverage) / nullif(sum(event_count), 0) as quantity_parameter_completeness,
    sum(event_count * promotion_parameter_coverage) / nullif(sum(event_count), 0) as promotion_parameter_completeness,
    sum(event_count * consent_state_coverage) / nullif(sum(event_count), 0) as consent_state_coverage
from {{ ref('stg_events') }}
group by 1, 2
