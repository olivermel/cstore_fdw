#!/usr/bin/env bash

sudo yum -y groupinstall 'Development Tools'
sudo yum -y install java-1.7.1*
sudo yum -y install vim
sudo yum -y install yum localinstall http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-centos94-9.4-1.noarch.rpm
sudo yum -y install postgresql9*
sudo yum -y install tree
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
sudo rpm -ivh epel-release-latest-6.noarch.rpm
sudo yum -y install protobuf-c-devel   #requirement

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

if [ "$SCRIPTPATH" = "/Users/ezeogum/Projects/rpm-git-clones/cstore_fdw" ] ; then
       SCRIPTPATH=/vagrant
   fi
  
  mkdir -p $HOME/rpmbuild/{BUILD,RPMS,SOURCES,SRPMS}
 ln -sf $SCRIPTPATH/SPECS $HOME/rpmbuild/SPECS
echo '%_topdir '$HOME'/rpmbuild' > $HOME/.rpmmacros
cd $HOME/rpmbuild/SOURCES
wget https://github.com/citusdata/cstore_fdw/archive/master.tar.gz
