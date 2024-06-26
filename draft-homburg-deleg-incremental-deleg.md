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

The mechanism is designed with minimal adaption to components and to current DNS practice in mind (such as what data is authoritative) to maximize ease of implementation and deployment, without sacrificing resolution performance.

<!--
Sections {{}}, {{}}, {{}} elaborate on

## Signaling capabilities

What capabilities and associated details are signaled is extensible to support future uses (such as keys for encrypting the TLS ClientHello {{?I-D.ietf-tls-esni}}).

## Outsourcing operation of the delegation

## DNSSEC protection of the delegation

-->

## Terminology

{::boilerplate bcp14-tagged}

# Security Considerations

TODO Security


# IANA Considerations

This document has no IANA actions.


--- back

# Acknowledgments
{:numbered="false"}

TODO acknowledge.
