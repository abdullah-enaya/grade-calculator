#!/bin/bash

# Set the directory where your files are located
directory="syllabi"

# Navigate to the directory
cd "$directory" || exit

# Loop through each file in the directory
for file in *_syllabus*; do
    # Check if the file name contains "_syllabus"
    if [[ -e "$file" ]]; then
        # Remove "_syllabus" from the file name and rename the file
        new_name=$(echo "$file" | sed 's/_syllabus//')
        mv "$file" "$new_name"
        echo "Renamed: $file to $new_name"
    fi
done
