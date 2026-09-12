#
# Conditional build:
%bcond_without	tests		# do not perform "make check"
#
Summary:	Embeddable, replicated and fault tolerant SQL engine
Name:		cowsql
Version:	1.15.9
Release:	1
License:	LGPL v3
Group:		Libraries
#Source0Download: https://github.com/cowsql/cowsql/releases
Source0:	https://github.com/cowsql/cowsql/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cf46c3e372eaa2e06addb95ece4a9bd5
Patch0:		cast.patch
URL:		https://github.com/cowsql/cowsql
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool >= 2:2
BuildRequires:	libuv-devel >= 1.8.0
BuildRequires:	pkgconfig
BuildRequires:	raft-devel >= 0.22.1
BuildRequires:	sqlite3-devel >= 3.22.0
Requires:	libuv >= 1.8.0
Requires:	raft >= 0.22.1
Requires:	sqlite3 >= 3.22.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cowsql is a C library implementing an embeddable, replicated SQL
database engine with high availability and automatic failover. It is a
fork of dqlite and uses the Raft algorithm to replicate an SQLite
database across a cluster of peers.

%description -l pl.UTF-8
cowsql to biblioteka C implementująca osadzalny, replikowany silnik
bazodanowy SQL o wysokiej dostępności i automatycznym przełączaniu
awaryjnym. Jest to fork biblioteki dqlite, wykorzystujący algorytm Raft
do replikowania bazy SQLite na klastrze węzłów.

%package devel
Summary:	Header files for cowsql library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki cowsql
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libuv-devel >= 1.8.0
Requires:	raft-devel >= 0.22.1
Requires:	sqlite3-devel >= 3.22.0

%description devel
Header files for cowsql library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki cowsql.

%package static
Summary:	Static cowsql library
Summary(pl.UTF-8):	Statyczna biblioteka cowsql
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static cowsql library.

%description static -l pl.UTF-8
Statyczna biblioteka cowsql.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcowsql.la

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
