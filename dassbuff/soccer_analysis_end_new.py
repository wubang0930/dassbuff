import json
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import mysql.connector
from mysql.connector import Error


# 数据库连接参数（与项目内现有用法保持一致）
DB_HOST = "127.0.0.1"
DB_NAME = "csgo"
DB_USER = "root"
DB_PASSWORD = "bangye"


def _fmt_time_from_ms(ms_ts: Optional[int]) -> Optional[str]:
    if ms_ts is None:
        return None
    try:
        return datetime.fromtimestamp(ms_ts / 1000).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def _safe_nsg_score(nsg: List[Dict[str, Any]], idx: int) -> Tuple[Optional[int], Optional[int]]:
    if not isinstance(nsg, list) or len(nsg) <= idx:
        return None, None
    sc = nsg[idx].get("sc") if isinstance(nsg[idx], dict) else None
    if not isinstance(sc, list) or len(sc) < 2:
        return None, None
    try:
        home = int(sc[0]) if sc[0] is not None else None
    except Exception:
        home = None
    try:
        guest = int(sc[1]) if sc[1] is not None else None
    except Exception:
        guest = None
    return home, guest


def _sum_optional(a: Optional[int], b: Optional[int]) -> Optional[int]:
    if a is None or b is None:
        return None
    return a + b


def insert_analysis_end_new(api_data: Dict[str, Any]) -> int:
    """
    按映射解析并写入到 `csgo.soccer_analysis_end_new` 表。

    返回成功插入的条数。
    """
    if not api_data or not isinstance(api_data, dict):
        return 0

    data = api_data.get("data") or {}
    records: List[Dict[str, Any]] = data.get("records") or []
    if not isinstance(records, list) or len(records) == 0:
        return 0

    # 组装插入数据
    rows: List[Tuple[Any, ...]] = []
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in records:
        if not isinstance(item, dict):
            continue

        soccer_id = item.get("id")

        lg = item.get("lg") or {}
        race_name = lg.get("na")
        race_id = lg.get("id")

        ts = item.get("ts") or []
        team_home = ts[0].get("na") if isinstance(ts, list) and len(ts) > 0 and isinstance(ts[0], dict) else None
        team_guest = ts[1].get("na") if isinstance(ts, list) and len(ts) > 1 and isinstance(ts[1], dict) else None

        # team_cr 未在映射中给出来源，置空字符串
        team_cr = ""

        c_time = 90

        nsg = item.get("nsg") or []
        goal_home, goal_guest = _safe_nsg_score(nsg, 0)
        goal_home_first, goal_guest_first = _safe_nsg_score(nsg, 1)
        goal_home_second, goal_guest_second = _safe_nsg_score(nsg, 2)

        m_type_value = _sum_optional(goal_home, goal_guest)

        start_time = _fmt_time_from_ms(item.get("bt"))
        create_time = now_str

        rows.append(
            (
                soccer_id,
                race_name,
                team_home,
                team_guest,
                team_cr,
                c_time,
                m_type_value,
                goal_home_first,
                goal_guest_first,
                goal_home_second,
                goal_guest_second,
                goal_home,
                goal_guest,
                start_time,
                create_time,
                race_id,
            )
        )

    if len(rows) == 0:
        return 0

    insert_sql = (
        "INSERT INTO `csgo`.`soccer_analysis_end_new`("
        "`soccer_id`, `race_name`, `team_home`, `team_guest`, `team_cr`, `c_time`, "
        "`m_type_value`, `goal_home_first`, `goal_guest_first`, `goal_home_second`, `goal_guest_second`, "
        "`goal_home`, `goal_guest`, `start_time`, `create_time`, `race_id`) "
        "VALUES (" + ",".join(["%s"] * 16) + ")"
    )

    affected = 0
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor()
        cursor.executemany(insert_sql, rows)
        conn.commit()
        affected = cursor.rowcount or 0
    except Error as e:
        print(f"数据库错误: {e}")
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if conn and getattr(conn, "is_connected", lambda: False)():
            try:
                conn.close()
            except Exception:
                pass

    return affected


def main(argv: List[str]) -> None:
    """
    用法:
      1) 通过文件运行:  python soccer_analysis_end_new.py path\to\response.json
      2) 通过标准输入:  cat response.json | python soccer_analysis_end_new.py -
    """
    if len(argv) < 2:
        print("缺少参数：请提供JSON文件路径或使用-从标准输入读取")
        return

    src = argv[1]
    if src == "-":
        text = sys.stdin.read()
    else:
        with open(src, "r", encoding="utf-8") as f:
            text = f.read()

    api_data = json.loads(text)
    inserted = insert_analysis_end_new(api_data)
    print(f"插入成功: {inserted} 条")


if __name__ == "__main__":
    main(sys.argv)


