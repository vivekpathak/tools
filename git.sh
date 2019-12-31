#!/bin/bash 
pushd ~

for dir in newlibertie/benchmarks newlibertie/docs newlibertie/web \
	newlibertie/server \
           clowdsource/cs-cui clowdsource/cs-db clowdsource/cs-rui clowdsource/cs-svc clowdsource/cs-admin
           # TODO pubcode/jfi pubcode/casters pubcode/tools pubcode/authrep \#newlibertie/client \ newlibertie/db newlibertie/voting-protocol \
do 
	if ! pushd $dir ; then
		echo exiting because of error at directory $dir
		exit 
	fi

	echo Working on $(pwd)
	if ! git diff --quiet ; then 
		echo Dirty : $dir .... skipping
	else
	    if ! git pull ; then
		    echo Conflict on pull for $dir .... reverting 
		    git merge --abort
	    else
		    echo $dir is updated
        fi
	fi 
	popd 
done

popd
