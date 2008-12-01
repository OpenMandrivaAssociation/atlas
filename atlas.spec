%define name	atlas
%define version	3.6.0
%define release	5

%define major		3
%define lapack_major 	%{major}
%define lapack_ver   	%{major}.2
%define	libname_orig	lib%{name}
%define libname	%mklibname %name %{major}

Name:           %{name}
Version:        %{version}
Release:        %mkrel %{release}
Summary:        Automatically Tuned Linear Algebra Software
Group:          Sciences/Mathematics
License:        BSD
URL:            http://math-atlas.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/math-atlas/%{name}%{version}.tar.bz2
Source1:        README.Fedora
Patch0:         http://ftp.debian.org/debian/pool/main/a/atlas/%{name}_%{version}-22.diff.gz
Patch1:         %{name}-%{version}-gfortran.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:       /etc/ld.so.conf.d
BuildRequires:  gcc-gfortran, lapack-devel, expect, sed, sharutils

%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

The performance improvements in ATLAS are obtained largely via
compile-time optimizations and tend to be specific to a given hardware
configuration. In order to package ATLAS for Mandriva some compromises
are necessary so that good performance can be obtained on a variety
of hardware. This set of ATLAS binary packages is therefore not
necessarily optimal for any specific hardware configuration.  However,
the source package can be used to compile customized ATLAS packages;
see the documentation for information.

%package -n %{libname}
Summary:        ATLAS shared libraries
Group:          Sciences/Mathematics
Provides:   	%{libname_orig} = %{version}-%{release}
Provides:   	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the shared libraries for programs linked against 
ATLAS (Automatically Tuned Linear Algebra Software).

%package -n %{libname}-devel
Summary:        Development libraries for ATLAS
Group:          Sciences/Mathematics
Requires:       %{libname} = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
This package contains the static libraries and headers for development
with ATLAS (Automatically Tuned Linear Algebra Software).

############## Subpackages for architecture extensions #################
#
# Because a set of ATLAS libraries is a ~5 MB package, separate packages
# are created for SSE, SSE2, and 3DNow extensions to ix86 and AltiVec
# extensions to PowerPC.

%ifarch i586
%define archt i386
%define types base sse sse2 3dnow

%package -n %{libname}-sse
Summary:        ATLAS libraries for SSE extensions
Group:          Sciences/Mathematics
Provides:   	%{libname_orig}-sse = %{version}-%{release}
Provides:   	%{name}-sse = %{version}-%{release}

%description -n %{libname}-sse
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the SSE extensions
to the ix86 architecture.

%package -n %{libname}-sse-devel
Summary:        Development libraries for ATLAS with SSE extensions
Group:          Sciences/Mathematics
Requires:       %{libname}-sse = %{version}-%{release}
Provides:	%{libname_orig}-sse-devel = %{version}-%{release}
Provides:	%{name}-sse-devel = %{version}-%{release}

%description -n %{libname}-sse-devel
This package contains headers and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the SSE extensions to the ix86 architecture.


%package -n %{libname}-sse2
Summary:        ATLAS libraries for SSE2 extensions
Group:          Sciences/Mathematics
Provides:   	%{libname_orig}-sse2 = %{version}-%{release}
Provides:   	%{name}-sse2 = %{version}-%{release}

%description -n %{libname}-sse2
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the SSE2
extensions to the ix86 architecture.

%package -n %{libname}-sse2-devel
Summary:        Development libraries for ATLAS with SSE2 extensions
Group:          Sciences/Mathematics
Requires:       %{libname}-sse2 = %{version}-%{release}
Provides:	%{libname_orig}-sse2-devel = %{version}-%{release}
Provides:	%{name}-sse2-devel = %{version}-%{release}

%description -n %{libname}-sse2-devel
This package contains headers and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the SSE2 extensions to the ix86 architecture.

%package -n %{libname}-3dnow
Summary:        ATLAS libraries for 3DNow extensions
Group:          Sciences/Mathematics
Provides:   	%{libname_orig}-3dnow = %{version}-%{release}
Provides:   	%{name}-3dnow = %{version}-%{release}

%description -n %{libname}-3dnow
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the 3DNow
extensions to the ix86 architecture.

