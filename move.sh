declare -i num_nodes=4   #81    #100
#declare -i r_max=5      #694   #3106
declare -i diff=11       #9306  #6894
declare -i r_max_new=15  #10000 #10000

for ((r=${diff};r<=${r_max_new};r+=1)); do
	echo "Running for r-${r}"
	
	cp -r /scratch/wey/2023_homogenisation/figures/poly/esbl_prep/init-4-reg/N-${num_nodes}/r-${r} /scratch/wey/2023_homogenisation/figures/poly/esbl_prep/init-4-reg_permanent/N-${num_nodes}/r-${r}
	#cp -r ~/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-4-reg/N-${num_nodes}/r-${r} ~/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-4-reg_permanent/N-${num_nodes}/r-${r}
done

echo "done"