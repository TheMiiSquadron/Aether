# Aether Device Model

**Version:** 0.2\
**Status:** Approved

## Purpose

The Aether Device Model defines how devices participate in an Aether
System and how Systems relate to the wider Aether Constellation.

Aether treats device identity, System membership, device role,
capabilities, trust, permissions, and Host status as separate concepts.

This separation allows Aether to support different operating systems,
device types, personal AI implementations, users, and network
configurations without tying the platform to a particular machine or
topology.

------------------------------------------------------------------------

## 1. Aether Devices

An Aether Device is a physical or virtual computing device running an
Aether implementation and capable of participating in an Aether System.

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
capabilities, network address, display name, Host status, or
connectivity changes.

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
and are not defined by Device Model v0.2.

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

## 3. Systems

A System is one user's independent Aether environment.

A System may contain one device or many devices.

A System may also contain or support the user's personal AI, Host
configuration, device relationships, permissions, and System-level
state.

For example:

``` text
Alex's System
├── Selene
├── NOVA
├── ENVY
├── ORION
├── iPhone
└── Apple Watch
```

A System is not identical to any individual device.

No Host, Node, Endpoint, or Companion is itself the System.

A System must therefore remain conceptually valid even when its
preferred Host is unavailable.

### System Principle

> **Systems belong to users. Systems contain devices.**

A device's membership is associated with its System.

A device from another user's System does not become a member of the
local System merely because the two Systems trust or communicate with
each other.

------------------------------------------------------------------------

## 4. Constellations

A Constellation is the larger Aether structure that connects one or more
Systems.

A Constellation may initially contain only one System.

For example:

``` text
Aether Constellation
└── Alex's System
```

It may later contain multiple independently controlled Systems:

``` text
Aether Constellation
├── Alex's System
├── Friend's System
└── Family Member's System
```

Each System retains its own identity, devices, personal AI, Host
configuration, authority boundaries, and permissions.

Connecting Systems through a Constellation does not merge them.

### Constellation Principle

> **Constellations connect Systems; they do not erase System
> boundaries.**

Cross-System trust and communication will require explicit security and
permission rules.

The exact cross-System trust model is deferred to future architectural
work.

------------------------------------------------------------------------

## 5. System and Constellation Identity

Systems and Constellations must be conceptually independent of the
devices participating in them.

A System should eventually have a stable identity that is not derived
solely from:

-   Its user's display name
-   Its personal AI's name
-   Its Primary Host
-   Its Active Host
-   A particular network address
-   A particular device

Likewise, a Constellation should not depend on one specific System or
device for its conceptual identity.

The exact identifier formats and cryptographic representations are
deferred.

------------------------------------------------------------------------

## 6. Device Roles

A device's role describes its general function within a System.

Roles are not identities and do not inherently grant authority.

Device Model v0.2 defines three initial roles.

### Node

A Node is a general-purpose computing device capable of participating
broadly in its System.

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
experience of another device or the wider System.

Wearable devices are a likely example.

The exact distinction between Endpoint and Companion may evolve as
Aether's mobile and wearable architecture develops.

------------------------------------------------------------------------

## 7. Roles Do Not Equal Authority

A device role describes what kind of participant a device is.

It does not determine what that device is authorized to do.

For example:

-   A Node does not automatically control another Node.
-   A Host does not automatically gain unrestricted access to every
    device.
-   An Endpoint does not automatically trust every Node.
-   System membership does not imply universal permission.
-   Constellation membership does not imply cross-System permission.

Authority and permissions must be evaluated separately.

------------------------------------------------------------------------

## 8. Capabilities

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
Device Model v0.2.

### Capability Principle

Aether should ask:

> Does this device advertise the required capability?

rather than:

> Is this the kind of device that should probably support this
> operation?

This allows Aether to remain platform-independent and extensible.

------------------------------------------------------------------------

## 9. Device Relationship States

Aether distinguishes between the existence of an installation and the
trust granted to that installation.

Conceptually, devices within a System may progress through states such
as:

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

Installation alone grants no relationship with another device or System.

### Discovered

Another Aether Device has learned that the device exists.

