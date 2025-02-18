# Manim Testing GUI

A graphical user interface for testing and previewing Manim animations. This project provides an interactive environment for creating, previewing, and modifying Manim scenes with real-time feedback.

## Features

- Live preview window for Manim scenes
- Object management interface
- State control for animations
- Code preview window
- Detailed property editor
- Real-time scene manipulation

## Prerequisites

- Python 3.10
- OpenGL support
- Qt libraries

## Installation

1. After you clone the repository:
```bash
cd manimTesting
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
src/
├── controllers/     # Scene and state control logic
├── file/           # File handling utilities
├── intermediate/   # Intermediate processing
├── scene/          # Manim scene definitions
├── states/         # State management
├── view/           # GUI components
└── main.py         # Application entry point
```

## Usage

Run the application using:

```bash
python src/main.py
```

The GUI consists of several components:
- Preview Window: Displays the Manim scene in real-time
- Objects Bar: Manage scene objects
- State Bar: Control animation states
- Details Bar: Edit object properties
- Code Preview: View and edit scene code

## Dependencies

- manim (0.18.1)
- PySide6 (6.3.0)
- PyQt5
- moderngl
- moderngl_window
- numpy
- bidict
- ipython (8.0.1)
