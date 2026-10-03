# Aether Charter

**Version:** 0.1  
**Status:** Approved

## Purpose

Aether is a local-first platform that allows a personal AI to exist securely across a trusted constellation of devices.

Aether provides the common infrastructure for device identity, discovery, trust, communication, capabilities, presence, and coordination while remaining independent of any particular AI identity, model, interface, or operating system.

## Aether Is Responsible For

Aether provides infrastructure for:

- Device identity
- Device discovery
- Trusted relationships between devices
- Constellation membership and coordination
- Secure communication between trusted devices
- Device capability advertisement and discovery
- Device presence and reachability
- Common APIs and protocols for applications using Aether
- Event transport and coordination
- Future trusted links between separate users' Constellations

## Aether Is Not Responsible For

Aether does not:

- Define or embody a particular personal AI
- Define an AI's name, identity, or personality
- Perform LLM reasoning
- Require a particular AI model or provider
- Own an AI's long-term memory
- Determine what an AI is authorized by its user to do
- Serve as Windows Home, Mac Home, iPhone Home, or another user interface
- Provide unrestricted remote control of trusted devices
- Assume that network reachability implies trust

## Aether and Personal AI

Aether is infrastructure used by personal AI systems.

For example, Selene may use Aether, but Selene does not define Aether.

Aether must not require an assistant to be named Selene, require a particular computer to act as Host, or assume any particular user's device arrangement.

A personal AI implementation may use Aether for communication and coordination while maintaining its own reasoning, personality, memory, awareness, and authority systems.

## Security Boundary

Aether device trust and personal AI authority are separate security layers.

A personal AI's authority system determines whether the AI is authorized by its user to request an action.

Aether independently determines whether the requesting device is authenticated, trusted, permitted to use the requested capability, and communicating with a device that exposes that capability.

Authorization at one layer does not automatically grant authorization at the other.

## Foundational Trust Principle

> **No Aether device trusts another device merely because it can reach it.**

Network access is not trust.

Devices must establish explicit trusted relationships before privileged Aether capabilities can be used.

## Architectural Independence

Aether should remain independent of:

- AI identity
- AI personality
- LLM provider
- Local or cloud inference provider
- User interface
- Operating system
- Specific device names
- Specific network topology

This independence allows multiple personal AI implementations and device configurations to use the same Aether platform.