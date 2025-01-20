#!/bin/bash

ENV="prod"

VERSION_TYPE=("major" "minor" "patch")
NEW_VERSION_NUMBER=""

illegal_option()
{
    echo "$(basename $0): illegal option: $OPTARG" >&2
    echo "usage: $(basename $0) [-t (major minor patch)]"
    exit 1
}

get_new_application_version()
{
  echo "❔ Is the application in production already? (yes/no)"
  read ans
  if [[ $ans == "yes" ]]; then
      echo "⏳ Version v1.1.0 will be created"
      NEW_VERSION_NUMBER="v1.1.0"
  else
    echo "⏳ Version v0.1.0 will be created"
      NEW_VERSION_NUMBER="v0.1.0"
  fi
}

create_tag()
{
  echo "🔍 Searching latest versions..."

  git pull > /dev/null 2>&1

  VERSION=`git tag -l --sort -version:refname | grep releases/ -m 1`

  if [ -z $VERSION ]
  then
      echo "❗❗ No release tag was found... Create first version? (yes/no)"
      read ans
      if [[ "$ans" == "yes" ]]; then
        get_new_application_version
      else
        echo "❗ No version will be created"
        exit 1
      fi
  else
    echo "✨  Latest version generated is $VERSION"
    VERSION_NUMBER=(${VERSION//v/ })
    VERSION_BITS=(${VERSION_NUMBER[1]//./ })

    VNUM1=${VERSION_BITS[0]}
    VNUM2=${VERSION_BITS[1]}
    VNUM3=${VERSION_BITS[2]}

    if [ $type = "minor" ]
    then
        VNUM2=$((VNUM2+1))
        VNUM3=0
    elif [ $type = "major" ]
    then
        VNUM1=$((VNUM1+1))
        VNUM2=0
        VNUM3=0
    else
        VNUM3=$((VNUM3+1))
    fi

    NEW_VERSION_NUMBER="v$VNUM1.$VNUM2.$VNUM3"
  fi

  echo "💣 Creating a new version - releases/$NEW_VERSION_NUMBER and deploying to $ENV with releases/$ENV/$NEW_VERSION_NUMBER"

  git tag releases/"$NEW_VERSION_NUMBER" > /dev/null 2>&1
  git tag releases/"$ENV"/"$NEW_VERSION_NUMBER" > /dev/null 2>&1
  git push --tags > /dev/null 2>&1

  REPOSITORY_URL=$(git config --get remote.origin.url)
  REPOSITORY_NAME=$(echo "$REPOSITORY_URL" | sed -E 's/.*\/(.*)\.git/\1/')

  echo "🚀 To see the deployment status, go to https://app.circleci.com/pipelines/github/<your-company>/$REPOSITORY_NAME?filter=mine&status=none&status=running"
}

validate_branch()
{
  git_version=$(git --version | awk '{print $3}' | sed 's/\([0-9]*\.[0-9]*\)\.[0-9]*/\1/')
  git_version=$(echo "$git_version" | tr -d '.')
  if [[ $(($git_version)) -lt 222 ]]; then
    branch=$(git rev-parse --abbrev-ref HEAD)
  else
    branch=$(git branch --show-current)
  fi

  if [[ "$branch" != "main" ]]; then
    echo "❗ Release tags can only be created from main branch. Current branch: $branch"
    exit 1
  fi
}

while getopts 't:' OPTION; do

  case "$OPTION" in
    t)
      type="$OPTARG"
      if [[ " ${VERSION_TYPE[@]} " =~ $OPTARG ]]; then
        validate_branch
        echo "✨  Creating tag for version type $type"
         date +'%d/%m/%Y %H:%M:%S'
        create_tag
      else
        illegal_option
      fi
      ;;

    ?)
      illegal_option
      ;;
  esac

done

if (( $OPTIND == 1 )); then
  illegal_option
fi