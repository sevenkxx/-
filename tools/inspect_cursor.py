#!/usr/bin/env python3
"""查看 MaCursor .cursor 主题文件的结构。

用法:
    python3 tools/inspect_cursor.py "themes/xxx.cursor"
    python3 tools/inspect_cursor.py "themes/xxx.cursor" --json

.cursor 本质是一个 plist XML，图片以 base64 PNG 内嵌在 Representations 里。
"""

import argparse
import json
import plistlib
import sys


def load(path):
    with open(path, "rb") as f:
        return plistlib.load(f)


def summarize(data):
    cursors = data.get("Cursors", {})
    meta = {k: v for k, v in data.items() if k != "Cursors"}
    rows = []
    for name, spec in sorted(cursors.items(), key=lambda kv: _sort_key(kv[0])):
        reps = spec.get("Representations", [])
        rows.append(
            {
                "id": name,
                "frames": spec.get("FrameCount", 1),
                "duration": round(float(spec.get("FrameDuration", 1.0)), 3),
                "hotspot": (spec.get("HotSpotX"), spec.get("HotSpotY")),
                "size": (spec.get("PointsWide"), spec.get("PointsHigh")),
                "layers": len(reps),
                "bytes": sum(len(r) for r in reps),
            }
        )
    total_frames = sum(r["frames"] for r in rows)
    return meta, rows, total_frames


def _sort_key(name):
    tail = name.rsplit(".", 1)[-1]
    return (0, int(tail), "") if tail.isdigit() else (1, 0, name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    data = load(args.path)
    meta, rows, total_frames = summarize(data)

    if args.json:
        print(json.dumps({"meta": meta, "cursors": rows, "total_frames": total_frames},
                         ensure_ascii=False, indent=2, default=str))
        return

    print(f"主题: {meta.get('ThemeName')}  v{meta.get('ThemeVersion')}")
    print(f"标识: {meta.get('Identifier')}")
    print(f"HiDPI: {meta.get('HiDPI')}   状态数: {len(rows)}   总帧数: {total_frames}")
    print("-" * 78)
    print(f"{'状态 ID':<34}{'帧':>4}{'间隔':>8}{'热点':>14}{'图层':>6}{'体积':>10}")
    print("-" * 78)
    for r in rows:
        hx, hy = r["hotspot"]
        print(
            f"{r['id']:<34}{r['frames']:>4}{r['duration']:>8.3f}"
            f"{f'({hx}, {hy})':>14}{r['layers']:>6}{r['bytes'] / 1024:>9.1f}K"
        )


if __name__ == "__main__":
    sys.exit(main())
