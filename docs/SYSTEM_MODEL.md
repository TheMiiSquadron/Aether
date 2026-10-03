# Aether System Model

**Version:** 0.1\
**Status:** Draft for Approval

## 1. Purpose

This document defines the Aether **System** model.

A System is the persistent logical environment belonging to one user. It
provides the boundary within which that user's Aether devices, Host
configuration, permissions, System-level state, and optional primary
personal AI are organized.

A System is not a device, a Host, a personal AI, a network, or a display
name.

> **Systems belong to users. Systems contain devices. Constellations
> connect Systems.**

## 2. System Identity

Every System has a stable identity independent of:

-   its display name;
-   its owner-facing name;
-   its personal AI;
-   its devices;
-   its Primary Host or Active Host;
-   its network location; and
-   its Constellation membership.

Conceptually, a System may include fields such as:

-   `system_id`
-   `display_name`
-   `owner`
-   `primary_ai`
-   `devices[]`
-   Host configuration
-   permissions
-   System-level state

The exact identifier format and cryptographic representation are
deferred.

A human-readable name such as **Alex's System** is a display name and is
not authoritative identity.

## 3. Ownership

A System has exactly one owner in Aether v0.1.

Other users may eventually be granted permission to interact with a
System, but those permissions do not make them co-owners.

System ownership persists through:

-   device replacement;
-   device loss;
-   device removal or revocation;
-   Host changes;
-   personal AI migration, removal, or replacement; and
-   changes in network topology.

Ownership must ultimately be cryptographically provable and recoverable.
Possession or control of an individual device, including the current
Host, is not by itself proof of System ownership.

The owner has authority over the personal AI within the System. The
personal AI does not own the System.

> **Possession of a device is not proof of ownership of its System.**

## 4. Personal AI Relationship

A System does not require a personal AI.

Aether v0.1 supports **zero or one primary personal AI identity per
System**.

The primary personal AI belongs conceptually to the System rather than
to an individual Host. Changing the Active Host does not create a new
personal AI identity.

A personal AI may be removed, migrated, rebuilt, or replaced without
destroying or replacing the System.

Other agents and services may be supported separately in the future
without being treated as the System's primary personal AI.

Aether provides infrastructure for a personal AI but does not define
that AI's identity, personality, reasoning model, model provider, memory
architecture, or user interface.

## 5. Device Membership

Installing Aether on a device does not automatically make that device a
member of a System.

Installation establishes an Aether device identity. **Enrollment**
establishes System membership.

Conceptually:

``` text
Install Aether
      |
      v
Create Device Identity
      |
      v
Unenrolled Aether Device
      |
      v
Owner-Authorized Enrollment
      |
      v
System Member
```

In Aether v0.1, a device belongs to at most one System. Multi-System
device membership is deferred.

System membership must be explicitly authorized by the System owner.
Discovery, network reachability, pairing, trust, or existing System
membership does not by itself grant authority to enroll another device.

Membership is System state rather than merely a relationship stored on
whichever device approved the enrollment.

The exact enrollment protocol is deferred.

## 6. Removal and Revocation

Aether distinguishes **removal** from **revocation**.

### Removal

Removal is the normal administrative retirement of a device from a
System.

Examples include replacing an old computer, retiring a phone, or
intentionally removing a device that is no longer needed.

### Revocation

Revocation is a security action used when a device is lost, stolen,
compromised, or otherwise no longer trusted.

A revoked device's existing System membership must no longer be
sufficient to regain access merely because the device later becomes
reachable.

Rejoining the System requires a new explicitly authorized enrollment
process.

The precise credential invalidation and revocation mechanisms are
deferred.

## 7. Device Identity and Reinstallation

Device identity follows Aether identity material, not the device's
display name or physical hardware alone.

A friendly name such as `ORION` is not proof that a newly installed
Aether instance is the previously trusted ORION device.

If a clean installation destroys or replaces the device's Aether
identity material, the installation is treated as a new Aether device
for membership purposes and must be explicitly enrolled.

Hardware identifiers or matching display names must not silently restore
System membership.

## 8. Membership Administration

System membership does not automatically grant membership-administration
authority.

An enrolled device cannot enroll, remove, or revoke other devices merely
because it belongs to the System.

Enrollment, removal, and revocation require an explicitly authorized
owner operation.

The mechanism by which owner authority is proven is deferred to later
security and protocol design.

## 9. Host Independence

The System is independent of its Hosts.

Primary Host and Active Host are System-level configuration concepts
applied to eligible devices within the System.

Loss, replacement, removal, or revocation of a Host does not destroy the
System or change its ownership.

When an eligible trusted member becomes the Active Host, the personal AI
remains the same System-level personal AI identity.

> **The personal AI belongs to its System, not to any individual Host.**

Host switching and failover remain subject to Aether trust,
authentication, eligibility, availability, required-service, and
owner-authority requirements defined elsewhere in the architecture.

## 10. System Continuity

System identity must not be stored exclusively on the current Host.

Authorized System members may retain sufficient System identity and
System state to recognize and participate in the same System when a Host
becomes unavailable.

System state may be replicated, but not all state is required to be
replicated.

Future state classifications may include:

