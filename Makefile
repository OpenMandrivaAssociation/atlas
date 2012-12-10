all:	config libs

libs:
	mkdir -p @@LIBDIR@@/atlas-source &&				\
	(cd @@ARCH@@ && make build && cd lib && make shared && make ptshared || :)

config:
	[ -f /usr/src/ATLAS/liblapack.a ] || (mkdir temp;		\
	pushd temp;							\
	    ar x @@LIBDIR@@/liblapack.a;				\
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
	  zpotri.o zpotri.f.o zpotrs.o zpotrs.f.o ztrtri.o ztrtri.f.o;	\
	    ar q /usr/src/ATLAS/liblapack.a *.o;			\
	popd; rm -fr temp)
	[ -d @@ARCH@@ ] || (mkdir -p @@ARCH@@ && cd @@ARCH@@ &&		\
	../configure -b @@MODE@@ -D c -DWALL -Fa alg			\
	'-Wa,--noexecstack -fPIC'					\
	-Ss f77lib `gfortran --print-file-name=libgfortran.so`		\
	--prefix=/usr							\
	--incdir=/usr/include/atlas					\
	--libdir=@@LIBDIR@@/atlas-source				\
	--with-netlib-lapack=/usr/src/ATLAS/liblapack.a)

clean:
	rm -f liblapack.a
	rm -fr @@ARCH@@

install:
	[ -e /usr/include/atlas ] &&					\
	(mv -f /usr/include/atlas /usr/include/atlas.save || :) || :
	[ -e /usr/include/cblas.h ] &&					\
	(mv -f /usr/include/cblas.h /usr/include/cblas.h.save || :) || :
	[ -e /usr/include/clapack.h ] &&				\
	(mv -f /usr/include/clapack.h /usr/include/clapack.h.save || :) || :
	(cd @@ARCH@@ && (make install || :) &&				\
	cp -pr lib/*.so* @@LIBDIR@@/atlas-source &&			\
	echo "@@LIBDIR@@/atlas-source" > @@LIBDIR@@/atlas-source/atlas.conf)
	mv /usr/include/atlas/* /usr/include/atlas-source
	rmdir /usr/include/atlas
	mv /usr/include/{cblas,clapack}.h /usr/include/atlas-source
	[ -e /usr/include/atlas.save ] &&				\
	(mv -f /usr/include/atlas.save /usr/include/atlas || :) || :
	[ -e /usr/include/cblas.h.save ] &&				\
	(mv -f /usr/include/cblas.h.save /usr/include/cblas.h || :) || :
	[ -e /usr/include/clapack.h.save ] &&				\
	(mv -f /usr/include/clapack.h.save /usr/include/clapack.h || :) || :
	update-alternatives --install @@LIBDIR@@/atlas atlas @@LIBDIR@@/atlas-source 100 --slave /etc/ld.so.conf.d/atlas.conf atlas-conf @@LIBDIR@@/atlas-source/atlas.conf
	update-alternatives --install /usr/include/atlas atlas-devel /usr/include/atlas-source 100 --slave /usr/include/cblas.h cblas.h /usr/include/atlas-source/cblas.h --slave /usr/include/clapack.h clapack.h /usr/include/atlas-source/clapack.h
	/sbin/ldconfig

uninstall:
	rm -fr @@LIBDIR@@/atlas-source
	rm -fr /usr/include/atlas-source
	update-alternatives --remove atlas @@LIBDIR@@/atlas-source
	update-alternatives --remove atlas-devel /usr/include/atlas-source
	/sbin/ldconfig
