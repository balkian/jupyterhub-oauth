#!/bin/sh

IFS="
"
for line in `cat userlist`; do
  test -z "$line" && continue
  user=`echo $line | cut -f 1 -d' '`
  admin=`echo $line | cut -f 2 -d' '`
  echo "adding user $user"
  useradd -m -s /bin/bash $user
  if [ "$admin" = "admin" ]; then
    echo "Making $user admin"
      usermod -a -G hubadmin $user
  fi
  #cp -r /srv/ipython/examples /shared/$user/examples
  #chown -R $user /home/$user/examples
done
