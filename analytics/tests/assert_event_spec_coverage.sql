with expected(event_name) as (
    values ('view_item_list'), ('select_item'), ('view_item'), ('add_to_cart'), ('remove_from_cart'),
           ('view_cart'), ('begin_checkout'), ('add_shipping_info'), ('add_payment_info'), ('purchase'), ('refund')
), actual as (
    select event_name, sum(event_count) as event_count from {{ ref('stg_events') }} group by 1
)
select expected.event_name
from expected left join actual using (event_name)
where actual.event_name is null or actual.event_count <= 0
union all
select event_name
from {{ ref('stg_events') }}
where least(transaction_id_parameter_coverage, currency_parameter_coverage, value_parameter_coverage,
            items_parameter_coverage, item_id_parameter_coverage, item_name_parameter_coverage,
            item_category_parameter_coverage, price_parameter_coverage, quantity_parameter_coverage,
            promotion_parameter_coverage, consent_state_coverage) < 0
   or greatest(transaction_id_parameter_coverage, currency_parameter_coverage, value_parameter_coverage,
               items_parameter_coverage, item_id_parameter_coverage, item_name_parameter_coverage,
               item_category_parameter_coverage, price_parameter_coverage, quantity_parameter_coverage,
               promotion_parameter_coverage, consent_state_coverage) > 1
