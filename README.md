# Aether

**Local-first infrastructure for personal AI across trusted devices and
Systems.**

Aether is a local-first platform that allows personal AI systems to
exist securely across trusted devices and, where explicitly permitted,
interact across trusted user environments.

Aether organizes each user's independent environment as a **System**. A
System may contain one device or many devices, along with a personal AI,
Host configuration, permissions, and System-level state.

One or more Systems may connect through an Aether **Constellation**
while retaining independent ownership, identity, devices, permissions,
and authority boundaries.

It provides common infrastructure for device identity, discovery, trust,
communication, capabilities, presence, coordination, Host mobility,
Systems, and Constellations while remaining independent of any
particular AI identity, model, interface, user, or operating system.

## Project Status

Aether is currently in early development.

The initial development target is the **Aether Foundation**,
establishing the architecture, device model, System model, security
boundaries, Constellation model, and core protocol before higher-level
integrations are built.

## Design Principles

-   Local-first
-   User-controlled
-   Platform-independent
-   AI-independent
-   Secure by default
-   Explicit trust between devices and Systems
-   No unrestricted remote control
-   Network access does not imply trust
-   Constellation membership does not imply unrestricted cross-System
    trust
-   Host mobility without loss of personal AI identity

## Core Architecture

``` text
Aether
└── Constellation
    ├── System
    │   ├── Personal AI
    │   └── Devices
    └── System
        ├── Personal AI
        └── Devices
```

**Systems belong to users. Systems contain devices. Constellations
connect Systems.**

## Documentation

See:

-   [`docs/CHARTER.md`](docs/CHARTER.md) --- Aether's purpose,
    responsibilities, boundaries, and foundational principles.
-   [`docs/DEVICE_MODEL.md`](docs/DEVICE_MODEL.md) --- Device identity,
    roles, capabilities, trust, and Host mobility.

## License

To be determined.
