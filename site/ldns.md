---
title: Incremental deleg support in ldns
layout: default
permalink: /ldns.html
---

The [ldns DNS library and tools](https://nlnetlabs.nl/projects/ldns/about/) software has been extended with support for incremental deleg (IDELEG) and also wesplaap-deleg (DELEG), which is available in the [`deleg-and-ideleg`](https://github.com/NLnetLabs/ldns/tree/deleg-and-ideleg) branch of the `NLnetLabs/ldns` github repository.

To build the `drill` DNS query tool and the other tools (among which the DNSSEC signer `ldns-signzone` with which the testbed's zones were signed) from source, we need to install several packages.
Below is shown how to install those prerequisites on an Ubuntu Linux machine:

```
~$ sudo apt install git build-essential libtool autoconf make libssl-dev
```

Then, to clone the repository, checkout the `deleg-and-ideleg` branch and initialize the repository:

```
~$ git clone https://github.com/NLnetLabs/ldns
Cloning into 'ldns'...
remote: Enumerating objects: 25995, done.
remote: Counting objects: 100% (798/798), done.
remote: Compressing objects: 100% (214/214), done.
remote: Total 25995 (delta 660), reused 605 (delta 583), pack-reused 25197 (from 4)
Receiving objects: 100% (25995/25995), 8.28 MiB | 32.74 MiB/s, done.
Resolving deltas: 100% (18132/18132), done.

~$ cd ldns

ldns$ git checkout deleg-and-ideleg
branch 'deleg-and-ideleg' set up to track 'origin/deleg-and-ideleg'.
Switched to a new branch 'deleg-and-ideleg'

~/ldns$ git submodule update --init
Submodule 'contrib/DNS-LDNS' (https://github.com/erikoest/DNS-LDNS) registered for path 'contrib/DNS-LDNS'
Submodule 'test/tpkg' (https://github.com/NLnetLabs/tpkg.git) registered for path 'test/tpkg'
Cloning into '/root/ldns/contrib/DNS-LDNS'...
Cloning into '/root/ldns/test/tpkg'...
Submodule path 'contrib/DNS-LDNS': checked out 'c2aedfffd629a61ee9bd850d6ff58b7e86626a83'
Submodule path 'test/tpkg': checked out 'ba58d3bb9a3a0c4940f2fb52bfc75dc4df56cc8d'
```

To generate the necessary autoconf and libtool files (`ltmain.sh` and `configure`), do:

```
~/ldns$ libtoolize -ci
libtoolize: putting auxiliary files in '.'.
libtoolize: copying file './config.guess'
libtoolize: copying file './config.sub'
libtoolize: copying file './install-sh'
libtoolize: copying file './ltmain.sh'
libtoolize: putting macros in AC_CONFIG_MACRO_DIRS, 'm4'.
libtoolize: copying file 'm4/libtool.m4'
libtoolize: copying file 'm4/ltoptions.m4'
libtoolize: copying file 'm4/ltsugar.m4'
libtoolize: copying file 'm4/ltversion.m4'
libtoolize: copying file 'm4/lt~obsolete.m4'
libtoolize: Consider adding '-I m4' to ACLOCAL_AMFLAGS in Makefile.am.

~/ldns$ autoreconf -fi
```

Configure the source tree for compiling with IDELEG support, do:

```
~/ldns$ ./configure --with-drill --with-examples --enable-rrtype-ideleg
```

Then to make the library, `drill` and the other tools, do:

```
~/ldns$ make -j

```

To install, do the following:

```
~/ldns$ sudo make install
```

By default, the library and tools will be installed below `/usr/local`.
I had to de the following on my Ubuntu 24.04.2 for the tools to be able to find the ldns library:

```
~/ldns$ sudo ldconfig

```

We can now test `drill` and see that the IDELEG resource records are displayed as intended:

```
~$ drill @ideleg.net something.something.customer3.ideleg.net A
;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 26614
;; flags: qr rd ; QUERY: 1, ANSWER: 0, AUTHORITY: 4, ADDITIONAL: 4
;; QUESTION SECTION:
;; something.something.customer3.ideleg.net.	IN	A

;; ANSWER SECTION:

;; AUTHORITY SECTION:
customer3.ideleg.net.	3600	IN	NS	legacy.ideleg.net.
customer3.ideleg.net.	3600	IN	NS	supporting.ideleg.net.
customer3._deleg.ideleg.net.	3600	IN	IDELEG	10 (
		supporting.ideleg.net.
		ipv4hint=188.245.247.219
		ipv6hint=2a01:4f8:c2c:99d7::1
		)
customer3._deleg.ideleg.net.	3600	IN	IDELEG	20 (
		legacy.ideleg.net.
		ipv4hint=94.130.76.72
		ipv6hint=2a01:4f8:c2c:b1ed::1
		)
;; ADDITIONAL SECTION:
legacy.ideleg.net.	3600	IN	AAAA	2a01:4f8:c2c:b1ed::1
supporting.ideleg.net.	3600	IN	AAAA	2a01:4f8:c2c:99d7::1
legacy.ideleg.net.	3600	IN	A	94.130.76.72
supporting.ideleg.net.	3600	IN	A	188.245.247.219

;; Query time: 1 msec
;; SERVER: 2a01:4f8:c0c:92cd::1
;; WHEN: Sun Mar  9 09:19:20 2025
;; MSG SIZE  rcvd: 335
```
_(output edited to make it fit the screen)_


And also DELEG RRs:
```
$ drill @deleg.org something.something.customer2.deleg.org A
;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 39026
;; flags: qr rd ; QUERY: 1, ANSWER: 0, AUTHORITY: 2, ADDITIONAL: 2
;; QUESTION SECTION:
;; something.something.customer2.deleg.org.	IN	A

;; ANSWER SECTION:

;; AUTHORITY SECTION:
customer2.deleg.org.	3600	IN	NS	ns.customer2.deleg.org.
customer2.deleg.org.	3600	IN	DELEG	1 (
		ns.customer2.deleg.org.
		Glue4=94.130.76.72
		Glue6=2a01:4f8:c2c:b1ed::1
		)
;; ADDITIONAL SECTION:
ns.customer2.deleg.org.	3600	IN	A	94.130.76.72
ns.customer2.deleg.org.	3600	IN	AAAA	2a01:4f8:c2c:b1ed::1

;; Query time: 354 msec
;; SERVER: 146.190.95.45
;; WHEN: Wed Mar 12 16:05:26 2025
;; MSG SIZE  rcvd: 184
```
_(output edited to make it fit the screen)_

