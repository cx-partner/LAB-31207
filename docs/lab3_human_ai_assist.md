# Lab 3 - Real-Time Assist

## Lab Purpose

In Lab 2, you connected the outbound campaign to Alex, an MCP-enabled Webex AI Agent. In this lab, you will add a short human-assist path using **Webex Contact Center AI Assistant**, **Real-Time Transcription**, **Generated Summaries**, and **Real-Time Assist**.

Because the MCP server is already provisioned, this lab focuses on enabling the feature, assigning the skill, and validating that the human agent receives useful guidance during a live call.

???+ purpose "Lab Objectives"
    By the end of this lab, you will be able to:

    - Enable AI Assistant features needed for RTA.
    - Confirm the Agent Desktop layout exposes AI Assistant and Real-Time Transcript components.
    - Create or import a compact Real-Time Assist skill.
    - Optionally attach MCP-backed actions to the skill [VERIFY].
    - Assign the skill to the target queue.
    - Validate transcript, summary, and guidance during a human escalation scenario.

???+ challenge "Lab Outcome"
    A human agent receives the call after Alex escalates or after the lab facilitator routes the test to the queue. The Agent Desktop shows Real-Time Transcript, AI Assistant guidance, and a generated summary.

---

## Pre-requisites

In order to complete this lab, you must have:

* [x] Completed [Lab 2 - AI Agent with MCP](lab2_debt_ai_agent.md).
* [x] A queue and agent available for the human-assist scenario.
* [x] AI Assistant features enabled or admin access to enable them.
* [x] Desktop layout with AI Assistant and Real-Time Transcript components, or the provided template.
* [x] RTA baseline skill import package [VERIFY: add exact filename], or permission to create the skill manually.

!!! note "RTA Time Box"
    This lab is designed to fit the final 35-40 minutes of LAB-31207. If the core outbound-to-AI-Agent path took longer than expected, complete only the AI Assistant feature enablement and queue assignment, then use the remaining time for validation.

---

## Lab Overview

In this lab you will perform the following tasks:

1. Enable AI Assistant features in Control Hub.
2. Confirm the flow supports Real-Time Transcription.
3. Confirm or update the Desktop Layout.
4. Create or import the Real-Time Assist skill.
5. Assign the skill to the queue.
6. Test the assisted handoff.

---

## Lab 3.1 - Enable AI Assistant Features

