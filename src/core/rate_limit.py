from slowapi import Limiter
from slowapi.util import get_remote_address
from src.config.config import Config

# in-memory storage: limits are per app instance. Move to a shared
# storage (e.g. redis) or the reverse proxy when running replicas.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[Config.get_instance().server_config.rate_limit],
)
