"""Storage utilities for file handling"""

def save_video(video_file, filename: str) -> str:
    """Save uploaded video file and return URL"""
    # Mock implementation for testing
    return f"/videos/{filename}"

def get_video_url(video_path: str) -> str:
    """Get video URL from path"""
    # Mock implementation for testing
    return f"https://example.com{video_path}"