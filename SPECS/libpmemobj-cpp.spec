%global __cmake_in_source_build 1
%global min_libpmemobj_ver 1.9
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
BuildRequires:	gdb
BuildRequires:  libatomic

# RHEL does not ship SFML-devel.  The library is only used for the pmpong
# example program, so the library can be built without this dependency,
# and without losing any features.
%if !0%{?rhel}
BuildRequires:	SFML-devel
%endif
BuildRequires: make

# There's nothing x86-64 specific in this package, but we have
# to duplicate what spec for pmdk/libpmemobj has at the moment.
# Relevant bug reports:
# https://bugzilla.redhat.com/show_bug.cgi?id=1340634
# https://bugzilla.redhat.com/show_bug.cgi?id=1340635
# https://bugzilla.redhat.com/show_bug.cgi?id=1340636
# https://bugzilla.redhat.com/show_bug.cgi?id=1340637
ExclusiveArch: x86_64 ppc64le

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
%setup -q -n libpmemobj-cpp-%{upstreamversion}

%build
mkdir build
cd build
# CXX_STANDARD=17 matters only for tests, it can be safely disabled in distros without c++17-compliant compiler
%cmake .. -DCMAKE_INSTALL_DOCDIR=%{_docdir}/libpmemobj++ -DBUILD_TESTS=off -DCXX_STANDARD=17 -DTESTS_USE_VALGRIND=OFF
%make_build

%install
cd build
%make_install

%changelog
* Mon Oct 31 2022 Bryan Gurney <bgurney@redhat.com> - 1.13.0-1
- Update to version 1.13.0
- Resolves: rhbz#2136803

* Mon Feb 28 2022 Bryan Gurney <bgurney@redhat.com> - 1.12-8
- Apply patch to fix undefined behavior on realloc
- Also add and apply patch to fix referencing empty array
- Related: rhbz#2034641

* Mon Jan 24 2022 Bryan Gurney <bgurney@redhat.com> - 1.12-7
- Add patch to fix undefined behavior on realloc
- Related: rhbz#2034641

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.12-6
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Mon Aug  2 2021 Jeff Moyer <jmoyer@redhat.com> - 1.12-5.el9
- Get rid of BuildRequires that are only used for testing (Jeff Moyer)
- Resolves: rhbz#1984934

* Wed Jun  9 2021 Jeff Moyer <jmoyer@redhat.com> - 1.12-4.el9
- Disable make check
- Resolves: rhbz#1970104

* Wed Jun  9 2021 Jeff Moyer <jmoyer@redhat.com> - 1.12-3.el9
- Enable ppc64le builds
- Resolves: rhbz#1871149

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.12-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Mon Feb 15 2021 Adam Borowski <kilobyte@angband.pl> - 1.12-1
- Update to version 1.12.

* Thu Feb 11 2021 Adam Borowski <kilobyte@angband.pl> - 1.11-4
- Make SFML-devel buildrequires dependent on !rhel (jmoyer)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 04 2020 Jeff Law <law@redhat.com> - 1.11-2
- Add libatomic to buildrequires

* Fri Oct  9 2020 Adam Borowski <kilobyte@angband.pl> - 1.11-1
- Update to version 1.11.
- Disable enumerable_thread_specific_access_0_drd
- Fix internal find in radix_tree

* Mon Aug 31 2020 Adam Borowski <kilobyte@angband.pl> - 1.10-1
- Update to version 1.10.

* Mon Aug 31 2020 Adam Borowski <kilobyte@angband.pl> - 1.9-5
- Fix FTBFS with new libunwind.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Jeff Law <law@redhat.com> - 1.9-2
- Use __cmake_in_source_build

* Wed Feb 12 2020 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.9-1
- Update to version 1.9.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.8.1-1
- Update to version 1.8.1.

* Fri Oct 04 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.8-2
- Work around https://github.com/pmem/libpmemobj-cpp/issues/469.

* Fri Oct 04 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.8-1
- Update to version 1.8.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.7-1
- Update to version 1.7.

* Thu Mar 28 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.6-2
- Bump required PMDK version to 1.6.

* Mon Mar 18 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.6-1
- Update to version 1.6

* Fri Mar 08 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5.1-1
- Update to version 1.5.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 14 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5-1
- Initial RPM release
