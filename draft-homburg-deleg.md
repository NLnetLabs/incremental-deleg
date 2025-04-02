---
###
# Internet-Draft Markdown Template
#
# Rename this file from draft-todo-yourname-protocol.md to get started.
# Draft name format is "draft-<yourname>-<workgroup>-<name>.md".
#
# For initial setup, you only need to edit the first block of fields.
# Only "title" needs to be changed; delete "abbrev" if your title is short.
# Any other content can be edited, but be careful not to introduce errors.
# Some fields will be set automatically during setup if they are unchanged.
#
# Don't include "-00" or "-latest" in the filename.
# Labels in the form draft-<yourname>-<workgroup>-<name>-latest are used by
# the tools to refer to the current version; see "docname" for example.
#
# This template uses kramdown-rfc: https://github.com/cabo/kramdown-rfc
# You can replace the entire file if you prefer a different format.
# Change the file extension to match the format (.xml for XML, etc...)
#
###
title: "Extensible Delegation for DNS"
abbrev: "deleg"
category: std

docname: draft-homburg-deleg-latest
submissiontype: IETF  # also: "independent", "editorial", "IAB", or "IRTF"
number:
consensus: true
v: 3
area: int
workgroup: DNS Delegation
keyword:
 - Internet-Draft
 - DNS
 - Resolver
 - Delegation
 - Authoritative
 - Deployable
 - Extensible
venue:
  group: deleg
  type: Working Group
  mail: dd@ietf.org
  arch: https://mailarchive.ietf.org/arch/browse/dd/
  github: NLnetLabs/incremental-deleg

author:
 -
    fullname: Philip Homburg
    organization: NLnet Labs
    email: philip@nlnetlabs.nl
 -
    fullname: Tim Wicinski
    organization: Cox Communications
    email: tjw.ietf@gmail.com
 -
    fullname: Jesse van Zutphen
    organization: University of Amsterdam
    email: Jesse.vanZutphen@os3.nl
 -
    fullname: Willem Toorop
    organization: NLnet Labs
    email: willem@nlnetlabs.nl

normative:

informative:
    IDELEG4UNBOUND:
        target: https://github.com/NLnetLabs/unbound/tree/ideleg
        title: "A proof of concept implementation of incremental deleg"
        author:
          -
            name: Jesse van Zutphen
            ins: J. van Zutphen
          -
            name: Philip Homburg
            ins: P. Homburg
    JZUTPHEN:
        target: https://nlnetlabs.nl/downloads/publications/extensible-deleg-in-resolvers_2024-07-08.pdf
        title: "Extensible delegations in DNS Recursive resolvers"
        author:
          -
            name: Jesse van Zutphen
            ins: J. van Zutphen
    IDELEG4NSD:
        target: https://github.com/WP-Official/nsd
        title: "A proof of concept support for IDELEG in the NSD authoritative name server software"
        author:
          -
            name: Wouter Petri
            ins: W. Petri
    WPETRI:
        target: https://nlnetlabs.nl/downloads/publications/extensible-delegations-in-authoritative-nameservers_2025-02-09.pdf
        title: "Extensible delegations in authoritative nameservers"
        author:
          -
            name: Wouter Petri
            ins: W. Petri
    IDELEG4LDNS:
        target: https://github.com/NLnetLabs/ldns/tree/features/ideleg
        title: "A proof of concept support for IDELEG in the ldns DNS library and tools"
        author:
          -
            name: Willem Toorop
            ins: W. Toorop

--- abstract

This document proposes a mechanism for extensible delegations in the DNS.
The mechanism realizes delegations with resource record sets placed below a `_deleg` label in the apex of the delegating zone.
This authoritative delegation point can be aliased to other names using CNAME and DNAME.
This document proposes a new DNS resource record type, IDELEG, which is based on the SVCB and inherits extensibility from it.

IDELEG RRsets containing delegation information will be returned in the authority section in referral responses from supportive authoritative name servers.
Lack of support in the authoritative name servers, forwarders or other components, does not obstruct obtaining the delegation information for resolvers, as it is originally authoritative information that can be queried for directly.
None, mixed or full deployment of the mechanism on authoritative name servers are all fully functional, allowing for the mechanism to be incrementally deployed on the authoritative name servers.

--- middle

# Introduction

This document describes a delegation mechanism for the Domain Name System (DNS) {{!STD13}} that addresses several matters that, at the time of writing, are suboptimally supported or not supported at all.
These matters are elaborated upon in sections {{<signaling}}, {{<outsourcing}} and {{<dnssec-protection}}.
In addition, the mechanism described in this document aspires to be maximally deployable, which is elaborated upon in {{deployability}}.

## Signaling capabilities of the authoritative name servers {#signaling}

A new IDELEG resource record (RR) type is introduced in this document, which is based on and inherits the wire and presentation format from SVCB {{!RFC9460}}.
All Service Binding Mappings, as well as the capability signalling, that are specified in {{!RFC9461}} are also applicable to IDELEG, with the exception of the limitations on AliasMode records in {{Section 6 of !RFC9460}}.
Capability signalling of {{!RFC7858 (DNS over Transport Layer Protocol)}} (DoT), {{!RFC8484 (DNS Queries over HTTPS)}} and {{!RFC9250 (DNS over Dedicated QUIC Connections)}}, on default or alternative ports, can all be used as specified in {{!RFC9461}}.
The IDELEG RR type inherits its extensibility from the SVCB RR type, which is designed to be extensible to support future uses (such as keys for encrypting the TLS ClientHello {{?I-D.ietf-tls-esni}}.)

## *Note to the RFC Editor*: please remove this subsection before publication.

The name IDELEG is chosen to avoid confusion with {{?I-D.wesplaap-deleg}}.

## Outsourcing operation of the delegation {#outsourcing}

