#!/bin/bash

get_seeded_random() {
  seed="$1"
  openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt \
    </dev/zero 2>/dev/null
}


SEED=42
NUM=500

temp_file=$(mktemp)


echo "Take sample of files to extract..."
ls $1 | shuf -n $NUM --random-source=<(get_seeded_random $SEED) | grep -v "house" > $temp_file

echo "Prepared to sample $(cat $temp_file | wc -l) files."

echo "Start of sample list:"
head -n 5 $temp_file
echo "..."

for output_folder in "$@"; do
    mkdir -p "$output_folder-sample"
    echo "Sampling $output_folder..."
    for file in `cat $temp_file`; do
        cp "$output_folder/$file" "$output_folder-sample/$file"
    done
    echo "Copying house files with it..."
    for house_file in `cat $temp_file | sed -r 's/\.txt/_house\.txt/g'`; do
        cp "$output_folder/$house_file" "$output_folder-sample/$house_file"
    done
    echo "Copied $(ls "$output_folder-sample" | wc -l) files."
    echo "Zipping..."
    zip "$output_folder-sample.zip" -r "$output_folder-sample"
done
