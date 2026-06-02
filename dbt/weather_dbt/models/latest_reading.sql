WITH staged AS (
    SELECT *
    FROM {{ ref('stg_weather') }}
),

latest AS (
    SELECT *
    FROM staged
    ORDER BY ingested_at DESC
    LIMIT 1
)

SELECT *
FROM latest