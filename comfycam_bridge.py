#!/usr/bin/env python3

import ffmpeg
import sys
import requests
from urllib.parse import urlparse, parse_qs

def get_stream_token(base_url: str) -> str:
    """Get a stream token from the server."""
    try:
        response = requests.post(f"{base_url}/api/stream-token")
        response.raise_for_status()
        data = response.json()
        return data['stream_id']
    except Exception as e:
        raise Exception(f"Failed to get stream token: {str(e)}")

def main():
    # Base URL for the ComfyUI server
    base_url = "http://localhost:8889"
    
    try:
        # Get a fresh stream token from the server
        token = get_stream_token(base_url)
        print(f"Using token: {token}")

        # Construct the MJPEG stream URL
        stream_url = f"{base_url}/api/stream?token={token}"

        # Output virtual camera device
        output_device = "/dev/video2"

        # Build and run the ffmpeg pipeline
        (
            ffmpeg
            .input(stream_url, format='mjpeg', re=None)  # '-f mjpeg -re -i URL'
            .output(output_device, format='v4l2', pix_fmt='yuv420p', vcodec='rawvideo')
            .run(overwrite_output=True)
        )
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
