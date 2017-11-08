#!/bin/bash

HOUSES_FOLDER="houses"
PICK_FOLDER=${3:-"pick"}

FOLDER=$1
PATTERN=$2

function joinstr { 
    local IFS="$1"
    shift
    echo "$*"
}

function pattern { 
    echo *$(joinstr \* $(echo "$*" | fold -w1))* 
}

tmpfile=$(mktemp)


COUNTER=1
PEOPLE=()

for person_file_with_ext in $(find "$FOLDER" -iname "$(pattern "$PATTERN")" -printf "%f\n"); do
    person_file=$(echo $person_file_with_ext | rev | cut -d'.' -f2- | rev )
    name=$(echo $person_file | rev | cut -d'_' -f4- | rev)
    person_year_house_id=$(echo $person_file | rev | cut -d'_' -f1-3 | rev)
    year=$(echo $person_year_house_id | cut -d'_' -f1)
    house=$(echo $person_year_house_id | cut -d'_' -f2)
    id=$(echo $person_year_house_id | cut -d'_' -f3)

    line=$(echo "$COUNTER|$name|$year|$house|$id")
    echo $line

    COUNTER=$((COUNTER + 1))
    PEOPLE+=("$line")
done >> $tmpfile


LEN=${#PEOPLE[@]}


if [ "$LEN" == 0 ]; then
    echo "No matches"
    exit
elif [ "$LEN" == 1 ]; then
    pick=0
else
    echo "Pick a number corresponding to the person you want:"
    echo

    cat $tmpfile | column -s'|' -t -N"#,NAME,BIRTH YEAR,HOUSEHOLD,ID" -R1,3,4,5

    echo
    echo -n "Pick: "
    read -r pick
    echo
fi


if [[ -z "$pick" ]]; then
    index=0
else
    index=$((pick-1))
fi

if [ "$index" == -1 ]; then
    echo "Invalid pick."
    exit
fi


person=${PEOPLE[$index]}
name=$(echo $person | cut -d'|' -f2)
year=$(echo $person | cut -d'|' -f3)
house=$(echo $person | cut -d'|' -f4)
id=$(echo $person | cut -d'|' -f5)

file="${name}_${year}_${house}_${id}.csv"

rm -rf $PICK_FOLDER
mkdir -p $PICK_FOLDER
mkdir -p $PICK_FOLDER/houses


# Copy person file
cp $FOLDER/$file $PICK_FOLDER

# Copy 1845 household for person
cp "$HOUSES_FOLDER/house_1845_${house}.csv" $PICK_FOLDER/houses

# COpy all households of matches from 1850

for house_num in `tail --lines=+6 $FOLDER/$file | cut -d'|' -f10`; do
    cp "$HOUSES_FOLDER/house_1850_$house_num.csv" $PICK_FOLDER/houses
done
