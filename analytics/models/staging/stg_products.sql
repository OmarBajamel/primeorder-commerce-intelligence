select
    cast(product_id as varchar) as product_id,
    cast(product_name_en as varchar) as product_name_en,
    cast(product_name_ar as varchar) as product_name_ar,
    cast(category as varchar) as category,
    cast(brand as varchar) as brand,
    cast(list_price_sar as decimal(18, 2)) as list_price_sar,
    cast(unit_cost_sar as decimal(18, 2)) as unit_cost_sar,
    cast(is_active as boolean) as is_active
from {{ ref('products') }}
