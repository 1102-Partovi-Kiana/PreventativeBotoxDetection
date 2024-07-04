# PreventativeBotoxDetection
Detects moments of confusion/concentration by monitoring forehead. Using advanced facial landmark detection, it provides real-time analysis and notifications. By identifying scrunching habits, it helps prevent wrinkle formation, potentially reducing future Botox and cosmetic needs.

# ForeheadFocus

**ForeheadFocus** is an innovative application designed to detect moments of confusion or concentration by monitoring the scrunching of the forehead. Utilizing advanced facial landmark detection technology, ForeheadFocus provides real-time analysis and notifications, helping users gain insights into their cognitive states during various activities. By identifying and alerting users to their facial scrunching habits, ForeheadFocus can help prevent the formation of wrinkles, potentially reducing the future need for Botox and other cosmetic interventions.

## Features
- Real-time detection of forehead scrunching.
- Notifications for identified scrunching habits.
- Helps users gain insights into moments of confusion or concentration.
- Potentially reduces the need for future cosmetic interventions by preventing wrinkle formation.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/foreheadfocus.git
    cd foreheadfocus
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application:**
    ```bash
    python forehead_focus.py
    ```

2. **Calibration:**
   - Follow the on-screen instructions to keep your face relaxed and press 'y' when ready.
   - The application will capture relaxed face data and display progress on the screen.
   - After capturing relaxed face data, the application will prompt you to prepare for scrunching your forehead.
   - Press 'y' when ready to start capturing scrunched forehead data.

3. **Detection Phase:**
   - After calibration, the application will start detecting scrunching in real-time based on the personalized threshold.
   - The application will display real-time analysis and notify you when forehead scrunching is detected.

## Requirements

- Python 3.6+
- OpenCV
- Mediapipe
- Pygame
- Numpy

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

