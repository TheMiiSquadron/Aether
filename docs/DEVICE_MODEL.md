# Aether Device Model

**Version:** 0.1\
**Status:** Approved

## Purpose

The Aether Device Model defines how devices participate in an Aether
Constellation.

Aether treats device identity, device role, capabilities, trust,
permissions, and Host status as separate concepts.

This separation allows Aether to support different operating systems,
device types, personal AI implementations, and network configurations
without tying the platform to a particular machine or topology.

------------------------------------------------------------------------

## 1. Aether Devices

An Aether Device is a physical or virtual computing device running an
Aether implementation and capable of participating in an Aether
Constellation.

Examples may include:

-   Windows computers
-   macOS computers
-   Linux computers
-   iPhones
-   iPads
-   Android devices
-   Watches
-   Future supported device classes

Every Aether Device has its own identity.

A device does not become a different device merely because its role,
capabilities, network address, display name, or Host status changes.

Conceptually, a device may expose information such as:

``` text
Device
├── device_id
├── public_key
├── display_name
├── platform
├── platform_version
├── aether_version
└── capabilities[]
```

The exact schema and protocol representation are implementation details
and are not defined by Device Model v0.1.

------------------------------------------------------------------------

## 2. Device Identity

Every Aether Device must have a unique device identity.

Human-readable names such as `NOVA`, `ORION`, or `ENVY` are display
names and must not serve as the authoritative identity of a device.

Display names may:

-   Change over time
-   Be duplicated
-   Contain user-defined values

Aether must therefore use a stable machine-readable identifier for
device identity.

Aether's security model should also associate devices with cryptographic
identity.

Conceptually, an Aether installation may generate a device key pair
during initial setup.

The device's private identity material must remain protected locally and
must not be treated as ordinary synchronized configuration data.

The exact cryptographic implementation will be defined separately.

------------------------------------------------------------------------

## 3. Constellations

A Constellation is a trusted collection of Aether Devices associated
with a personal Aether environment.

A device may participate in a Constellation after completing the
appropriate pairing and trust process.

The Constellation provides a logical environment in which devices can
discover, authenticate, communicate with, and coordinate with other
trusted devices.

Membership in a Constellation does not automatically grant unrestricted
access to other devices.

------------------------------------------------------------------------

## 4. Device Roles

A device's role describes its general function within a Constellation.

Roles are not identities and do not inherently grant authority.

Device Model v0.1 defines three initial roles.

### Node

A Node is a general-purpose computing device capable of participating
broadly in the Constellation.

Nodes may:

-   Expose Aether capabilities
-   Consume capabilities provided by other devices
-   Run Aether services
-   Participate in coordination
-   Potentially become an Active Host if Host-eligible

Desktop and laptop computers will commonly operate as Nodes.

### Endpoint

An Endpoint is a more constrained device primarily used to interact with
services provided through Aether.

Endpoints may provide user interaction, notifications, sensors,
presence, or other device-specific capabilities.

Phones and similar mobile devices may commonly operate as Endpoints.

Being an Endpoint does not inherently prevent a device from gaining
additional capabilities in future versions of Aether.

### Companion

A Companion is a constrained device that primarily extends the
experience of another device or the wider Constellation.

Wearable devices are a likely example.

The exact distinction between Endpoint and Companion may evolve as
Aether's mobile and wearable architecture develops.

------------------------------------------------------------------------

## 5. Roles Do Not Equal Authority

A device role describes what kind of participant a device is.

It does not determine what that device is authorized to do.

For example:

-   A Node does not automatically control another Node.
-   A Host does not automatically gain unrestricted access to every
    device.
-   An Endpoint does not automatically trust every Node.
-   Constellation membership does not imply universal permission.

Authority and permissions must be evaluated separately.

------------------------------------------------------------------------

## 6. Capabilities

Capabilities describe what an Aether Device can actually provide.

Aether should not assume that a capability exists merely because a
device uses a particular operating system or belongs to a particular
role.

Instead, devices advertise supported capabilities.

Conceptually, capabilities might eventually represent functionality
involving:

-   Files
-   Applications
-   Notifications
-   Clipboard access
-   Sensors
-   Context awareness
-   Local inference
-   User interfaces
-   Device-specific services

The final capability namespace and permission model are not defined by
Device Model v0.1.