Delegation information is stored at an authoritative location in the zone with this mechanism.
Legacy methods to redirect this information to another location, possible under the control of another operator, such as (CNAME {{Section 3.6.2 of RFC1034}}) and DNAME {{!RFC6672}} remain functional.
One could even outsource all delegation operational practice to another party with a DNAME record on the `_deleg` label on the apex of the delegating zone.

Additional to the legacy methods, a delegation may be outsourced to a set of third parties by having RRs in AliasMode.
Unlike SVCB, IDELEG allows for more than a single IDELEG RR in AliasMode in an IDELEG RRset, enabling outsourcing a delegation to multiple different operators.

## DNSSEC protection of the delegation {#dnssec-protection}

With legacy delegations, the NS RRset at the parent side of a delegation as well as glue records for the names in the NS RRset are not authoritative and not DNSSEC signed.
An adversary that is able to spoof a referral response, can alter this information and redirect all traffic for the delegation to a rogue name server undetected.
The adversary can then perceive all queries for the redirected zone (Privacy concern) and alter all unsigned parts of responses (such as further referrals, which is a Security concern).

DNSSEC protection of delegation information prevents that, and is the only countermeasure that also works against on-path attackers.
At the time of writing, the only way to DNSSEC-validate and verify delegations at all levels in the DNS hierarchy is to revalidate delegations {{?I-D.ietf-dnsop-ns-revalidation}}, which is done after the fact and has other security concerns ({{Section 7 of ?I-D.ietf-dnsop-ns-revalidation}}).

Direct delegation information (provided by IDELEG RRs in ServiceMode) includes the hostnames of the authoritative name servers for the delegation as well as IP addresses for those hostnames.
Since the information is stored authoritatively in the delegating zone, it will be DNSSEC-signed if the zone is signed.
When the delegation is outsourced, then it's protected when the zones providing the aliasing resource records *and* the zones serving the targets of the aliases are all DNSSEC-signed.

## Maximize ease of deployment {#deployability}

Delegation information is stored authoritatively within the delegating zone.
No semantic changes as to what zones are authoritative for what data are needed.
As a consequence, existing DNS software, such as authoritative name servers and DNSSEC signing software, can remain unmodified.
Unmodified authoritative name server software will serve the delegation information when queried for.
Unmodified signers will sign the delegation information in the delegating zone.
Support for IDELEG is only required for functionalities following delegations (like recursive resolvers), but they do not need of the components it queries.
None, mixed or full deployment of the mechanism on authoritative name servers are all fully functional, allowing for the mechanism to be incrementally deployed on the authoritative name servers.

## Terminology

{::boilerplate bcp14-tagged}

This document follows terminology as defined in {{?BCP219}}.

Throughout this document we will also use terminology with the meaning as defined below:

{: vspace="0"}
Deleg:
: The delegation mechanism as specified in this document.

IDELEG delegation:
: A delegation as specified in this document

Legacy delegations:
: The way delegations are done in the DNS traditionally as defined in {{!STD13}}.

Delegating zone:
: The zone in which the delegation is administered.
  Sometimes also called the "parent zone" of a delegation.

Subzone:
: The zone that is delegated to from the delegating zone.

Delegating name:
: The name which realizes the delegation.
  In legacy delegations, this name is the same as the name of the subzone to which the delegation refers.
  Delegations described in this document are provided with a different name than the zone that is delegated to.
  If needed we differentiate by explicitly calling it IDELEG delegation name or legacy delegation name.

Deleg query:
: An explicit query for IDELEG RRset at the delegating name as used for IDELEG delegations.

Delegation point:
: The location in the delegating zone where the RRs are provided that make up the delegation.
  In legacy delegations, this is the parent side of the zone cut and has the same name as the subzone.
  With deleg, this is the location given by the delegating name.
  If needed we differentiate by explicitly calling it IDELEG delegation point or legacy delegation point.

Triggering query:
: The query on which resolution a recursive resolver is working.

Target zone:
: The zone for which the authoritative servers, that a resolver contacts while iterating, are authoritative.

# The IDELEG resource record type {#the-deleg-resource-record-type}

The IDELEG RR type is a variant of SVCB {{!RFC9460}} for use with resolvers to perform iterative resolution ({{Section 5.3.3 of RFC1034}}).
The IDELEG type requires registration in the "Resource Record (RR) TYPEs" registry under the "Domain Name System (DNS) Parameters" registry group (see {{deleg-rr-type (IDELEG RR type)}}).
The protocol-specific mapping specification for iterative resolutions are the same as those for "DNS Servers" {{!RFC9461}}.

{{Section 2.4.2 of !RFC9460}} states that SVCB RRsets SHOULD only have a single RR in AliasMode, and that if multiple AliasMode RRs are present, clients or recursive resolvers SHOULD pick one at random.
Different from SVCB ({{Section 2.4.2 of RFC9460}}), IDELEG allows for multiple AliasMode RRs to be present in a single IDELEG RRset.
Note however that the target of an IDELEG RR in AliasMode is an SVCB RRset for the "dns" service type adhering fully to the Service Binding Mapping for DNS Servers as specified in {{!RFC9461}}.

{{Section 2.4.1 of !RFC9460}} states that within an SVCB RRset, all RRs SHOULD have the same mode, and that if an RRset contains a record in AliasMode, the recipient MUST ignore any ServiceMode records in the set.
Different from SVCB, mixed ServiceMode and AliasMode RRs are allowed in an IDELEG RRset.
When a mixed ServiceMode and AliasMode IDELEG RRset is encountered by a resolver, the resolver first picks one of the AliasMode RRs or all ServiceMode RRs, giving all ServiceMode RRs equal weight as each single AliasMode RR.
When the result of that choice is an AliasMode RR, then that RR is followed and the resulting IDELEG RRset is reevaluated.
When the result of that choice is all ServiceMode RRs, then within that set the resolver adheres to the ServicePriority value.

