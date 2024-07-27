import subprocess

# Path to the parameters file
parameters_file = "run_extract_clips_parameters.txt"
output_dir = "data\clips"

# Activate the virtual environment
venv_activate = r".venv\Scripts\activate"

# Read the parameters from the file
with open(parameters_file, 'r') as file:
    lines = file.readlines()

# Loop through the lines and run the script
for line in lines:
    # Split the line into video_path and time_params
    parts = line.strip().split()
    video_path = parts[0]
    time_params = parts[1:]

    command = [
        "python", "extract_clips.py", video_path,
        *time_params, "--output_dir", output_dir
    ]
    
    # Run the command within the virtual environment
    subprocess.run(f"{venv_activate} && " + " ".join(command), shell=True)
