---
title: Incremental deleg support in Unbound
layout: default
permalink: /unbound.html
---

The [Unbound validating, recursive, caching DNS resolver](https://nlnetlabs.nl/projects/unbound/about/) software has been extended with support for IDELEG, by Jesse van Zutphen as part of his master thesis for the Security and Network Engineering master program of the University of Amsterdam.
For the full report, see: [Extensible delegations in DNS Recursive resolvers](https://nlnetlabs.nl/downloads/publications/extensible-deleg-in-resolvers_2024-07-08.pdf), Jesse van Zutphen, University of Amsterdam, July 2024.

The source code is available in the [`ideleg`](https://github.com/NLnetLabs/unbound/tree/ideleg) branch of the `NLnetLabs/unbound` github repository.

To build this version from source, we need to meet a few prerequisites.
Below is shown how to install those prerequisites on an Ubuntu Linux machine:

```
~$ sudo apt install git build-essential autoconf make libevent-dev libssl-dev libexpat1-dev flex bison
```

Then, to clone and initialize the repository, do:

```
~$ git clone https://github.com/NLnetLabs/unbound.git
Cloning into 'unbound'...
remote: Enumerating objects: 65183, done.
remote: Counting objects: 100% (542/542), done.
remote: Compressing objects: 100% (294/294), done.
remote: Total 65183 (delta 317), reused 248 (delta 248), pack-reused 64641 (from 4)
Receiving objects: 100% (65183/65183), 100.37 MiB | 39.64 MiB/s, done.
Resolving deltas: 100% (53012/53012), done.

~$ cd unbound
~/unbound$ git checkout ideleg
branch 'ideleg' set up to track 'origin/ideleg'.
Switched to a new branch 'ideleg'
```

Then to configure and make, do:

```
~/unbound$ ./configure
~/unbound$ make -j
```

To install, do the following:

```
~/unbound$ sudo make install
/bin/bash ./install-sh -m 755 -d /usr/local/lib
/bin/bash ./install-sh -m 755 -d /usr/local/include
/bin/bash ./install-sh -m 755 -d /usr/local/share/man
/bin/bash ./install-sh -m 755 -d /usr/local/share/man/man3
/bin/bash ./install-sh -c -m 644 doc/libunbound.3 /usr/local/share/man/man3
for mpage in ub_ctx ub_result ub_ctx_create ub_ctx_delete \
	ub_ctx_set_option ub_ctx_get_option ub_ctx_config ub_ctx_set_fwd \
	ub_ctx_resolvconf ub_ctx_hosts ub_ctx_add_ta ub_ctx_add_ta_file \
	ub_ctx_trustedkeys ub_ctx_debugout ub_ctx_debuglevel ub_ctx_async \
	ub_poll ub_wait ub_fd ub_process ub_resolve ub_resolve_async ub_cancel \
	ub_resolve_free ub_strerror ub_ctx_print_local_zones ub_ctx_zone_add \
	ub_ctx_zone_remove ub_ctx_data_add ub_ctx_data_remove; \
do \
	echo ".so man3/libunbound.3" > /usr/local/share/man/man3/$mpage.3 ; \
done
./libtool --mode=install cp unbound.h /usr/local/include/unbound.h
libtool: install: cp unbound.h /usr/local/include/unbound.h
/bin/bash ./install-sh -m 755 -d /usr/local/lib/pkgconfig
/bin/bash ./install-sh -m 644 contrib/libunbound.pc /usr/local/lib/pkgconfig
./libtool --mode=install cp libunbound.la /usr/local/lib
libtool: install: cp .libs/libunbound.so.8.1.28 /usr/local/lib/libunbound.so.8.1.28
libtool: install: (cd /usr/local/lib && { ln -s -f libunbound.so.8.1.28 libunbound.so.8 || { rm -f libunbound.so.8 && ln -s libunbound.so.8.1.28 libunbound.so.8; }; })
libtool: install: (cd /usr/local/lib && { ln -s -f libunbound.so.8.1.28 libunbound.so || { rm -f libunbound.so && ln -s libunbound.so.8.1.28 libunbound.so; }; })
libtool: install: cp .libs/libunbound.lai /usr/local/lib/libunbound.la
libtool: install: cp .libs/libunbound.a /usr/local/lib/libunbound.a
libtool: install: chmod 644 /usr/local/lib/libunbound.a
libtool: install: ranlib /usr/local/lib/libunbound.a
libtool: finish: PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/sbin" ldconfig -n /usr/local/lib
----------------------------------------------------------------------
Libraries have been installed in:
   /usr/local/lib

If you ever happen to want to link against installed libraries
in a given directory, LIBDIR, you must either use libtool, and
specify the full pathname of the library, or use the '-LLIBDIR'
flag during linking and do at least one of the following:
   - add LIBDIR to the 'LD_LIBRARY_PATH' environment variable
     during execution
   - add LIBDIR to the 'LD_RUN_PATH' environment variable
     during linking
   - use the '-Wl,-rpath -Wl,LIBDIR' linker flag
   - have your system administrator add LIBDIR to '/etc/ld.so.conf'

See any operating system documentation about shared libraries for
more information, such as the ld(1) and ld.so(8) manual pages.
----------------------------------------------------------------------
./libtool --mode=finish /usr/local/lib
libtool: finish: PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/sbin" ldconfig -n /usr/local/lib
----------------------------------------------------------------------
Libraries have been installed in:
   /usr/local/lib

If you ever happen to want to link against installed libraries
in a given directory, LIBDIR, you must either use libtool, and
specify the full pathname of the library, or use the '-LLIBDIR'
flag during linking and do at least one of the following:
   - add LIBDIR to the 'LD_LIBRARY_PATH' environment variable
     during execution
   - add LIBDIR to the 'LD_RUN_PATH' environment variable
     during linking
   - use the '-Wl,-rpath -Wl,LIBDIR' linker flag
   - have your system administrator add LIBDIR to '/etc/ld.so.conf'

See any operating system documentation about shared libraries for
more information, such as the ld(1) and ld.so(8) manual pages.
----------------------------------------------------------------------
/bin/bash ./install-sh -m 755 -d /usr/local/sbin
/bin/bash ./install-sh -m 755 -d /usr/local/share/man
/bin/bash ./install-sh -m 755 -d /usr/local/share/man/man8
/bin/bash ./install-sh -m 755 -d /usr/local/share/man/man5
/bin/bash ./install-sh -m 755 -d /usr/local/share/man/man1
./libtool --mode=install cp -f unbound /usr/local/sbin/unbound
libtool: install: cp -f unbound /usr/local/sbin/unbound
./libtool --mode=install cp -f unbound-checkconf /usr/local/sbin/unbound-checkconf
libtool: install: cp -f unbound-checkconf /usr/local/sbin/unbound-checkconf
./libtool --mode=install cp -f unbound-control /usr/local/sbin/unbound-control
libtool: install: cp -f unbound-control /usr/local/sbin/unbound-control
./libtool --mode=install cp -f unbound-host /usr/local/sbin/unbound-host
libtool: install: cp -f .libs/unbound-host /usr/local/sbin/unbound-host
./libtool --mode=install cp -f unbound-anchor /usr/local/sbin/unbound-anchor
libtool: install: cp -f .libs/unbound-anchor /usr/local/sbin/unbound-anchor
/bin/bash ./install-sh -c -m 644 doc/unbound.8 /usr/local/share/man/man8
/bin/bash ./install-sh -c -m 644 doc/unbound-checkconf.8 /usr/local/share/man/man8
/bin/bash ./install-sh -c -m 644 doc/unbound-control.8 /usr/local/share/man/man8
/bin/bash ./install-sh -c -m 644 doc/unbound-control.8 /usr/local/share/man/man8/unbound-control-setup.8
/bin/bash ./install-sh -c -m 644 doc/unbound-anchor.8 /usr/local/share/man/man8
/bin/bash ./install-sh -c -m 644 doc/unbound.conf.5 /usr/local/share/man/man5
/bin/bash ./install-sh -c -m 644 doc/unbound-host.1 /usr/local/share/man/man1
/bin/bash ./install-sh -c -m 755 unbound-control-setup /usr/local/sbin/unbound-control-setup
if test ! -e "/usr/local/etc/unbound/unbound.conf"; then /bin/bash ./install-sh -d `dirname "/usr/local/etc/unbound/unbound.conf"`; /bin/bash ./install-sh -c -m 644 doc/example.conf "/usr/local/etc/unbound/unbound.conf"; fi
```

This version of Unbound performs the algorithm as described in [Section 4. Minimal implementation](https://ideleg.net/draft-homburg-deleg-incremental-deleg-latest.html#name-minimal-implementation) in the draft.
It does not (yet) leverage optimized responses.
It also does not (yet) support the AliasMode.
It can be used to test your own incremental delegations, as long as they do not involve AliasMode IDELEG RRs.

