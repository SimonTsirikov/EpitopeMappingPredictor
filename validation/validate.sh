unzip anbase-master_cleaned_up.zip

mkdir ag_source

for file in anbase-master/data/*/prepared_schrod/*ag_u.pdb 
do
    cp $file ag_source/
done

mkdir ab_source

for file in anbase-master/data/*/prepared_schrod/*ab_u.pdb 
do
    cp $file ab_source/
done

for item in ag_source/*
do
    curl http://biosig.unimelb.edu.au/epitope3d/api/submission -X POST -i -F pdb_file="@$item" >> query.txt 
done

grep '{"job_id": .*' query.txt | cut -d'"' -f4 > ids.txt
ls ag_source | cut -d'_' -f1 > names.txt
paste ids.txt names.txt > zipped.txt

cat zipped.txt | while IFS=$'\t' read -r col1 col2
do
    wget http://biosig.unimelb.edu.au/epitope3d/static/results_file/$col1/output_prediction.csv -O result/$col2.csv
done

cat anbase-master/anbase_summary.csv | cut -d',' -f12 > new_names.txt
cat anbase-master/anbase_summary.csv | cut -d'_' -f1 > old_names.txt
paste old_names new_names > change.txt

cat comparison.txt | while IFS=$'\t' read -r col1
do
    cat change.txt | grep $col1 | cut -d' ' -f2 | awk '{print}' ORS=' ' >> ags.txt
    echo "\n" >> ags.txt
done

cat change.txt | while IFS=$'\t' read -r col1 col2
do
    mv result/$col1.csv result/$col2.csv
done

cat change.txt | while IFS=$'\t' read -r col1 col2
do
    python3 markup_epitope.py $col1 >> epitope/$col2.csv
    echo ',' >> epitope/$col2.csv
done

for file in epitope/*
do
    if [ -s $file ]
    then
        echo $file | cut -d'/' -f2 | cut -d'.' -f1 >> names_nonempty.txt
    fi
done

python3 compare_datasets.py > comparison.txt

cat comparison.txt | while read -r col1
do
    python3 count_predicted.py $col1 >> statistics.txt
done

python3 build_statistics.py
