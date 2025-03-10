---
title: Incremental deleg support in NSD
layout: default
permalink: /nsd.html
---

The [NSD authoritative name server](https://nlnetlabs.nl/projects/nsd/about/) software has been extended with support for IDELEG, by Wouter Petri as part of a research project for the Security and Network Engineering master program of the University of Amsterdam.
For the full report, see: [Extensible delegations in authoritative nameservers](https://nlnetlabs.nl/downloads/publications/extensible-delegations-in-authoritative-nameservers_2025-02-09.pdf), Wouter Petri, University of Amsterdam, February 2025.

The source code for Wouter's version of NSD is available in the [`master`](https://github.com/WP-Official/nsd/tree/master) branch of the `WP-Official/nsd` github repository.

To build this version from source, we need to meet a few prerequisites.
Below is shown how to install those prerequisites on an Ubuntu Linux machine:

```
~$ sudo apt install git build-essential autoconf make cmake libevent-dev libssl-dev flex bison
```

Then, to clone and initialize the repository, do:

```
~$ git clone https://github.com/WP-Official/nsd.git
Cloning into 'nsd'...
remote: Enumerating objects: 33298, done.
remote: Counting objects: 100% (7207/7207), done.
remote: Compressing objects: 100% (554/554), done.
remote: Total 33298 (delta 6848), reused 6653 (delta 6653), pack-reused 26091 (from 4)
Receiving objects: 100% (33298/33298), 176.95 MiB | 35.88 MiB/s, done.
Resolving deltas: 100% (24621/24621), done.

~$ cd nsd
~/nsd$ git checkout master
Already on 'master'
Your branch is up to date with 'origin/master'.

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
~/nsd$ ./configure --enable-deleg --enable-drafts
```

Then, to make the IDELEG supporting NSD, do:

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

This version of NSD will include the IDELEG delegation in the referral responses.
An IDELEG supporting NSD is running on the name servers serving the ideleg.net zone.
For example:

```
~$ dig @ideleg.net something.something.customer3.ideleg.net A +multiline +norec

; <<>> DiG 9.18.30-0ubuntu0.24.04.2-Ubuntu <<>> @ideleg.net something.something.customer3.ideleg.net A +multiline +norec
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 49310
;; flags: qr; QUERY: 1, ANSWER: 0, AUTHORITY: 4, ADDITIONAL: 5

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: d6b20ea0027f38f30100000067cd6a6fe532c1667d3b8844 (good)
;; QUESTION SECTION:
;something.something.customer3.ideleg.net. IN A

;; AUTHORITY SECTION:
customer3.ideleg.net.	3600 IN	NS legacy.ideleg.net.
customer3.ideleg.net.	3600 IN	NS supporting.ideleg.net.
customer3._deleg.ideleg.net. 3600 IN TYPE65280 \# 53 ( 000A0A737570706F7274696E67066964656C6567036E
				65740000040004BCF5F7DB000600102A0104F80C2C99
				D70000000000000001 )
customer3._deleg.ideleg.net. 3600 IN TYPE65280 \# 49 ( 0014066C6567616379066964656C6567036E65740000
				0400045E824C48000600102A0104F80C2CB1ED000000
				0000000001 )

;; ADDITIONAL SECTION:
legacy.ideleg.net.	3600 IN	AAAA 2a01:4f8:c2c:b1ed::1
supporting.ideleg.net.	3600 IN	AAAA 2a01:4f8:c2c:99d7::1
legacy.ideleg.net.	3600 IN	A 94.130.76.72
supporting.ideleg.net.	3600 IN	A 188.245.247.219

;; Query time: 11 msec
;; SERVER: 2a01:4f8:c0c:92cd::1#53(ideleg.net) (UDP)
;; WHEN: Sun Mar 09 11:16:15 CET 2025
;; MSG SIZE  rcvd: 374
```

or to view the content of the IDELEG RRs as intended, using a version of [`drill` compiled for IDELEG support](/ldns.html):

```
$ drill -ord @ideleg.net something.something.customer3.ideleg.net A 
;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 210
;; flags: qr ; QUERY: 1, ANSWER: 0, AUTHORITY: 4, ADDITIONAL: 4 
;; QUESTION SECTION:
;; something.something.customer3.ideleg.net.	IN	A

;; ANSWER SECTION:

;; AUTHORITY SECTION:
customer3.ideleg.net.	3600	IN	NS	legacy.ideleg.net.
customer3.ideleg.net.	3600	IN	NS	supporting.ideleg.net.
customer3._deleg.ideleg.net.	3600	IN	IDELEG	10 (
		supporting.ideleg.net.
		ipv4hint=188.245.247.219
		ipv6hint=2a01:4f8:c2c:99d7::1 )
customer3._deleg.ideleg.net.	3600	IN	IDELEG	20 (
		legacy.ideleg.net.
		ipv4hint=94.130.76.72
		ipv6hint=2a01:4f8:c2c:b1ed::1 )

;; ADDITIONAL SECTION:
legacy.ideleg.net.	3600	IN	AAAA	2a01:4f8:c2c:b1ed::1
supporting.ideleg.net.	3600	IN	AAAA	2a01:4f8:c2c:99d7::1
legacy.ideleg.net.	3600	IN	A	94.130.76.72
supporting.ideleg.net.	3600	IN	A	188.245.247.219

;; Query time: 14 msec
;; SERVER: 2a01:4f8:c0c:92cd::1
;; WHEN: Sun Mar  9 11:18:32 2025
;; MSG SIZE  rcvd: 335
```
_(output edited to make it fit the web page)_
