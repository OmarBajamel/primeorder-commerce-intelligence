select anonymous_customer_id
from {{ ref('stg_orders') }}
group by 1
having count(distinct customer_type) <> 1
   or max(case when customer_type = 'returning' and customer_first_purchase_date >= date '2025-01-01' then 1
               when customer_type = 'new' and customer_first_purchase_date < date '2025-01-01' then 1
               else 0 end) <> 0
