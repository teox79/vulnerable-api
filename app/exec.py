"""Network diagnostics endpoint."""
import ipaddress
import re
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


@bp.get("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    if not _is_valid_host(host):
        return {"error": "invalid host"}, 400
    # No shell: arguments are passed as a list, so even a value that slipped past
    # validation cannot inject shell metacharacters (CWE-78).
    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.stdout
