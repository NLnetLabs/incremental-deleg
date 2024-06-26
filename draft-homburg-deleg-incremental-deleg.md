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

Support in recursive resolvers suffices for the mechanism to be fully functional.
The number of subsequent interactions between the recursive resolver and the authoritative name servers is comparable to that with DNS Query Name Minimisation.
Additionally, but not required, support in the authoritative name servers enables optimized behavior with reduced (simultaneous) queries.
None, mixed or full deployment of the mechanism on authoritative name servers are all fully-functional, allowing for the mechanism to be incrementally deployed on the authoritative name servers.

--- middle

# Introduction

This document describes a delegation mechanism for the Domain Name System (DNS) {{!STD13}} that addresses several matters that are at the time of writing are suboptimally supported or not at all:

1. Signaling capabilities of the authoritative name servers that serve the delegated zone.
2. Outsourcing operation of the delegation.
3. DNSSEC protection of the delegation.

Other properties of this mechanisms design are to:

{:start="4"}
4. Minimize the needed changes to DNS components and DNS practice (such as what data is authoritative), with the goal to maximize ease of implementation and deployment
5. Not sacrifice resolution performance.

How these properties are met is elaborated upon further in this document referencing the bullet points above.

<!--
// Something like this somewhere
## Signaling capabilities

What capabilities and associated details are signaled is extensible to support future uses (such as keys for encrypting the TLS ClientHello {{}}?I-D.ietf-tls-esni).

## Outsourcing operation of the delegation

## DNSSEC protection of the delegation

-->

## Terminology

{::boilerplate bcp14-tagged}

<!-- TODO for terminology: delegating zone, delegation name, subzone, delegation point,  -->

# Zone content

An extensible delegation is realized with an SVCB resource record (RR) set (RRset) {{!RFC9460}} below a specially for the purpose reserved label with the name `_deleg`, at the apex of the delegating zone.
The `_label` scopes the interpretation of the SVCB records and requires registration in the "Underscored and Globally Scoped DNS Node Names" {{!RFC8552}} {{IANA}}.
The full scoping of delegations includes the labels that are below the `_label` and those, together with the name of the delegating domain, make up the name that is delegated to.
For example, if the delegating zone is `example.`, then a delegation to subzone `customer.example.` is realized by an SVCB RRset at the name `customer._deleg.example.` in the parent zone.
A fully scoped delegation name (such as `customer._deleg.example.`) is referred to further in this document as the "delegation point".

The use of the SVCB RR type requires a mapping document for each service type.
This document uses the SVCB for the "dns" service type and the contents of the SVCB SvcParams MUST be interpreted as specified in Service Binding Mapping for DNS Servers {{!RFC9461}}.
At the delegation point (for example `customer._deleg.example.`), the host names of the authoritative name servers for the subzone, are given in the TargetName RDATA field of SVCB records in ServiceMode.
Port Prefix Naming {{Section 3 of !RFC9461}} is not used at the delegation point, but MUST be used when resolving the aliased to name server with SVCB RRs in AliasMode.

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


# Security Considerations

TODO Security


# IANA Considerations {#IANA}

This document has no IANA actions.


--- back

# Acknowledgments
{:numbered="false"}

TODO acknowledge.
