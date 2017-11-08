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
    if [[ "$file" == _* ]]; then
        continue
    fi
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
    mkdir -p "$output_folder-sample/people"
    mkdir -p "$output_folder-sample/houses"

    echo "Sampling ${output_folder}..."

    cp "$output_folder/_default_parameters.ini" "$output_folder-sample/_default_parameters.ini" |& indent2
    cp "$output_folder/_specific_parameters.ini" "$output_folder-sample/_specific_parameters.ini" |& indent2

    echo "Copying person files..." | indent2
    for file in `cat $sample_file`; do
        cp "$output_folder/$file" "$output_folder-sample/people/$file" |& indent4

        #echo "Copying house files with it..." | indent4

        for house_num in `sed '3q;d' $output_folder/$file | cut -d'|' -f10`; do
            cp "houses/house_1845_$house_num.csv" "$output_folder-sample/houses/" |& indent4
        done

        for house_num in `tail --lines=+6 $output_folder/$file | cut -d'|' -f10`; do
            cp "houses/house_1850_$house_num.csv" "$output_folder-sample/houses/" |& indent4
        done
    done

    echo -n "Copied $(ls "$output_folder-sample/people" | wc -l) people" | indent2
    echo "and $(ls "$output_folder-sample/houses" | wc -l) houses."

    echo "Zipping..." | indent2
    zip "$output_folder-sample.zip" -r "$output_folder-sample" |& indent4
done
