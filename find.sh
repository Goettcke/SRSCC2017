#!/bin/bash

HOUSES_FOLDER="houses"
PICK_FOLDER=${3:-"pick"}

FOLDER=$1
PATTERN=$2

# Functions to do fuzzy pattern search. They insert a * between each letter in pattern.
function joinstr { 
    local IFS="$1"
    shift
    echo "$*"
}

function fuzzy_pattern { 
    echo \*$(joinstr \* $(echo "$*" | fold -w1))\*
}


# Create two temporary files.
# One will hold a list of people
# The other will hold the same but with line numbers and header (for printing)
tmpfile=$(mktemp)
tmpfile2=$(mktemp)


# Find a list of files that match (with fuzzy search) the pattern
for person_file_with_ext in $(find "$FOLDER" -iname "$(fuzzy_pattern "$PATTERN")" -printf "%f\n"); do
    if [[ "$person_file_with_ext" == _* ]]; then
        continue
    fi
    person_file=$(echo $person_file_with_ext | rev | cut -d'.' -f2- | rev )
    name=$(echo $person_file | rev | cut -d'_' -f4- | rev)
    person_year_house_id=$(echo $person_file | rev | cut -d'_' -f1-3 | rev)
    year=$(echo $person_year_house_id | cut -d'_' -f1)
    house=$(echo $person_year_house_id | cut -d'_' -f2)
    id=$(echo $person_year_house_id | cut -d'_' -f3)

    echo "$name|$year|$house|$id"
done | sort -k2 -t'|' >> $tmpfile # Sort it and store it

# Find number of people
LEN=$(cat $tmpfile | wc -l)

# Make a file with header and line number
echo "#|NAME|BIRTH YEAR|HOUSEHOLD|ID" > $tmpfile2
cat $tmpfile | awk '{printf "%d|%s\n", NR, $0}' >> $tmpfile2


if [ "$LEN" == 0 ]; then
    echo "No matches"
    exit
elif [ "$LEN" == 1 ]; then
    echo "Found person:"
    echo

    cat $tmpfile2 | column -s'|' -t #-R1,3,4,5
    
    echo

    pick=1
else
    echo "Pick a number corresponding to the person you want:"
    echo

    cat $tmpfile2 | column -s'|' -t #-R1,3,4,5

    echo
    echo -n "Pick: "
    read -r pick
    echo
fi


# Get the index of the person based on pick
if [[ -z "$pick" ]]; then
    index=0
else
    index=$((pick-1))
fi

if [ "$index" == -1 ]; then
    echo "Invalid pick."
    exit
fi


# Store all people from file in array
PEOPLE=()
for person in $(cat $tmpfile); do
    PEOPLE+=("$person")
done

# Extract chosen person and data about the person
person=${PEOPLE[$index]}
name=$(echo $person | cut -d'|' -f1)
year=$(echo $person | cut -d'|' -f2)
house=$(echo $person | cut -d'|' -f3)
id=$(echo $person | cut -d'|' -f4)

file="${name}_${year}_${house}_${id}.csv"

# Clean up and make ready
rm -rf $PICK_FOLDER
mkdir -p $PICK_FOLDER
mkdir -p $PICK_FOLDER/houses


echo -n "Copying files into '$PICK_FOLDER'... "

# Copy person file
cp $FOLDER/$file $PICK_FOLDER

# Copy 1845 household for person
cp "$HOUSES_FOLDER/house_1845_${house}.csv" $PICK_FOLDER/houses

# Copy all households of matches from 1850
for house_num in `tail --lines=+6 $FOLDER/$file | cut -d'|' -f10`; do
    cp "$HOUSES_FOLDER/house_1850_$house_num.csv" $PICK_FOLDER/houses
done

echo "Done."