%package -n %{libname}-3dnow-devel
Summary:        Development libraries for ATLAS with 3DNow extensions
Group:         	Sciences/Mathematics
Requires:       %{libname}-3dnow = %{version}-%{release}
Provides:	%{libname_orig}-3dnow-devel = %{version}-%{release}
Provides:	%{name}-3dnow-devel = %{version}-%{release}

%description -n %{libname}-3dnow-devel
This package contains headers and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the 3DNow extensions to the ix86 architecture.

%endif # %ifarch i586

%ifarch ppc
%define archt powerpc
%define types base altivec

%package -n %{libname}-altivec
Summary:        ATLAS libraries for AltiVec extensions
Group:          Science/Mathematics
Provides:   	%{libname_orig}-altivec = %{version}-%{release}
Provides:   	%{name}-altivec = %{version}-%{release}

%description -n %{libname}-altivec
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the AltiVec
extensions to the PowerPC architecture.

%package -n %{libname}-altivec-devel
Summary:        Development libraries for ATLAS with AltiVec extensions
Group:          Science/Mathematics
Requires:       %{libname}-altivec = %{version}-%{release}
Provides:	%{libname_orig}-altivec-devel = %{version}-%{release}
Provides:	%{name}-altivec-devel = %{version}-%{release}

%description -n %{libname}-altivec-devel
This package contains headers and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
optimizations for the AltiVec extensions to the PowerPC architecture.

%endif
%ifarch x86_64
%define archt amd64
%define types base
%define bit 2
%else
%define bit 1
%endif

%if "%{?enable_custom_atlas}" == "1"
# This flag enables building customized ATLAS libraries with all
# compile-time optimizations. Note that compilation will take a very
# long time, and that the resulting binaries are not guaranteed to
# work well or even at all on other hardware.

%define archt %{_arch}
%define types custom

%package -n %{libname}-custom
Summary:        Custom-compiled ATLAS libraries
Group:          Science/Mathematics
Provides:   	%{libname_orig}-custom = %{version}-%{release}
Provides:   	%{name}-custom = %{version}-%{release}

%description -n %{libname}-custom
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with all compile-time optimizations enabled.

%package -n %{libname}-custom-devel
Summary:        Custom-compiled development libraries for ATLAS
Group:          Science/Mathematics
Requires:       %{libname}-custom = %{version}-%{release}
Provides:	%{libname_orig}-custom-devel = %{version}-%{release}
Provides:	%{name}-custom-devel = %{version}-%{release}

%description -n %{libname}-custom-devel
This package contains headers and static versions of the ATLAS
(Automatically Tuned Linear Algebra Software) libraries compiled with
all compile-time optimizations enabled.
%endif # %if "%{?enable_custom_atlas}" == "1"


%prep
%setup -q -n ATLAS
zcat %{PATCH0} | sed -e s,gcc-4.3,gcc,g | sed -e s,gfortran-4.3,gfortran,g | patch -p1
%patch1 -p0
cp %{SOURCE1} doc


%build

# The following build procedure is more or less copied from the Debian
# sources, where the output of a previously recorded build is
# replayed, so as to bypass the compile-time optimizations and produce
# predictable results independent of the hardware on which it is
# compiled. This forces builds to be sequential, so SMP builds are not
# supported.
chmod +x debian/config.expect debian/ab
sed -i debian/ab -e "s,g77,gfortran,"