At the delegation point (for example `customer._deleg.example.`), the host names of the authoritative name servers for the subzone, are given in the TargetName RDATA field of IDELEG records in ServiceMode.
Port Prefix Naming {{Section 3 of RFC9461}} is not used at the delegation point, but MUST be used when resolving the aliased-to name servers with IDELEG RRs in AliasMode.

# Delegation administration

An IDELEG delegation is realized with an IDELEG Resource Record set (RRset) {{!RFC9460}} below a specially for the purpose reserved label with the name `_deleg` at the apex of the delegating zone.
The `_deleg` label scopes the interpretation of the IDELEG records and requires registration in the "Underscored and Globally Scoped DNS Node Names" registry (see {{node-name (\_deleg Node Name)}}).
The full scoping of delegations includes the labels that are **below** the `_deleg` label and those, together with the name of the delegating domain, make up the name of the subzone to which the delegation refers.
For example, if the delegating zone is `example.`, then a delegation to subzone `customer.example.` is realized by a IDELEG RRset at the name `customer._deleg.example.` in the parent zone.
A fully scoped delegating name (such as `customer._deleg.example.`) is referred to further in this document as the "delegation point".

Note that if the delegation is outsourcing to a single operator represented in a single IDELEG RR, it is RECOMMENDED to refer to the name of the operator's IDELEG RRset with a CNAME on the delegation point instead of a IDELEG RR in AliasMode {{Section 10.2 of !RFC9460}}.

## Examples

### One name server within the subzone

~~~~
$ORIGIN example.
@                 IN  SOA    ns zonemaster ...
customer1._deleg  IN  IDELEG 1 ( ns.customer1
                                 ipv4hint=198.51.100.1,203.0.113.1
                                 ipv6hint=2001:db8:1::1,2001:db8:2::1
                               )
