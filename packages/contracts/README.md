# Shared public analytics contracts

`index.ts` describes the static JSON contract and `primeorder_contracts` contains
the equivalent Pydantic response models used by FastAPI. Currency values are SAR,
rates are decimal fractions, dates are ISO-8601, and every public response carries
the synthetic-data disclosure.

Revenue semantics are consistent across runtimes: gross revenue is pre-discount
and pre-refund; net revenue is gross minus discounts and refunds; average order
value is net revenue divided by completed purchases; gross margin is net revenue
minus reliable synthetic cost.
