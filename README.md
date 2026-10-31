<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/integratech-org/bloca-edge">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">BLOCA Edge</h3>

  <p align="center">
    IoT Edge Hub for LDPE–Sand Brick Compaction
    <br />
    Real-time Telemetry • ML-Powered Quality Grading • Remote Machine Control
    <br />
    <a href="https://github.com/integratech-org/bloca-edge"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/integratech-org/bloca-edge/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/integratech-org/bloca-edge/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#related-projects">Related Projects</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![BLOCA Edge Banner][product-banner]](https://github.com/integratech-org/bloca-edge)

**BLOCA Edge** is the local intelligence hub of the BLOCA machine. It runs on a Raspberry Pi 5 and bridges the ESP32-based sensor and actuator node with the cloud services. During each compaction cycle it collects process telemetry from the ESP32 via MQTT, captures an image of the finished block using the Pi Camera Module v2, and coordinates with BLOCA ML for compressive strength prediction (Random Forest regression) and surface defect classification (CNN). It also maintains communication with BLOCA API for data persistence and with BLOCA Mobile for monitoring and remote machine control.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![MQTT][MQTT.org]][MQTT-url]
* [![WebSockets][WebSocket]][WebSocket-url]
* [![Raspberry Pi][RaspberryPi]][RaspberryPi-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This service is designed to run on a Raspberry Pi 5 with access to a local Mosquitto MQTT broker and a Pi Camera module.

### Prerequisites

* **Hardware:**
  - Raspberry Pi 5 (recommended) or Raspberry Pi 4
  - Raspberry Pi Camera Module v2 or v3
  - Stable network connection for cloud communication

* **Software:**
  - Python 3.12 or higher
  - [uv](https://docs.astral.sh/uv/) package manager
  - Docker and Docker Compose (for local MQTT broker)
  - Raspbian OS or Ubuntu for Raspberry Pi

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/integratech-org/bloca-edge.git
   cd bloca-edge
   ```

2. Run the setup script (installs uv and dependencies)
   ```sh
   make setup
   ```

3. Create environment configuration
   ```sh
   cp .env.example .env
   # Edit .env with your specific configuration:
   # - MQTT broker settings
   # - BLOCA ML API endpoint
   # - BLOCA API endpoint and credentials
   # - Pi Camera settings
   ```

4. Start the local Mosquitto broker (if not already running on your Pi)
   ```sh
   docker compose up -d
   ```

5. Install pre-commit hooks (for development)
   ```sh
   make pre-commit-install
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Start the BLOCA Edge service:

```sh
uv run python -m bloca_edge
```

The service will:
1. **Initialize connections** to the local MQTT broker (Mosquitto) and BLOCA cloud services
2. **Start WebSocket server** for receiving remote control commands from BLOCA Mobile (e.g. emergency stop, reset)
3. **Monitor batch events** published by the ESP32 over MQTT topics
4. **Collect process telemetry** during an active batch: temperature, pressure, heating duration, cooling time, compressed height, and power draw
5. **Capture a block image** with the Pi Camera once the finished block reaches the inspection point
6. **Request ML predictions** from BLOCA ML: compressive strength (MPa) from the logged process data, and surface quality (Acceptable, Defective, or Reject) from the block image
7. **Stream live readings** to BLOCA API for real-time dashboard updates
8. **Submit complete batch data** with predictions and images to BLOCA API for storage and reporting

### Monitoring

Check service status:
```sh
# View logs
journalctl -u bloca-edge -f

# Check MQTT broker
docker compose logs mosquitto
```

### Development

Run pre-commit checks on all files:
```sh
make pre-commit-all
```

Update pre-commit hooks:
```sh
make pre-commit-update
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- FEATURES -->
## Features

### Core Functionality
- **Process Telemetry**: Real-time collection of compaction data from the ESP32 via MQTT (temperature, pressure, heating duration, cooling time, compressed height, power draw)
- **Image Capture**: Pi Camera Module v2 integration to photograph each finished block for CNN-based surface inspection
- **ML Integration**: Communication with BLOCA ML for:
  - Compressive strength prediction (Random Forest regression)
  - Surface defect classification (CNN)
- **Batch Lifecycle Management**: Tracking from material dosing to heating, compression, cooling, and inspection, with automated data aggregation per batch

### Communication & Control
- **WebSocket Server**: Real-time bidirectional communication for remote machine control via BLOCA Mobile
- **Live Data Streaming**: Push telemetry to BLOCA API during active batches
- **API Integration**: RESTful communication with BLOCA API for data persistence and retrieval

### Reliability & Performance
- **Local Data Buffering**: SQLite-based storage for offline operation and data integrity
- **Async Architecture**: High-performance async/await Python implementation for concurrent operations
- **Edge Computing**: Local processing reduces latency and cloud dependency
- **Fault Tolerance**: Automatic reconnection and data recovery mechanisms

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- RELATED PROJECTS -->
## Related Projects

BLOCA Edge is part of the **BLOCA (Batch-Level Optimization through Compaction Analytics)** ecosystem:

* **[bloca-ml](https://github.com/integratech-org/bloca-ml)** - Machine learning service for compressive strength prediction and CNN-based surface defect classification
* **[bloca-api](https://github.com/integratech-org/bloca-api)** - Cloud REST API backend for data persistence, user management, and business logic
* **[bloca-mobile](https://github.com/integratech-org/bloca-mobile)** - Mobile application for operators: feedstock submission, batch tracking, and remote machine control
* **[IntegraTech Organization](https://github.com/integratech-org)** - View all BLOCA projects and documentation

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

IntegraTech - [Facebook](https://www.facebook.com/profile.php?id=61592806334500) - integratech1@outlook.com

Project Link: [https://github.com/integratech-org/bloca-edge](https://github.com/integratech-org/bloca-edge)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/integratech-org/bloca-edge.svg?style=for-the-badge
[contributors-url]: https://github.com/integratech-org/bloca-edge/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/integratech-org/bloca-edge.svg?style=for-the-badge
[forks-url]: https://github.com/integratech-org/bloca-edge/network/members
[stars-shield]: https://img.shields.io/github/stars/integratech-org/bloca-edge.svg?style=for-the-badge
[stars-url]: https://github.com/integratech-org/bloca-edge/stargazers
[issues-shield]: https://img.shields.io/github/issues/integratech-org/bloca-edge.svg?style=for-the-badge
[issues-url]: https://github.com/integratech-org/bloca-edge/issues
[product-banner]: images/banner.png

<!-- Technology Badges -->
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[MQTT.org]: https://img.shields.io/badge/MQTT-660066?style=for-the-badge&logo=mqtt&logoColor=white
[MQTT-url]: https://mqtt.org/
[WebSocket]: https://img.shields.io/badge/WebSocket-010101?style=for-the-badge&logo=socketdotio&logoColor=white
[WebSocket-url]: https://websockets.readthedocs.io/
[RaspberryPi]: https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=raspberry-pi&logoColor=white
[RaspberryPi-url]: https://www.raspberrypi.com/
