# Interval Training MP3 Generator

A Python application that creates custom workout MP3s with alternating intense and moderate music, designed to help you stay on pace during interval training workouts.

## 🎮 The Inspiration

This project was inspired by the *Resident Evil* video game series, which terrified me. Just as the music in Resident Evil tells you when danger is near, this program uses music to tell you when to push hard and when to recover - no need to watch a clock while you're focused on your workout!

## 💡 The Problem It Solves

During interval training (short bursts of intense cardio followed by recovery periods), it's hard to keep track of time while you're exercising. You're focused on your body and movement, not watching a timer. This program solves that by creating an MP3 that automatically switches between "intense" and "moderate" music at the exact intervals you need.

## ✨ Features

- **Five Built-in Workout Methods:**
  - **Tabata**: 20s work / 10s recovery (high intensity)
  - **Gibala**: 60s work / 75s recovery (moderate volume)
  - **Zuniga**: 30s work / 30s recovery (balanced)
  - **General**: 30s work / 15s recovery (2:1 ratio)
  - **Custom**: Set your own work and recovery intervals for personalized training

- **Customizable Settings:**
  - Choose your own intense and moderate music files
  - Set number of rounds/cycles
  - Adjust warm-up time (default: 3 minutes)
  - Adjust cool-down time (default: 3 minutes)
  - Real-time workout length calculation as you adjust settings
  
- **Two Music Modes:**
  - **Pull from Start**: Uses the beginning of each song for every interval
  - **Cycle Through**: Plays through your entire song progressively, so you hear all of it

- **Voice Guidance:**
  - Safety disclaimer at the start
  - Workout details announcement (method, rounds, intervals, total time)
  - "Begin warm-up", "Begin workout", "Begin cool-down" cues
  - "Workout complete" celebration message

- **Smart Interface:**
  - Auto-calculates total workout length
  - Music files stay loaded between generations (create multiple variations easily)
  - Simple, intuitive GUI

## 🚀 Installation

### Prerequisites

You'll need Python 3.7 or higher installed on your system.

### Required Packages

Install the required Python packages:

```bash
pip install pydub
pip install gTTS
```

### Install ffmpeg

The `pydub` library requires ffmpeg to process audio files:

- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/)
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

## 📖 How to Use

1. **Run the program:**
   ```bash
   python PythonWorkout.py
   ```

2. **Select your music:**
   - Click "Browse" next to "Intense Music MP3" and choose an energetic, fast-paced song
   - Click "Browse" next to "Moderate Music MP3" and choose a calmer song

3. **Configure your workout:**
   - Choose a workout method from the dropdown (or select "Custom" to set your own intervals)
   - Set the number of rounds
   - Adjust warm-up/cool-down times if desired
   - Check "Cycle through music" if you want to hear your entire songs
   - Watch the workout length auto-calculate as you make changes

4. **Generate:**
   - Click "Generate Workout MP3"
   - Choose where to save your file
   - Wait a moment while it generates
   - Done! Load it onto your phone or music player

## 🎯 Use Cases

- **Gym workouts**: Load the MP3 on your phone and go
- **Home exercise**: No need for timers or apps
- **Outdoor running/cycling**: Stay on pace without checking your watch
- **Athletes with specific training protocols**: Use Custom mode to match your exact interval requirements

## 🔬 The Science

HIIT - (High-Intensity Interval Training) has been shown to be as effective as longer, steady-state cardio for cardiovascular health and fitness. By alternating between high and moderate intensity, you can get an effective workout in less time.

Each method in this program is based on published research:
- **Tabata Protocol**: Developed by Dr. Izumi Tabata
- **Gibala Method**: Created by Dr. Martin Gibala for non-elite athletes
- **Zuniga & General**: Popular time-efficient protocols
- **Custom**: For athletes and trainers who have developed their own optimal interval ratios

## 🛠️ Technical Details

- Built with Python's `tkinter` for the GUI
- Uses `pydub` for audio processing
- Uses `gTTS` (Google Text-to-Speech) for voice announcements
- Voice clips are automatically sped up 25% for punchier delivery

## 📝 License

Feel free to use, modify, and distribute this program. If you make improvements, consider sharing them!

## 🐛 Known Limitations

- Requires internet connection for text-to-speech generation (uses Google's TTS service)
- Only works with MP3 files (not WAV, FLAC, etc.)
- Generated files can be large depending on workout length

## 💬 Feedback

Found a bug? Have an idea for a new feature? Feel free to open an issue or reach out!

---

*"Just like Resident Evil taught us - the right soundtrack makes all the difference."*
