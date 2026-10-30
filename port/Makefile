PORTNAME=	nfsrdma-kmod
DISTVERSION=	0.3.2026103000
CATEGORIES=	net
MASTER_SITES=	https://github.com/VersatusHPC/freebsd-nfsrdma-kmod/releases/download/v${DISTVERSION}/

MAINTAINER=	ferrao@versatushpc.com.br
COMMENT=	NFS over RDMA server kernel module
WWW=		https://github.com/VersatusHPC/freebsd-nfsrdma-kmod

LICENSE=	BSD2CLAUSE
LICENSE_FILE=	${WRKSRC}/LICENSE

USES=		kmod
MAKE_ARGS=	SRCTOP=${SRC_BASE}
PLIST_FILES=	${KMODDIR}/nfsrdma.ko

.include <bsd.port.pre.mk>

.if ${OSVERSION} < 1600029
IGNORE=		requires FreeBSD main at a3d1d4e88ae7 or later and matching kernel sources
.endif

do-install:
	${INSTALL_KLD} ${WRKSRC}/nfsrdma.ko ${STAGEDIR}${KMODDIR}/nfsrdma.ko

.include <bsd.port.post.mk>
