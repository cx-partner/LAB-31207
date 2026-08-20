# LAB-31207 Overview

## Purpose

LAB-31207 is a focused 4-hour hands-on lab for building a proactive outbound customer journey in Webex Contact Center. You will configure native Campaign Manager, connect answered calls to a Webex AI Agent, attach MCP-backed actions, and enable Real-Time Assist for the human handoff.

The lab starts from a prepared tenant. The MCP server is already provisioned, so you will select available MCP tools from the AI Agent or AI Assistant configuration instead of building backend fulfillment flows.

???+ purpose "Lab Objectives"
    By the end of this lab, you will be able to:

    - Configure a native Webex Campaign Manager outbound IVR campaign.
    - Import or configure a baseline Webex AI Agent for the debt-resolution scenario.
    - Attach tenant-provisioned MCP tools to the AI Agent and validate tool execution.
    - Route Campaign Manager live-voice calls into the AI Agent.
    - Enable Real-Time Assist for a human escalation scenario if the core path completes on time.

???+ note "What Is Pre-Staged"
    The following items should already be available in the lab tenant:

    - Webex Contact Center tenant with Campaign Manager enabled.
    - Webex AI Agent and AI Assistant features enabled.
    - Tenant-provisioned MCP Agentic App and tools.
    - Baseline AI Agent import package [VERIFY: add exact filename and location].
    - Test customer data available through the MCP server [VERIFY: confirm test records and phone numbers].
    - An agent queue and desktop layout suitable for RTA, or a provided desktop layout template.

## 4-Hour Agenda

| Time | Segment | Outcome |
|---|---:|---|
| 0:00-0:10 | Orientation | Confirm tenant access, lab naming, test number, and MCP assumptions. |
| 0:10-1:55 | Lab 1 - Native Campaign Manager | Build and activate the outbound campaign, upload a contact list, and receive the validation call. |
| 1:55-2:05 | Break / catch-up | Absorb Campaign Manager processing delays. |
| 2:05-3:00 | Lab 2 - AI Agent with MCP | Import/configure Alex, select MCP tools, and validate the AI Agent in Preview. |
| 3:00-3:25 | Lab 2 - Campaign to AI Agent | Replace the temporary Lab 1 message flow with Virtual Agent V2 and test the outbound call to Alex. |
| 3:25-4:00 | Lab 3 - Real-Time Assist | Enable AI Assistant features, create/assign the RTA skill, and validate guidance in Agent Desktop. |

!!! warning "Time Box"
    The lab is designed to fit 4 hours. If Campaign Manager processing or tenant access delays consume the RTA window, complete Labs 1 and 2 first. RTA is valuable, but the primary success path is outbound campaign to MCP-enabled AI Agent.


## Useful Links

- [Control Hub](https://admin.webex.com)
- [Webex Developer Portal](https://developer.webex.com)
- Campaign Manager portal: [VERIFY: add tenant-specific Campaign Manager URL]
- AI Agent Studio: Open from **Control Hub** > **Contact Center** > **Quick Links** > **Webex AI Agent**
