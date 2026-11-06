#!/usr/bin/env python3
"""Computes today's daily password (same algorithm as the unlocker).

Secret must match GfxDailyPassword.Secret in the C# source.
Run by the GitHub Action; also usable locally: python daily.py
"""
import datetime
import hashlib
import hmac
import os

SECRET = os.environ["GFX_SECRET"].encode()
ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"


def for_date(d: datetime.date) -> str:
    digest = hmac.new(SECRET, d.strftime("%Y%m%d").encode(), hashlib.sha256).digest()
    chars = "".join(ALPHABET[b % len(ALPHABET)] for b in digest[:8])
    return f"{chars[:4]}-{chars[4:]}"


def main() -> None:
    today = datetime.date.today()
    lines = [
        "# 果粉汇助手解锁器 · 今日密码",
        "",
        f"**{today.isoformat()}：`{for_date(today)}`**",
        "",
        "未来 7 天（方便提前查看）：",
        "",
        "| 日期 | 密码 |",
        "| --- | --- |",
    ]
    for i in range(7):
        d = today + datetime.timedelta(days=i)
        lines.append(f"| {d.isoformat()} | {for_date(d)} |")
    with open("password.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