~~~
{: #zone-within title="One name server within the subzone"}

### Two name servers within the subzone

    $ORIGIN example.
    @                 IN  SOA    ns zonemaster ...
    customer2._deleg  IN  IDELEG 1 ns1.customer2 ( ipv4hint=198.51.100.1
                                                   ipv6hint=2001:db8:1::1
                                                 )
                      IN  IDELEG 1 ns2.customer2 ( ipv4hint=203.0.113.1
                                                   ipv6hint=2001:db8:2::1
                                                 )
{: #zones-within title="Two name servers within the subzone"}

### Outsourced to an operator

    $ORIGIN example.
    @                 IN  SOA   ns zonemaster ...
    customer3._deleg  IN  CNAME _dns.ns.operator1
{: #outsourced-cname title="Outsourced with CNAME"}

Instead of using CNAME, the outsourcing could also have been accomplished with an IDELEG RRset with a single IDELEG RR in AliasMode.
The configuration below is operationally equivalent to the CNAME configuration above.
It is RECOMMENDED to use a CNAME over an IDELEG RRset with a single IDELEG RR in AliasMode ({{Section 10.2 of !RFC9460}}).
Note that an IDELEG RRset refers with TargetName to a DNS service {{!RFC9461}}, which will be looked up using Port Prefix Naming {{Section 3 of RFC9461}}, but that an CNAME refers to the domain name of the target SVCB RRset instead (or CNAME) which may have a `_dns` prefix.

    $ORIGIN example.
    @                 IN  SOA    ns zonemaster ...
    customer3._deleg  IN  IDELEG 0 ns.operator1
{: #outsourced-svcb title="Outsourced with an AliasMode IDELEG RR"}

The operator SVCB RRset could for example be:

    $ORIGIN operator1.example.
    @                 IN  SOA    ns zonemaster ...
    _dns.ns           IN  SVCB   1 ns ( alpn=h2,dot,h3,doq
                                        ipv4hint=192.0.2.1
                                        ipv6hint=2001:db8:3::1
                                        dohpath=/q{?dns}
                                      )
                      IN  SVCB   2 ns ( ipv4hint=192.0.2.2
                                        ipv6hint=2001:db8:3::2
                                      )
    ns                IN  AAAA   2001:db8:3::1
                      IN  AAAA   2001:db8:3::2
                      IN  A      192.0.2.1
                      IN  A      192.0.2.2
{: #operator-zone title="Operator zone"}

### DNSSEC-signed name servers within the subzone

~~~
$ORIGIN
@                 IN  SOA    ns zonemaster ...
                  IN  RRSIG  SOA ...
                  IN  DNSKEY 257 3 15 ...
                  IN  RRSIG  DNSKEY ...
                  IN  NS     ns.example.
                  IN  RRSIG  NS ...
                  IN  NSEC   customer5._deleg NS SOA RRSIG NSEC DNSKEY
                  IN  RRSIG  NSEC ...

customer5._deleg  IN  IDELEG 1 ns.customer5 alpn=h2,h3 (
                                            ipv4hint=198.51.100.5
                                            ipv6hint=2001:db8:5::1
                                            dohpath=/dns-query{?dns}
                                            )
                  IN  RRSIG  IDELEG ...
                  IN  NSEC   customer7._deleg RRSIG NSEC IDELEG
                  IN  RRSIG  NSEC ...

customer7._deleg  IN  CNAME  customer5._deleg
                  IN  RRSIG  CNAME ...
                  IN  NSEC   customer5 CNAME RRSIG NSEC
                  IN  RRSIG  NSEC ...

customer5         IN  NS     ns.customer5
ns.customer5      IN  A      198.51.100.5
                  IN  AAAA   2001:db8:5::1
customer5         IN  DS     17405 15 2 ...
                  IN  RRSIG  DS ...
                  IN  NSEC   customer6 NS DS RRSIG NSEC
                  IN  RRSIG  NSEC ...

customer6         IN  NS     ns.customer6
ns.customer6      IN  A      203.0.113.1
                  IN  AAAA   2001:db8:6::1
customer6         IN  DS     ...
                  IN  RRSIG  DS ...
                  IN  NSEC   customer7 NS DS RRSIG NSEC
                  IN  RRSIG  NSEC ...

customer7         IN  NS     ns.customer5
                  IN  DS     ...
                  IN  RRSIG  DS ...
                  IN  NSEC   example. NS DS RRSIG NSEC
                  IN  RRSIG  NSEC ...
~~~
{: #dnssec-zone title="DNSSEC-signed deleg zone"}

`customer5.example.` is delegated to in an extensible way and `customer6.example.` is delegated only in a legacy way.
`customer7.example.`'s delegation is outsourced to customer5's delegation.

The delegation signals that the authoritative name server supports DoH.
`customer5.example.`, `customer6.example.` and `example.` are all DNSSEC-signed.
The DNSSEC authentication chain links from `example.` to `customer5.example.` in the for DNSSEC conventional way with the signed `customer5.example. DS` RRset in the `example.` zone.
Also, `customer6.example.` is linked to from `example.` with the signed `customer6.example. DS` RRset in the `example.` zone.

Note that both `customer5.example.` and `customer6.example.` have legacy delegations in the zone as well.
It is important to have those legacy delegations to maintain support for legacy resolvers, that do not support deleg.
DNSSEC signers SHOULD construct the NS RRset and glue for the legacy delegation from the IDELEG RRset.

# Authoritative name server support

Deleg supporting authoritative name servers include the IDELEG delegation information (or the NSEC(3) records showing the non-existence) in the authority section of referral responses to legacy DNS queries.
For example, querying the zone from {{dnssec-zone}} for `www.customer5.example. A`, will return the following referral response:

~~~
;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 54349
;; flags: qr ; QUERY: 1, ANSWER: 0, AUTHORITY: 5, ADDITIONAL: 2
;; QUESTION SECTION:
;; www.customer5.example.       IN      A

;; ANSWER SECTION:

;; AUTHORITY SECTION:
customer5.example.      3600    IN      NS      ns.customer5.example.
customer5.example.      3600    IN      DS      ...
customer5.example.      3600    IN      RRSIG   DS ...
customer5._deleg.example.       3600    IN      IDELEG 1 (
                ns.customer5.example. alpn=h2,h3
                ipv4hint=198.51.100.5 ipv6hint=2001:db8:5::1
                dohpath=/dns-query{?dns}
                )
customer5._deleg.example.       3600    IN      RRSIG   IDELEG ...

;; ADDITIONAL SECTION:
ns.customer5.example.   3600    IN      A       198.51.100.5
ns.customer5.example.   3600    IN      AAAA    2001:db8:5::1

;; Query time: 0 msec
;; EDNS: version 0; flags: do ; udp: 1232
;; SERVER: 192.0.2.53
;; WHEN: Mon Feb 24 20:36:25 2025
;; MSG SIZE  rcvd: 456
~~~
{: #deleg-response title="An deleg referral response"}

The referral response in {{deleg-response}} includes the signed IDELEG RRset in the authority section.

As another example, querying the zone from {{dnssec-zone}} for `www.customer6.example. A`, will return the following referral response:

~~~
;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 36574
;; flags: qr ; QUERY: 1, ANSWER: 0, AUTHORITY: 9, ADDITIONAL: 2
;; QUESTION SECTION:
;; www.customer6.example.       IN      A

;; ANSWER SECTION:

;; AUTHORITY SECTION:
customer6.example.      3600    IN      NS      ns.customer6.example.
customer6.example.      3600    IN      DS      ...
customer6.example.      3600    IN      RRSIG   DS ...
customer5._deleg.example.       1234    IN      NSEC    (
                customer7._deleg.example.  RRSIG NSEC IDELEG )
customer5._deleg.example.       1234    IN      RRSIG   NSEC ...
example.        1234    IN      NSEC    (
                customer5._deleg.example.  NS SOA RRSIG NSEC DNSKEY )
example.        1234    IN      RRSIG   NSEC ...

;; ADDITIONAL SECTION:
ns.customer6.example.   3600    IN      A       203.0.113.1
ns.customer6.example.   3600    IN      AAAA    2001:db8:6::1

;; Query time: 0 msec
;; EDNS: version 0; flags: do ; udp: 1232
;; SERVER: 192.0.2.53
;; WHEN: Tue Feb 25 10:23:53 2025
;; MSG SIZE  rcvd: 744
~~~
{: #no-incr-deleg-response title="Referral response without deleg"}

Next to the legacy delegation, the deleg supporting authoritative returns the NSEC(3) RRs needed to show that there was no IDELEG delegation in the referral response in {{no-incr-deleg-response}}.

Querying the zone from {{dnssec-zone}} for `www.customer7.example. A`, will return the following referral response:

~~~
;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 9456
;; flags: qr ; QUERY: 1, ANSWER: 0, AUTHORITY: 7, ADDITIONAL: 2
;; QUESTION SECTION:
;; www.customer7.example.       IN      A

;; ANSWER SECTION:

;; AUTHORITY SECTION:
customer7.example.      3600    IN      NS      ns.customer5.example.
customer7.example.      3600    IN      DS      ...
customer7.example.      3600    IN      RRSIG   DS ...
customer7._deleg.example.       3600    IN      CNAME   (
                customer5._deleg.example. )
customer7._deleg.example.       3600    IN      RRSIG   CNAME ...
customer5._deleg.example.       3600    IN      IDELEG   1 (
                ns.customer5.example. alpn=h2,h3
                ipv4hint=198.51.100.5 ipv6hint=2001:db8:5::1 )
customer5._deleg.example.       3600    IN      RRSIG   IDELEG ...

;; ADDITIONAL SECTION:
ns.customer5.example.   3600    IN      A       198.51.100.5
ns.customer5.example.   3600    IN      AAAA    2001:db8:5::1

;; Query time: 0 msec
;; EDNS: version 0; flags: do ; udp: 1232
;; SERVER: 192.0.2.53
;; WHEN: Tue Feb 25 10:55:07 2025
;; MSG SIZE  rcvd: 593
~~~
{: #alias-response title="Aliasing referral response"}

The delegation of `customer7.example.` is aliased to the one that is also used by `customer5.example.`
Since both delegations are in the same zone, the authoritative name server for `example.` returns both the CNAME realising the alias, as well as the IDELEG RRset which is the target of the alias in {{alias-response}}.
In other cases a returned CNAME or IDELEG RR in AliasMode may need further chasing by the resolver.
<!-- TODO: Add an AliasMode referral without expansion within the zone -->

With unsigned zones, only if an IDELEG delegation exists, the IDELEG RRset (or CNAME) will be present in the authority section of referral responses.
<!-- TODO: Add a referral response for an unsigned zone -->
If there is no IDELEG delegation, then the IDELEG RRset (or CNAME) is simply absent from the authority section and the referral response is indistinguishable from an non deleg supportive authoritative.
<!-- TODO: Add a non deleg referral response for an unsigned zone -->

## Resolver behavior {#behavior-with-auth-support}

Deleg supporting authoritative name servers will include the IDELEG delegation information (or the NSEC(3) records showing the non-existence) in the authority section of referral responses.
For an unsigned zone, an deleg supporting authoritative cannot return that an IDELEG delegation is absent (because of lack of an authenticated denial of existence), however with support from the served zone (the zone has the Resource Record provisioned `*._deleg IN IDELEG 0 .`), the authoritative name server can signal support also for unsigned zones (see {{controlled-support-registration (Controlled support registration)}}).

When the authority section of a referral response contains an IDELEG RRset or a CNAME record on the IDELEG delegation name, or valid NSEC(3) RRs showing the non-existence of such an IDELEG or CNAME RRset, then the resolver SHOULD register that the contacted authoritative name server supports deleg for the duration indicated by the TTL for that IDELEG, CNAME or NSEC(3) RRset, adjusted to the resolver's TTL boundaries, but only if it is longer than any already registered duration.

For example, in {{deleg-response}}, the IDELEG RRset at the IDELEG delegation point has TTL 3600.
The resolver should register that the contacted authoritative name server supports deleg for (at least) 3600 seconds (one hour).
All subsequent queries to that authoritative name server SHOULD NOT include deleg queries to be send in parallel.

If the authority section contains more than one RRset making up the IDELEG delegation, then the RRset with the longest TTL MUST be taken to determine the duration for which deleg support is registered.

For example, in {{alias-response}}, both a CNAME and an IDELEG RRset for the IDELEG delegation are included in the authority section.
The longest TTL must be taken for deleg support registration, though because the TTL of both RRsets is 3600, it does not matter in this case.

With DNSSEC-signed zones, support is apparent with all referral responses.
With unsigned zones, support is apparent only from referral responses for which an IDELEG delegation exists, unless the zone has the Resource Record `*._deleg IN IDELEG 0 .` provisioned (see {{controlled-support-registration (Controlled support registration)}}).

If the resolver knows that the authoritative name server supports deleg, *and* a DNSSEC-signed zone is being served, then all referrals SHOULD contain either an IDELEG delegation, or NSEC(3) records showing that the delegation does not exist.
If a referral is returned that does not contain an IDELEG delegation nor an indication that it does not exist, then the resolver MAY register that authoritative server does not support deleg and MUST send an additional deleg query to find the delegation (or denial of its existence) (see also {{without-support (Resolving without authoritative name server support)}}).

## Controlled support registration {#controlled-support-registration}

An IDELEG RRset on an IDELEG delegation point, with an IDELEG RR in AliasMode, aliasing to the root zone, MUST be interpreted to mean that the legacy delegation information MUST be used to follow the referral.
All service parameters for such AliasMode (aliasing to the root) IDELEG RRs on the IDELEG delegation point, MUST be ignored.

For example, such an IDELEG RRset registered on the wildcard below the `_deleg` label on the apex of a zone, can signal that legacy DNS referrals MUST be used for both signed and *unsigned* zones:

~~~
$ORIGIN example.
@                 IN  SOA   ns zonemaster ...
*._deleg   86400  IN  IDELEG 0 .
customer1._deleg  IN  IDELEG 1 ( ns.customer1
                                 ipv4hint=198.51.100.1,203.0.113.1
                                 ipv6hint=2001:db8:1::1,2001:db8:2::1
                               )
customer3._deleg  IN  CNAME _dns.ns.operator1
~~~
{: #wildcard-deleg title="Wildcard IDELEG delegation to control duration of detected support"}

Resolvers SHOULD register that an authoritative name server supports deleg, if such an IDELEG RRset is returned in the authority section of referral responses, for the duration of the TTL if the IDELEG RRset, adjusted to the resolver's TTL boundaries, but only if it is longer than any already registered duration.
Note that this will also be included in referral responses for unsigned zones, which would otherwise not have signalling of deleg support by the authoritative name server.

Also, signed zones need fewer RRs to indicate that no IDELEG delegation exists.
The wildcard expansion already shows the closest encloser (i.e. `_deleg.<apex>`), so only one additional NSEC(3) is needed to show non-existence of the queried-for name below the closest encloser.

This method of signalling that the legacy delegation MUST be used, is RECOMMENDED.

# Resolving without authoritative name server support {#without-support}

In two cases, resolvers do not need to do additional processing.

1. As part of the processing a recursive resolver does, it learns where the zone boundaries are in the DNS name tree.
   If the triggering query name is already known to be the apex of a zone, then no further delegation point probing will need to be done for this name (subject to the TTL of this information).

2. If a resolver encounters a non-referral response, then no delegations are involved and no further delegation probing is needed for this name (subject to the TTL of this information).

If a resolver encounters an referral that does not contain an IDELEG delegation nor an indication that it does not exist, then the resolver MUST find out wether the queried zone contains IDELEG delegations at all.

1. For DNSSEC signed zones, a direct query for the IDELEG delegation information suffices (see {{deleg-query (The deleg query)}}).

2. For unsigned zones, if unknown, the presence of the `_deleg` label at the zone's apex needs to be detected in addition to a direct query for the IDELEG delegation information (see {{presence (`_deleg` label presence)}}).

Sub section {{additional-summary (Summary)}} contains an overview summerizing sub sections {{deleg-query}} and {{presence}}

## The deleg query {#deleg-query}

The deleg query name is constructed by concatenating the first label below the part that the triggering query name has in common with the target zone, a `_deleg` label and the name of the target zone.
For example if the triggering query is `www.customer.example.` and the target zone `example.`, then the deleg query name is `customer._deleg.example.`
For another example, if the triggering query is `www.faculty.university.example.` and the target zone `faculty.university.example.` then the deleg query name is `www._deleg.faculty.university.example.`

DNAME, CNAME and IDELEG in AliasMode processing happens as before, though note that when following an IDELEG RR in AliasMode the target RR type is SVCB (see {{the-deleg-resource-record-type}}).
The eventual deleg query response, after following all redirections caused by DNAME, CNAME and AliasMode IDELEG RRs, has three possible outcomes:

1. An IDELEG RRset in ServiceMode is returned in the response's answer section containing the delegation for the subzone.

   The IDELEG RRs in the RRset MUST be used to follow the referral.
   The TargetName data field in the IDELEG RRs in the RRset MUST be used as the names for the name servers to contact for the subzone, and the ipv4hint and ipv6hint parameters MUST be used as the IP addresses for the TargetName in the same IDELEG RR.

   The NS RRset and glue, from the referral response, MUST NOT be used, but the signed DS record (or NSEC(3) records indicating that there was no DS) MUST be used in linking the DNSSEC authentication chain as which would conventionally be done with DNSSEC as well.

2. The deleg query name does not exist (NXDOMAIN).

   There is no IDELEG delegation for the subzone, and the referral response for the legacy delegation MUST be processed as would be done with legacy DNS and DNSSEC processing.

   When the query was for an DNSSEC signed zone, the NXDOMAIN response will expose whether or not the `_deleg` label exists at the zone's apex.
   If it does not exist, this should be registered for the duration of the maximum of the TTL of the NSEC(3) covering the `_deleg` label and the minimum rdata field of the SOA for the zone, adjusted to the boundaries for TTL values that the resolver has ({{Section 4 of !RFC8767}}).
   For this period, deleg queries to this zone MUST NOT be made (see also {{presence}}).

3. The deleg query name does exist, but resulted in a NOERROR no answer response (also known as a NODATA response).

   If the legacy query, did result in a referral for the same number of labels as the subdomain that the deleg query was for, then there was no IDELEG delegation for the subzone, and the referral response for the legacy delegation MUST be processed as would be done with legacy DNS and DNSSEC processing.

   Otherwise, the subzone may be more than one label below the delegating zone.

   A new deleg query MUST be spawned, matching the zone cut of the initial referral response.
   For example if the triggering query is `www.university.ac.example.` and the target zone `example.`, and the legacy response contained an NS RRset for `university.ac.example.`, then the deleg query name is `university.ac._deleg.example.`
   The response to the new deleg query MUST be processed as described above, as if it was the initial deleg query.

   If the legacy query was sent minimised and needs a followup query, then parallel to that followup query a new deleg query will be sent, adding a single label to the previous deleg query name.
   For example if the triggering query is `www.university.ac.example.` and the target zone is `example.` and the minimised legacy query name is `ac.example.` (which also resulted in a NOERROR no answer response), then the deleg query to be sent along in parallel with the followup legacy query will become `university.ac._deleg.example.`
   Processing of the responses of those two new queries will be done as described above.

## `_deleg` label presence {#presence}

Absence of the `_deleg` label in a zone is a clear signal that the zone does not contain any IDELEG delegations.
Recursive resolvers SHOULD NOT send any additional deleg queries for zones for which it is known that it does not contain the `_deleg` label at the apex.
The state regarding the presence of the `_deleg` label within a resolver can be "unknown", "known not to be present", or "known to be present".

The state regarding the presence of the `_deleg` label can be deduced from the response of the deleg query, if the target zone is signed with DNSSEC.
**No** additional queries are needed.
If the target zone is unsigned, the procedure as described in the remainder of this section SHOULD be followed.

### Test `_deleg` label presence (unsigned zones only)

When the presence of a `_deleg` label is "unknown", a `_deleg` presence test query SHOULD be sent in parallel to the next query for the unsigned target zone (though not when the target name server is known to support _deleg, which is discussed in {{authoritative-name-server-support}}).
The query name for the test query is the `_deleg` label prepended to the apex of zone for which to test presence, with query type NS.

The testing query can have three possible outcomes:

1. The `_deleg` label does not exist within the zone, and an NXDOMAIN response is returned.

   The non-existence of the `_deleg` label MUST be registered for the duration indicated by the "minimum" RDATA field of the SOA resource record in the authority section, adjusted to the boundaries for TTL values that the resolver has ({{Section 4 of !RFC8767}}).
   For the period the non-existence of the `_deleg` label is cached, the label is "known not to be present" and the resolver SHOULD NOT send any (additional) deleg queries.

2. The `_deleg` label does exist within the zone but contains no data.
   A NOERROR response is returned with no RRs in the answer section.

   The existence of the `_deleg` name MUST be cached for the duration indicated by the "minimum" RDATA field of the SOA resource record in the authority section, adjusted to the resolver's TTL boundaries.
   For the period the existence of the empty non-terminal at the `_deleg` label is cached, the label is "known to be present".

3. The `_deleg` label does exist within the zone, but is a delegation.
   A NOERROR legacy referral response is returned with an NS RRset in the authority section.

   The resolver MUST record that the zone does not have valid IDELEG delegations deployed for the duration indicated by the NS RRset's TTL value, adjusted to the resolver's TTL boundaries.
   For the period indicated by the NS RRset's TTL value, the zone is considered to **not** to have valid IDELEG delegations, and MUST NOT send any (additional) deleg queries.

## Summary {#additional-summary}

Table {{xtraqueries}} provides an overview of when extra queries, following a non-IDELEG referral response, are sent.

|---|------------|--------------|-------------------|---|------------------------------|-------------------------|
|   | apex query | auth support | `_deleg` presence |   | `<sub>._deleg.<apex> IDELEG` | `_deleg.<apex> A`       |
|:-:|:----------:|:------------:|:-----------------:|---|:----------------------------:|:-----------------------:|
| 1 | Yes        | \*           | \*                |   |                              |                         |
|---|------------|--------------|-------------------|---|------------------------------|-------------------------|
| 2 | No         | \*           | No                |   |                              |                         |
|---|------------|--------------|-------------------|---|------------------------------|-------------------------|
| 3 | No         | Yes          | \*                |   |                              |                         |
|---|------------|--------------|-------------------|---|------------------------------|-------------------------|
| 4 | No         | Unknown      | Yes               |   | X                            |                         |
|---|------------|--------------|-------------------|---|------------------------------|-------------------------|
| 5 | No         | Unknown      | Unknown           |   | X                            | only for unsigned zones |
|---|------------|--------------|-------------------|---|------------------------------|-------------------------|
{: #xtraqueries title="Additional queries to an non-IDELEG referral response"}

The three headers on the left side of the table mean the following:

{: vspace="0"}
apex query:
: Whether the query is for the apex of the target zone.
  "Yes" means an apex query, "No" means a query below the apex which may be delegated

auth support:
: Whether or not the target authoritative server supports incremental deleg.
  "Yes" means it supports it and "Unknown" means support is not detected.
  "\*" means it does not matter

`_deleg` presence:
: Whether or not the `_deleg` label is present in the target zone (and thus incremental delegations)

On the right side of the table are the additional follow-up queries, to be sent in response to non-IDELEG referrals.
The `_deleg` presence test query (most right column) only needs to be sent to unsigned target zones, because its non-existence will be shown in the NSEC(3) records showing the non-existence of the incremental delegation (second from right column).

If the query name is the same as the apex of the target zone, no additional queries need to be sent (Row 1).
If the `_deleg` label is known not to exist in the target zone (Row 2) or if the target name server is known to support incremental deleg (Row 3), no additional queries need to be sent.
Only if it is unknown that the target name server supports incremental deleg, and the `_deleg` label is known to exist in the target zone (Row 4) or it is not known whether or not the `_deleg` label exists (Row 5), and additional deleg query needs to be sent.
If the target zone is unsigned, presence of the `_deleg` label needs to be tested explicitly (Row 5).

### Reduced latency

Latency can be reduced with one roundtrip when the deleg query is sent in parallel to the legacy query.
This will induce more additional queries since authoritative name server support (eliminating the need to send deleg queries), is detected from the legacy query.

# Priming queries {#priming-queries}

Some zones, such as the root zone, are targeted directly from hints files.
Information about which authoritative name servers and with capabilities, MAY be provided in an IDELEG RRset directly at the `_deleg` label under the apex of the zone.
Priming queries from an deleg supporting resolver, MUST send an `_deleg.<apex> IDELEG` query in parallel to the legacy `<apex> NS` query and process the content as if it was found through an referral response.

# Limitations

The presence of the `_deleg` label in the delegation information reduces that maximum length of a domain name for a zone to 248 bytes.
Note that names within zones are not limited and can still be 255 bytes.

# How does the protocol described in this draft meet the requirements

This section will discuss how deleg meets the requirements for a new delegation mechanism as described in {{?I-D.ietf-deleg-requirements-02}}

+ H1. DELEG must not disrupt the existing registration model of domains.

  The existing zone structure including the concept of delegations from
  a parent zone to a child zone is left unchanged.

+ H2. DELEG must be backwards compatible with the existing ecosystem.

  The new delegations do not interfere with legacy software.

  The behavior of deleg supporting resolvers includes a fallback to NS
  records if no IDELEG delegation is present (See {{deleg-query}}).

+ H3. DELEG must not negatively impact most DNS software.

  Deleg introduces a new RR type.
  Software that parses zone file format needs to be changed to support the new
  type.
  Though unknown type notation {{!RFC3597}} can be used in some cases if no support for the new RR type is present.
  Existing authoritatives can serve IDELEG zones (though less efficiently), existing signers can sign IDELEG zones, existing diagnostic tools can query IDELEG zones.
  Non-recursive DNSSEC validators can operate independently from (possibly legacy) recursive resolvers.

+ H4. DELEG must be able to secure delegations with DNSSEC.

  IDELEG delegations as described in this document are automatically secured with DNSSEC
  (if the parent zone is signed). A replacement for DS records is described in {{?I-D.homburg-deleg-incremental-dnssec}}.

+ H5. DELEG must support updates to delegation information with the same relative ease as currently exists with NS records.

  IDELEG delegations are affected by TTL like any other
  DNS record.

+ H6. DELEG must be incrementally deployable and not require any sort of flag day of universal change.

  IDELEG zones can be added without upgrading authoritatives.
  IDELEG zones still work with old resolvers and validators.
  Basically any combination of old and new should work, though with
  reduced efficiency for some combinations.

+ H7. DELEG must allow multiple independent operators to simultaneously serve a zone.

  Deleg allows for multiple IDELEG records. This allows
  multiple operators to serve the zone.

+ S1. DELEG should facilitate the use of new DNS transport mechanisms

  New transports are already defined for the DNS mode of SVCB ({{!RFC9461}}).
  The same parameters are used for IDELEG.

+ S2. DELEG should make clear all of the necessary details for contacting a service

  Most of the needed SVCB parameters are already defined in existing standards.
  The exception is a replacement for the DS records, which is described in {{?I-D.homburg-deleg-incremental-dnssec}}.

+ S3. DELEG should minimize transaction cost in its usage.

  Assuming Qname-minimisation, there are no extra queries needed in most cases
  if the authoritative name server has deleg support. The exception
  is when the parent zone is not signed and has no IDELEG records.
  In that case, one extra query is needed when the parent zone is first
  contacted (and every TTL).

  Additional queries may be needed to resolve aliases.

+ S4. DELEG should simplify management of a zone's DNS service.

  Zone management can be simplified using the alias mode of IDELEG.
  This allows the zone operator to change the details of the delegation
  without involving the parent zone.

  Draft {{?I-D.homburg-deleg-incremental-dnssec}} defines the dnskeyref parameter which offers the same simplification for DNSSEC delegations.

+ S5. DELEG should allow for backward compatibility to the conventional NS-based delegation mechanism.

  NS records and glue can be extracted from the IDELEG record assuming no aliasing is used.

  The ds parameter in {{?I-D.homburg-deleg-incremental-dnssec}} has the same value as the rdata of a DS record.

+ S6. DELEG should be extensible and allow for the easy incremental addition of new delegation features after initial deployment.

  SVCB-style records are extensible by design.

+ S7. DELEG should be able to convey a security model for delegations stronger than currently exists with DNSSEC.

  IDELEG delegations are protected by DNSSEC, unlike
  NS records at the parent zone.

# Implementation Status

**Note to the RFC Editor**: please remove this entire section before publication.

We are using RR type code 65280 for experiments.

Jesse van Zutphen has built a proof of concept implementation supporting IDELEG delegations as specified in a previous version of this document {{?I-D.homburg-deleg-incremental-deleg-00}} for the Unbound recursive resolver as part of his master thesis for the Security and Network Engineering master program of the University of Amsterdam {{JZUTPHEN}}.
Jesse's implementation has been adapted to query for the IDELEG RR types (with code point 65280).
This version is available in the `ideleg` branch of the `NLnetLabs/unbound` github repository {{IDELEG4UNBOUND}}.
Note that this implementation does not yet support {{behavior-with-auth-support (optimized behaviour)}}, and also does not yet follow AliasMode IDELEG RRs.

The ldns DNS library and tools software has been extended with support for IDELEG, which is available in the `features/ideleg` branch of the `NLnetLabs/ldns` github repository {{IDELEG4LDNS}}.
This includes support for IDELEG in the DNS lookup utility `drill`, as well as in the DNSSEC zone signer `ldns-signzone` and all other tools and examples included with the ldns software.

Wouter Petri has built a proof of concept support for IDELEG in the NSD authoritative name server software as part of a research project for the Security and Network Engineering master program of the University of Amsterdam {{WPETRI}}.
The source code of his implementation is available on github {{IDELEG4NSD}}.

Wouter's implementation is serving the `ideleg.net.` domain, containing a variety of different IDELEG delegations, for evaluation purposes.
We are planning to provide information about the deployment, including what software to evaluate these delegations, at [http://ideleg.net/](http://ideleg.net/), hopefully before the [IETF 122 in Bangkok](https://datatracker.ietf.org/meeting/122/proceedings).

# Security Considerations

Deleg moves the location of  referral information to a unique  location that currently exists. However, as this is a new approach, thought must be given to usage.   There must be some checks to ensure that the registering a `_deleg` subdomain happens at the time the domain is provisioned. The same care needs to be addressed when a domain is de-provisioned that the `_deleg` is removed.  This is similar to what happens to A/AAAA glue records for NS records deployed in parent zones.

While the recommendation is to deploy DNSSEC with deleg, it is not mandatory.  However, using deleg with unsigned zones can create possibilities of domain hijackings. This could  be hard to detect when not speaking directly to the authoritative name server.
This risk of domain hijacking is not expected to increase significantly compared to the situation without deleg.

There are bound to be other considerations.


# IANA Considerations

## IDELEG RR type {#deleg-rr-type}

IANA is requested to update the "Resource Record (RR) TYPEs" registry under the "Domain Name System (DNS) Parameters" registry group as follows:

|--------|-------|------------|-------------------|
| TYPE   | Value | Meaning    | Reference         |
|--------|:------|:-----------|-------------------|
| IDELEG | TBD   | Delegation | \[this document\] |
|--------|-------|------------|-------------------|

## \_deleg Node Name {#node-name}

Per {{?RFC8552}}, IANA is requested to add the following entry to the DNS "Underscored and Globally Scoped DNS Node Names" registry:


|---------|-------------|-------------------|
| RR Type | \_NODE NAME | Reference         |
|---------|:------------|-------------------|
| IDELEG  | \_deleg     | \[this document\] |
|---------|-------------|-------------------|
{: title="Entry in the Underscored and Globally Scoped DNS Node Names registry"}

--- back

# Acknowledgments
{:numbered="false"}

The idea to utilize SVCB based RRs to signal capabilities was first proposed by Tim April in {{?I-D.tapril-ns2}}.

The idea to utilize SVCB for IDELEG delegations (and also the idea described in this document) emerged from the DNS Hackathon at the IETF 118.
The following participants contributed to this brainstorm session: Vandan Adhvaryu, Roy Arends, David Blacka, Manu Bretelle, Vladimír Čunát, Klaus Darilion, Peter van Dijk, Christian Elmerot, Bob Halley, Philip Homburg, Shumon Huque, Shane Kerr, David C Lawrence, Edward Lewis, George Michaelson, Erik Nygren, Libor Peltan, Ben Schwartz, Petr Špaček, Jan Včelák and Ralf Weber
