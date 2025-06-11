# ComfyCam

ComfyCam is a tool that captures AI-processed video frames from [ComfyStream](https://github.com/livepeer/comfystream) and outputs them to a virtual camera device, allowing you to use the processed video stream in any application that supports video input (like OBS, Zoom, etc.).

## Prerequisites

### System Requirements
- Ubuntu 24.04 (tested and verified)
- NVIDIA GPU with CUDA support
- Docker

### Virtual Camera Setup and Usage

> [!IMPORTANT]
> The virtual camera setup requires kernel module installation and loading. This is a system-level operation that should be done with caution. The configuration has been tested on Ubuntu 24.04 with Docker and may require adjustments for other distributions.

1. Install the required kernel modules:
```bash
sudo apt update
sudo apt install dkms v4l2loopback-dkms
```

2. Reboot your system to ensure the kernel modules are properly loaded:
```bash
sudo reboot
```

3. After reboot, load the v4l2loopback module with the following parameters:
```bash
sudo modprobe v4l2loopback video_nr=2 card_label="ComfyCam" exclusive_caps=1 max_buffers=8
```

4. Clone the ComfyCam repository:
```bash
git clone https://github.com/GizmoQuest/comfycam.git
```

5. Navigate to the project directory:
```bash
cd comfycam
```

6. Build the Docker images. This will create two images:
   - `comfycam-base:latest`: The base image with all dependencies
   - `comfycam:latest`: The final image with ComfyCam and ComfyStream
```bash
docker build -f docker/Dockerfile.base -t comfycam-base:latest . && docker build -f docker/Dockerfile -t comfycam:latest --build-arg BASE_IMAGE=comfycam-base:latest .
```

7. Run the container:
```bash
docker run -it --gpus all \
  -p 8188:8188 \
  -p 8889:8889 \
  -p 5678:5678 \
  --device=/dev/video2 \
  --name comfycam \
  -v ~/models/ComfyUI--models:/workspace/ComfyUI/models \
  -v ~/models/ComfyUI--output:/workspace/ComfyUI/output \
  comfycam:latest \
  --download-models --build-engines --server
```

8. Start the Comfystream server and UI (Use Runpod settings)

9. Launch your Comfy Workflow (JSON API file)

10. Deploy ComfyCam in a new terminal
```bash
docker exec -ti comfycam \
    conda run -n comfystream \
    --no-capture-output \
    python /workspace/comfystream/comfycam_bridge.py
```
    
11. Use ComfyCam with your application (OBS, Zoom, etc)

## Troubleshooting

### Common Issues

1. **Virtual camera not showing up**
   - Verify the v4l2loopback module is loaded: `lsmod | grep v4l2loopback`
   - Check available video devices: `v4l2-ctl --list-devices`
   - Ensure you have the correct permissions to access `/dev/video2`

2. **Permission denied errors**
   - Add your user to the video group: `sudo usermod -a -G video $USER`
   - Log out and back in for the group changes to take effect

### System Information

This project has been tested with the following setup:
- OS: Ubuntu 24.04 LTS
- GPU: NVIDIA RTX 4060 Ti
- Driver: 550.127.05
- CUDA: 12.5
- PyTorch: 2.5.1+cu121

## Security Note

The virtual camera setup requires system-level modifications. Always verify the source of any kernel modules or system modifications before applying them. The provided configuration has been tested on Ubuntu 24.04 and should be used with caution on other systems.
