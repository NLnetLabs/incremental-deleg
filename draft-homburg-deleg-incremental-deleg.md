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
title: "Incrementally Deployable Extensible Delegation for DNS"
abbrev: "incremental-deleg"
category: std

docname: draft-homburg-deleg-incremental-deleg-latest
submissiontype: IETF  # also: "independent", "editorial", "IAB", or "IRTF"
number:
date: 2024-06-25
consensus: true
v: 3
area: int
workgroup: DNS Delegation
keyword:
 - DNS
 - delegation
 - Internet-Draft
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
    fullname: Jesse van Zutphen
    organization: University of Amsterdam
    email: Jesse.vanZutphen@os3.nl
 -
    fullname: Willem Toorop
    organization: NLnet Labs
    email: willem@nlnetlabs.nl

normative:

informative:


--- abstract

This document proposes a mechanism for extensible delegations in the DNS.
The mechanism realizes delegations with SVCB resource record sets placed below a `_deleg` label in the apex of the delegating zone.
The mechanism inherits extensibility, as well as the possibility to alias the delegation details, from SVCB.
Legacy aliasing with CNAME also remains usable with this way of doing delegations.

Support in recursive resolvers suffices for the mechanism to be fully functional.
The number of subsequent interactions between the recursive resolver and the authoritative name servers is comparable to that with DNS Query Name Minimisation.
Additionally, but not required, support in the authoritative name servers enables optimized behavior with reduced (simultaneous) queries.
None, mixed or full deployment of the mechanism on authoritative name servers are all fully functional, allowing for the mechanism to be incrementally deployed on the authoritative name servers.

--- middle

# Introduction

This document describes a delegation mechanism for the Domain Name System (DNS) {{!STD13}} that addresses several matters that are at the time of writing are suboptimally supported or not at all.
These matters are elaborated upon in sections {{<signaling}}, {{<outsourcing}} and {{<dnssec-protection}}.
On top of that, the mechanism described in this document also has the ambition to be maximally deployable which is elaborated upon in {{deployability}}.

## Signaling capabilities of the authoritative name servers {#signaling}

The SVCB Resource Record (RR) type {{!RFC9460}} in "dns" service mode {{!RFC9461}} is used in which capability signalling of {{!RFC7858 (DNS over Transport Layer Protocol)}} (DoT), {{!RFC8484 (DNS Queries over HTTPS)}} and {{!RFC9250 (DNS over Dedicated QUIC Connections)}}, on default or alternative ports, are already specified.
The SVCB RR type is designed to be extensible to support future uses (such as keys for encrypting the TLS ClientHello {{?I-D.ietf-tls-esni}}.)

## Outsourcing operation of the delegation {#outsourcing}

Delegation information is stored at an authoritative location in the zone with this mechanism.
Legacy methods to redirect this information to another location, possible under the control of another operator, such as (CNAME {{Section 3.6.2 of RFC1034}}) and DNAME {{!RFC6672}} remain functional.
One could even outsource all delegation operational practice to another party with an DNAME on the `_deleg` label on the apex of the delegating zone.

Additional to the legacy methods, a delegation may be outsourced to multiple third parties by having multi SVCB RRs in AliasMode, each aliasing to another operator, on the delegation point.

## DNSSEC protection of the delegation {#dnssec-protection}

With legacy delegations, the NS RRset at the parent side of a delegation as well as glue records for the names in the NS RRset are not authoritative and not DNSSEC signed.
An adversary that is able to spoof a referral response, can alter this information and redirect all traffic for the delegation to a rogue name server undetected.
The adversary can then perceive all queries for the redirected zone (Privacy concern) and alter all unsigned parts of responses (such as further referrals, which is a Security concern).

DNSSEC protection of delegation information prevents that, and is the only counter measure that also works against on-path attackers.
At the time of writing, the only way to DNSSEC validate and verify delegations at all levels in the DNS hierarchy is to revalidate delegations {{?I-D.ietf-dnsop-ns-revalidation}}, which is done after the fact and has other security concerns ({{Section 7 of ?I-D.ietf-dnsop-ns-revalidation}}).

Direct delegation information (provided by SVCB RRs in ServiceMode) includes the hostnames of the authoritative name serversfor the delegation as well as IP addresses for those hostnames.
Since the information is stored authoritatively in the delegating zone, it will be DNSSEC signed if the zone is signed.
When the delegation is outsourced, then the delegation is protected when the zones providing the aliasing resource records *and* the zones serving the targets of the aliases are DNSSEC signed.

## Maximize ease of deployment {#deployability}

Delegation information is stored authoritatively within the delegation zone.
No semantic changes as to what zones are authoritative for what data are needed.
As a consequence, existing DNS software, such as authoritative name servers and DNSSEC signing software, can remain unmodified.
Unmodified authoritative name server software will serve the delegation information when queried for.
Unmodified signers will sign the delegation information in the delegating zone.
Only the recursive resolver needs modification to follow referrals as provided by the delegation information.

