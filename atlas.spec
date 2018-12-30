# Based on fedora package:
# http://pkgs.fedoraproject.org/cgit/atlas.git

%define Werror_cflags %nil
%global _duplicate_files_terminate_build	0

%define enable_native_atlas	0
%define __isa_bits		32
%ifarch %{x86_64} aarch64
	%define __isa_bits	64
%endif

%define types			base
%define pr_base			%(echo $((%{__isa_bits}+0)))

# Keep these libraries private because they are not in %%{_libdir}
#% if %{_use_internal_dependency_generator}
#% define __noautoprov 'libsatlas\\.so\\.(.*)|libtatlas\\.so\\.(.*)'
#% define __noautoreq 'libsatlas\\.so\\.(.*)|libtatlas\\.so\\.(.*)'
#% endif

%define major		3
%define libatlas	libatlas

%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Name:		atlas
Version:	3.10.3
%if "%{?enable_native_atlas}" != "0"
	%define dist	.native
%endif
Release:	1.5%{?dist}
Summary:	Automatically Tuned Linear Algebra Software
License:	BSD
Group:		Sciences/Mathematics
URL:		http://math-atlas.sourceforge.net/
Source0:	http://downloads.sourceforge.net/math-atlas/%{name}%{version}.tar.bz2
Source1:	PPRO32.tgz
Source3:	README.dist
Source10:	http://www.netlib.org/lapack/lapack-3.6.0.tgz
#archdefs taken from debian:
Source11:	POWER332.tar.bz2
Source12:	IBMz932.tar.bz2
Source13:	IBMz964.tar.bz2
#upstream arm uses softfp abi, fedora arm uses hard
Source14:	ARMv732NEON.tar.bz2
Source100:	%{name}.rpmlintrc

Patch2:		atlas-no-m32-on-ARM.patch
# Properly pass -melf_* to the linker with -Wl, fixes FTBFS bug 817552
# https://sourceforge.net/tracker/?func=detail&atid=379484&aid=3555789&group_id=23725
Patch3:		atlas-melf.patch
Patch4:		atlas-throttling.patch

#credits Lukas Slebodnik
Patch5:		atlas-shared_libraries.patch


#Patch7:		0001-aarch64-support.patch
Patch8:		atlas-genparse.patch
# Unbundle LAPACK (BZ #1181369)
Patch9:		atlas.3.10.1-unbundle.patch

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
Obsoletes:	%{libatlas}-devel
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
	/usr/sbin/alternatives --install %{_includedir}/atlas atlas-devel	\
	%{_includedir}/atlas-%{_arch}-base %{pr_base}
fi

%preun -n %{devname}
if [ $1 -ge 0 ] ; then
	/usr/sbin/alternatives --remove atlas-devel				\
	%{_includedir}/atlas-%{_arch}-base
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
%patch2 -p1 -b .m32arm
%patch3 -p1 -b .melf
%patch4 -p1 -b .thrott
%patch5 -p2 -b .sharedlib
#affinity crashes with fewer processors than the builder but increases performance of locally builded library
#% if "%{?enable_native_atlas}" == "0"
#% patch6 -p1 -b .affinity
#% endif
#% ifarch aarch64
#% patch7 -p1 -b .aarch64
#% endif
%patch8 -p1 -b .genparse
%patch9 -p1

cp %{SOURCE1} CONFIG/ARCHS/
cp %{SOURCE3} doc
cp %{SOURCE11} CONFIG/ARCHS/
cp %{SOURCE12} CONFIG/ARCHS/
cp %{SOURCE13} CONFIG/ARCHS/
cp %{SOURCE14} CONFIG/ARCHS/

%ifarch %{arm}
# Set arm flags in atlcomp.txt
sed -i -e 's,-mfpu=vfpv3,-mfpu=neon,' CONFIG/src/atlcomp.txt
sed -i -e 's,-mfloat-abi=softfp,-mfloat-abi=hard,' CONFIG/src/atlcomp.txt
# Some extra arm flags not needed
sed -i -e 's,-mfpu=vfpv3,,' tune/blas/gemm/CASES/*.flg
%endif

%build

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
%endif

%ifarch %ix86
%define flags %{nil}
%define base_options "-A PIII -V 512"
%endif

%ifarch %{arm}
%define flags "-DATL_ARM_HARDFP=1"
%define base_options "-A ARMa7 -V 1"
%endif

%ifarch aarch64
%define flags %{nil}
%define base_options "-A ARM64a53 -V 1"
%endif

%if "%{?enable_native_atlas}" != "0"
%define    threads_option %{nil}
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
	../configure %{mode} $arg_options $thread_options -D c -DWALL -Fa alg '%{flags} -g -Wa,--noexecstack -fPIC %{ldflags}'\
	--cc=gcc					\
	--prefix=%{buildroot}%{_prefix}			\
	--incdir=%{buildroot}%{_includedir}		\
	--libdir=%{buildroot}%{_libdir}/${libname}
#	--with-netlib-lapack-tarfile=%{SOURCE10}

        sed -i 's#SLAPACKlib.*#SLAPACKlib = %{_libdir}/liblapack.so#' Make.inc

%endif
	make build
	cd lib
	make shared
	make ptshared
	popd
done

########################################################################

%install
for type in %{types}; do
	pushd %{_arch}_${type}
	make DESTDIR=%{buildroot} install
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
		echo "%{_libdir}/atlas"		\
		> %{buildroot}/etc/ld.so.conf.d/atlas-%{_arch}.conf
	else
		echo "%{_libdir}/atlas-${type}"	\
		> %{buildroot}/etc/ld.so.conf.d/atlas-%{_arch}-${type}.conf
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

