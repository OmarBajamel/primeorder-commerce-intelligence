select *
from {{ ref('stg_commerce_daily') }}
where activity_date < date '2025-01-01' or activity_date > date '2025-12-31'