Discovery does not imply authentication, System membership, or trust.

### Paired

Devices have completed an explicit process establishing and verifying
their identities.

Pairing alone must not mean unrestricted access.

### Trusted

A trusted relationship has been explicitly established.

Trust may still be limited by permissions, capabilities, user authority,
System boundaries, or other security policy.

------------------------------------------------------------------------

## 10. Network Reachability Is Not Trust

Aether maintains the foundational principle established by the Aether
Charter:

> **No Aether device trusts another device merely because it can reach
> it.**

Two devices being able to communicate over a LAN, VPN, relay, Internet
connection, or another transport mechanism does not establish trust.

The same principle applies across Systems.

Network transport and Aether trust are separate layers.

------------------------------------------------------------------------

## 11. Host Eligibility

Host is not a permanent device type.

Instead, Host status is a function that an eligible Node may perform
within its System.

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

Host eligibility is scoped to the device's own System unless a future
cross-System architecture explicitly defines otherwise.

------------------------------------------------------------------------

## 12. Primary Host

The Primary Host is the preferred Host of a System.

It represents the device that should normally provide the central
services used by that System's personal AI or other Aether applications.

For example:

``` text
system: Alex's System
primary_host: NOVA
```

The Primary Host designation describes the preferred topology.

It does not guarantee that the device is currently online or available.

A System can continue to exist when its Primary Host is unavailable.

------------------------------------------------------------------------

## 13. Active Host

The Active Host is the Host currently providing the relevant central
services for a System.

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
user's preferred System topology.

------------------------------------------------------------------------

## 14. User-Directed Host Switching

Host selection must support explicit user-directed switching.

A user should eventually be able to request an operation equivalent to:

> Switch the Active Host to ORION.

Before completing a Host switch, Aether must be able to determine
whether the requested device is:

-   A member of the appropriate System
-   Available
-   Authenticated
-   Trusted
-   Host-eligible
-   Capable of providing the required Host services

A Host switch must not silently grant new device permissions.

A personal AI may provide a natural-language interface for requesting
Host changes, but Aether remains responsible for enforcing the
underlying device, System, and trust requirements.

------------------------------------------------------------------------

## 15. Host Selection Modes

Aether should be designed to support multiple Host selection policies
within a System.

### Manual

The Active Host changes only when explicitly requested by the user or
another properly authorized operation.

### Assisted

When the Active Host becomes unavailable, Aether or the System's
personal AI may identify eligible alternatives and ask the user whether
to switch.

Assisted behavior is the preferred eventual default because it provides
resilience while preserving user control.

### Automatic

Aether may automatically select another eligible Host according to a
user-approved failover policy.

Automatic failover must be explicitly configurable and must not imply
unrestricted authority.

Device Model v0.2 defines these modes conceptually but does not
implement their selection algorithms.

------------------------------------------------------------------------

## 16. Host Preference

Host-eligible devices may eventually have preference or priority
information within their System.

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

## 17. Graceful Degradation

A personal AI using Aether must not conceptually depend on one physical
Host for its identity.

If the preferred Host becomes unavailable, another eligible device
within the System may provide a reduced set of services.

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

## 18. Personal AI Identity and Host Mobility

A personal AI is not identical to its Host device.

For an AI implementation using Aether:

> **The personal AI belongs to its System, not to any individual Host.**

Changing the Active Host must not inherently change:

-   The AI's identity
-   The AI's name
-   The user's relationship with the AI
-   The logical identity of the System

Host migration changes where services are currently being provided.

It does not create a new AI or a new System.

------------------------------------------------------------------------

## 19. State and Replication

Host mobility creates a future requirement for determining which state
must be available across Host-eligible devices within a System.

Aether will eventually need explicit rules for distinguishing between:

-   Device-local state
-   System state
-   Constellation state
-   Replicated state
-   Sensitive state that must not be replicated
-   Cached state
-   Authoritative state

Device Model v0.2 does not define a replication architecture.

Replication must be designed separately with explicit consideration for
security, consistency, privacy, conflict resolution, System boundaries,
and failure recovery.

------------------------------------------------------------------------

## 20. Personal AI Authority

