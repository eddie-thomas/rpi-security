#!/bin/bash -

# Initializes this project in order to be able to run several of its scripts.

# Exit when any command fails
set -e

script_start=$(date +%s)

script_directory=$(dirname "$0")

# ================================
myFileNames=$(ls *.h264)
for file in $myFileNames
do
    # Make copies of the file with the appropriate extension
    fileNameWithoutExtension="${file%.*}"
    # No backslash needed to continue after the control operator (&&)
    ffmpeg -r 30 -i $file -y "$fileNameWithoutExtension.mp4" &&
      rm -f "./$file"
done

# ================================

echo
script_end=$(date +%s)
dur_secs=$((script_end - script_start))
if ((dur_secs > 60)); then
  echo "Finished in $((dur_secs/60)) minutes."
else
  echo "Finished in $dur_secs seconds."
fi