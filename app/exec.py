"""Network diagnostics endpoint."""
import ipaddress
import re
import socket
import subprocess

from flask import Blueprint, request

bp = Blueprint("diag", __name__)

# RFC 1123 hostname: dot-separated labels of letters/digits/hyphen, no leading or
# trailing hyphen, 1..253 chars. Contains no shell metacharacters by construction.
_HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
)


def _is_valid_host(host: str) -> bool:
    """Accept only a valid IP address or RFC 1123 hostname (allowlist)."""
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return bool(_HOSTNAME_RE.match(host))


def _is_public_ip(ip: str) -> bool:
    """True only for globally-routable addresses — blocks loopback, private,
    link-local (incl. cloud metadata 169.254.169.254), reserved and multicast."""
    addr = ipaddress.ip_address(ip)
    return not (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
        or addr.is_multicast
        or addr.is_unspecified
    )


def _resolve_public_target(host: str) -> str | None:
    """Resolve `host` and return a single public IP to probe, or None if it maps
    to any non-public address. Pinning to the resolved IP (instead of re-passing
    the hostname) prevents SSRF via internal targets and DNS rebinding (CWE-918)."""
    try:
        resolved = {info[4][0] for info in socket.getaddrinfo(host, None)}
    except socket.gaierror:
        return None
    if not resolved or any(not _is_public_ip(ip) for ip in resolved):
        return None
    return next(iter(resolved))


@bp.get("/ping")
def ping():
    host = request.args.get("host", "")
    if not _is_valid_host(host):
        return {"error": "invalid host"}, 400
    target = _resolve_public_target(host)
    if target is None:
        return {"error": "host not allowed"}, 403
    # No shell + IP pinned to a vetted public address: neither shell injection
    # (CWE-78) nor SSRF to internal resources (CWE-918) is possible.
    result = subprocess.run(
        ["ping", "-c", "1", target],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.stdout
