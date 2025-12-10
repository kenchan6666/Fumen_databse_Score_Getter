# debug_proxy.py - 超级调试版（什么请求都显示）
from mitmproxy import http
from mitmproxy import ctx

def request(flow: http.HTTPFlow):
    if "donderhiroba.jp" in flow.request.pretty_url:
        ctx.log.info(f"[CYN 调试] 请求: {flow.request.method} {flow.request.pretty_url}")

def response(flow: http.HTTPFlow):
    if "donderhiroba.jp" in flow.request.pretty_url:
        ctx.log.info(f"[CYN 调试] 响应: {flow.response.status_code} {len(flow.response.content)} bytes")
        if "score" in flow.request.pretty_url:
            ctx.log.info(f"[CYN 成绩页] {flow.request.pretty_url}")
            ctx.log.info(f"[CYN 内容预览] {flow.response.get_text()[:500]}")