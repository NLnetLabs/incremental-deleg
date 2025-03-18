---
title: Incrementally Deployable Extensible Delegation testbed
layout: default
permalink: /
---
This website hosts information on the domains we have deployed for evaluating and testing the [`draft-homburg-deleg-incremental-deleg`](/draft-homburg-deleg-incremental-deleg-latest.html) protocol proposal, as well as [`draft-wesplaap-deleg`](https://datatracker.ietf.org/doc/draft-wesplaap-deleg/).

## Zones and name servers

{% assign tb = site.data.testbed %}
The `{{ tb.zone }}` zone has been provisioned with several incremental delegations (using 65280 as the value for the `IDELEG` RR type), and is served by two [incremental deleg supporting authoritative name servers](/nsd.html) (`{{ tb.ideleg.name }}` and `{{ tb.nlnetlabs.name }}`) and one legacy, non incremental deleg supporting, authoritative name server (`{{ tb.legacy.name }}`) as hidden secondary:

|        name         |       IPv4        |       IPv6        |       location       |
|---------------------|-------------------|-------------------|----------------------|
| `{{ tb.ideleg.name }}` | <a href="" onclick="navigator.clipboard.writeText('{{ tb.ideleg.ipv4}}')" title="copy '{{ tb.ideleg.ipv4}}' to clipboard">{{ tb.ideleg.ipv4}}</a> | <a href="" onclick="navigator.clipboard.writeText('{{ tb.ideleg.ipv6}}')" title="copy '{{ tb.ideleg.ipv6}}' to clipboard">{{ tb.ideleg.ipv6}}</a> | {{ tb.ideleg.location}} |
| `{{ tb.nlnetlabs.name }}` | <a href="" onclick="navigator.clipboard.writeText('{{ tb.nlnetlabs.ipv4}}')" title="copy '{{ tb.nlnetlabs.ipv4}}' to clipboard">{{ tb.nlnetlabs.ipv4}}</a> | <a href="" onclick="navigator.clipboard.writeText('{{ tb.nlnetlabs.ipv6}}')" title="copy '{{ tb.nlnetlabs.ipv6}}' to clipboard">{{ tb.nlnetlabs.ipv6}}</a> | {{ tb.nlnetlabs.location}} |
| `{{ tb.legacy.name }}` | <a href="" onclick="navigator.clipboard.writeText('{{ tb.legacy.ipv4}}')" title="copy '{{ tb.legacy.ipv4}}' to clipboard">{{ tb.legacy.ipv4}}</a> | <a href="" onclick="navigator.clipboard.writeText('{{ tb.legacy.ipv6}}')" title="copy '{{ tb.legacy.ipv6}}' to clipboard">{{ tb.legacy.ipv6}}</a> | {{ tb.legacy.location}} |

The `{{ tb.deleg.name }}` zone has been provisioned with several wesplaap-deleg delegations (using 65432 as the value for the `DELEG` RR type), and is served by two wesplaap-deleg supporting authoritative name servers (`{{ tb.deleg.name }}` and `{{ tb.dnlnetlabs.name }}`) and one legacy, non incremental deleg supporting, authoritative name server (`{{ tb.legacy.name }}`) as hidden secondary:

|        name         |       IPv4        |       IPv6        |       location       |
|---------------------|-------------------|-------------------|----------------------|
| `{{ tb.deleg.name }}` | <a href="" onclick="navigator.clipboard.writeText('{{ tb.deleg.ipv4}}')" title="copy '{{ tb.deleg.ipv4}}' to clipboard">{{ tb.deleg.ipv4}}</a> | <a href="" onclick="navigator.clipboard.writeText('{{ tb.deleg.ipv6}}')" title="copy '{{ tb.deleg.ipv6}}' to clipboard">{{ tb.deleg.ipv6}}</a> | {{ tb.deleg.location}} |
| `{{ tb.dnlnetlabs.name }}` | <a href="" onclick="navigator.clipboard.writeText('{{ tb.dnlnetlabs.ipv4}}')" title="copy '{{ tb.dnlnetlabs.ipv4}}' to clipboard">{{ tb.dnlnetlabs.ipv4}}</a> | <a href="" onclick="navigator.clipboard.writeText('{{ tb.dnlnetlabs.ipv6}}')" title="copy '{{ tb.dnlnetlabs.ipv6}}' to clipboard">{{ tb.dnlnetlabs.ipv6}}</a> | {{ tb.dnlnetlabs.location}} |
| `{{ tb.legacy.name }}` | <a href="" onclick="navigator.clipboard.writeText('{{ tb.legacy.ipv4}}')" title="copy '{{ tb.legacy.ipv4}}' to clipboard">{{ tb.legacy.ipv4}}</a> | <a href="" onclick="navigator.clipboard.writeText('{{ tb.legacy.ipv6}}')" title="copy '{{ tb.legacy.ipv6}}' to clipboard">{{ tb.legacy.ipv6}}</a> | {{ tb.legacy.location}} |

## Querying the zones

These IP addresses can be queried directly to get a taste for the referral responses.
If queried with a [specially compiled version](/ldns.html) of `drill`, the `IDELEG` RRs will be displayed as intended.
See [this page](/ldns.html) for instructions how to compile LDNS and `drill` with `IDELEG` support.

For example, to get an incremental deleg referral from `{{ tb.ideleg.name }}``:

```
$ drill/drill -Dord @{{ ideleg.ipv4 }} www.customer1.ideleg.net.
;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 40708
;; flags: qr ; QUERY: 1, ANSWER: 0, AUTHORITY: 5, ADDITIONAL: 4 
;; QUESTION SECTION:
;; www.customer1.ideleg.net.	IN	A

;; ANSWER SECTION:

;; AUTHORITY SECTION:
customer1.ideleg.net.	3600	IN	NS	supporting.ideleg.net.
customer1._deleg.ideleg.net.	3600	IN	IDELEG	10 (
		supporting.ideleg.net.
		ipv4hint=188.245.247.219
		ipv6hint=2a01:4f8:c2c:99d7::1 )
customer1._deleg.ideleg.net.	3600	IN	RRSIG	IDELEG 13 4 3600 (
		20250403135716 20250306135716 60397 ideleg.net. 4UuzgvStSu... )
customer1.ideleg.net.	3600	IN	NSEC	customer2.ideleg.net. NS (
		RRSIG NSEC )
customer1.ideleg.net.	3600	IN	RRSIG	NSEC 13 3 3600 (
		20250403135716 ( 20250306135716 60397 ideleg.net. TeMDps2J... )

;; ADDITIONAL SECTION:
supporting.ideleg.net.	3600	IN	A	188.245.247.219
supporting.ideleg.net.	3600	IN	RRSIG	A 13 3 3600 (
		20250403135716 20250306135716 60397 ideleg.net. RNWvNn/HsO... )
supporting.ideleg.net.	3600	IN	AAAA	2a01:4f8:c2c:99d7::1
supporting.ideleg.net.	3600	IN	RRSIG	AAAA 13 3 3600 (
		20250403135716 20250306135716 60397 ideleg.net. QxDs43bLqX... )

;; Query time: 25 msec
;; EDNS: version 0; flags: do ; udp: 1232
;; SERVER: {{ ideleg.ipv4 }}
;; WHEN: Thu Mar  6 16:49:55 2025
;; MSG SIZE  rcvd: 670
```
_(This drill output has been edited for readability)_

## The NSEC3 signed zone

There is also a version with the same kinds of delegations, but NSEC3 signed, in the `nsec3.ideleg.net` zone, served by an [ideleg supporting authoritative name server](/nsd.html) (`{{ tb.supporting.name }}`) and also at one legacy, non incremental deleg supporting, auithoritative name server (`{{ tb.legacy.name }}`) as hidden secondary:

|        name         |       IPv4        |       IPv6        |       location       |
|---------------------|-------------------|-------------------|----------------------|
| `{{ tb.supporting.name }}` | <a href="" onclick="navigator.clipboard.writeText('{{ tb.supporting.ipv4}}')" title="copy '{{ tb.supporting.ipv4}}' to clipboard">{{ tb.supporting.ipv4}}</a> | <a href="" onclick="navigator.clipboard.writeText('{{ tb.supporting.ipv6}}')" title="copy '{{ tb.supporting.ipv6}}' to clipboard">{{ tb.supporting.ipv6}}</a> | {{ tb.supporting.location}} |
| `{{ tb.legacy.name }}` | <a href="" onclick="navigator.clipboard.writeText('{{ tb.legacy.ipv4}}')" title="copy '{{ tb.legacy.ipv4}}' to clipboard">{{ tb.legacy.ipv4}}</a> | <a href="" onclick="navigator.clipboard.writeText('{{ tb.legacy.ipv6}}')" title="copy '{{ tb.legacy.ipv6}}' to clipboard">{{ tb.legacy.ipv6}}</a> | {{ tb.legacy.location}} |

## Zone transfers

All the name servers in the testbed allow anyone to transfer all the zones that are being served by them.
For example to transfer the `ideleg.net` zone:

```
$ drill -Dord @{{ ideleg.ipv4 }} ideleg.net AXFR
ideleg.net.	3600	IN	SOA	ideleg.net. wouter.petri.os3.nl. ...
ideleg.net.	3600	IN	RRSIG	SOA 13 2 3600 20250403135716 ...
ideleg.net.	3600	IN	RRSIG	A 13 2 3600 20250403135716 ...
etc.
```
_(The transfer is cut-off and edited for readability)_

## IDELEG Resolver

A resolver implementing the [minimal implementation](https://ideleg.net/draft-homburg-deleg-incremental-deleg-latest.html#name-minimal-implementation) is provided at `resolver.ideleg.net` with IP addresses <a href="" onclick="navigator.clipboard.writeText('{{ tb.resolver.ipv4}}')" title="copy '{{ tb.resolver.ipv4}}' to clipboard">{{ tb.resolver.ipv4}}</a> and <a href="" onclick="navigator.clipboard.writeText('{{ tb.resolver.ipv6}}')" title="copy '{{ tb.resolver.ipv6}}' to clipboard">{{ tb.resolver.ipv6}}</a>.
The addresses are accessable over TCP or TLS, or over UDP with a valid server cookie.

The resolver is running a special version of [Unbound](/unbound.html).
It does not anticipate [optimized](/draft-homburg-deleg-incremental-deleg-latest.html#name-optimized-implementation) and [extra optimized](draft-homburg-deleg-incremental-deleg-latest.html#name-extra-optimized-implementat) responses, and it does not (yet) follow AliasMode IDELEG RRs, but it can be used to test our own IDELEG (only) delegations.

## Zones at name servers table

| zone                       | ideleg.net | nlnetlabs[^1] | supporting[^2] | legacy[^3]       |  signed  |
|----------------------------|:----------:|:-------------:|:--------------:|:----------------:|:--------:|
| ideleg.net                 | &#x2714;   | &#x2713;      |                | hidden           | &#x2714; |
| customer1.ideleg.net       |            |               | &#x2714;       |                  | &#x2714; |
| customer2.ideleg.net       |            |               | &#x2714;[^4]   |                  | &#x2714; |
| customer3.ideleg.net       |            |               | &#x2714;       | &#x2713;         | &#x2714; |
| customer4.ideleg.net       |            |               | &#x2714;[^5]   |                  | &#x2714; |
| nsec3.ideleg.net           |            |               | &#x2714;       | hidden           | &#x2714; |
| customer1.nsec3.ideleg.net |            |               |                | &#x2714;         | &#x2714; |
| customer2.nsec3.ideleg.net |            |               |                | &#x2714;[^6]     | &#x2714; |
| customer3.nsec3.ideleg.net |            | &#x2714;      |                | &#x2713;         | &#x2714; |
| customer4.nsec3.ideleg.net |            |               |                | &#x2714;[^7]     | &#x2714; |

| zone                       | deleg.org  | nlnetlabs[^8] | supporting[^9] | legacy[^3]       |  signed  |
|----------------------------|:----------:|:-------------:|:--------------:|:----------------:|:--------:|
| deleg.org                  | &#x2714;   | &#x2713;      |                | hidden           | &#x2714; |
| customer1.deleg.org        |            |               |                | &#x2714;         | &#x2714; |
| customer2.deleg.org        |            |               |                | &#x2714;         | &#x2714; |
| customer3.deleg.org        |            |               |                | &#x2714;         | &#x2714; |
| customer4.deleg.org        |            |               |                | &#x2714;         |          |
| customer5.deleg.org        |            |               |                | &#x2714;         |          |
| nsec3.deleg.org            |            |               | &#x2714;       | hidden           | &#x2714; |
| customer1.nsec3.deleg.org  |            |               |                | &#x2714;         | &#x2714; |
| customer2.nsec3.deleg.org  |            |               |                | &#x2714;         | &#x2714; |
| customer3.nsec3.deleg.org  |            |               |                | &#x2714;         | &#x2714; |
| customer4.nsec3.deleg.org  |            |               |                | &#x2714;         |          |
| customer5.nsec3.deleg.org  |            |               |                | &#x2714;         |          |

### footnotes
[^1]: ideleg.nlnetlabs.nl
[^2]: supporting.ideleg.net
[^3]: legacy.ideleg.net
[^4]: customer2.ideleg.net has the authoritative NS RRset in the customer2.ideleg.net zone
[^5]: customer4.ideleg.net has outsourced operations to ideleg.customer2.ideleg.net
[^6]: customer2.nsec3.ideleg.net has the authoritative NS RRset in the customer2.nsec3.ideleg.net zone
[^7]: customer4.nsec3.ideleg.net has outsourced operations to ideleg.nsec3.customer2.ideleg.net
[^8]: deleg.nlnetlabs.nl
[^9]: supporting.deleg.org