???+ webex "Configure AI Assistant Features"
    1. Open [Control Hub](https://admin.webex.com).
    2. Navigate to **Contact Center** > **AI Features**. In some tenants, this menu may appear as **AI Assistant**.
    3. Enable **Generated Summaries**.
    4. Select the summarization types required for the lab. For a shared lab tenant, selecting **All queues** is the fastest option [VERIFY: tenant policy].
    5. Enable **Real-Time Transcription**.
    6. Enable **Real-Time Assist**.
    7. Save the configuration.

!!! note
    In production, these features are usually scoped by queue. For this lab, use the assigned queue for the exercise.

---

## Lab 3.2 - Confirm Real-Time Transcription in the Flow

Real-Time Transcription requires media streaming to start when the human agent accepts the call.

???+ webex "Add Start Media Stream"
    1. Open the `AI_Agent_DebtCollection` flow in **Control Hub** > **Contact Center** > **Flows**.
    2. Go to **Event Flows**.
    3. Drag a **Start Media Stream** node onto the canvas.
    4. Connect the **AgentAnswered** event node to **Start Media Stream**.

        !!! info "Event Name"
            In some tenants, **AgentAnswered** appears as **AgentAccepted**. Use the event that is available in your Flow Designer.

    5. Connect **Start Media Stream** to **End Flow**.
    6. Validate and publish the flow.

???+ webex "Route Escalation to the Queue"
    1. In the **Main Flow**, locate the **Virtual Agent V2** node used for Alex.
    2. Connect the **Escalated** outcome to the queue used by the human agent [VERIFY: exact queue node and queue name].
    3. Keep the **Errored** outcome connected to a safe fallback path.
    4. Publish the flow.

!!! warning
    The exact escalation routing depends on the tenant's existing queue and flow design. If the baseline flow already includes the queue route, verify the path and continue.

---

## Lab 3.3 - Confirm Desktop Layout

The Agent Desktop must expose the AI Assistant and Real-Time Transcript surfaces.

???+ webex "Desktop Layout Check"
    1. In Control Hub, navigate to **Contact Center** > **Desktop Layouts** [VERIFY: exact path].
    2. Open the layout assigned to the lab agent's team.
    3. Confirm the layout includes the AI Assistant component.
    4. Confirm the layout includes Real-Time Transcript tab/panel support.
    5. Assign the layout to the team used by the human agent.

!!! download "Desktop Layout Template"
    If a template is needed, use `docs/bcamp_files/Finance_Desktop.json` [VERIFY: replace with LAB-31207-specific desktop layout if provided].

---

## Lab 3.4 - Create or Import the Real-Time Assist Skill

Use an import package if one is provided. If not, create a compact skill manually.

???+ webex "Import or Create the RTA Skill"
    1. Open **Webex AI Agent Studio** from Control Hub.
    2. Select the **AI Assistant Skill** area [VERIFY: exact icon/label].
    3. Import the baseline skill package [VERIFY: exact filename], or click **Create Skill** > **Start from scratch**.
    4. Use the following values if creating manually:

        | Field | Value |
        |---|---|
        | **Skill name** | `LAB31207_RTA_Assistant` |
        | **Goal** | `Assist the human agent during a debt-resolution or fraud/dispute conversation by providing concise next-step guidance based on the live transcript.` |

    5. Add or confirm the instructions:

        ```text
        You assist the human agent, not the customer.

        Watch the live conversation for identity verification issues, balance questions, payment intent, dispute language, suspicious transaction language, and requests for a human specialist.

        Keep guidance short and actionable. Tell the agent what to ask next, what to confirm, and what to avoid saying.

        If MCP tools are available to this AI Assistant skill, use them only when the required values were explicitly provided in the conversation or confirmed by the human agent [VERIFY]. Do not invent customer IDs, transaction IDs, payment amounts, or case IDs.

        If the customer disputes a transaction, guide the agent to confirm the transaction details, explain the next step, and create or prepare the case using the configured MCP action [VERIFY: exact action name].
        ```

    6. Attach the fraud or policy Knowledge Base if provided.

        !!! download "Fraud Knowledge Base"
            Use `docs/bcamp_files/Fraud_KB.docx` [VERIFY: keep or replace with LAB-31207-specific RTA KB].

???+ webex "Optional: Add MCP Actions to the RTA Skill"
    1. Open the skill's **Actions** tab.
    2. Click **Add action** or **Select Available** [VERIFY: exact UI label].
    3. Select the MCP tools intended for human-agent assistance [VERIFY: exact tool list].

        | Tool | Purpose |
        |---|---|
        | `[VERIFY: get_recent_transactions]` | Retrieve recent transactions when the customer disputes a charge. |
        | `[VERIFY: create_case]` | Create or prepare a dispute/fraud case after agent confirmation. |
        | `[VERIFY: get_customer_summary]` | Retrieve customer context for the agent. |

    4. Mark agent review/confirmation as required where the UI supports it [VERIFY].
    5. Save and publish the skill.

!!! important "MCP-Backed RTA Actions"
    If RTA needs an action, use the MCP tool selected from the pre-provisioned Agentic App.

---

## Lab 3.5 - Assign the Skill to the Queue

???+ webex "Assign RTA Skill"
    1. Go to **Control Hub** > **Contact Center** > **AI Features**.
    2. Open the **Queue** tab [VERIFY: exact UI label].
    3. Select the queue used by the lab's human agent.
    4. In the **Real-Time Assist** section, enable **Apply Real-Time Assist**.
    5. Select `LAB31207_RTA_Assistant`.
    6. Save the queue configuration.

???+ info "Skill-to-Queue Mapping"
    RTA skills are assigned to queues. Any agent receiving a call from the assigned queue should receive the skill's guidance for that interaction.

---

## Lab 3.6 - Test RTA

???+ webex "Execute the Test"
    1. Start the outbound call from Campaign Manager or use the provided inbound shortcut [VERIFY].
    2. Speak with Alex and trigger the escalation path by saying something like:

        <copy>`I do not recognize one of these transactions and want to speak with someone.`</copy>

    3. Accept the call as the human agent.
    4. Confirm the Agent Desktop shows:

        | Feature | Expected Result |
        |---|---|
        | Real-Time Transcript | Live transcript appears after the agent accepts the call. |
        | AI Assistant | Guidance appears during the conversation. |
        | RTA Skill | Guidance matches the dispute/fraud scenario. |
        | MCP Action [VERIFY] | If configured, action suggestions require confirmed values before execution. |
        | Generated Summary | Summary appears during wrap-up or after call completion [VERIFY]. |

    5. End the call and review the generated summary.

???+ failure "Troubleshooting"
    - **No transcript**: Confirm **Start Media Stream** is connected from **AgentAnswered** or **AgentAccepted**.
    - **No RTA guidance**: Confirm the skill is published and assigned to the queue receiving the call.
    - **No AI Assistant widget**: Confirm the Desktop Layout includes the AI Assistant component and is assigned to the agent's team.
    - **MCP action unavailable**: Confirm MCP actions are supported for the RTA skill in this tenant [VERIFY]. Use guidance-only RTA if not.

---

## Lab Completion

At this point, you have successfully:

- [x] Enabled AI Assistant, RTT, summaries, and RTA.
- [x] Confirmed the flow can start media streaming for RTT.
- [x] Created or imported an RTA skill.
- [x] Assigned the skill to the queue.
- [x] Tested human-agent guidance during the escalation scenario.

**Congratulations!** You have completed the LAB-31207 core journey: native Campaign Manager to MCP-enabled AI Agent, with Real-Time Assist for the human handoff.
