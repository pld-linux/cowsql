Summary:	Embeddable, replicated and fault tolerant SQL engine
Name:		cowsql
Version:	1.15.9
Release:	1
License:	LGPL v3
Group:		Libraries
#Source0Download: https://github.com/cowsql/cowsql/releases
Source0:	https://github.com/cowsql/cowsql/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cf46c3e372eaa2e06addb95ece4a9bd5
URL:		https://github.com/cowsql/cowsql
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool >= 2:2
BuildRequires:	libuv-devel >= 1.8.0
BuildRequires:	pkgconfig
BuildRequires:	raft-devel >= 0.22.1
BuildRequires:	sqlite3-devel >= 3.22.0
Requires:	libuv >= 1.8.0
Requires:	raft >= 0.18.0
Requires:	sqlite3 >= 3.22.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package is a fork the dqlite C library (libdqlite), which can be
used to expose a dqlite database over the network and replicate it
across a cluster of peers, using the Raft algorithm.

%description -l pl.UTF-8
Ten pakiet zawiera fork biblioteki C dqlite (libdqlite), którą można
wykorzystywać do udostępnienia bazy danych dqlite przez sieć i
replikować ją na klaster partnerów przy użyciu algorytmu Raft.

%package devel
Summary:	Header files for dqlite development
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dqlite
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libuv-devel >= 1.8.0
Requires:	raft-devel >= 0.14.0
Requires:	sqlite3-devel >= 3.22.0

%description devel
This package contains development files for the dqlite library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki dqlite.

%package static
Summary:	Static dqlite library
Summary(pl.UTF-8):	Statyczna biblioteka dqlite
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static dqlite library.

%description static -l pl.UTF-8
Ten pakiet zawiera bibliotekę statyczną dqlite.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
CFLAGS="-Wno-error %{rpmcflags}" %configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/libcowsql.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md
%{_libdir}/libcowsql.so.*.*.*
%ghost %{_libdir}/libcowsql.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcowsql.so
%{_includedir}/cowsql.h
%{_pkgconfigdir}/cowsql.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcowsql.a
