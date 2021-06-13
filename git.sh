#!/bin/bash 
pushd ~

for dir in newlibertie/benchmarks newlibertie/db newlibertie/docs \
				  newlibertie/web \
	newlibertie/server newlibertie/voting-protocol \
        clowdsource/cs-cui clowdsource/cs-db clowdsource/cs-rui \
	clowdsource/cs-svc clowdsource/cs-admin \
        pub/psychic-eureka \
	pub/tools newlibertie/client pub/casters pub/authrep
do 
	if ! pushd $dir ; then
		echo exiting because of error at directory $dir
		exit 
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