### Capability Principle

Aether should ask:

> Does this device advertise the required capability?

rather than:

> Is this the kind of device that should probably support this
> operation?

This allows Aether to remain platform-independent and extensible.

------------------------------------------------------------------------

## 7. Device Relationship States

Aether distinguishes between the existence of an installation and the
trust granted to that installation.

Conceptually, devices may progress through states such as:

``` text
Installed
    ↓
Discovered
    ↓
Paired
    ↓
Trusted
```

### Installed

Aether exists on the device.

Installation alone grants no relationship with another device.

### Discovered

Another Aether Device has learned that the device exists.

Discovery does not imply authentication or trust.

### Paired

Devices have completed an explicit process establishing and verifying
their identities.

Pairing alone must not mean unrestricted access.

### Trusted

A trusted relationship has been explicitly established.

Trust may still be limited by permissions, capabilities, user authority,
or other security policy.

------------------------------------------------------------------------

## 8. Network Reachability Is Not Trust

Aether maintains the foundational principle established by the Aether
Charter:

> **No Aether device trusts another device merely because it can reach
> it.**

Two devices being able to communicate over a LAN, VPN, relay, Internet
connection, or another transport mechanism does not establish trust.

Network transport and Aether trust are separate layers.

------------------------------------------------------------------------

## 9. Host Eligibility

Host is not a permanent device type.

Instead, Host status is a function that an eligible Node may perform.

A Node may declare or be configured with Host eligibility.

Conceptually:

``` text
ORION
  role: Node

  host:
    eligible: true
```

A device that cannot provide the required Host services may be marked:

``` text
iPhone
  role: Endpoint

  host:
    eligible: false
```

Host eligibility does not mean that the device is currently acting as
Host.

------------------------------------------------------------------------

## 10. Primary Host

The Primary Host is the preferred Host of a Constellation.

It represents the device that should normally provide the central
services used by a personal AI or other Aether applications.

For example:

``` text
primary_host: NOVA
```

The Primary Host designation describes the preferred topology.

It does not guarantee that the device is currently online or available.

------------------------------------------------------------------------

## 11. Active Host

The Active Host is the Host currently providing the relevant central
services for the Constellation.

Normally:

``` text
Primary Host: NOVA
Active Host:  NOVA
```

During maintenance, failure, travel, testing, or user-directed
switching, the Active Host may differ:

``` text
Primary Host: NOVA
Active Host:  ORION
```

Changing the Active Host does not necessarily change the Primary Host.

This distinction allows temporary Host migration without rewriting the
user's preferred topology.

------------------------------------------------------------------------

## 12. User-Directed Host Switching

Host selection must support explicit user-directed switching.

A user should eventually be able to request an operation equivalent to:

> Switch the Active Host to ORION.

Before completing a Host switch, Aether must be able to determine
whether the requested device is:

-   Available
-   Authenticated
-   Trusted
-   Host-eligible
-   Capable of providing the required Host services

A Host switch must not silently grant new device permissions.

A personal AI may provide a natural-language interface for requesting
Host changes, but Aether remains responsible for enforcing the
underlying device and trust requirements.

------------------------------------------------------------------------

## 13. Host Selection Modes

Aether should be designed to support multiple Host selection policies.

### Manual

The Active Host changes only when explicitly requested by the user or
another properly authorized operation.

### Assisted

When the Active Host becomes unavailable, Aether or a personal AI may
identify eligible alternatives and ask the user whether to switch.

Assisted behavior is the preferred eventual default because it provides
resilience while preserving user control.

### Automatic

Aether may automatically select another eligible Host according to a
user-approved failover policy.

Automatic failover must be explicitly configurable and must not imply
unrestricted authority.

Device Model v0.1 defines these modes conceptually but does not
implement their selection algorithms.

------------------------------------------------------------------------

## 14. Host Preference

Host-eligible devices may eventually have preference or priority
information.

Conceptually:

``` text
NOVA
  host:
    eligible: true
    preference: primary

ENVY
  host:
    eligible: true
    preference: fallback
    priority: 1

ORION
  host:
    eligible: true
    preference: fallback
    priority: 2
```

The exact ranking and failover algorithm will be defined separately.

------------------------------------------------------------------------

## 15. Graceful Degradation

A personal AI using Aether must not conceptually depend on one physical
Host for its identity.

