---
title: wesplaap-deleg support in NSD
layout: default
permalink: /nsd-deleg.html
---

The [NSD authoritative name server](https://nlnetlabs.nl/projects/nsd/about/) software has been extended with support for the [draft-wesplaap-deleg](https://www.ietf.org/archive/id/draft-wesplaap-deleg-02.html) version of DELEG.

To build this version from source, we need to meet a few prerequisites.
Below is shown how to install those prerequisites on an Ubuntu Linux machine:

```
~$ sudo apt install git build-essential autoconf make cmake libevent-dev libssl-dev flex bison
```

Then, to clone and initialize the repository, do:

```
~$ git clone https://github.com/NLnetLabs/nsd.git
Cloning into 'nsd'...
remote: Enumerating objects: 33298, done.
remote: Counting objects: 100% (7207/7207), done.
remote: Compressing objects: 100% (554/554), done.
remote: Total 33298 (delta 6848), reused 6653 (delta 6653), pack-reused 26091 (from 4)
Receiving objects: 100% (33298/33298), 176.95 MiB | 35.88 MiB/s, done.
Resolving deltas: 100% (24621/24621), done.

~$ cd nsd
~/nsd$ git checkout features/deleg
Switched to branch 'features/deleg'
Your branch is up to date with 'origin/features/deleg'.

~/nsd$ git submodule update --init
Submodule 'simdzone' (https://github.com/WP-Official/simdzone.git) registered for path 'simdzone'
Cloning into '/root/nsd/simdzone'...
Submodule path 'simdzone': checked out 'd720518a774bc14e5b05d074e1ebb534e94553e0'
```

To generate the necessary autoconf files (`configure` and `simdzone/configure` etc.), do:

```
~/nsd$ autoreconf -fi
```

To configure the source tree for compiling with IDELEG support, do:

```
~/nsd$ ./configure
```

Then, to make the DELEG supporting NSD, do:

```
~/nsd$ make -j

```

To install, do the following:

```
~/nsd$ sudo make install
./install-sh -c -d /usr/local/sbin
./install-sh -c -d /etc/nsd
if test -n "/var/run"; then ./install-sh -c -d /var/run; fi
./install-sh -c -d /tmp
./install-sh -c -d `dirname /var/db/nsd/xfrd.state`
./install-sh -c -d `dirname /var/db/nsd/zone.list`
./install-sh -c -d `dirname /var/db/nsd/cookiesecrets.txt`
./install-sh -c -d /usr/local/share/man
./install-sh -c -d /usr/local/share/man/man8
./install-sh -c -d /usr/local/share/man/man5
./install-sh -c nsd /usr/local/sbin/nsd
./install-sh -c nsd-control-setup.sh /usr/local/sbin/nsd-control-setup
./install-sh -c nsd-checkconf /usr/local/sbin/nsd-checkconf
./install-sh -c nsd-checkzone /usr/local/sbin/nsd-checkzone
./install-sh -c nsd-control /usr/local/sbin/nsd-control
./install-sh -c -m 644 nsd.8 /usr/local/share/man/man8
./install-sh -c -m 644 nsd-checkconf.8 /usr/local/share/man/man8/nsd-checkconf.8
./install-sh -c -m 644 nsd-checkzone.8 /usr/local/share/man/man8/nsd-checkzone.8
./install-sh -c -m 644 nsd-control.8 /usr/local/share/man/man8/nsd-control.8
./install-sh -c -m 644 nsd.conf.5 /usr/local/share/man/man5/nsd.conf.5
./install-sh -c -m 644 nsd.conf.sample /etc/nsd/nsd.conf.sample
```

This version of NSD will include the DELEG delegation in the referral responses if queried with the DE flag.
DELEG supporting NSD is running on the name servers serving the deleg.org zone.
For example:

```
~$ dig @deleg.org customer4.deleg.org +ednsflags=0x2000 +multiline +norec

; <<>> DiG 9.18.30-0ubuntu0.24.04.2-Ubuntu <<>> @deleg.org customer4.deleg.org +ednsflags=0x2000 +multiline +norec
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 17239
;; flags: qr; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 594a08e4d375f10b0100000067e55e2c769bd801252fb74b (good)
;; QUESTION SECTION:
;customer4.deleg.org.  IN A

;; AUTHORITY SECTION:
customer4.deleg.org.   3600 IN  TYPE65432 \# 48 (
                                0001066C65676163790564656C6567036F7267000004
				0004867A2763000600102604A8800CAD00D000000000
				A4171001 )

;; Query time: 182 msec
;; SERVER: 2400:6180:0:d2:0:1:ac7b:8000#53(deleg.org) (UDP)
;; WHEN: Thu Mar 27 15:18:20 CET 2025
;; MSG SIZE  rcvd: 136
```

or to view the content of the IDELEG RRs as intended, using a version of [`drill` compiled for DELEG support](/ldns.html):

```
$ drill -ord @deleg.org something.something.customer3.deleg.org -E
;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 19365
;; flags: qr ; QUERY: 1, ANSWER: 0, AUTHORITY: 2, ADDITIONAL: 2 
;; QUESTION SECTION:
;; something.something.customer3.deleg.org.  IN  A

;; ANSWER SECTION:

;; AUTHORITY SECTION:
customer3.deleg.org.    3600  IN  NS     ns.customer2.deleg.org.
customer3.deleg.org.    3600  IN  DELEG  0 deleg.customer2.deleg.org.

;; ADDITIONAL SECTION:
ns.customer2.deleg.org. 3600  IN  A      134.122.39.99
ns.customer2.deleg.org. 3600  IN  AAAA   2604:a880:cad:d0::a417:1001

;; Query time: 201 msec
;; EDNS: version 0; flags: ; udp: 1232
;; SERVER: 146.190.95.45
;; WHEN: Thu Mar 27 15:20:02 2025
;; MSG SIZE  rcvd: 180
```
