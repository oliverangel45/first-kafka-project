WITH staged AS (
    SELECT *
    FROM {{ ref('stg_weather') }}
)

SELECT
    DATE(observation_time) AS observation_date,
    ROUND(AVG(temperature_celsius), 1) AS avg_temperature_celsius,
    ROUND(MAX(temperature_celsius), 1) AS max_temperature_celsius,
    ROUND(MIN(temperature_celsius), 1) AS min_temperature_celsius,
    ROUND(AVG(windspeed_kmh), 1) AS avg_windspeed_kmh,
    COUNT(*) AS reading_count
FROM staged
GROUP BY DATE(observation_time)
ORDER BY observation_date DESC