##########################
# Set global SPEC variables
############################
%global _version 1.4

###############
# Set metadata
###############

Name:    cstore_fdw
Version: %{_version}
Release: 1%{?dist}
Summary: An extension that implements a columnar store for PostgreSQL.

Group:   Development/Tools
License: Apache License
URL:     https://github.com/citusdata/cstore_fdw
Source:  https://github.com/citusdata/cstore_fdw/archive/master.tar.gz
Obsoletes: cstore_fdw <= 1.4
Provides: cstore_fdw = 1.4
Requires: protobuf-c-devel

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

make


%install

%make_install
###########################################################
# INSTALL
# This directive is where the code is actually installed
# in the %{buildroot} folder in preparation for packaging.
###########################################################

%clean
[ -d "%{buildroot}" -a "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/usr/pgsql-9.4/lib/cstore_fdw.so
/usr/pgsql-9.4/share/extension/cstore_fdw--1.0--1.1.sql
/usr/pgsql-9.4/share/extension/cstore_fdw--1.1--1.2.sql
/usr/pgsql-9.4/share/extension/cstore_fdw--1.2--1.3.sql
/usr/pgsql-9.4/share/extension/cstore_fdw--1.3--1.4.sql
/usr/pgsql-9.4/share/extension/cstore_fdw--1.4.sql
/usr/pgsql-9.4/share/extension/cstore_fdw.control


%doc



%changelog

