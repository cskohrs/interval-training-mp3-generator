"""
Interval Training MP3 Generator
Created by Colin

This program creates custom workout MP3s that alternate between intense and moderate music
based on popular interval training methods. Inspired by Resident Evil's dynamic music system!

Required packages (install these first):
    pip install pydub
    pip install gTTS
    
You'll also need ffmpeg installed on your system for pydub to work:
    - Windows: Download from https://ffmpeg.org/ or use: pip install ffmpeg-python
    - Mac: brew install ffmpeg
    - Linux: sudo apt-get install ffmpeg
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pydub import AudioSegment
from gtts import gTTS
import os
import tempfile

# Define the workout methods with their intervals (in seconds)
WORKOUT_METHODS = {
    "Tabata": {"work": 20, "recovery": 10, "default_rounds": 8},
    "Gibala": {"work": 60, "recovery": 75, "default_rounds": 10},
    "Zuniga": {"work": 30, "recovery": 30, "default_rounds": 10},
    "General": {"work": 30, "recovery": 15, "default_rounds": 10},
    "Custom": {"work": 30, "recovery": 30, "default_rounds": 10}  # Default values for custom
}


class IntervalTrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interval Training MP3 Generator")
        self.root.geometry("600x700")
        
        # Variables to store user choices
        self.intense_mp3_path = tk.StringVar()
        self.moderate_mp3_path = tk.StringVar()
        self.selected_method = tk.StringVar(value="Tabata")
        self.num_rounds = tk.IntVar(value=8)
        self.warmup_time = tk.IntVar(value=180)  # 3 minutes in seconds
        self.cooldown_time = tk.IntVar(value=180)  # 3 minutes in seconds
        self.cycle_through = tk.BooleanVar(value=False)
        self.workout_length = tk.StringVar(value="4:00")
        self.custom_work = tk.IntVar(value=30)  # Custom work interval
        self.custom_recovery = tk.IntVar(value=30)  # Custom recovery interval
        
        self.create_widgets()
        self.update_workout_length()  # Calculate initial workout length
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Interval Training MP3 Generator", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame for MP3 file selections
        file_frame = tk.LabelFrame(self.root, text="Select Music Files", padx=10, pady=10)
        file_frame.pack(padx=10, pady=10, fill="x")
        
        # Intense MP3 selection
        tk.Label(file_frame, text="Intense Music MP3:").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(file_frame, textvariable=self.intense_mp3_path, width=40).grid(row=0, column=1, padx=5)
        tk.Button(file_frame, text="Browse", command=self.browse_intense_mp3).grid(row=0, column=2)
        
        # Moderate MP3 selection
        tk.Label(file_frame, text="Moderate Music MP3:").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(file_frame, textvariable=self.moderate_mp3_path, width=40).grid(row=1, column=1, padx=5)
        tk.Button(file_frame, text="Browse", command=self.browse_moderate_mp3).grid(row=1, column=2)
        
        # Frame for workout settings
        settings_frame = tk.LabelFrame(self.root, text="Workout Settings", padx=10, pady=10)
        settings_frame.pack(padx=10, pady=10, fill="x")
        
        # Method selection
        tk.Label(settings_frame, text="Workout Method:").grid(row=0, column=0, sticky="w", pady=5)
        method_dropdown = ttk.Combobox(settings_frame, textvariable=self.selected_method, 
                                       values=list(WORKOUT_METHODS.keys()), state="readonly", width=15)
        method_dropdown.grid(row=0, column=1, sticky="w", padx=5)
        method_dropdown.bind("<<ComboboxSelected>>", lambda e: self.on_method_change())
        
        # Custom interval inputs (only visible when Custom is selected)
        self.custom_frame = tk.Frame(settings_frame)
        self.custom_frame.grid(row=1, column=0, columnspan=3, sticky="w", pady=5)
        
        tk.Label(self.custom_frame, text="  Work interval (seconds):").grid(row=0, column=0, sticky="w", padx=(20,5))
        self.custom_work_spinbox = tk.Spinbox(self.custom_frame, from_=1, to=300, 
                                              textvariable=self.custom_work, width=10,
                                              command=self.update_workout_length)
        self.custom_work_spinbox.grid(row=0, column=1, sticky="w")
        # Update when user types (not just when using arrows)
        self.custom_work.trace_add('write', lambda *args: self.update_workout_length())
        
        tk.Label(self.custom_frame, text="  Recovery interval (seconds):").grid(row=1, column=0, sticky="w", padx=(20,5))
        self.custom_recovery_spinbox = tk.Spinbox(self.custom_frame, from_=1, to=300, 
                                                  textvariable=self.custom_recovery, width=10,
                                                  command=self.update_workout_length)
        self.custom_recovery_spinbox.grid(row=1, column=1, sticky="w")
        # Update when user types (not just when using arrows)
        self.custom_recovery.trace_add('write', lambda *args: self.update_workout_length())
        
        # Hide custom inputs by default
        self.custom_frame.grid_remove()
        
        # Number of rounds
        tk.Label(settings_frame, text="Number of Rounds:").grid(row=2, column=0, sticky="w", pady=5)
        rounds_spinbox = tk.Spinbox(settings_frame, from_=1, to=100, textvariable=self.num_rounds, 
                                    width=10, command=self.update_workout_length)
        rounds_spinbox.grid(row=2, column=1, sticky="w", padx=5)
        # Update when user types (not just when using arrows)
        self.num_rounds.trace_add('write', lambda *args: self.update_workout_length())
        
        # Workout length display (calculated automatically)
        tk.Label(settings_frame, text="Workout Length:").grid(row=3, column=0, sticky="w", pady=5)
        tk.Label(settings_frame, textvariable=self.workout_length, font=("Arial", 10, "bold")).grid(
            row=3, column=1, sticky="w", padx=5)
        
        # Warm-up time
        tk.Label(settings_frame, text="Warm-up Time (seconds):").grid(row=4, column=0, sticky="w", pady=5)
        tk.Spinbox(settings_frame, from_=0, to=600, textvariable=self.warmup_time, 
                  width=10).grid(row=4, column=1, sticky="w", padx=5)
        
        # Cool-down time
        tk.Label(settings_frame, text="Cool-down Time (seconds):").grid(row=5, column=0, sticky="w", pady=5)
        tk.Spinbox(settings_frame, from_=0, to=600, textvariable=self.cooldown_time, 
                  width=10).grid(row=5, column=1, sticky="w", padx=5)
        
        # Cycle through option
        tk.Checkbutton(settings_frame, text="Cycle through music (instead of repeating from start)", 
                      variable=self.cycle_through).grid(row=6, column=0, columnspan=2, sticky="w", pady=10)
        
        # Info box explaining the methods
        info_frame = tk.LabelFrame(self.root, text="Method Information", padx=10, pady=10)
        info_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        info_text = tk.Text(info_frame, height=8, wrap=tk.WORD)
        info_text.pack(fill="both", expand=True)
        info_text.insert("1.0", 
            "Tabata: 20s work / 10s recovery (high intensity, short bursts)\n"
            "Gibala: 60s work / 75s recovery (moderate volume for regular folks)\n"
            "Zuniga: 30s work / 30s recovery (balanced work-rest ratio)\n"
            "General: 30s work / 15s recovery (2:1 work-to-rest ratio)\n"
            "Custom: Set your own work and recovery intervals\n\n"
            "The program will create an MP3 with:\n"
            "• Safety disclaimer at the start\n"
            "• Warm-up section with your moderate music\n"
            "• Alternating intense/moderate intervals\n"
            "• Cool-down section with your moderate music")
        info_text.config(state="disabled")
        
        # Generate button
        generate_btn = tk.Button(self.root, text="Generate Workout MP3", 
                                command=self.generate_mp3, bg="#4CAF50", fg="white", 
                                font=("Arial", 12, "bold"), pady=10)
        generate_btn.pack(padx=10, pady=20, fill="x")
        
    def browse_intense_mp3(self):
        """Opens a file browser to select the intense music MP3"""
        filename = filedialog.askopenfilename(
            title="Select Intense Music MP3",
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        if filename:
            self.intense_mp3_path.set(filename)
    
    def browse_moderate_mp3(self):
        """Opens a file browser to select the moderate music MP3"""
        filename = filedialog.askopenfilename(
            title="Select Moderate Music MP3",
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        if filename:
            self.moderate_mp3_path.set(filename)
    
    def on_method_change(self):
        """When the user changes the method, update the default rounds and workout length"""
        method = self.selected_method.get()
        
        # Show or hide custom interval inputs
        if method == "Custom":
            self.custom_frame.grid()
        else:
            self.custom_frame.grid_remove()
        
        default_rounds = WORKOUT_METHODS[method]["default_rounds"]
        self.num_rounds.set(default_rounds)
        self.update_workout_length()
    
    def update_workout_length(self):
        """Calculate and display the total workout time (excluding warm-up/cool-down)"""
        method = self.selected_method.get()
        
        # Get work and recovery times based on method
        if method == "Custom":
            try:
                work_time = self.custom_work.get()
                recovery_time = self.custom_recovery.get()
            except:
                # If the boxes are empty or invalid, use default values
                work_time = 30
                recovery_time = 30
        else:
            work_time = WORKOUT_METHODS[method]["work"]
            recovery_time = WORKOUT_METHODS[method]["recovery"]
        
        try:
            rounds = self.num_rounds.get()
        except:
            rounds = 1
        
        total_seconds = (work_time + recovery_time) * rounds
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        self.workout_length.set(f"{minutes}:{seconds:02d}")
    
    def format_time_for_speech(self, time_string):
        """Converts time format (4:00) into natural speech (4 minutes)"""
        parts = time_string.split(":")
        minutes = int(parts[0])
        seconds = int(parts[1])
        
        if seconds == 0:
            return f"{minutes} minutes"
        else:
            return f"{minutes} minutes and {seconds} seconds"
    
    def create_tts_audio(self, text, filename):
        """Creates a text-to-speech audio file from the given text, sped up by 25%"""
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        audio = AudioSegment.from_mp3(filename)
        # Speed up by 25% (1.25x speed)
        faster_audio = audio.speedup(playback_speed=1.25)
        return faster_audio
    
    def get_audio_segment(self, audio, start_ms, duration_ms, cycle_mode, cycle_position):
        """
        Gets a segment of audio based on the mode:
        - If cycle_mode is False: always start from the beginning
        - If cycle_mode is True: continue from where we left off, looping if necessary
        """
        audio_duration = len(audio)
        
        if not cycle_mode:
            # Simple mode: always pull from the start
            if duration_ms <= audio_duration:
                return audio[:duration_ms]
            else:
                # If the audio is shorter than needed, loop it
                loops_needed = (duration_ms // audio_duration) + 1
                looped_audio = audio * loops_needed
                return looped_audio[:duration_ms]
        else:
            # Cycle through mode: continue from cycle_position
            if cycle_position + duration_ms <= audio_duration:
                # We can get the segment without looping
                return audio[cycle_position:cycle_position + duration_ms]
            else:
                # We need to loop back to the beginning
                segment = audio[cycle_position:]
                remaining_duration = duration_ms - len(segment)
                
                # Loop the audio until we have enough
                while remaining_duration > 0:
                    if remaining_duration <= audio_duration:
                        segment += audio[:remaining_duration]
                        remaining_duration = 0
                    else:
                        segment += audio
                        remaining_duration -= audio_duration
                
                return segment
    
    def generate_mp3(self):
        """Main function that generates the workout MP3"""
        
        # Validate inputs
        if not self.intense_mp3_path.get() or not self.moderate_mp3_path.get():
            messagebox.showerror("Error", "Please select both intense and moderate music MP3 files.")
            return
        
        if not os.path.exists(self.intense_mp3_path.get()):
            messagebox.showerror("Error", "Intense music file not found.")
            return
            
        if not os.path.exists(self.moderate_mp3_path.get()):
            messagebox.showerror("Error", "Moderate music file not found.")
            return
        
        # Ask where to save the output
        output_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3")],
            title="Save Workout MP3 As"
        )
        
        if not output_path:
            return
        
        try:
            # Show progress message
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Generating...")
            progress_window.geometry("300x100")
            tk.Label(progress_window, text="Generating your workout MP3...\nThis may take a minute.", 
                    font=("Arial", 10)).pack(pady=20)
            progress_window.update()
            
            # Load the music files
            intense_music = AudioSegment.from_mp3(self.intense_mp3_path.get())
            moderate_music = AudioSegment.from_mp3(self.moderate_mp3_path.get())
            
            # Get workout parameters
            method = self.selected_method.get()
            
            # Get work and recovery intervals based on method
            if method == "Custom":
                work_interval = self.custom_work.get() * 1000  # Convert to milliseconds
                recovery_interval = self.custom_recovery.get() * 1000
            else:
                work_interval = WORKOUT_METHODS[method]["work"] * 1000
                recovery_interval = WORKOUT_METHODS[method]["recovery"] * 1000
            
            rounds = self.num_rounds.get()
            warmup_duration = self.warmup_time.get() * 1000
            cooldown_duration = self.cooldown_time.get() * 1000
            cycle_mode = self.cycle_through.get()
            
            # Create temporary directory for TTS files
            temp_dir = tempfile.mkdtemp()
            
            # Create TTS segments
            disclaimer_text = ("Warning: Consult with a medical professional before starting any new exercise regimen. "
                             "Do not over-exert yourself. Listen to your body and stop if you feel pain or discomfort.")
            
            # Create method-specific announcement
            if method == "Custom":
                workout_info_text = (f"You have selected a custom workout. "
                                   f"{rounds} rounds. "
                                   f"Work intervals are {self.custom_work.get()} seconds. "
                                   f"Recovery intervals are {self.custom_recovery.get()} seconds. "
                                   f"Total workout time: {self.format_time_for_speech(self.workout_length.get())}.")
            else:
                workout_info_text = (f"You have selected the {method} regimen. "
                                   f"{rounds} rounds. "
                                   f"Work intervals are {WORKOUT_METHODS[method]['work']} seconds. "
                                   f"Recovery intervals are {WORKOUT_METHODS[method]['recovery']} seconds. "
                                   f"Total workout time: {self.format_time_for_speech(self.workout_length.get())}.")
            
            disclaimer_audio = self.create_tts_audio(disclaimer_text, os.path.join(temp_dir, "disclaimer.mp3"))
            workout_info_audio = self.create_tts_audio(workout_info_text, os.path.join(temp_dir, "info.mp3"))
            warmup_start_audio = self.create_tts_audio("Begin warm-up.", os.path.join(temp_dir, "warmup.mp3"))
            workout_start_audio = self.create_tts_audio("Begin workout.", os.path.join(temp_dir, "workout.mp3"))
            cooldown_start_audio = self.create_tts_audio("Begin cool-down.", os.path.join(temp_dir, "cooldown.mp3"))
            workout_complete_audio = self.create_tts_audio("Workout complete. Great job!", os.path.join(temp_dir, "complete.mp3"))
            
            # Start building the final audio
            final_audio = AudioSegment.silent(duration=500)  # Start with half-second of silence
            
            # Add disclaimer
            final_audio += disclaimer_audio
            final_audio += AudioSegment.silent(duration=1000)
            
            # Add workout info
            final_audio += workout_info_audio
            final_audio += AudioSegment.silent(duration=1000)
            
            # Add warm-up
            final_audio += warmup_start_audio
            final_audio += AudioSegment.silent(duration=500)
            
            # Add warm-up music (use moderate music)
            if warmup_duration > 0:
                warmup_segment = self.get_audio_segment(moderate_music, 0, warmup_duration, False, 0)
                final_audio += warmup_segment
                final_audio += AudioSegment.silent(duration=500)
            
            # Add workout start announcement
            final_audio += workout_start_audio
            final_audio += AudioSegment.silent(duration=500)
            
            # Add the workout intervals
            intense_position = 0  # Track position in intense music if cycling
            moderate_position = 0  # Track position in moderate music if cycling
            
            for round_num in range(rounds):
                # Work interval (intense music)
                intense_segment = self.get_audio_segment(intense_music, 0, work_interval, 
                                                        cycle_mode, intense_position)
                final_audio += intense_segment
                
                if cycle_mode:
                    intense_position = (intense_position + work_interval) % len(intense_music)
                
                # Recovery interval (moderate music)
                moderate_segment = self.get_audio_segment(moderate_music, 0, recovery_interval, 
                                                         cycle_mode, moderate_position)
                final_audio += moderate_segment
                
                if cycle_mode:
                    moderate_position = (moderate_position + recovery_interval) % len(moderate_music)
            
            # Add cool-down
            final_audio += AudioSegment.silent(duration=500)
            final_audio += cooldown_start_audio
            final_audio += AudioSegment.silent(duration=500)
            
            if cooldown_duration > 0:
                cooldown_segment = self.get_audio_segment(moderate_music, 0, cooldown_duration, False, 0)
                final_audio += cooldown_segment
                final_audio += AudioSegment.silent(duration=500)
            
            # Add completion message
            final_audio += workout_complete_audio
            final_audio += AudioSegment.silent(duration=500)
            
            # Export the final MP3
            final_audio.export(output_path, format="mp3")
            
            # Clean up temporary files
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
            
            # Close progress window and show success
            progress_window.destroy()
            messagebox.showinfo("Success", f"Workout MP3 generated successfully!\n\nSaved to:\n{output_path}")
            
        except Exception as e:
            if 'progress_window' in locals():
                progress_window.destroy()
            messagebox.showerror("Error", f"An error occurred while generating the MP3:\n\n{str(e)}")


def main():
    root = tk.Tk()
    app = IntervalTrainingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()