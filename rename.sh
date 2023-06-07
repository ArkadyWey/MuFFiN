declare -i num_nodes=4 #81   #100
declare -i r_max=5     #694  #3106
declare -i diff=1      #9306 #6894

for ((r=${r_max};r>=0;r-=1)); do
	echo "Running for r-${r}"
	
	declare -i r_new=${r}+${diff}
	echo r ${r}
	echo r_new ${r_new}
	
	mv /scratch/wey/2023_homogenisation/figures/poly/esbl_prep/init-4-reg/N-${num_nodes}/r-${r} /scratch/wey/2023_homogenisation/figures/poly/esbl_prep/init-4-reg/N-${num_nodes}/r-${r_new}
	#echo old ~/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-4-reg/N-${num_nodes}/r-${r}
	#echo new ~/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-4-reg/N-${num_nodes}/r-${r_new}
	#mv ~/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-4-reg/N-${num_nodes}/r-${r} ~/projects/papers/2023_homogenisation/figures/poly/esbl_prep/init-4-reg/N-${num_nodes}/r-${r_new}
done
