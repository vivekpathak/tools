#!/bin/bash 
pushd ~

for dir in 1power/psychic-eureka 1power/vigilant-lamp 1power/business-planning \
	pub/tools pub/casters \
	newlibertie/benchmarks newlibertie/db newlibertie/docs \
                                  newlibertie/web 
do 
	if ! pushd $dir ; then
		echo error at directory $dir - please fix
		continue
	fi

	#echo Working on $(pwd)
	if ! git diff --quiet ; then 
		echo Dirty : $dir .... skipping
	else
	    if ! git pull ; then
		    echo Conflict on pull for $dir .... reverting 
		    git merge --abort
	    #else
		    #echo $dir is up to date
            fi
	fi 
	popd 
done

popd

#  newlibertie/client  pub/authrep

