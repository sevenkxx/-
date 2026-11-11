#!/usr/bin/env python3
"""把 MaCursor .cursor 主题里的所有帧导出成 PNG，便于替换美术素材。

用法:
    python3 tools/extract_frames.py "themes/xxx.cursor" -o ./frames
    python3 tools/extract_frames.py "themes/xxx.cursor" -o ./frames --state 11

产物目录结构:
    frames/<cursor-id>/<层序>-<分辨率>px-<帧号>.png
"""

import argparse
import os
import plistlib
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("-o", "--out", default="frames")
    ap.add_argument("--state", help="只导出某个状态（如 11 或 com.apple.coregraphics.Wait）")
    args = ap.parse_args()

    with open(args.path, "rb") as f:
        data = plistlib.load(f)

    cursors = data.get("Cursors", {})
    if args.state:
        key = args.state
        if not key.startswith("com.apple."):
            key = f"com.apple.cursor.{key}"
        if key not in cursors:
            sys.exit(f"找不到状态: {key}")
        cursors = {key: cursors[key]}

    count = 0
    for name, spec in cursors.items():
        target = os.path.join(args.out, name)
        os.makedirs(target, exist_ok=True)

        # 代表图是若干「图层」，每个图层内的 PNG 条带包含全部动画帧
        # 帧序号按图层顺序累加；单图层最常见。
        frame_index = 0
        for layer_i, blob in enumerate(spec.get("Representations", [])):
            # 一个图层 bloby 里可能是多帧拼接的 PNG 序列，逐帧探测
            offset = 0
            width = int(spec.get("PointsWide", 32))
            while offset < len(blob):
                if blob[offset:offset + 8] != b"\x89PNG\r\n\x1a\n":
                    break
                end = _png_end(blob, offset)
                if end is None:
                    break
                chunk = blob[offset:end]
                px = _png_width(chunk)
                path = os.path.join(target, f"{layer_i}-{px or width}px-{frame_index:03d}.png")
                with open(path, "wb") as fh:
                    fh.write(chunk)
                count += 1
                frame_index += 1
                offset = end

    print(f"已导出 {count} 个 PNG -> {args.out}")


def _png_end(buf, start):
    """返回从 start 开始的 PNG 数据结束偏移（含 IEND），失败返回 None。"""
    pos = start + 8
    while pos + 8 <= len(buf):
        length = int.from_bytes(buf[pos:pos + 4], "big")
        ctype = buf[pos + 4:pos + 8]
        pos += 12 + length
        if ctype == b"IEND":
            return pos if pos <= len(buf) else None
    return None


def _png_width(chunk):
    if len(chunk) < 24:
        return None
    return int.from_bytes(chunk[16:20], "big")


if __name__ == "__main__":
    sys.exit(main())
