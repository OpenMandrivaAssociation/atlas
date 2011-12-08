# Based on fedora package:
# http://pkgs.fedoraproject.org/gitweb/?p=atlas.git;a=tree

%bcond_with		custom_atlas

%define name		atlas
%define major		3
%define libatlas	libatlas
%define libname		%mklibname %{name} %{major}

Name:		%{name}
Version:	3.8.4
Release:	%mkrel 3
Summary:        Automatically Tuned Linear Algebra Software
Group:          Sciences/Mathematics
License:        BSD
URL:            http://math-atlas.sourceforge.net/
Source0:	http://downloads.sourceforge.net/math-atlas/atlas%{version}.tar.bz2
Source1:	http://math-atlas.sourceforge.net/errata.html
Source2:	http://math-atlas.sourceforge.net/faq.html
Source3:	http://www.cs.utsa.edu/~whaley/papers.html
Source4:	Makefile
Source5:	README.mandriva

Patch0:		atlas-fedora_shared.patch

Conflicts:	%{libname}-custom < %{version}-%{release}
Conflicts:	%{libatlas}-custom-devel < %{version}-%{release}
%ifarch %{ix86}
Conflicts:	%{libname}-sse < %{version}-%{release}
Conflicts:	%{libatlas}-sse-devel < %{version}-%{release}
%endif
%ifarch %{ix86} x86_64
Conflicts:	%{libname}-sse2 < %{version}-%{release}
Conflicts:	%{libatlas}-sse2-devel < %{version}-%{release}
Conflicts:	%{libname}-sse3 < %{version}-%{release}
Conflicts:	%{libatlas}-sse3-devel < %{version}-%{release}
%endif
%ifnarch %{ix86} x86_64
Conflicts:	%{libname}-%{_arch} < %{version}-%{release}
Conflicts:	%{libatlas}-%{_arch}-devel < %{version}-%{release}
%endif

Requires(post):	update-alternatives
Requires(postun): update-alternatives

Requires:	gcc-gfortran liblapack-devel make
BuildRequires:	gcc-gfortran
# ensure it has a pic liblapack.a
BuildRequires:	lapack-devel > 3.3.1-1

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

The performance improvements in ATLAS are obtained largely via
compile-time optimizations and tend to be specific to a given hardware
configuration.

########################################################################
%if %{with custom_atlas}
%define types	custom
%define mode	%(gcc -dumpmachine | perl -e '$_ = <>; if (/^i.86-/) { print 32; } elsif (/[^-]+64-/) { print 64; } else { print 32; }')
%package	-n %{libname}-custom
Summary:	Custom ATLAS libraries
Group:		Development/Other
Conflicts:	%{libatlas}-custom-devel < %{version}-%{release}
%ifarch %{ix86}
Conflicts:	%{libname}-sse < %{version}-%{release}
Conflicts:	%{libatlas}-sse-devel < %{version}-%{release}
%endif
%ifarch %{ix86} x86_64
Conflicts:	%{libname}-sse2 < %{version}-%{release}
Conflicts:	%{libatlas}-sse2-devel < %{version}-%{release}
Conflicts:	%{libname}-sse3 < %{version}-%{release}
Conflicts:	%{libatlas}-sse3-devel < %{version}-%{release}
%endif
%ifnarch %{ix86} x86_64
Conflicts:	%{libname}-%{_arch} < %{version}-%{release}
Conflicts:	%{libatlas}-%{_arch}-devel < %{version}-%{release}
%endif
Conflicts:	atlas < %{version}-%{release}
Requires(post):	update-alternatives
Requires(postun): update-alternatives

%description	-n %{libname}-custom
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with custom optimizations.

%posttrans	-n %{libname}-custom
update-alternatives							\
    --install %{_libdir}/atlas atlas %{_libdir}/atlas-custom 4		\
    --slave %{_sysconfdir}/ld.so.conf.d/atlas.conf atlas-conf %{_libdir}/atlas-custom/atlas.conf
/sbin/ldconfig

%postun		-n %{libname}-custom
if [ $1 -eq 0 ]; then
    update-alternatives --remove atlas %{_libdir}/atlas-custom
    /sbin/ldconfig
fi

