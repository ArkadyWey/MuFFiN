
for N in 1 4 9 16 25 36 49 64 81 100; do
    for data_type in stats fulls; do 
        mkdir -p  ~/Projects/data_to_transfer/init-4-reg/N-${N} &&  cp -r /scratch/wey/2023_homogenisation/figures/poly/esbl_prep/init-4-reg/N-${N}/${data_type}_init-4-reg_N-${N}/ ~/Projects/data_to_transfer/init-4-reg/N-${N}/${data_type}_init-4-reg_N-${N}/
    done
done
