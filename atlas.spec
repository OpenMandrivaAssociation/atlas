# Based on fedora package:
# http://pkgs.fedoraproject.org/cgit/atlas.git

%define Werror_cflags %nil
%global _duplicate_files_terminate_build 0

%define _disable_lto 1

%define enable_native_atlas 0
%define __isa_bits 32
%ifarch %{x86_64} aarch64 riscv64
%define __isa_bits 64
%endif

%define types base
%define pr_base %(echo $((%{__isa_bits}+0)))

# Keep these libraries private because they are not in %%{_libdir}
#% if %{_use_internal_dependency_generator}
#% define __noautoprov 'libsatlas\\.so\\.(.*)|libtatlas\\.so\\.(.*)'
#% define __noautoreq 'libsatlas\\.so\\.(.*)|libtatlas\\.so\\.(.*)'
#% endif

%define major 3
%define libatlas libatlas

%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

# "-msse2", "-mavx2 and similar compiler flags get garbled by Atlas'
# build system inserting spaces. This should be fixed properly at some
# point...
%ifarch znver1
%global optflags -O3 -march=znver1 -mtune=znver1 -mfpmath=sse
%endif
%ifarch riscv64
%global optflags %nil
%endif

Name:		atlas
Version:	3.10.3
%if "%{?enable_native_atlas}" != "0"
%define dist .native
%endif
Release:	3
Summary:	Automatically Tuned Linear Algebra Software
License:	BSD
Group:		Sciences/Mathematics
URL:		https://math-atlas.sourceforge.net/
Source0:	http://downloads.sourceforge.net/math-atlas/%{name}%{version}.tar.bz2
Source1:	PPRO32.tgz
Source3:	README.dist
Source10:	https://github.com/Reference-LAPACK/lapack/archive/v3.8.0.tar.gz
#archdefs taken from debian:
Source11:	POWER332.tar.bz2
Source12:	IBMz932.tar.bz2
Source13:	IBMz964.tar.bz2
#upstream arm uses softfp abi, fedora arm uses hard
Source14:	ARMv732NEON.tar.bz2
Source15:	ARMa732.tar.bz2
Source100:	%{name}.rpmlintrc

Patch2:         atlas-fedora-arm.patch
# Properly pass -melf_* to the linker with -Wl, fixes FTBFS bug 817552
# https://sourceforge.net/tracker/?func=detail&atid=379484&aid=3555789&group_id=23725
Patch3:         atlas-melf.patch
Patch4:         atlas-throttling.patch

#credits Lukas Slebodnik
Patch5:         atlas-shared_libraries.patch

Patch8:         atlas-genparse.patch

# Unbundle LAPACK (BZ #1181369)
Patch9:         atlas.3.10.1-unbundle.patch
Patch10:        atlas-gcc10.patch
Patch11:	atlas-riscv64-port.patch


BuildRequires:	gcc-gfortran
BuildRequires:	lapack-devel

%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

#-----------------------------------------------------------------------
%package -n %{libname}
Summary:	Automatically Tuned Linear Algebra Software
Provides:	%{libatlas} = %{version}-%{release}
Obsoletes:	%{libatlas}-sse2 < %{EVRD}
Obsoletes:	%{libatlas}-sse3 < %{EVRD}
%ifnarch %{ix86} %{x86_64}
Obsoletes:	%{libatlas}-%{_arch} < %{EVRD}
%endif

%description -n %{libname}
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

The performance improvements in ATLAS are obtained largely via
compile-time optimizations and tend to be specific to a given hardware
configuration. In order to package ATLAS some compromises
are necessary so that good performance can be obtained on a variety
of hardware. This set of ATLAS binary packages is therefore not
necessarily optimal for any specific hardware configuration. However,
the source package can be used to compile customized ATLAS packages;
see the documentation for information.

%files -n %{libname}
%doc doc/README.dist
%dir %{_libdir}/atlas
%{_libdir}/atlas/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}.conf

#-----------------------------------------------------------------------

%package -n %{devname}
Summary:	Development libraries for ATLAS
Requires:	%{libname} = %{version}-%{release}
Provides:	%{libatlas}-devel
Requires(posttrans):	update-alternatives
Requires(preun):	update-alternatives
Obsoletes:	%{libatlas}-sse2-devel
Obsoletes:	%{libatlas}-sse3-devel
%ifnarch %{ix86} %{x86_64}
Obsoletes:	%{libatlas}-%{_arch}-devel
%endif

%description -n %{devname}
This package contains headers for development with ATLAS
(Automatically Tuned Linear Algebra Software).

%posttrans -n %{devname}
if [ $1 -eq 0 ] ; then
    /usr/sbin/alternatives --install %{_includedir}/atlas atlas-devel %{_includedir}/atlas-%{_arch}-base %{pr_base}
fi

%postun -n %{devname}
if [ $1 -ge 0 ] ; then
    /usr/sbin/alternatives --remove atlas-devel %{_includedir}/atlas-%{_arch}-base
fi