Aether device trust and personal AI authority remain separate security
layers.

A personal AI's authority system determines whether the AI has
permission from its user to request an action.

Aether independently determines whether:

-   The requesting device is authenticated
-   The requesting device belongs to the appropriate System
-   The requesting device is trusted
-   The requested capability exists
-   The relationship permits use of that capability
-   The target device accepts the request
-   Any applicable cross-System boundary permits the request

Approval at one layer does not automatically grant approval at another.

------------------------------------------------------------------------

## 21. Cross-System Relationships

Devices remain members of their own Systems when Systems are connected
through a Constellation.

For example:

``` text
Aether Constellation
│
├── Alex's System
│   ├── Selene
│   ├── NOVA
│   └── ORION
│
└── Friend's System
    ├── Personal AI
    └── Friend's PC
```

The Friend's PC does not become a Node in Alex's System.

Likewise, NOVA does not become a Node in the Friend's System.

Any communication or capability use across the System boundary must be
governed by an explicit cross-System trust and permission model.

That model is not defined by Device Model v0.2.

------------------------------------------------------------------------

## 22. Example System

An example System may eventually appear conceptually as:

``` text
Alex's System

Selene
  personal_ai: true

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

Apple Watch
  role: Companion
  platform: watchOS
  host_eligible: false
  status: online
```

This example describes topology and current state.

It does not imply unrestricted permissions between any of these devices.

------------------------------------------------------------------------

## 23. Example Constellation

The same System may participate in a larger Constellation:

``` text
Aether Constellation
│
├── Alex's System
│   ├── Selene
│   ├── NOVA
│   ├── ENVY
│   ├── ORION
│   ├── iPhone
│   └── Apple Watch
│
├── Friend's System
│   ├── Personal AI
│   └── Devices
│
└── Family Member's System
    ├── Personal AI
    └── Devices
```

Each System remains independently controlled.

Constellation membership does not merge ownership, authority, Host
selection, or device membership.

------------------------------------------------------------------------

## 24. Design Principles

The Aether Device Model follows these principles:

1.  Every device has an independent identity.
2.  Human-readable device names are not authoritative identities.
3.  Every device belongs to a System.
4.  A System represents one user's independent Aether environment.
5.  A System may contain one device or many devices.
6.  A Constellation connects one or more Systems.
7.  Connecting Systems does not merge their ownership or authority
    boundaries.
8.  Roles describe function, not authority.
9.  Capabilities describe what devices can actually provide.
10. Network reachability does not imply trust.
11. Pairing does not imply unrestricted access.
12. Trust does not imply unrestricted permission.
13. Host is a function, not a permanent device type.
14. Primary Host and Active Host are separate concepts within a System.
15. Users must be able to explicitly direct Host switching.
16. Failover policy must remain under user control.
17. Host migration must not change personal AI identity.
18. Loss of a Host should reduce capability, not destroy identity.
19. A personal AI belongs to its System, not to an individual Host.
20. Aether must remain independent of any particular AI, operating
    system, model provider, user, or device arrangement.

------------------------------------------------------------------------

## 25. Deferred Design Work

Device Model v0.2 intentionally does not define:

-   Device identifier format
-   System identifier format
-   Constellation identifier format
-   Cryptographic algorithms
-   Pairing protocol
-   Device enrollment protocol
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
-   Multi-System device membership
-   Cross-System trust
-   Cross-System capability exchange
-   Constellation creation and administration
-   Revocation protocol

These areas require separate architectural decisions and should not be
implied by this document.

------------------------------------------------------------------------

## Summary

Aether treats a System as one user's independent environment containing
independently identified devices that expose capabilities under
controlled permissions.

Devices may assume different roles without changing identity.

Eligible Nodes may provide Host services, and the Active Host may move
between devices within a System without changing the identity of the
personal AI using Aether.

Systems may connect to other Systems through a Constellation without
surrendering their independent ownership, identity, or authority
boundaries.

The Primary Host represents where the personal AI normally lives.

The Active Host represents where it is running now.

The System represents where it belongs.

The Constellation represents the larger whole to which Systems may
connect.
