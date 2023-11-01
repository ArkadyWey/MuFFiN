declare init=4-reg

for N in 1 4 9 16 25 36 49 64 81 100; do
    for data_type in stats fulls; do 
        mkdir -p  ~/Projects/data_to_transfer/init-${init}/N-${N} &&  cp -r /scratch/wey/2023_homogenisation/figures/poly/esbl_prep/init-${init}/N-${N}/${data_type}_init-${init}_N-${N}/ ~/Projects/data_to_transfer/init-${init}/N-${N}/${data_type}_init-${init}_N-${N}/
    done
done