%files -n %{devname}
%doc doc
%{_libdir}/atlas/*.so
%{_libdir}/pkgconfig/atlas.pc
%{_includedir}/atlas-%{_arch}-base/
%{_includedir}/*.h
%ghost %{_includedir}/atlas


########################################################################

########################################################################

%prep
%setup -q -n ATLAS
#patch0 -p0 -b .shared
#arm patch not applicable, probably not needed
#%ifarch %{arm}
#%patch2 -p0 -b .arm
#%endif
%patch3 -p1 -b .melf
%patch4 -p1 -b .thrott
%patch5 -p2 -b .sharedlib
%patch8 -p1 -b .genparse
%patch9 -p1 -b .unbundle
%patch10 -p1
%patch11 -p1

cp %{SOURCE1} CONFIG/ARCHS/
cp %{SOURCE3} doc
cp %{SOURCE11} CONFIG/ARCHS/
cp %{SOURCE12} CONFIG/ARCHS/
cp %{SOURCE13} CONFIG/ARCHS/
cp %{SOURCE14} CONFIG/ARCHS/
cp %{SOURCE15} CONFIG/ARCHS/

%ifarch %{arm}
# Set arm flags in atlcomp.txt
#sed -i -e 's,-mfpu=vfpv3,-mfpu=neon,' CONFIG/src/atlcomp.txt
sed -i -e 's,-mfloat-abi=softfp,-mfloat-abi=hard,' CONFIG/src/atlcomp.txt
# Some extra arm flags not needed
#sed -i -e 's,-mfpu=vfpv3,,' tune/blas/gemm/CASES/*.flg
%endif

%build
%setup_compile_flags
export CC=gcc
export CXX=g++

%ifarch %{arm}
%global mode %{nil}
%else
%global mode -b %{__isa_bits}
%endif

%define arg_options %{nil}
%define flags %{nil}
%define threads_option "-t 2"

#Target architectures for the 'base' versions

%ifarch %{x86_64}
%define flags %{nil}
%define base_options "-A HAMMER -V 896"
# (tpg) get rid of error
# x86_64-linux-gnu-gcc-8.3.0: error: 64: No such file or directory
# x86_64-linux-gnu-gcc-8.3.0: error: unrecognized command line option '-m'
%global optflags %(echo %{optflags}|sed -e 's/-m64//g')
%endif

%ifarch %{ix86}
%define flags %{nil}
%define base_options "-A PIII -V 512"
%endif

%ifarch %{arm}
%define flags "-DATL_ARM_HARDFP=1"
%define base_options "-A ARMv7 -V 1"
%endif

%ifarch aarch64
%define flags %{nil}
%define base_options "-A ARM64a53 -V 1"
%endif

%ifarch riscv64
%define flags %{nil}
%define base_options "-A RISCV64 -V 1"
%endif

%if "%{?enable_native_atlas}" != "0"
%define threads_option %{nil}
%define base_options %{nil}
%define flags %{nil}
%endif

for type in %{types}; do
    if [ "$type" = "base" ]; then
	libname=atlas
	arg_options=%{base_options}
	thread_options=%{threads_option}
    else
	libname=atlas-${type}
    fi

    mkdir -p %{_arch}_${type}
    pushd %{_arch}_${type}
%ifarch %{ix86} %{arm}
    ../configure %{mode} $arg_options $thread_options -D c -DWALL -Fa alg '%{flags} -g -Wa,--noexecstack -fPIC' \
%else
    ../configure %{mode} $arg_options $thread_options -D c -DWALL -Fa alg '%{flags} -g -Wa,--noexecstack -fPIC %{ldflags}' \
%endif
    --cc=gcc \
    --prefix=%{buildroot}%{_prefix} \
    --incdir=%{buildroot}%{_includedir} \
    --libdir=%{buildroot}%{_libdir}/${libname} \
    --with-netlib-lapack-tarfile=%{S:10}

    sed -i 's#SLAPACKlib.*#SLAPACKlib = %{_libdir}/liblapack.so#' Make.inc
    cat Make.inc

    %make_build -j1 build
    cd lib
    %make_build -j1 shared
    %make_build -j1 ptshared
    popd
done

########################################################################

%install
for type in %{types}; do
    pushd %{_arch}_${type}
    %make_install DESTDIR=%{buildroot} install
    mv %{buildroot}%{_includedir}/atlas %{buildroot}%{_includedir}/atlas-%{_arch}-${type}
    if [ "$type" = "base" ]; then
	cp -pr lib/*.so* %{buildroot}%{_libdir}/atlas/
	rm -f %{buildroot}%{_libdir}/atlas/*.a
    else
	cp -pr lib/*.so* %{buildroot}%{_libdir}/atlas-${type}/
	rm -f %{buildroot}%{_libdir}/atlas-${type}/*.a
    fi
    popd

    mkdir -p %{buildroot}/etc/ld.so.conf.d
    if [ "$type" = "base" ]; then
	echo "%{_libdir}/atlas" > %{buildroot}/etc/ld.so.conf.d/atlas-%{_arch}.conf
    else
	echo "%{_libdir}/atlas-${type}" > %{buildroot}/etc/ld.so.conf.d/atlas-%{_arch}-${type}.conf
    fi
done
mkdir -p %{buildroot}%{_includedir}/atlas

#create pkgconfig file
mkdir -p %{buildroot}/%{_libdir}/pkgconfig/
cat > %{buildroot}/%{_libdir}/pkgconfig/atlas.pc << DATA
Name: %{name}
Version: %{version}
Description: %{summary}
Cflags: -I%{_includedir}/atlas/
Libs: -L%{_libdir}/atlas/ -lsatlas
DATA

########################################################################

%check
for type in %{types}; do
    pushd %{_arch}_${type}
    make check ptcheck || :
    popd
done

