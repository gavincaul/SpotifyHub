from flask import jsonify
from spotipy import SpotifyException


class APIError(Exception):
    """Base class for API errors."""
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        if status_code:
            self.status_code = status_code
        self.message = message
        self.payload = payload or {}

    def to_dict(self):
        rv = dict(self.payload)
        rv['error'] = self.message
        return rv


# Standard HTTP-like errors
class NotFoundError(APIError):
    def __init__(self, message="Resource not found", payload=None):
        super().__init__(message, status_code=404, payload=payload)


class UnauthorizedError(APIError):
    def __init__(self, message="Unauthorized", payload=None):
        super().__init__(message, status_code=401, payload=payload)


class ForbiddenError(APIError):
    def __init__(self, message="Forbidden", payload=None):
        super().__init__(message, status_code=403, payload=payload)


class BadRequestError(APIError):
    def __init__(self, message="Bad request", payload=None):
        super().__init__(message, status_code=400, payload=payload)


class ConflictError(APIError):
    def __init__(self, message="Conflict", payload=None):
        super().__init__(message, status_code=409, payload=payload)


class ServerError(APIError):
    def __init__(self, message="Internal server error", payload=None):
        super().__init__(message, status_code=500, payload=payload)


# Spotify-specific
class SpotifyAPIError(APIError):
    def __init__(self, message="Spotify API error", payload=None):
        super().__init__(message, status_code=502, payload=payload)


class SpotifyRateLimitError(APIError):
    """Raised when Spotify API returns 429 Too Many Requests"""

    def __init__(self, retry_after=None, payload=None):
        message = f"Spotify rate limit exceeded. Retry after {retry_after} seconds." if retry_after else "Spotify rate limit exceeded."
        super().__init__(message, status_code=429, payload=payload)


# Optional: Domain-specific errors
class PlaylistOperationError(APIError):
    """Raised for invalid playlist operations"""

    def __init__(self, message="Playlist operation failed", payload=None):
        super().__init__(message, status_code=400, payload=payload)


class CurrentUserOperationError(APIError):
    """Raised for invalid currentUser operations"""

    def __init__(self, message="currentUser operation failed", payload=None):
        super().__init__(message, status_code=400, payload=payload)


class TrackOperationError(APIError):
    """Raised for invalid track operations"""

    def __init__(self, message="Track operation failed", payload=None):
        super().__init__(message, status_code=400, payload=payload)


class AlbumOperationError(APIError):
    """Raised for invalid album operations"""

    def __init__(self, message="Album operation failed", payload=None):
        super().__init__(message, status_code=400, payload=payload)


class ArtistOperationError(APIError):
    """Raised for invalid artist operations"""

    def __init__(self, message="Artist operation failed", payload=None):
        super().__init__(message, status_code=400, payload=payload)


class UserOperationError(APIError):
    """Raised for invalid user operations"""

    def __init__(self, message="User operation failed", payload=None):
        super().__init__(message, status_code=400, payload=payload)


def map_spotify_error(spotify_error, resource_type="resource", resource_id=None):
    """
    Convert spotipy.SpotifyAPIError to appropriate domain error

    Args:
        spotify_error: The SpotifyAPIError from spotipy
        resource_type: Type of resource ('album', 'track', 'artist', 'playlist')
        resource_id: The ID of the resource that caused the error
    """
    resource_desc = f"{resource_type} '{resource_id}'" if resource_id else resource_type
    error_msg = str(spotify_error).lower()

    # Extract status code from the error message or attributes
    status_code = _extract_spotify_status_code(spotify_error, error_msg)
    if status_code == 400 or "bad request" in error_msg:
        print("400 error detected")
        return BadRequestError(f"Invalid {resource_type} ID: {resource_id}")
    elif status_code == 401 or "unauthorized" in error_msg:
        return UnauthorizedError("Spotify authentication expired - please reauthenticate")
    elif status_code == 403 or "forbidden" in error_msg:
        return ForbiddenError(f"Access to {resource_desc} is forbidden")
    elif status_code == 404 or "not found" in error_msg:
        return NotFoundError(f"{resource_type.capitalize()} '{resource_id}' not found on Spotify")
    elif status_code == 429 or "rate limit" in error_msg or "too many requests" in error_msg:
        retry_after = _extract_retry_after(spotify_error, error_msg)
        return SpotifyRateLimitError(retry_after=retry_after)
    else:
        # Default to domain-specific operation error
        if resource_type == "album":
            return AlbumOperationError(f"Spotify error for {resource_desc}: {str(spotify_error)}")
        elif resource_type == "track":
            return TrackOperationError(f"Spotify error for {resource_desc}: {str(spotify_error)}")
        elif resource_type == "artist":
            return ArtistOperationError(f"Spotify error for {resource_desc}: {str(spotify_error)}")
        elif resource_type == "playlist":
            return PlaylistOperationError(f"Spotify error for {resource_desc}: {str(spotify_error)}")
        else:
            return ServerError(f"Spotify API error: {str(spotify_error)}")


def _extract_spotify_status_code(spotify_error, error_msg):
    """Extract HTTP status code from SpotifyAPIError"""
    # Try to get status code from error attributes first
    if hasattr(spotify_error, 'http_status'):
        return spotify_error.http_status
    elif hasattr(spotify_error, 'status_code'):
        return spotify_error.status_code

    # Fallback: parse from error message
    import re
    match = re.search(r'(\d{3})', error_msg)
    return int(match.group(1)) if match else None


def _extract_retry_after(spotify_error, error_msg):
    """Extract retry-after seconds from SpotifyAPIError"""
    # Try to get from error attributes
    if hasattr(spotify_error, 'headers') and spotify_error.headers:
        retry_after = spotify_error.headers.get('Retry-After')
        if retry_after:
            return int(retry_after)

    # Fallback: parse from error message
    import re
    match = re.search(r'retry[_\s-]*after[_\s-]*(\d+)',
                      error_msg, re.IGNORECASE)
    return int(match.group(1)) if match else None