Such a resolver would explicitly query for the delegations administered as specified in this document.
The number of round trips form the recursive resolver to the authoritative name server is comparable to what is needed for DNS Query Name Minimisation {{!RFC9156}}.
Additional implementation in the authoritative name server optimizes resolution and reduces the number of simultaneous in parallel queries to that what would be needed for legacy delegations.
None, mixed or full deployment of the mechanism on authoritative name servers are all fully functional, allowing for the mechanism to be incrementally deployed on the authoritative name servers.

Implementation in the recursive may be less demanding with respect to (among other things) DNSSEC validation because of not making additional exceptions to what is authoritative at the parent side of a delegation.

## Terminology

{::boilerplate bcp14-tagged}

This document follows terminology as defined in {{?RFC9499}}.

Throughout this document we will also use terminology with the meaning as defined below:

{: vspace="0"}
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

Delegation point:
: The location in the delegating zone where the RRs are provided that make up the delegation.
  In legacy delegations, the parent side of the zone cut.
  With this document's delegation mechanism, at the location given by the delegating name.

# Delegation administration

An extensible delegation is realized with an SVCB Resource Record set (RRset) {{!RFC9460}} below a specially for the purpose reserved label with the name `_deleg` at the apex of the delegating zone.
The `_deleg` label scopes the interpretation of the SVCB records and requires registration in the "Underscored and Globally Scoped DNS Node Names" registry (see {{iana-considerations (IANA Considerations)}}).
The full scoping of delegations includes the labels that are **below** the `_label` and those, together with the name of the delegating domain, make up the name of the subzone to which the delegation refers.
For example, if the delegating zone is `example.`, then a delegation to subzone `customer.example.` is realized by an SVCB RRset at the name `customer._deleg.example.` in the parent zone.
A fully scoped delegating name (such as `customer._deleg.example.`) is referred to further in this document as the "delegation point".

The use of the SVCB RR type requires a mapping document for each service type.
This document uses the SVCB for the "dns" service type and the contents of the SVCB SvcParams MUST be interpreted as specified in Service Binding Mapping for DNS Servers {{!RFC9461}}.
At the delegation point (for example `customer._deleg.example.`), the host names of the authoritative name servers for the subzone, are given in the TargetName RDATA field of SVCB records in ServiceMode.
Port Prefix Naming {{Section 3 of RFC9461}} is not used at the delegation point, but MUST be used when resolving the aliased to name servers with "dns" service type SVCB RRs in AliasMode.

Note that if the delegation is outsourcing to a single operator represented in a single SVCB RRset, for performance reasons it is RECOMMENDED to refer to the name of the operator's SVCB RRset with a CNAME on the delegation point instead of an SVCB RR in AliasMode {{Section 10.2 of !RFC9460}}.

## Examples

### One name server within the subzone

    $ORIGIN example.
    @                  IN  SOA   ns zonemaster ...
    customer1._deleg   IN  SVCB  1 ns.customer1 (
                                   ipv6hint=2001:db8:1::1,2001:db8:2::1
                                   ipv4hint=198.51.100.1,203.0.113.1 )

### Two name servers within the subzone

    $ORIGIN example.
    @                  IN  SOA   ns zonemaster ...
    customer2._deleg   IN  SVCB  1 ns1.customer2 ( ipv6hint=2001:db8:1::1
                                                   ipv4hint=198.51.100.1 )
                       IN  SVCB  1 ns2.customer2 ( ipv6hint=2001:db8:2::1
                                                   ipv4hint=203.0.113.1 )

### Outsourced to a single operator

    $ORIGIN example.
    @                  IN  SOA   ns zonemaster ...
    customer3._deleg   IN  CNAME _dns.ns.operator1

Where the operator SVCB RRset could be:

    $ORIGIN operator1.example.
    @                  IN  SOA   ns zonemaster ...
    _dns.ns            IN  SVCB  1 ns ( ipv6hint=2001:db8:3::1
                                        ipv4hint=192.0.2.1
                                        alpn=h2,dot,h3,doq
                                        dohpath=/q{?dns} )
    ns                 IN  AAAA  2001:db8:3::1
                       IN  A     192.0.2.1

### Outsourced to two operator

    $ORIGIN example.
    @                  IN  SOA   ns zonemaster ...
    customer3._deleg   IN  SVCB 0 ns.operator1
                       IN  SVCB 0 ns.operator2

### DNSSEC signed name servers within the subzone


# Implementation

## Recursive Resolver

## Authoritative name server

# Limitations

TODO Limitations

# Comparison with other delegation mechanisms

## Comparison with legacy delegations

## Comparison with Name DNS Query Name Minimisation

## Comparison with {{?I-D.dnsop-deleg}}

# Implementation Status

**Note to the RFC Editor**: please remove this entire section before publication.

# Security Considerations

TODO Security

# IANA Considerations

Per {{?RFC8552}}, IANA is requested to add the following entry to the DNS "Underscored and Globally Scoped DNS Node Names" registry:

|---------|------------|-------------------|
| RR Type | _NODE NAME | Reference         |
|---------|:-----------|-------------------|
| SVCB    | _deleg     | \[this document\] |
|---------|------------|-------------------|


--- back

# Acknowledgments
{:numbered="false"}

TODO acknowledge.