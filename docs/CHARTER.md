# Aether Charter

**Version:** 0.2\
**Status:** Approved

## Purpose

Aether is a local-first platform that allows personal AI systems to
exist securely across trusted devices and, where explicitly permitted,
interact across trusted user environments.

Aether provides common infrastructure for device identity, discovery,
trust, communication, capabilities, presence, coordination, Systems, and
Constellations while remaining independent of any particular AI
identity, model, interface, user, or operating system.

## Core Structure

Aether distinguishes between a **System** and a **Constellation**.

### System

A System is one user's independent Aether environment.

A System may contain one device or many devices and may support that
user's personal AI, Host configuration, trusted devices, permissions,
and System-level state.

A System is not identical to any individual device or Host.

### Constellation

A Constellation is the larger Aether structure that connects one or more
Systems.

A Constellation may contain only one System or may connect multiple
independently controlled Systems.

Connecting Systems through a Constellation does not merge their
ownership, device membership, permissions, personal AI identities, or
authority boundaries.

> **Systems belong to users. Systems contain devices. Constellations
> connect Systems.**

## Aether Is Responsible For

Aether provides infrastructure for:

-   Device identity
-   Device discovery
-   System identity and membership
-   Trusted relationships between devices
-   System coordination
-   Constellation membership and coordination
-   Secure communication between trusted devices
-   Device capability advertisement and discovery
-   Device presence and reachability
-   Common APIs and protocols for applications using Aether
-   Event transport and coordination
-   Host mobility within a System
-   Future trusted relationships between separate users' Systems

## Aether Is Not Responsible For

Aether does not:

-   Define or embody a particular personal AI
-   Define an AI's name, identity, or personality
-   Perform LLM reasoning
-   Require a particular AI model or provider
-   Own an AI's long-term memory
-   Determine what an AI is authorized by its user to do
-   Serve as Windows Home, Mac Home, iPhone Home, or another user
    interface
-   Provide unrestricted remote control of trusted devices
-   Assume that network reachability implies trust
-   Merge user authority merely because Systems share a Constellation

## Aether and Personal AI

Aether is infrastructure used by personal AI systems.

For example, Selene may use Aether, but Selene does not define Aether.

Aether must not require an assistant to be named Selene, require a
particular computer to act as Host, or assume any particular user's
device arrangement.

A personal AI implementation may use Aether for communication and
coordination while maintaining its own reasoning, personality, memory,
awareness, and authority systems.

A personal AI belongs conceptually to its user's System rather than to
any individual Host.

Changing the Active Host must not inherently create a new personal AI or
change the AI's identity.

## Systems and User Boundaries

Each System represents an independent user environment.

Devices belonging to another user's System do not become members of the
local System merely because the Systems communicate or participate in
the same Constellation.

Cross-System communication must respect explicit trust, permission, and
authority boundaries.

A Constellation must not be treated as a universal trust domain.

## Host Mobility

Host is a function that an eligible device may perform within a System,
not a permanent device type.

A System may distinguish between:

-   **Primary Host** --- the preferred Host under normal conditions
-   **Active Host** --- the Host currently providing the relevant
    services

The Active Host may differ from the Primary Host during maintenance,
failure, travel, testing, or explicit user-directed switching.

Users must be able to direct Host switching when appropriate.

Future Aether implementations may also support assisted or explicitly
configured automatic failover.

Host mobility must preserve the identity of the System and the personal
AI using it.

> **Loss of a Host should reduce capability, not destroy identity.**

## Security Boundary

Aether device trust and personal AI authority are separate security
layers.

A personal AI's authority system determines whether the AI is authorized
by its user to request an action.

Aether independently determines whether the requesting device and System
are authenticated, trusted, permitted to use the requested capability,
and communicating with a device that exposes that capability.

Authorization at one layer does not automatically grant authorization at
the other.

Trust within one System does not automatically extend across a
Constellation.

## Foundational Trust Principle

> **No Aether device trusts another device merely because it can reach
> it.**

Network access is not trust.

Devices must establish explicit trusted relationships before privileged
Aether capabilities can be used.

Likewise, participation in the same Constellation does not itself
establish permission between Systems.

## Architectural Independence

Aether should remain independent of:

-   AI identity
-   AI personality
-   LLM provider
-   Local or cloud inference provider
-   User interface
-   Operating system
-   Specific users
-   Specific device names
-   Specific Host devices
-   Specific network topology

This independence allows multiple personal AI implementations, users,
Systems, device configurations, and network arrangements to use the same
Aether platform.

## Foundational Principles

Aether v0.2 adopts the following foundational principles:

1.  A System represents one user's independent Aether environment.
2.  Systems contain devices.
3.  A Constellation connects one or more Systems.
4.  Connecting Systems does not erase their ownership or authority
    boundaries.
5.  A personal AI belongs to its System, not to an individual Host.
6.  Host is a function, not a permanent device type.
7.  Primary Host and Active Host are separate concepts.
8.  Users must be able to explicitly direct Host switching.
9.  Loss of a Host should reduce capability, not destroy identity.
10. Network reachability does not imply trust.
11. Constellation membership does not imply unrestricted cross-System
    trust.
12. Aether device trust and personal AI authority remain separate
    security layers.
13. Aether remains independent of any particular AI, user, operating
    system, model provider, device arrangement, or network topology.
