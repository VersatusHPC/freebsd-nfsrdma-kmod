KMOD=	nfsrdma
SRCS=	svc_verbs.c nfsrdma_sink.c nfsrdma_decode.c nfsrdma_data.c
SRCS+=	nfsrdma_conn.c svc_rdma.c
SRCS+=	${LINUXKPI_GENSRCS}
SRCS+=	opt_inet.h opt_inet6.h opt_ofed.h

CFLAGS+= -I${.CURDIR}
CFLAGS+= -I${SRCTOP}/sys/ofed/include
CFLAGS+= -I${SRCTOP}/sys/ofed/include/uapi
CFLAGS+= ${LINUXKPI_INCLUDES}

# config.mk supplies INET/INET6 defaults for standalone module builds and
# uses the configured option headers when KERNBUILDDIR is provided.
.if !defined(KERNBUILDDIR)
opt_ofed.h:
	@echo "#define OFED 1" > ${.TARGET}
.endif

.include <bsd.kmod.mk>

CWARNFLAGS+= -Wno-cast-qual -Wno-pointer-arith
