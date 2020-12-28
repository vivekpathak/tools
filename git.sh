#!/bin/bash 


pushd ~

for dir in ~/pub/psychic-eureka/ ~/pub/tools ~/notes
do
    echo Working on $(pwd)

    if pushd $dir ; then
        echo OK                          # pushed $dir OK !
    else
        echo ERROR - failed to push $dir now at $(pwd)
        exit 1
    fi

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
