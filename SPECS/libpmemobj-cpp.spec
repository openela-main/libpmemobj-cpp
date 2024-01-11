%global min_libpmemobj_ver 1.11.1
%global upstreamversion 1.13.0

Name:		libpmemobj-cpp
Version:	1.13.0
Release:	1%{?dist}
Summary:	C++ bindings for libpmemobj
# Note: tests/external/libcxx is dual licensed using University of Illinois "BSD-Like" license and the MIT license. It's used only during development/testing and is NOT part of the binary RPM.
License:	BSD
URL:		http://pmem.io/pmdk/cpp_obj/

Source0:	https://github.com/pmem/%{name}/archive/%{upstreamversion}.tar.gz#/%{name}-%{upstreamversion}.tar.gz

BuildRequires:	libpmemobj-devel >= %{min_libpmemobj_ver}
BuildRequires:	cmake >= 3.3
BuildRequires:	glibc-devel
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	doxygen
BuildRequires:	perl-Encode
BuildRequires:	libatomic

# There's nothing x86-64 specific in this package, but we have
# to duplicate what spec for pmdk/libpmemobj has at the moment.
# Relevant bug reports:
# https://bugzilla.redhat.com/show_bug.cgi?id=1340634
# https://bugzilla.redhat.com/show_bug.cgi?id=1340635
# https://bugzilla.redhat.com/show_bug.cgi?id=1340636
# https://bugzilla.redhat.com/show_bug.cgi?id=1340637
ExclusiveArch: x86_64

%description
This package contains header files for libpmemobj C++ bindings and C++
containers built on top of them.

# Specify a virtual Provide for libpmemobj++-static package, so the package
# usage can be tracked.
%package -n libpmemobj++-devel
Summary: C++ bindings for Persistent Memory Transactional Object Store library
Provides: libpmemobj++-static = %{version}-%{release}
Requires: libpmemobj-devel >= %{min_libpmemobj_ver}

%description -n libpmemobj++-devel
This package contains header files for libpmemobj C++ bindings and C++
containers built on top of them.

The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming.

%files -n libpmemobj++-devel
%{_libdir}/pkgconfig/libpmemobj++.pc
%dir %{_includedir}/libpmemobj++
%{_includedir}/libpmemobj++/*.hpp
%dir %{_includedir}/libpmemobj++/detail
%{_includedir}/libpmemobj++/detail/*.hpp
%dir %{_includedir}/libpmemobj++/container
%{_includedir}/libpmemobj++/container/*.hpp
%dir %{_includedir}/libpmemobj++/container/detail
%{_includedir}/libpmemobj++/container/detail/*.hpp
%dir %{_includedir}/libpmemobj++/experimental
%{_includedir}/libpmemobj++/experimental/*.hpp
%dir %{_libdir}/libpmemobj++
%dir %{_libdir}/libpmemobj++/cmake
%{_libdir}/libpmemobj++/cmake/libpmemobj++-config-version.cmake
%{_libdir}/libpmemobj++/cmake/libpmemobj++-config.cmake

%license LICENSE

%doc ChangeLog README.md

%package -n libpmemobj++-doc
Summary: HTML documentation for libpmemobj++

%description -n libpmemobj++-doc
HTML documentation for libpmemobj++.

%files -n libpmemobj++-doc
%dir %{_docdir}/libpmemobj++
%{_docdir}/libpmemobj++/*

%license LICENSE

%doc ChangeLog README.md

%global debug_package %{nil}

%prep
%setup -q

%build

mkdir build
cd build
%cmake .. -DCMAKE_INSTALL_DOCDIR=%{_docdir}/libpmemobj++ -DBUILD_TESTS=off -DCXX_STANDARD=17 -DTESTS_USE_VALGRIND=OFF
%make_build

%install
cd build
%make_install

%changelog
* Mon Nov 21 2022 Bryan Gurney <bgurney@redhat.com> - 1.13.0-1
- Update to version 1.13.0
- Related: rhbz#2111428

* Thu Mar 10 2022 Bryan Gurney <bgurney@redhat.com> - 1.11-2
- Add libatomic to BuildRequires
- Related: rhbz#2061720

* Wed Jan 26 2022 Bryan Gurney <bgurney@redhat.com> - 1.11-1
- Update to upstream version 1.11
- Related: rhbz#2009889

* Mon Feb  1 2021 Jeff Moyer <jmoyer@redhat.com> - 1.9-1
- Update to upstream version 1.9
- get rid of % check, as the builtin tests now require packages we don't ship.
- Related: rhbz#1780389

* Tue Jun 18 2019 Jeff Moyer <jmoyer@redhat.com> - 1.6-2.el8
- new build to kick off gating tests
- Related: rhbz#1659659

* Mon Jun 17 2019 Jeff Moyer <jmoyer@redhat.com> - 1.6-1.el8
- initial RHEL8 import
- Resolves: rhbz#1659659

* Thu Nov 8 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5-1
- Initial RPM release
