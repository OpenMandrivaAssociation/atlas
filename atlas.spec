# Based on fedora package:
# http://pkgs.fedoraproject.org/cgit/atlas.git

%global _duplicate_files_terminate_build	0

%define enable_native_atlas	0
%define __isa_bits		32
%ifarch x86_64 aarch64 znver1
	%define __isa_bits	64
%endif

%define types			base
%define pr_base			%(echo $((%{__isa_bits}+0)))
%ifarch %{ix86}
	%define types			base sse2 sse3
	%define pr_sse2		%(echo $((%{__isa_bits}+3)))
	%define pr_sse3		%(echo $((%{__isa_bits}+4)))
%endif
%ifarch s390 s390x
	%define pr_z10		%(echo $((%{__isa_bits}+1)))
	%define pr_z196		%(echo $((%{__isa_bits}+2)))
%endif

# Keep these libraries private because they are not in %%{_libdir}
#% if %{_use_internal_dependency_generator}
#% define __noautoprov 'libsatlas\\.so\\.(.*)|libtatlas\\.so\\.(.*)'
#% define __noautoreq 'libsatlas\\.so\\.(.*)|libtatlas\\.so\\.(.*)'
#% endif

%define major		3
%define libatlas	libatlas

%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d
%define libname_sse2	%mklibname %{name}-sse2 %{major}
%define devname_sse2	%mklibname %{name}-sse2 -d
%define libname_sse3	%mklibname %{name}-sse3 %{major}
%define devname_sse3	%mklibname %{name}-sse3 -d

Name:		atlas
Version:	3.10.3
%if "%{?enable_native_atlas}" != "0"
	%define dist	.native
%endif
Release:	1.3%{?dist}
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

#Patch1:		atlas-s390port.patch
Patch2:		atlas-no-m32-on-ARM.patch
# Properly pass -melf_* to the linker with -Wl, fixes FTBFS bug 817552
# https://sourceforge.net/tracker/?func=detail&atid=379484&aid=3555789&group_id=23725
Patch3:		atlas-melf.patch
Patch4:		atlas-throttling.patch

#credits Lukas Slebodnik
Patch5:		atlas-shared_libraries.patch


#Patch7:		0001-aarch64-support.patch
Patch8:		atlas-genparse.patch

BuildRequires:	gcc-gfortran
#BuildRequires:	lapack-devel

%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

#-----------------------------------------------------------------------
%package	-n %{libname}
Summary:	Automatically Tuned Linear Algebra Software
Provides:	%{libatlas} = %{version}-%{release}
Obsoletes:	%{libatlas}-devel
%ifarch x86_64 znver1
Obsoletes:	%{libatlas}-sse2
%endif
%ifarch x86_64 znver1
Obsoletes:	%{libatlas}-sse3
%endif
%ifnarch %{ix86} x86_64 znver1
Obsoletes:	%{libatlas}-%{_arch}
%endif

%description	-n %{libname}
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

%files		-n %{libname}
%doc doc/README.dist
%dir %{_libdir}/atlas
%{_libdir}/atlas/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}.conf

#-----------------------------------------------------------------------

%package	-n %{devname}
Summary:	Development libraries for ATLAS
Requires:	%{libname} = %{version}-%{release}
Provides:	%{libatlas}-devel
Requires(posttrans):	update-alternatives
Requires(preun):	update-alternatives
%ifarch x86_64 znver1
Obsoletes:	%{libatlas}-sse2-devel
%endif
%ifarch x86_64 znver1
Obsoletes:	%{libatlas}-sse3-devel
%endif
%ifnarch %{ix86} x86_64 znver1
Obsoletes:	%{libatlas}-%{_arch}-devel
%endif

%description	-n %{devname}
This package contains headers for development with ATLAS
(Automatically Tuned Linear Algebra Software).

%posttrans	-n %{devname}
if [ $1 -eq 0 ] ; then
	/usr/sbin/alternatives --install %{_includedir}/atlas atlas-devel	\
	%{_includedir}/atlas-%{_arch}-base %{pr_base}
fi

