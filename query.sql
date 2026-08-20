WITH ride_events_pickup_and_dropoff AS (
    SELECT
        r.id_ride,
        r.id_driver_id,
        MIN(CASE
            WHEN re.description = 'Status changed to pickup'
            THEN re.created_at
        END) AS pickup_time,
        MIN(CASE
            WHEN re.description = 'Status changed to dropoff'
            THEN re.created_at
        END) AS dropoff_time
    FROM ride r
    JOIN ride_event re
        ON r.id_ride = re.id_ride_id
    GROUP BY r.id_ride, r.id_driver_id
)

SELECT
    strftime('%Y-%m', events.pickup_time) AS month,
    u.first_name || ' ' || substr(u.last_name, 1, 1) AS driver,
    COUNT(*) AS trip_count
FROM ride_events_pickup_and_dropoff events
JOIN user u
    ON events.id_driver_id = u.id_user
WHERE events.pickup_time IS NOT NULL
    AND events.dropoff_time IS NOT NULL
    AND (
        strftime('%s', events.dropoff_time) -
        strftime('%s', events.pickup_time)
    ) > 3600
GROUP BY
    strftime('%Y-%m', events.pickup_time),
    u.id_user
ORDER BY month, driver;
