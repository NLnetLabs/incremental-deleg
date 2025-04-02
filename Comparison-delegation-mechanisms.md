# Comparison with other delegation mechanisms

Table {{xtraqueries}} provides an overview of when extra queries, in parallel to the legacy query, are sent.

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
{: #xtraqueries title="Additional queries in parallel to the legacy query"}

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

On the right side of the table are the extra queries, to be sent in parallel with the legacy query.
The `_deleg` presence test query (most right column) only needs to be sent to unsigned target zones, because its non-existence will be shown in the NSEC(3) records showing the non-existence of the incremental delegation (second from right column).

If the query name is the same as the apex of the target zone, no extra queries need to be sent (Row 1).
If the `_deleg` label is known not to exist in the target zone (Row 2) or if the target name server is known to support incremental deleg (Row 3), no extra queries need to be sent.
Only if it is unknown that the target name server supports incremental deleg, and the `_deleg` label is known to exist in the target zone (Row 4) or it is not known whether or not the `_deleg` label exists (Row 5), and extra incremental deleg query is sent in parallel to the legacy query.
If the target zone is unsigned, presence of the `_deleg` label needs to be tested explicitly (Row 5).

## Comparison with legacy delegations

### The delegation point

Legacy delegations are realized by a non-authoritative NS RRset at the name of the delegated zone, but in the delegating zone (the parent side of the zone cut).
However, there is another NS RRset by the same name, but now authoritative, in the delegated zone (the child side of the zone cut).
Some resolvers prefer to use the authoritative child side NS RRset (see {{Section 5.4.1 of !RFC2181}}) for contacting the authoritative name servers of the delegated zone, and will use it to reach the zone if they encounter the child side NS RRset authoritatively in responses.
Some resolvers query explicitly for the authoritative child side NS RRset {{I-D.ietf-dnsop-ns-revalidation}}.
However, these NS RRsets can differ in content leading to errors and inconsistencies (see {{Section 3 of I-D.ietf-dnsop-ns-revalidation}}).

Incremental deleg eliminates these issues by placing the referral information, not at the name of the delegated zone, but authoritatively in the delegating zone.

Having the referral information at an authoritative location brings clarity.
There can be no misinterpretation about who is providing the referral (the delegating zone, or the delegated zone).
In a future world where all delegations would be incremental delegations, all names will only be authoritative data, derivable from the name, for resolvers and other applications alike.

### Legacy referrals

Resolvers that support only legacy referrals will be on the internet for the foreseeable future, therefore a legacy referral MUST always be provided alongside the incremental referral.

Legacy referrals can be deduced from the incremental delegation.
An authoritative name server could (in some cases) synthesize the legacy referral from the incremental delegation, however this is NOT RECOMMENDED.
It introduces an element of dynamism which is at the time of writing not part of authoritative name server behavior specification.
Moreover, authoritative name servers could transfer the zone data to non incremental deleg supporting and aware name servers, which would not have this feature.
We leave provisioning of legacy referrals from incremental delegations (for now) out of scope for this document.

### Number of queries

Legacy resolvers that do not do DNS Query Name Minimisation, will get a referral in a single query.
The resolution process with incremental delegations must find the exact zone cut explicitly, comparable with DNS Query Name Minimisation.
The query increase to find the zone cut (and referral) is comparable to that of a resolver performing DNS Query Name minimisation.

## Comparison with Name DNS Query Name Minimisation

There are no extra queries needed in most cases if the authoritative name server has incremental deleg support. The exception is when the parent zone is not signed and has no incremental deleg records.
In that case, one extra query is needed when the parent zone is first contacted (and every TTL)

## Comparison with {{?I-D.wesplaap-deleg}}

{: cols="50%l 50%l"}
|-------------------------|-------------------|
| \[?I-D.wesplaap-deleg\] | \[this document\] |
|-------------------------|-------------------|
| Requires implementation in both authoritative name server as well as in the resolver, DNSSEC signers and validators | Only implementation required for functionalities following the delegations (like in resolvers). No support from the authoritative name server, DNSSEC signers or validators are needed. But optimized with updated authoritative software. |
|-------------------------|-------------------|
| DELEG resolvers need to contact DELEG authoritatives directly | IDELEG resolvers can query for the incremental delegation data, therefore direct contact with IDELEG supporting authoritatives is not necessary. All legacy infrastructure (including forwarders etc.) is supported. |
|-------------------------|-------------------|
| DNSKEY flag needed to signal IDELEG support with all authoritative name servers that serve the parent (delegating) domain. Special requirements for the child domain. | No DNSKEY flag needed. Separation of concerns. |
|-------------------------|-------------------|
| Authoritative name servers need to be updated all at once | Authoritative name servers may be updated gradually for optimization |
|-------------------------|-------------------|
| New semantics about what is authoritative (BOGUS with current DNSSEC validators) | Works with current DNS and DNSSEC semantics. Easier to implement. |
|-------------------------|-------------------|
| No extra queries | One extra query, in parallel to the legacy query, *per authoritative* server when incremental deleg support is not yet detected, and one extra query *per unsigned zone* to determine presence of the `_deleg` label |
|-------------------------|-------------------|
{: title="Comparison of [I-D.wesplaap-deleg] with [this document]"}