########## Static Libraries ##########################################
for TYPE in %{types}; do
  if [ "$TYPE" = "3dnow" ]; then
    TDN=y
  else
    TDN=n
  fi
  BUILD_DIR=Linux_${TYPE}_static
  ARCH_DIR=$BUILD_DIR CACHE_SIZE= BIT=%{bit} \
    DEFAULTS=y TDNCOMP=$TDN debian/config.expect
  cat Make.$BUILD_DIR |\
	sed -e "s, TOPdir = \(.*\), TOPdir = `pwd`,1" \
	    -e "s, FLAPACKlib = , FLAPACKlib = %{_libdir}/liblapack.a,1" >foo
  mv foo Make.$BUILD_DIR
  make killall arch=$BUILD_DIR
  make startup arch=$BUILD_DIR

  # Use existing custom ATLAS build data residing in 
  # SOURCE/atlas-custom-%{archt} if it exists:
  if [ "$TYPE" = "custom" ]; then
    BUILD_DATA_DIR=atlas-$TYPE-%{archt}
    if [ -a %{_sourcedir}/$BUILD_DATA_DIR.tgz ]; then
      tar zxf %{_sourcedir}/$BUILD_DATA_DIR.tgz
    else
      make install arch=$BUILD_DIR >out 2>&1 &
      pid=$!
      echo Waiting on $pid
      tail -f --pid $pid out &
      wait $pid
      rm -rf ${BUILD_DATA_DIR}
      mkdir -p ${BUILD_DATA_DIR}
      cat out | sed -e "s,`pwd`,TOPDIR,g" -e "s,$BUILD_DIR,CARCH,g" | \
		gzip -9 | uuencode - >${BUILD_DATA_DIR}/build.uu
      rm -f out
      mkdir -p ${BUILD_DATA_DIR}/include
      cp include/$BUILD_DIR/* ${BUILD_DATA_DIR}/include
      mkdir -p ${BUILD_DATA_DIR}/mm
      cp tune/blas/gemm/$BUILD_DIR/res/* ${BUILD_DATA_DIR}/mm
      mkdir -p ${BUILD_DATA_DIR}/mv
      cp tune/blas/gemv/$BUILD_DIR/res/* ${BUILD_DATA_DIR}/mv
      mkdir -p ${BUILD_DATA_DIR}/r1
      cp tune/blas/ger/$BUILD_DIR/res/* ${BUILD_DATA_DIR}/r1
      mkdir -p ${BUILD_DATA_DIR}/l1
      cp tune/blas/level1/$BUILD_DIR/res/* ${BUILD_DATA_DIR}/l1
      tar zcf %{_sourcedir}/${BUILD_DATA_DIR}.tgz ${BUILD_DATA_DIR}
    fi
  else
    BUILD_DATA_DIR=debian/%{archt}/${TYPE}
  fi

  cp ${BUILD_DATA_DIR}/mm/* tune/blas/gemm/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/mv/* tune/blas/gemv/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/r1/* tune/blas/ger/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/l1/* tune/blas/level1/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/include/* include/$BUILD_DIR

  cat ${BUILD_DATA_DIR}/build.uu | uudecode | zcat - | \
	sed -e "s,g77,gfortran," -e "s,-DAdd__,-DAdd_," | debian/ab topdir=`pwd` \
	carch=$BUILD_DIR fpic="-Wa,--noexecstack" debug= | bash -x -e
  mv lib/$BUILD_DIR/liblapack.a lib/$BUILD_DIR/liblapack_atlas.a

  # Create replacement for BLAS and LAPACK Libraries
  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/libatlas.a
    ar x ../lib/$BUILD_DIR/libf77blas.a
    ar x ../lib/$BUILD_DIR/libcblas.a
  popd
  rm -f lib/$BUILD_DIR/libblas.a
  ar r lib/$BUILD_DIR/libblas.a tmp/*.o
  rm -rf tmp

  mkdir tmp
  pushd tmp
    ar x %{_libdir}/liblapack.a
    ar x ../lib/$BUILD_DIR/liblapack_atlas.a
    ar x ../lib/$BUILD_DIR/libcblas.a
  popd
  rm -f lib/$BUILD_DIR/liblapack.a
  ar r lib/$BUILD_DIR/liblapack.a tmp/*.o
  rm -rf tmp

  ########## Shared Libraries ##########################################
  BUILD_DIR=Linux_${TYPE}_shared
  ARCH_DIR=$BUILD_DIR CACHE_SIZE= BIT=%{bit} \
      DEFAULTS=y TDNCOMP=$TDN debian/config.expect
  cat Make.$BUILD_DIR |\
	sed -e "s, TOPdir = \(.*\), TOPdir = `pwd`,1" \
	    -e "s, FLAPACKlib = , FLAPACKlib = %{_libdir}/liblapack_pic.a,1" \
	    -e "s, F77FLAGS = \(.*\), F77FLAGS = \1 -fPIC,1" \
	    -e "s, CCFLAGS = \(.*\), CCFLAGS = \1 -fPIC,1" \
	    -e "s, MMFLAGS = \(.*\), MMFLAGS = \1 -fPIC,1" \
	    -e "s, XCCFLAGS = \(.*\), XCCFLAGS = \1 -fPIC,1" >foo
  mv foo Make.$BUILD_DIR
  make killall arch=$BUILD_DIR
  make startup arch=$BUILD_DIR

  cp ${BUILD_DATA_DIR}/mm/* tune/blas/gemm/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/mv/* tune/blas/gemv/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/r1/* tune/blas/ger/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/l1/* tune/blas/level1/$BUILD_DIR/res
  cp ${BUILD_DATA_DIR}/include/* include/$BUILD_DIR

  cat ${BUILD_DATA_DIR}/build.uu | uudecode | zcat - | \
	sed -e "s,g77,gfortran," -e "s,-DAdd__,-DAdd_," | debian/ab topdir=`pwd` \
	carch=$BUILD_DIR fpic="-Wa,--noexecstack -fPIC" debug= | bash -x -e
  mv lib/$BUILD_DIR/liblapack.a lib/$BUILD_DIR/liblapack_atlas.a

  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/libatlas.a
    rm -f ilaenv.o
  popd
  cc -shared -Wl,-soname=libatlas.so.%{lapack_major} \
	-o lib/$BUILD_DIR/libatlas.so.%{lapack_ver} tmp/*.o -lm
  ln -s libatlas.so.%{lapack_ver} lib/$BUILD_DIR/libatlas.so.%{lapack_major}
  ln -s libatlas.so.%{lapack_ver} lib/$BUILD_DIR/libatlas.so
  rm -rf tmp

  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/libcblas.a
    rm -f ilaenv.o
  popd
  cc -shared -Wl,-soname=libcblas.so.%{lapack_major} \
	-o lib/$BUILD_DIR/libcblas.so.%{lapack_ver} tmp/*.o -L lib/$BUILD_DIR -latlas
  ln -s libcblas.so.%{lapack_ver} lib/$BUILD_DIR/libcblas.so.%{lapack_major}
  ln -s libcblas.so.%{lapack_ver} lib/$BUILD_DIR/libcblas.so
  rm -rf tmp

  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/libf77blas.a
    rm -f ilaenv.o
  popd
  cc -shared -Wl,-soname=libf77blas.so.%{lapack_major} \
	-o lib/$BUILD_DIR/libf77blas.so.%{lapack_ver} tmp/*.o \
	-L lib/$BUILD_DIR -latlas -lgfortran
  ln -s libf77blas.so.%{lapack_ver} lib/$BUILD_DIR/libf77blas.so.%{lapack_major}
  ln -s libf77blas.so.%{lapack_ver} lib/$BUILD_DIR/libf77blas.so
  rm -rf tmp

  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/liblapack_atlas.a
    rm -f ilaenv.o
  popd
  cc -shared -Wl,-soname=liblapack_atlas.so.%{lapack_major} \
	-o lib/$BUILD_DIR/liblapack_atlas.so.%{lapack_ver} tmp/*.o \
	-L lib/$BUILD_DIR -lcblas -lf77blas
  ln -s liblapack_atlas.so.%{lapack_ver} lib/$BUILD_DIR/liblapack_atlas.so.%{lapack_major}
  ln -s liblapack_atlas.so.%{lapack_ver} lib/$BUILD_DIR/liblapack_atlas.so
  rm -rf tmp

  # Create replacement for BLAS and LAPACK Libraries
  mkdir tmp
  pushd tmp
    ar x ../lib/$BUILD_DIR/libatlas.a
    ar x ../lib/$BUILD_DIR/libf77blas.a
    ar x ../lib/$BUILD_DIR/libcblas.a
  popd
  cc -shared -Wl,-soname=libblas.so.%{lapack_major} \
	-o lib/$BUILD_DIR/libblas.so.%{lapack_ver} tmp/*.o -lgfortran
  ln -s libblas.so.%{lapack_ver} lib/$BUILD_DIR/libblas.so.%{lapack_major}
  ln -s libblas.so.%{lapack_ver} lib/$BUILD_DIR/libblas.so
  rm -rf tmp

  mkdir tmp
  pushd tmp
    ar x %{_libdir}/liblapack_pic.a
    ar x ../lib/$BUILD_DIR/liblapack_atlas.a
    ar x ../lib/$BUILD_DIR/libcblas.a
  popd
  cc -shared -Wl,-soname=liblapack.so.%{lapack_major} \
	-o lib/$BUILD_DIR/liblapack.so.%{lapack_ver} tmp/*.o \
	-L lib/$BUILD_DIR -lblas -lgfortran
  ln -s liblapack.so.%{lapack_ver} lib/$BUILD_DIR/liblapack.so.%{lapack_major}
  ln -s liblapack.so.%{lapack_ver} lib/$BUILD_DIR/liblapack.so
  rm -rf tmp
done

%install
%__rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
mkdir -p $RPM_BUILD_ROOT%{_includedir}/atlas
cp -a include/*.h $RPM_BUILD_ROOT%{_includedir}/atlas

LIBNAMES="libatlas libcblas libf77blas liblapack_atlas libblas liblapack"
for TYPE in %{types}; do
  if [ "$TYPE" = "base" ]; then
    EXTDIR="atlas"
    echo "%{_libdir}/atlas" \
      > $RPM_BUILD_ROOT/etc/ld.so.conf.d/atlas-%{_arch}.conf
  elif [ "$TYPE" = "custom" ]; then
    EXTDIR="atlas-custom"
    echo "%{_libdir}/atlas-custom" \
      > $RPM_BUILD_ROOT/etc/ld.so.conf.d/atlas-custom-%{_arch}.conf
  else
    EXTDIR=$TYPE
    echo "/usr/lib/$TYPE" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/atlas-$TYPE.conf
  fi

  mkdir -p $RPM_BUILD_ROOT%{_libdir}/${EXTDIR}
  for LIB in $LIBNAMES; do
    LIBS="lib/Linux_${TYPE}_static/$LIB.a lib/Linux_${TYPE}_shared/$LIB.so*"
    cp -a $LIBS ${RPM_BUILD_ROOT}%{_libdir}/${EXTDIR}
  done
done

%clean
%__rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%ifarch i586

%if %mdkversion < 200900
%post -n %{libname}-sse -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname}-sse -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libname}-sse2 -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname}-sse2 -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libname}-3dnow -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname}-3dnow -p /sbin/ldconfig
%endif

%endif
%ifarch ppc

%if %mdkversion < 200900
%post -n %{libname}-altivec -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname}-altivec -p /sbin/ldconfig
%endif

%endif
%if "%{?enable_custom_atlas}" == "1"

%if %mdkversion < 200900
%post -n %{libname}-custom -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname}-custom -p /sbin/ldconfig
%endif

%files -n %{libname}-custom
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/atlas-custom
%{_libdir}/atlas-custom/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-custom-%{_arch}.conf

%files -n %{libname}-custom-devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%dir %{_libdir}/atlas-custom
%{_libdir}/atlas-custom/*.so
%{_libdir}/atlas-custom/*.a
%{_includedir}/atlas

%else

%files -n %{libname}
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/atlas
%{_libdir}/atlas/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}.conf

%files -n %{libname}-devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%{_libdir}/atlas/*.so
%{_libdir}/atlas/*.a
%{_includedir}/atlas

%ifarch i586

%files -n %{libname}-sse
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/sse
%{_libdir}/sse/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-sse.conf

%files -n %{libname}-sse-devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%dir %{_libdir}/sse
%{_libdir}/sse/*.so
%{_libdir}/sse/*.a
%{_includedir}/atlas


%files -n %{libname}-sse2
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/sse2
%{_libdir}/sse2/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-sse2.conf

%files -n %{libname}-sse2-devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%dir %{_libdir}/sse2
%{_libdir}/sse2/*.so
%{_libdir}/sse2/*.a
%{_includedir}/atlas


%files -n %{libname}-3dnow
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/3dnow
%{_libdir}/3dnow/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-3dnow.conf

%files -n %{libname}-3dnow-devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%dir %{_libdir}/3dnow
%{_libdir}/3dnow/*.so
%{_libdir}/3dnow/*.a
%{_includedir}/atlas

%endif # %ifarch i586
%ifarch ppc

%files -n %{libname}-altivec
%defattr(-,root,root,-)
%doc debian/copyright doc/README.Fedora
%dir %{_libdir}/altivec
%{_libdir}/altivec/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-altivec.conf

%files -n %{libname}-altivec-devel
%defattr(-,root,root,-)
%doc debian/copyright doc
%dir %{_libdir}/altivec
%{_libdir}/altivec/*.so
%{_libdir}/altivec/*.a
%{_includedir}/atlas

%endif # %ifarch ppc

%endif # %if "%{?enable_custom_atlas}" == "1"