%files		-n %{libname}-custom
%defattr(-,root,root,-)
%dir %{_libdir}/atlas-custom
%{_libdir}/atlas-custom/*.so.*
%{_libdir}/atlas-custom/atlas.conf

%package	-n %{libatlas}-custom-devel
Summary:	Custom development files for ATLAS
Group:		Development/Other
Requires:	%{libname}-custom = %{version}-%{release}
Requires(post):	update-alternatives
Requires(postun): update-alternatives

%description	-n %{libatlas}-custom-devel
This package contains headers and development libraries of ATLAS
(Automatically Tuned Linear Algebra Software) compiled with custom
optimizations.

%posttrans	-n %{libatlas}-custom-devel
update-alternatives							\
    --install %{_includedir}/atlas atlas-devel %{_includedir}/atlas-custom 4 \
    --slave %{_includedir}/cblas.h cblas.h %{_includedir}/atlas-custom/cblas.h \
    --slave %{_includedir}/clapack.h clapack.h %{_includedir}/atlas-custom/clapack.h
/sbin/ldconfig

%postun		-n %{libatlas}-custom-devel
if [ $1 -eq 0 ]; then
    update-alternatives --remove atlas-devel %{_includedir}/atlas-custom
    /sbin/ldconfig
fi

%files		-n %{libatlas}-custom-devel
%defattr(-,root,root,-)
%doc doc/*
%{_libdir}/atlas-custom/*.a
%{_libdir}/atlas-custom/*.so
%{_includedir}/atlas-custom/

########################################################################
# with custom_atlas
%else

  %define mode		32
  %define types		%{_arch}
  %ifarch %{ix86}
    %define types	sse sse2 sse3
  %else
    %ifarch x86_64
      %define types	sse2 sse3
      %define mode	64
    %else
      %ifarch ppc64
        %define mode	64
      %endif
    %endif
  %endif

#--#####################################################################
  %ifarch %{ix86}
#----###################################################################
%package	-n %{libname}-sse
Summary:	ATLAS libraries for SSE extensions (Pentium III)
Group:		System/Libraries
Obsoletes:	%mklibname %{name}3.0-sse
Obsoletes:	%mklibname %{name}3.0-3dnow
Obsoletes:	%mklibname %{name}%{major}-3dnow
Conflicts:	%{libname}-custom < %{version}-%{release}
Conflicts:	%{libatlas}-custom-devel < %{version}-%{release}
Conflicts:	%{libatlas}-sse-devel < %{version}-%{release}
Conflicts:	%{libname}-sse2 < %{version}-%{release}
Conflicts:	%{libatlas}-sse2-devel < %{version}-%{release}
Conflicts:	atlas < %{version}-%{release}
Requires(post):	update-alternatives
Requires(postun): update-alternatives

%description	-n %{libname}-sse
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with SSE optimizations (Pentium III).
This is a generic binary package. Install the "%{name}" package
to build a version tuned for your computer.

%posttrans	-n %{libname}-sse
update-alternatives							\
    --install %{_libdir}/atlas atlas %{_libdir}/atlas-sse 1		\
    --slave %{_sysconfdir}/ld.so.conf.d/atlas.conf atlas-conf %{_libdir}/atlas-sse/atlas.conf
/sbin/ldconfig

%postun		-n %{libname}-sse
if [ $1 -eq 0 ]; then
    update-alternatives --remove atlas %{_libdir}/atlas-sse
    /sbin/ldconfig
fi

%files		-n %{libname}-sse
%defattr(-,root,root,-)
%dir %{_libdir}/atlas-sse
%{_libdir}/atlas-sse/*.so.*
%{_libdir}/atlas-sse/atlas.conf

#------#################################################################
%package	-n %{libatlas}-sse-devel
Summary:	Development files for ATLAS SSE (Pentium III)
Group:		Development/Other
Requires:	%{libname}-sse = %{version}-%{release}
Obsoletes:	%mklibname -d %{name}3.0-sse
Obsoletes:	%mklibname -d %{name}3.0-3dnow
Obsoletes:	%mklibname -d %{name}%{major}-3dnow
Requires(post):	update-alternatives
Requires(postun): update-alternatives

%description	-n %{libatlas}-sse-devel
This package contains headers and development libraries of ATLAS
(Automatically Tuned Linear Algebra Software) compiled with SSE
optimizations (Pentium III).

%posttrans	-n %{libatlas}-sse-devel
update-alternatives							\
    --install %{_includedir}/atlas atlas-devel %{_includedir}/atlas-sse 1 \
    --slave %{_includedir}/cblas.h cblas.h %{_includedir}/atlas-sse/cblas.h \
    --slave %{_includedir}/clapack.h clapack.h %{_includedir}/atlas-sse/clapack.h
/sbin/ldconfig

%postun		-n %{libatlas}-sse-devel
if [ $1 -eq 0 ]; then
    update-alternatives --remove atlas-devel %{_includedir}/atlas-sse
    /sbin/ldconfig
fi

%files		-n %{libatlas}-sse-devel
%defattr(-,root,root,-)
%doc doc/*
%{_libdir}/atlas-sse/*.a
%{_libdir}/atlas-sse/*.so
%{_includedir}/atlas-sse/

# ifarch ix86
  %endif

#--#####################################################################
  %ifarch %{ix86} x86_64
#----###################################################################
%package	-n %{libname}-sse2
Summary:	ATLAS libraries for SSE2 extensions
Group:		System/Libraries
%ifarch %{ix86}
Obsoletes:	%mklibname %{name}3.0-sse2
%else
Obsoletes:	%{libname}-x86_64
%endif
Provides:	%{libatlas} = %{version}-%{release}
Conflicts:	%{libname}-custom < %{version}-%{release}
Conflicts:	%{libatlas}-custom-devel < %{version}-%{release}
%ifnarch x86_64
Conflicts:	%{libname}-sse < %{version}-%{release}
Conflicts:	%{libatlas}-sse-devel < %{version}-%{release}
%endif
Conflicts:	%{libatlas}-sse2-devel < %{version}-%{release}
Conflicts:	%{libname}-sse3 < %{version}-%{release}
Conflicts:	%{libatlas}-sse3-devel < %{version}-%{release}
Conflicts:	atlas < %{version}-%{release}
Requires(post):	update-alternatives
Requires(postun): update-alternatives

%description	-n %{libname}-sse2
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with SSE2 optimizations.
This is a generic binary package. Install the "%{name}" package
to build a version tuned for your computer.

%posttrans	-n %{libname}-sse2
update-alternatives							\
    --install %{_libdir}/atlas atlas %{_libdir}/atlas-sse2 2		\
    --slave %{_sysconfdir}/ld.so.conf.d/atlas.conf atlas-conf %{_libdir}/atlas-sse2/atlas.conf
/sbin/ldconfig

%postun		-n %{libname}-sse2
if [ $1 -eq 0 ]; then
    update-alternatives --remove atlas %{_libdir}/atlas-sse2
    /sbin/ldconfig
fi

%files		-n %{libname}-sse2
%defattr(-,root,root,-)
%dir %{_libdir}/atlas-sse2
%{_libdir}/atlas-sse2/*.so.*
%{_libdir}/atlas-sse2/atlas.conf

#------#################################################################
%package	-n %{libatlas}-sse2-devel
Summary:	Development files for ATLAS SSE2
Group:		Development/Other
Requires:	%{libname}-sse2 = %{version}-%{release}
Provides:	%{libatlas}-devel = %{version}-%{release}
%ifarch x86_64
Obsoletes:	%{libatlas}-x86_64-devel
%endif
Requires(post):	update-alternatives
Requires(postun): update-alternatives

%description	-n %{libatlas}-sse2-devel
This package contains headers and development libraries of ATLAS
(Automatically Tuned Linear Algebra Software) compiled with SSE2
optimizations.

%posttrans	-n %{libatlas}-sse2-devel
update-alternatives							\
    --install %{_includedir}/atlas atlas-devel %{_includedir}/atlas-sse2 2 \
    --slave %{_includedir}/cblas.h cblas.h %{_includedir}/atlas-sse2/cblas.h \
    --slave %{_includedir}/clapack.h clapack.h %{_includedir}/atlas-sse2/clapack.h
    /sbin/ldconfig

%postun		-n %{libatlas}-sse2-devel
if [ $1 -eq 0 ]; then
    update-alternatives --remove atlas-devel %{_includedir}/atlas-sse2
    /sbin/ldconfig
fi

%files		-n %{libatlas}-sse2-devel
%defattr(-,root,root,-)
%doc doc/*
%{_libdir}/atlas-sse2/*.a
%{_libdir}/atlas-sse2/*.so
%{_includedir}/atlas-sse2/

#----###################################################################
%package	-n %{libname}-sse3
Summary:	ATLAS libraries for SSE3 extensions
Group:		System/Libraries
Provides:	%{libatlas} = %{version}-%{release}
%ifarch x86_64
Obsoletes:	%{libname}-x86_64
%endif
Conflicts:	%{libname}-custom < %{version}-%{release}
Conflicts:	%{libatlas}-custom-devel < %{version}-%{release}
%ifnarch x86_64
Conflicts:	%{libname}-sse < %{version}-%{release}
Conflicts:	%{libatlas}-sse-devel < %{version}-%{release}
%endif
Conflicts:	%{libname}-sse2 < %{version}-%{release}
Conflicts:	%{libatlas}-sse2-devel < %{version}-%{release}
Conflicts:	atlas < %{version}-%{release}
Conflicts:	%{libatlas}-sse3-devel < %{version}-%{release}
Conflicts:	atlas < %{version}-%{release}
Requires(post):	update-alternatives
Requires(postun): update-alternatives

%description	-n %{libname}-sse3
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with SS3 optimizations.
This is a generic binary package. Install the "%{name}" package
to build a version tuned for your computer.

%posttrans	-n %{libname}-sse3
update-alternatives							\
    --install %{_libdir}/atlas atlas %{_libdir}/atlas-sse3 3		\
    --slave %{_sysconfdir}/ld.so.conf.d/atlas.conf atlas-conf %{_libdir}/atlas-sse3/atlas.conf
/sbin/ldconfig

%postun		-n %{libname}-sse3
if [ $1 -eq 0 ]; then
    update-alternatives --remove atlas %{_libdir}/atlas-sse3
    /sbin/ldconfig
fi

%files		-n %{libname}-sse3
%defattr(-,root,root,-)
%dir %{_libdir}/atlas-sse3
%{_libdir}/atlas-sse3/*.so.*
%{_libdir}/atlas-sse3/atlas.conf

#------#################################################################
%package	-n %{libatlas}-sse3-devel
Summary:	Development files for ATLAS SSE3
Group:		Development/Other
%ifarch x86_64
Obsoletes:	%{libatlas}-x86_64-devel
%endif
Requires:	%{libname}-sse3 = %{version}-%{release}
Provides:	%{libatlas}-devel = %{version}-%{release}
Requires(post):	update-alternatives
Requires(postun): update-alternatives

%description	-n %{libatlas}-sse3-devel
This package contains headers and development libraries of ATLAS
(Automatically Tuned Linear Algebra Software) compiled with SSE3
optimizations.

%posttrans	-n %{libatlas}-sse3-devel
update-alternatives							\
    --install %{_includedir}/atlas atlas-devel %{_includedir}/atlas-sse3 3 \
    --slave %{_includedir}/cblas.h cblas.h %{_includedir}/atlas-sse3/cblas.h \
    --slave %{_includedir}/clapack.h clapack.h %{_includedir}/atlas-sse3/clapack.h

%postun		-n %{libatlas}-sse3-devel
if [ $1 -eq 0 ]; then
    update-alternatives --remove atlas-devel %{_includedir}/atlas-sse3
fi

%files		-n %{libatlas}-sse3-devel
%defattr(-,root,root,-)
%doc doc/*
%{_libdir}/atlas-sse3/*.so
%{_libdir}/atlas-sse3/*.a
%{_includedir}/atlas-sse3/

# ifarch ix86 x86_64
  %endif

#--#####################################################################
  %ifnarch %{ix86} x86_64
#----###################################################################
%package	-n %{libname}-%{_arch}
Summary:	ATLAS libraries for %{_arch}
Group:		System/Libraries
Provides:	%{libatlas} = %{version}-%{release}
Conflicts:	%{libname}-custom < %{version}-%{release}
Conflicts:	%{libatlas}-custom-devel < %{version}-%{release}
Conflicts:	%{libatlas}-%{_arch}-devel < %{version}-%{release}
Conflicts:	atlas < %{version}-%{release}
Requires(post):	update-alternatives
Requires(postun): update-alternatives

%description	-n %{libname}-%{_arch}
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with %{_arch} optimizations.
This is a generic binary package. Install the "%{name}" package
to build a version tuned for your computer.

%posttrans	-n %{libname}-%{_arch}
update-alternatives							\
    --install %{_libdir}/atlas atlas %{_libdir}/atlas-%{_arch} 2	\
    --slave %{_sysconfdir}/ld.so.conf.d/atlas.conf atlas-conf %{_libdir}/atlas-%{_arch}/atlas.conf
/sbin/ldconfig

%postun		-n %{libname}-%{_arch}
if [ $1 -eq 0 ]; then
    update-alternatives --remove atlas %{_libdir}/atlas-%{_arch}
/sbin/ldconfig
fi

%files		-n %{libname}-%{_arch}
%defattr(-,root,root,-)
%dir %{_libdir}/atlas
%{_libdir}/atlas-%{_arch}/*.so.*
%{_libdir}/atlas-%{_arch}/atlas.conf

#------#################################################################
%package	-n %{libatlas}-%{_arch}-devel
Summary:	Development files for ATLAS for %{_arch}
Group:		Development/Other
Requires:	%{libname}-%{_arch} = %{version}-%{release}
Provides:	%{libatlas}-devel = %{version}-%{release}
Requires(post):	update-alternatives
Requires(postun): update-alternatives

%description	-n %{libatlas}-%{_arch}-devel
This package contains headers and development libraries of ATLAS
(Automatically Tuned Linear Algebra Software) compiled with %{_arch}
optimizations.

%posttrans	-n %{libatlas}-%{_arch}-devel
update-alternatives							\
    --install %{_includedir}/atlas atlas-devel %{_includedir}/atlas-%{_arch} 2 \
    --slave %{_includedir}/cblas.h cblas.h %{_includedir}/atlas-%{_arch}/cblas.h \
    --slave %{_includedir}/clapack.h clapack.h %{_includedir}/atlas-%{_arch}/clapack.h
/sbin/ldconfig

%postun		-n %{libatlas}-%{_arch}-devel
if [ $1 -eq 0 ]; then
    update-alternatives --remove atlas-devel %{_includedir}/atlas-%{_arch}
    /sbin/ldconfig
fi

%files		-n %{libatlas}-%{_arch}-devel
%defattr(-,root,root,-)
%doc doc/*
%{_libdir}/atlas-%{_arch}/*.a
%{_libdir}/atlas-%{_arch}/*.so
%{_includedir}/atlas-%{_arch}/

# ifnarch ix86 x86_64
  %endif
# with custom_atlas
%endif

########################################################################
%prep
%setup -q -n ATLAS

%patch0 -p0 -b .shared

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} doc

mkdir temp
pushd temp
    ar x %{_libdir}/liblapack.a
    rm -f cgesv.f.o cgetrf.o cgetrf.f.o cgetri.o cgetri.f.o		\
	  cgetrs.o cgetrs.f.o clauum.o clauum.f.o cposv.o cposv.f.o	\
	  cpotrf.o cpotrf.f.o cpotri.o cpotri.f.o cpotrs.o cpotrs.f.o	\
	  ctrtri.o ctrtri.f.o dgesv.o dgesv.f.o dgetrf.o dgetrf.f.o	\
	  dgetri.o dgetri.f.o dgetrs.o dgetrs.f.o dlauum.o dlauum.f.o	\
	  dposv.o dposv.f.o dpotrf.o dpotrf.f.o dpotri.o dpotri.f.o	\
	  dpotrs.o dpotrs.f.o dtrtri.o dtrtri.f.o ieeeck.o ieeeck.f.o	\
	  ilaenv.o ilaenv.f.o sgesv.o sgesv.f.o sgetrf.o sgetrf.f.o	\
	  sgetri.o sgetri.f.o sgetrs.o sgetrs.f.o slauum.o slauum.f.o	\
	  sposv.o sposv.f.o spotrf.o spotrf.f.o spotri.o spotri.f.o	\
	  spotrs.o spotrs.f.o strtri.o strtri.f.o zgesv.o zgesv.f.o	\
	  zgetrf.o zgetrf.f.o zgetri.o  zgetri.f.o zgetrs.o zgetrs.f.o	\
	  zlauum.o zlauum.f.o zposv.o zposv.f.o zpotrf.o zpotrf.f.o	\
	  zpotri.o zpotri.f.o zpotrs.o zpotrs.f.o ztrtri.o ztrtri.f.o
    ar q ../liblapack.a *.o
popd
rm -fr temp

%build
for type in %{types}; do
    case $type in
	%{_arch})	libname=%{name}		;;
	*)		libname=%{name}-$type	;;
    esac
    rm -fr %{_arch}_${type}
    mkdir -p %{_arch}_${type}
    pushd %{_arch}_${type}
	../configure -b %{mode} -D c -DWALL -Fa alg			\
	    '-Wa,--noexecstack -fPIC'					\
	    -Ss f77lib `gfortran --print-file-name=libgfortran.so`	\
	    --prefix=%{buildroot}%{_prefix}				\
	    --incdir=%{buildroot}%{_includedir}				\
	    --libdir=%{buildroot}%{_libdir}/${libname}			\
	    --with-netlib-lapack=%{_builddir}/ATLAS/liblapack.a
	if [ "$type" = "sse" ]; then
		sed -i 's#ARCH =.*#ARCH = PIII32SSE1#' Make.inc
		sed -i 's#-DATL_SSE3 -DATL_SSE2##' Make.inc 
	elif [ "$type" = "sse2" ]; then
%ifarch %{ix86}
		sed -i 's#ARCH =.*#ARCH = P432SSE2#' Make.inc
		sed -i 's#-DATL_SSE3##' Make.inc 
		sed -i 's#-msse3#-msse2#' Make.inc
%endif
%ifarch x86_64
		sed -i 's#ARCH =.*#ARCH = HAMMER64SSE2#' Make.inc
		sed -i 's#-DATL_SSE3##' Make.inc 
		sed -i 's#-msse3#-msse2#' Make.inc
%endif
	elif [ "$type" = "sse3" ]; then
%ifarch %{ix86}
		sed -i 's#ARCH =.*#ARCH = P4E32SSE3#' Make.inc
%endif
%ifarch x86_64
		sed -i 's#ARCH =.*#ARCH = HAMMER64SSE3#' Make.inc
%endif
	fi
	make build
	cd lib
	make shared
	make ptshared
    popd
done

%install
for type in %{types}; do
    dirname=%{name}-$type
    pushd %{_arch}_${type}
	make DESTDIR=%{buildroot} install || :
	mkdir -p %{buildroot}%{_libdir}/${dirname}
	cp -pr lib/*.so* %{buildroot}%{_libdir}/${dirname}/
	mv %{buildroot}%{_includedir}/atlas %{buildroot}%{_includedir}/${dirname}
	mv %{buildroot}%{_includedir}/*.h %{buildroot}%{_includedir}/${dirname}
    popd
    echo "%{_libdir}/${dirname}"					\
	> %{buildroot}%{_libdir}/${dirname}/atlas.conf
done

mkdir -p %{buildroot}%{_libdir}/%{name}-source
mkdir -p %{buildroot}%{_includedir}/%{name}-source
mkdir -p %{buildroot}%{_usrsrc}
tar jxf %{SOURCE0} -C %{buildroot}%{_usrsrc}
pushd %{buildroot}%{_usrsrc}/ATLAS
    patch -p0 < %{PATCH0}
popd

install -D %{SOURCE4} %{buildroot}%{_usrsrc}/ATLAS/Makefile
perl -pi -e 's|\@\@LIBDIR\@\@|%{_libdir}|g;'				\
	 -e 's|\@\@ARCH\@\@|%{_arch}|g;'				\
	 -e 's|\@\@MODE\@\@|%{mode}|g;'					\
	%{buildroot}%{_usrsrc}/ATLAS/Makefile

install -D %{SOURCE5} %{buildroot}%{_usrsrc}/ATLAS/README.mandriva
perl -pi -e 's|\@\@VERSION\@\@|%{version}|g;'				\
	 -e 's|\@\@RELEASE\@\@|%{release}|g;'				\
	 -e 's|\@\@ARCH\@\@|%{_arch}|g;'				\
	%{buildroot}%{_usrsrc}/ATLAS/README.mandriva

%clean
rm -rf %{buildroot}

########################################################################
%post
echo "

  Please check %{_usrsrc}/ATLAS/README.mandriva for build instructions.

"

%files
%defattr(-,root,root,-)
%dir %{_usrsrc}/ATLAS
%{_usrsrc}/ATLAS/*
%dir %{_includedir}/%{name}-source
%dir %{_libdir}/%{name}-source
%doc doc/*