%preun		-n %{devname}
if [ $1 -ge 0 ] ; then
	/usr/sbin/alternatives --remove atlas-devel				\
	%{_includedir}/atlas-%{_arch}-base
fi

%files		-n %{devname}
%doc doc
%{_libdir}/atlas/*.so
%{_libdir}/pkgconfig/atlas.pc
%{_includedir}/atlas-%{_arch}-base/
%{_includedir}/*.h
%ghost %{_includedir}/atlas

########################################################################
%if "%{?enable_native_atlas}" == "0"
%ifarch %{ix86}

#-----------------------------------------------------------------------

%package	-n %{libname_sse2}
Summary:	ATLAS libraries for SSE2 extensions
Provides:	%{libatlas} = %{version}-%{release}

%description	-n %{libname_sse2}
This package contains ATLAS (Automatically Tuned Linear Algebra Software)
shared libraries compiled with optimizations for the SSE2
extensions to the ix86 architecture. ATLAS builds with
SSE(1) and SSE3 extensions also exist.

%files		-n %{libname_sse2}
%doc doc/README.dist
%dir %{_libdir}/atlas-sse2
%{_libdir}/atlas-sse2/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-sse2.conf

#-----------------------------------------------------------------------

%package	-n %{devname_sse2}
Summary:	Development files for ATLAS SSE2
Requires(posttrans):	update-alternatives
Requires(preun):	update-alternatives

%description	-n %{devname_sse2}
This package contains ATLAS (Automatically Tuned Linear Algebra Software)
headers for libraries compiled with optimizations for the SSE2 extensions
to the ix86 architecture.

%posttrans	-n %{devname_sse2}
if [ $1 -eq 0 ] ; then
	/usr/sbin/alternatives --install %{_includedir}/atlas atlas-devel	\
	%{_includedir}/atlas-%{_arch}-sse2 %{pr_sse2}
fi

%preun		-n %{devname_sse2}
if [ $1 -ge 0 ] ; then
	/usr/sbin/alternatives --remove atlas-devel				\
	%{_includedir}/atlas-%{_arch}-sse2
fi

%files	-n %{devname_sse2}
%doc doc
%{_libdir}/atlas-sse2/*.so
%{_includedir}/atlas-%{_arch}-sse2/
%{_includedir}/*.h
%ghost %{_includedir}/atlas

#-----------------------------------------------------------------------

%package	-n %{libname_sse3}
Summary:	ATLAS libraries for SSE3 extensions
Provides:	%{libatlas} = %{version}-%{release}

%description	-n %{libname_sse3}
This package contains ATLAS (Automatically Tuned Linear Algebra Software)
headers for libraries compiled with optimizations for the SSE3 extensions
to the ix86 architecture.

%files		-n %{libname_sse3}
%doc doc/README.dist
%dir %{_libdir}/atlas-sse3
%{_libdir}/atlas-sse3/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-sse3.conf

#-----------------------------------------------------------------------

%package	-n %{devname_sse3}
Summary:	Development files for ATLAS SSE3
Requires(posttrans):	update-alternatives
Requires(preun):	update-alternatives

%description	-n %{devname_sse3}
This package contains ATLAS (Automatically Tuned Linear Algebra Software)
headers for libraries compiled with optimizations for the SSE3 extensions
to the ix86 architecture.

%posttrans	-n %{devname_sse3}
if [ $1 -eq 0 ] ; then
	/usr/sbin/alternatives --install %{_includedir}/atlas atlas-devel	\
	%{_includedir}/atlas-%{_arch}-sse3 %{pr_sse3}
fi

%preun		-n %{devname_sse3}
if [ $1 -ge 0 ] ; then
	/usr/sbin/alternatives --remove atlas-devel				\
	%{_includedir}/atlas-%{_arch}-sse3
fi

%files		-n %{devname_sse3}
%doc doc
%{_libdir}/atlas-sse3/*.so
%{_includedir}/atlas-%{_arch}-sse3/
%{_includedir}/*.h
%ghost %{_includedir}/atlas

#-----------------------------------------------------------------------
%endif
%endif

########################################################################

%ifarch %{arm}
#beware - arch constant can change between releases
%define arch_option -A 46
%define threads_option -t 2
%global armflags -DATL_ARM_HARDFP=1
%global mode %{nil}
%else
%global mode -b %{__isa_bits}
%global armflags %{nil}
%if "%{?enable_native_atlas}" == "0"
%define threads_option -t 4
%endif
%endif

########################################################################

%prep
%setup -q -n ATLAS
#% ifarch s390 s390x
#% patch1 -p1 -b .s390
#% endif
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
for type in %{types}; do
	if [ "$type" = "base" ]; then
		libname=atlas
	else
		libname=atlas-${type}
	fi

	mkdir -p %{_arch}_${type}
	pushd %{_arch}_${type}
	../configure %{mode} %{?threads_option} %{?arch_option} -D c -DWALL -Fa alg '%{armflags} -g -Wa,--noexecstack -fPIC'\
	--cc=gcc					\
	--prefix=%{buildroot}%{_prefix}			\
	--incdir=%{buildroot}%{_includedir}		\
	--libdir=%{buildroot}%{_libdir}/${libname}	\
	--with-netlib-lapack-tarfile=%{SOURCE10}

%if "%{?enable_native_atlas}" == "0"
cat Make.inc # enable fof debug only
%ifarch x86_64 znver1
	if [ "$type" = "base" ]; then
#		sed -i 's#ARCH =.*#ARCH = HAMMER64SSE2#' Make.inc
		sed -i 's#ARCH =.*#ARCH = HAMMER64SSE3#' Make.inc
#		sed -i 's#-DATL_SSE3##' Make.inc
		sed -i 's#-DATL_AVX##' Make.inc
#		sed -i 's#-msse3#-msse2#' Make.inc
#		sed -i 's#-mavx#-msse3#' Make.inc
		sed -i 's#-mavx[0-9].*#-msse3#' Make.inc
		sed -i 's#-mavx#-msse3#' Make.inc
		sed -i 's#MAC##' Make.inc
		echo 'base makefile edited'
#		sed -i 's#PMAKE = $(MAKE) .*#PMAKE = $(MAKE) -j 1#' Make.inc
	elif [ "$type" = "sse3" ]; then
#		sed -i 's#ARCH =.*#ARCH = Corei264AVX#' Make.inc
#		sed -i 's#PMAKE = $(MAKE) .*#PMAKE = $(MAKE) -j 1#' Make.inc
		sed -i 's#-DATL_AVX##' Make.inc
		sed -i 's#-DATL_SSE2##' Make.inc
		sed -i 's#-mavx[0-9].*#-msse2#' Make.inc
		sed -i 's#-mavx#-msse2#' Make.inc
		sed -i 's#-msse3#-msse2#' Make.inc
		echo 'sse makefile edited'
	fi
%endif

%ifarch %{ix86}
	if [ "$type" = "base" ]; then
		sed -i 's#ARCH =.*#ARCH = PPRO32#' Make.inc
		#sed -i 's#-DATL_SSE3 -DATL_SSE2 -DATL_SSE1##' Make.inc
		sed -i 's#-DATL_SSE3##' Make.inc
		sed -i 's#-DATL_SSE2##' Make.inc
		sed -i 's#-DATL_SSE1##' Make.inc
		sed -i 's#-mfpmath=sse -msse3#-mfpmath=387#' Make.inc
	elif [ "$type" = "sse" ]; then
		sed -i 's#ARCH =.*#ARCH = PIII32SSE1#' Make.inc
		sed -i 's#-DATL_SSE3#-DATL_SSE1#' Make.inc
		sed -i 's#-msse3#-msse#' Make.inc
	elif [ "$type" = "sse2" ]; then
#		sed -i 's#ARCH =.*#ARCH = P432SSE2#' Make.inc
		sed -i 's#ARCH =.*#ARCH = x86SSE232SSE2#' Make.inc
		sed -i 's#-DATL_SSE3#-DATL_SSE2#' Make.inc
		sed -i 's#-msse3#-msse2#' Make.inc
	elif [ "$type" = "sse3" ]; then
		sed -i 's#ARCH =.*#ARCH = P4E32SSE3#' Make.inc
	fi
%endif


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

