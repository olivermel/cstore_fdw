##########################
# Set global SPEC variables
############################
%global _version 1.4

###############
# Set metadata
###############

Name:    	cstore_fdw%{suffix}
Version: 	%{_version}
Release: 	1%{?dist}
Summary: 	An extension that implements a columnar store for PostgreSQL.

Group:   	Development/Tools
License: 	Apache License
URL:    	https://github.com/citusdata/cstore_fdw
Source:  	https://github.com/citusdata/cstore_fdw/archive/master.tar.gz
Obsoletes: 	cstore_fdw%{suffix} <= 1.4
Provides: 	cstore_fdw%{suffix} = 1.4
Requires: 	protobuf-c-devel

%description

This extension implements a columnar store for PostgreSQL. Columnar stores provide notable benefits for analytic use-cases where data is loaded in batches.

#####################
# Build requirements
#####################
BuildRoot: %(mktemp -ud %{_tmppath}/build/%{name}-%{version}-%{release}-XXXXXX)


########################################################
# PREP and SETUP
# The prep directive removes existing build directory
# and extracts source code so we have a fresh code base
# -n defines the name of the directory
#######################################################

###%prep

#%setup -q -n %{name}-%{version}
%setup -n cstore_fdw-master

###########################################################
# BUILD
# The build directive does initial prep for building,
# then runs the configure script and then make to compile.
# Compiled code is placed in %{buildroot}
###########################################################

%build

#make

###########################################################
# INSTALL
# This directive is where the code is actually installed
# in the %{buildroot} folder in preparation for packaging.

%install

mkdir -p %{buildroot}/etc/profile.d

echo 'export PATH=$PATH:/usr/pgsql-9.5/bin/' >> %{buildroot}/etc/profile.d/cstore.sh
echo 'export USE_PGXS=1' >> %{buildroot}/etc/profile.d/cstore.sh
source %{buildroot}/etc/profile.d/cstore.sh

%make_install

###########################################################

%clean
[ -d "%{buildroot}" -a "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/usr/pgsql-9.5/lib/cstore_fdw.so
/usr/pgsql-9.5/share/extension/cstore_fdw--1.0--1.1.sql
/usr/pgsql-9.5/share/extension/cstore_fdw--1.1--1.2.sql
/usr/pgsql-9.5/share/extension/cstore_fdw--1.2--1.3.sql
/usr/pgsql-9.5/share/extension/cstore_fdw--1.3--1.4.sql
/usr/pgsql-9.5/share/extension/cstore_fdw--1.4.sql
/etc/profile.d/cstore.sh
/usr/pgsql-9.5/share/extension/cstore_fdw.control


%doc



%changelog 
