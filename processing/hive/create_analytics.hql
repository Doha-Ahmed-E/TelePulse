USE telepulse;


-- Analytics tables

CREATE TABLE IF NOT EXISTS urban_vitality AS
SELECT
    cellid,
    SUM(smsin) AS total_sms_in,
    SUM(smsout) AS total_sms_out,
    SUM(callin) AS total_call_in,
    SUM(callout) AS total_call_out,
    SUM(internet) AS total_internet,
    (
        SUM(smsin)
        + SUM(smsout)
        + SUM(callin)
        + SUM(callout)
        + SUM(internet)
    ) AS urban_vitality_index
FROM sms_call_internet
GROUP BY cellid;


CREATE TABLE IF NOT EXISTS land_use_classification AS
SELECT
    cellid,
    SUM(
        CASE
            WHEN HOUR(FROM_UNIXTIME(datetime / 1000)) BETWEEN 9 AND 17
            THEN internet + callin
            ELSE 0
        END
    ) AS total_business,
    SUM(
        CASE
            WHEN HOUR(FROM_UNIXTIME(datetime / 1000)) < 9
              OR HOUR(FROM_UNIXTIME(datetime / 1000)) > 17
            THEN internet + callin
            ELSE 0
        END
    ) AS total_residential,
    CASE
        WHEN
            SUM(
                CASE
                    WHEN HOUR(FROM_UNIXTIME(datetime / 1000)) BETWEEN 9 AND 17
                    THEN internet + callin
                    ELSE 0
                END
            )
            >
            SUM(
                CASE
                    WHEN HOUR(FROM_UNIXTIME(datetime / 1000)) < 9
                      OR HOUR(FROM_UNIXTIME(datetime / 1000)) > 17
                    THEN internet + callin
                    ELSE 0
                END
            )
        THEN 'Business/Office'
        ELSE 'Residential'
    END AS land_use_category
FROM sms_call_internet
GROUP BY cellid;


CREATE TABLE IF NOT EXISTS spatial_diversity AS

WITH interaction_totals AS (
    SELECT
        cellid,
        SUM(cell2province) AS total_interactions
    FROM cell_provinces
    GROUP BY cellid
),

probabilities AS (
    SELECT
        p.cellid,
        p.cell2province / t.total_interactions AS probability
    FROM cell_provinces p
    JOIN interaction_totals t
        ON p.cellid = t.cellid
)

SELECT
    cellid,
    SUM(
        -1 * probability * LOG(probability)
    ) AS shannon_entropy_diversity_index
FROM probabilities
GROUP BY cellid;



-- Internal helper views

CREATE OR REPLACE VIEW activity_enriched AS
SELECT
    s.datetime,
    s.cellid,
    p.provincename,
    s.smsin,
    s.smsout,
    s.callin,
    s.callout,
    s.internet
FROM sms_call_internet s
JOIN cell_provinces p
    ON s.datetime = p.datetime
   AND s.cellid = p.cellid;



-- Analytics views

CREATE OR REPLACE VIEW province_activity AS
SELECT
    provincename,
    SUM(smsin) AS total_sms_in,
    SUM(smsout) AS total_sms_out,
    SUM(callin) AS total_call_in,
    SUM(callout) AS total_call_out,
    SUM(internet) AS total_internet
FROM activity_enriched
GROUP BY provincename;


CREATE OR REPLACE VIEW cell_activity AS
SELECT
    cellid,
    SUM(smsin + smsout) AS total_sms,
    SUM(callin + callout) AS total_calls,
    SUM(internet) AS total_internet
FROM activity_enriched
GROUP BY cellid;


CREATE OR REPLACE VIEW hourly_activity AS
SELECT
    HOUR(FROM_UNIXTIME(datetime / 1000)) AS hour,
    SUM(smsin + smsout) AS total_sms,
    SUM(callin + callout) AS total_calls,
    SUM(internet) AS total_internet
FROM activity_enriched
GROUP BY HOUR(FROM_UNIXTIME(datetime / 1000));


CREATE OR REPLACE VIEW province_hourly_activity AS
SELECT
    provincename,
    HOUR(FROM_UNIXTIME(datetime / 1000)) AS hour,
    SUM(smsin + smsout) AS total_sms,
    SUM(callin + callout) AS total_calls,
    SUM(internet) AS total_internet
FROM activity_enriched
GROUP BY
    provincename,
    HOUR(FROM_UNIXTIME(datetime / 1000));