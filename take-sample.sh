#!/bin/bash

indent2() { 
  sed 's/^/  /'; 
}

indent4() { 
  sed 's/^/    /'; 
}


get_seeded_random() {
  seed="$1"
  openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt \
    </dev/zero 2>/dev/null
}


SEED=42
NUM=500

temp_file=$(mktemp)
sample_file=$(mktemp)


echo "Take sample of files to extract..."
ls $1 | shuf -n $NUM --random-source=<(get_seeded_random $SEED) | grep -v "house" > $temp_file

echo

echo "Checking if all files in sample is present in all data folders..."
for file in `cat $temp_file`; do
    exists_everywhere=true
    for output_folder in "$@"; do
        if [ ! -f "$output_folder/$file" ]; then
            exists_everywhere=false
            break
        fi
    done
    if [ "$exists_everywhere" = true ]; then
        echo $file >> $sample_file
    fi
done

echo

echo "Start of sample list:"
head -n 5 $sample_file
echo "..."
echo 

echo "Number of samples: $(cat $sample_file | wc -l)"

echo 

for output_folder in "$@"; do
    mkdir -p "$output_folder-sample"
    echo "Sampling ${output_folder}..."
    echo "Copying person files..." | indent2
    for file in `cat $sample_file`; do
        cp "$output_folder/$file" "$output_folder-sample/$file" |& indent4
    done
    echo "Copying house files with it..." | indent2
    for house_file in `cat $sample_file | sed -r 's/\.txt/_house\.txt/g'`; do
        cp "$output_folder/$house_file" "$output_folder-sample/$house_file" |& indent4
    done
    echo "Copied $(ls "$output_folder-sample" | wc -l) files." | indent2
    echo "Zipping..." | indent2
    zip "$output_folder-sample.zip" -r "$output_folder-sample" |& indent4
done