-   device-local state;
-   System-wide state;
-   replicated state;
-   sensitive nonreplicated state;
-   cached state; and
-   authoritative state.

Loss of a device may therefore reduce available capabilities or make
nonreplicated data unavailable without destroying System identity.

> **Loss of a Host should reduce capability, not destroy identity.**

## 11. Continuity and Disaster Recovery

Aether distinguishes normal System continuity from disaster recovery.

### Normal Continuity

If a Host becomes unavailable while other authorized System members
remain available, the System continues to exist.

Subject to the configured Host-selection mode and required
authorization, another eligible device may assume the Active Host
function.

Only services, capabilities, and state available to that device can
resume. Device-local or nonreplicated resources on the unavailable Host
may remain unavailable.

### Disaster Recovery

If all enrolled devices and their usable System credentials are lost,
recovery becomes a separate ownership-recovery process.

Disaster recovery must require independent proof of owner authority.

Knowledge of any of the following is insufficient by itself to claim or
recover a System:

-   System display name;
-   `system_id`;
-   device names;
-   personal AI name;
-   prior Host identity; or
-   possession of old System data.

Recovering an existing System must be distinguishable from creating a
new System with the same human-readable name.

The recovery mechanism itself is deferred.

## 12. Security Boundaries

A System is an ownership, membership, and coordination boundary. It is
not a universal permission boundary.

The following do not automatically imply unrestricted authority:

-   System membership;
-   device trust;
-   Host status;
-   network reachability;
-   possession of replicated System state; or
-   Constellation membership.

Aether device/network trust and personal-AI authority remain separate
security layers.

A request may require both valid Aether trust and valid user/AI
authority before an action is permitted.

## 13. Relationship to Constellations

A System may operate independently or participate in an Aether
Constellation.

Constellation membership does not merge Systems.

Each connected System retains its own:

-   owner;
-   System identity;
-   devices;
-   personal AI;
-   Host configuration;
-   permissions;
-   authority boundaries; and
-   System-level state.

Cross-System communication and capability use require explicit trust,
permission, and authority.

A device belonging to another user's System does not become a member of
this System merely because both Systems participate in the same
Constellation.

## 14. Example: Alex's System

Conceptually:

``` text
Alex
 |
 | owns
 v
Alex's System
 |
 +-- Primary Personal AI: Selene
 |
 +-- Devices
 |   +-- NOVA
 |   |   +-- Role: Node
 |   |   +-- Host eligible: yes
 |   |   +-- Primary Host: yes
 |   |
 |   +-- ENVY
 |   |   +-- Role: Node
 |   |   +-- Host eligible: yes
 |   |
 |   +-- ORION
 |   |   +-- Role: Node
 |   |   +-- Host eligible: yes
 |   |
 |   +-- iPhone
 |   |   +-- Role: Endpoint
 |   |
 |   +-- Apple Watch
 |       +-- Role: Companion
 |
 +-- Host Configuration
 +-- Permissions
 +-- System State
```

If NOVA becomes unavailable, Alex's System remains Alex's System. An
eligible authorized device such as ORION may become the Active Host
without creating a new System or a new Selene identity.

## 15. Deferred Design Decisions

The following are intentionally not defined by System Model v0.1:

-   exact `system_id` format;
-   System cryptographic identity format;
-   owner identity and authentication format;
-   owner key storage;
-   enrollment transport and protocol;
-   QR codes, one-time codes, invitations, or nearby approval
    mechanisms;
-   device credential issuance;
-   revocation protocol and propagation;
-   recovery keys or recovery credentials;
-   encrypted backup or escrow mechanisms;
-   hardware-backed credential use;
-   detailed state replication protocol;
-   authoritative-state election;
-   conflict resolution;
-   network-partition behavior;
-   multi-System device membership;
-   System transfer of ownership;
-   multi-owner Systems;
-   cross-System trust protocol; and
-   Constellation administration and governance.

These decisions belong to later protocol, security, recovery, and
Constellation design.

## 16. Foundational System Principles

Aether System design follows these principles:

1.  A System belongs to one user.
2.  A System has a persistent identity independent of its devices,
    Hosts, personal AI, and display name.
3.  A System can exist without a personal AI.
4.  Aether v0.1 supports zero or one primary personal AI identity per
    System.
5.  Installation creates a device identity; enrollment creates System
    membership.
6.  System membership requires explicit owner authorization.
7.  Device identity follows Aether identity material rather than display
    name or hardware identity alone.
8.  Removal and revocation are distinct operations.
9.  Membership does not automatically grant membership-administration
    authority.
10. Possession of a device is not proof of System ownership.
11. The personal AI belongs to the System, not to an individual Host.
12. Loss of a Host may reduce capability but must not destroy System
    identity.
13. Normal continuity and disaster recovery are distinct.
14. Disaster recovery requires independent proof of owner authority.
15. Constellation membership does not erase System boundaries.

## 17. Summary

An Aether System is the persistent personal environment that connects a
user to their trusted Aether devices, Host configuration, permissions,
System state, and optional primary personal AI.

Devices may come and go. Hosts may move. Personal AIs may migrate or be
replaced. Networks may change.

The System remains the stable ownership and coordination boundary across
those changes.