If the preferred Host becomes unavailable, another eligible device may
provide a reduced set of services.

For example, a fallback Host may lack:

-   Files stored only on the unavailable device
-   Operating-system-specific automation
-   High-performance local inference
-   Hardware-specific capabilities
-   Data that has intentionally not been replicated

The system should expose these limitations rather than pretending
unavailable capabilities still exist.

This produces the following principle:

> **Loss of a Host should reduce capability, not destroy identity.**

------------------------------------------------------------------------

## 16. Personal AI Identity and Host Mobility

A personal AI is not identical to its Host device.

For an AI implementation using Aether:

> **The AI belongs to the Constellation, not to the Host.**

Changing the Active Host must not inherently change:

-   The AI's identity
-   The AI's name
-   The user's relationship with the AI
-   The logical identity of the Constellation

Host migration changes where services are currently being provided.

It does not create a new AI.

------------------------------------------------------------------------

## 17. State and Replication

Host mobility creates a future requirement for determining which state
must be available across Host-eligible devices.

Aether will eventually need explicit rules for distinguishing between:

-   Device-local state
-   Constellation state
-   Replicated state
-   Sensitive state that must not be replicated
-   Cached state
-   Authoritative state

Device Model v0.1 does not define a replication architecture.

Replication must be designed separately with explicit consideration for
security, consistency, privacy, conflict resolution, and failure
recovery.

------------------------------------------------------------------------

## 18. Personal AI Authority

Aether device trust and personal AI authority remain separate security
layers.

A personal AI's authority system determines whether the AI has
permission from its user to request an action.

Aether independently determines whether:

-   The requesting device is authenticated
-   The requesting device is trusted
-   The requested capability exists
-   The relationship permits use of that capability
-   The target device accepts the request

Approval at one layer does not automatically grant approval at another.

------------------------------------------------------------------------

## 19. Example Constellation

An example Constellation may eventually appear conceptually as:

``` text
Constellation

NOVA
  role: Node
  platform: Windows
  host_eligible: true
  primary_host: true
  active_host: false
  status: offline

ENVY
  role: Node
  platform: Windows
  host_eligible: true
  primary_host: false
  active_host: false
  status: online

ORION
  role: Node
  platform: macOS
  host_eligible: true
  primary_host: false
  active_host: true
  status: online

iPhone
  role: Endpoint
  platform: iOS
  host_eligible: false
  status: online
```

This example describes topology and current state.

It does not imply unrestricted permissions between any of these devices.

------------------------------------------------------------------------

## 20. Design Principles

The Aether Device Model follows these principles:

1.  Every device has an independent identity.
2.  Human-readable device names are not authoritative identities.
3.  Roles describe function, not authority.
4.  Capabilities describe what devices can actually provide.
5.  Network reachability does not imply trust.
6.  Pairing does not imply unrestricted access.
7.  Trust does not imply unrestricted permission.
8.  Host is a function, not a permanent device type.
9.  Primary Host and Active Host are separate concepts.
10. Users must be able to explicitly direct Host switching.
11. Failover policy must remain under user control.
12. Host migration must not change personal AI identity.
13. Loss of a Host should reduce capability, not destroy identity.
14. Aether must remain independent of any particular AI, operating
    system, model provider, or device arrangement.

------------------------------------------------------------------------

## 21. Deferred Design Work

Device Model v0.1 intentionally does not define:

-   Device identifier format
-   Cryptographic algorithms
-   Pairing protocol
-   Discovery protocol
-   Network transport
-   Capability namespace
-   Capability negotiation
-   Permission schema
-   Host election algorithm
-   Failover timing
-   State replication
-   Conflict resolution
-   Recovery after network partition
-   Multi-Constellation membership
-   Cross-Constellation trust
-   Revocation protocol

These areas require separate architectural decisions and should not be
implied by this document.

------------------------------------------------------------------------

## Summary

Aether treats a Constellation as a collection of independently
identified, explicitly trusted devices that expose capabilities under
controlled permissions.

Devices may assume different roles without changing identity.

Eligible Nodes may provide Host services, and the Active Host may move
between devices without changing the identity of the personal AI using
Aether.

The Primary Host represents where the AI normally lives.

The Active Host represents where it is running now.

The Constellation represents where it belongs.