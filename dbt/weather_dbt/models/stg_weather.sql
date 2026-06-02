WITH raw_weather AS (
    SELECT *
    FROM {{ source('weather_data', 'weather_readings') }}
),

weather_codes AS (
    SELECT *
    FROM {{ ref('weather_codes') }}
)

SELECT
    r.ingested_at,
    r.observation_time,
    r.latitude,
    r.longitude,
    r.temperature AS temperature_celsius,
    r.windspeed AS windspeed_kmh,
    r.winddirection AS wind_direction_degrees,
    CASE 
        WHEN r.is_day = 1 THEN 'Day'
        WHEN r.is_day = 0 THEN 'Night'
    END AS is_day,
    c.description AS weather_description,
    c.category AS weather_category
FROM raw_weather r
LEFT JOIN weather_codes c
    ON r.weathercode = c.weathercode