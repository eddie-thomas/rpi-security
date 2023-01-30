#!/bin/bash -

#
# Copyright © 2018 - 2023 by Edward K Thomas Jr
# GNU GENERAL PUBLIC LICENSE https://www.gnu.org/licenses/gpl-3.0.en.html
#

# Initializes this project in order to be able to run several of its scripts.

# Exit when any command fails
set -e

script_start=$(date +%s)

# ================================
myFileNames=$(ls *.h264)
for file in $myFileNames
do
    # Make copies of the file with the appropriate extension
    fileNameWithoutExtension="${file%.*}"
    # No backslash needed to continue after the control operator (&&)
    ffmpeg -r 30 -i $file -y "$fileNameWithoutExtension.mp4" && \
      rm -f "./$file" && \
      mkdir -p ./video/ && \
      mv "$fileNameWithoutExtension.mp4" "./video/$fileNameWithoutExtension.mp4" && \
      echo -e "\nSuccessfuly completed file configuration and move..."
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