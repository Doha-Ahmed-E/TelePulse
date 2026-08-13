from services.hive import get_hive_connection


def get_province_activity():
    conn = get_hive_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            provincename,
            total_sms_in,
            total_sms_out,
            total_call_in,
            total_call_out,
            total_internet
        FROM province_activity
    """)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [dict(zip(columns, row)) for row in rows]


def get_cell_activity():
    conn = get_hive_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.cellid,
            c.total_sms,
            c.total_calls,
            c.total_internet,
            u.urban_vitality_index,
            l.land_use_category,
            d.shannon_entropy_diversity_index
        FROM cell_activity c
        LEFT JOIN urban_vitality u
            ON c.cellid = u.cellid
        LEFT JOIN land_use_classification l
            ON c.cellid = l.cellid
        LEFT JOIN spatial_diversity d
            ON c.cellid = d.cellid
        LIMIT 5000
    """)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [dict(zip(columns, row)) for row in rows]


def get_hourly_activity(province=None):
    conn = get_hive_connection()
    cursor = conn.cursor()

    if province:
        cursor.execute("""
            SELECT
                provincename,
                hour,
                total_sms,
                total_calls,
                total_internet
            FROM province_hourly_activity
            WHERE provincename = %s
            ORDER BY hour
        """, (province,))
    else:
        cursor.execute("""
            SELECT
                hour,
                total_sms,
                total_calls,
                total_internet
            FROM hourly_activity
            ORDER BY hour
        """)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [dict(zip(columns, row)) for row in rows]