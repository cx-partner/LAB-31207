# Lab 2 - AI Agent with MCP

## Lab Purpose

In Lab 1, you configured native Campaign Manager to place outbound calls and route live-voice answers into the `AI_Agent_DebtCollection` flow. In this lab, you will configure **Alex**, a Webex AI Agent that uses tenant-provisioned **MCP tools** to retrieve customer context, support the debt-resolution conversation, and prepare the call for human escalation when needed.

The backend actions are provided by the pre-staged MCP server. You will select available MCP tools in AI Agent Studio rather than building fulfillment flows.

???+ purpose "Lab Objectives"
    By the end of this lab, you will be able to:

    - Import or create a baseline autonomous Webex AI Agent.
    - Review the agent prompt, welcome message, and knowledge configuration.
    - Select available MCP tools as AI Agent actions.
    - Validate MCP tool execution in AI Agent Preview.
    - Connect the outbound campaign flow to Alex using Virtual Agent V2.

???+ challenge "Lab Outcome"
    At the end of Lab 2, an answered outbound campaign call is routed to Alex. Alex can greet the customer by name, use MCP tools to look up account context [VERIFY], and handle the debt-resolution scenario.

---

## Pre-requisites

In order to complete this lab, you must have:

* [x] Completed [Lab 1 - Native Campaign Manager](lab1_campaign_manager.md).
* [x] Access to **Control Hub** and **Webex AI Agent Studio**.
* [x] MCP Agentic App already provisioned in the Webex tenant.
* [x] MCP tools already enabled by the tenant administrator [VERIFY: confirm tool list].
* [x] Baseline AI Agent import package available [VERIFY: add exact filename and download link].

!!! important "MCP-Backed Actions"
    Backend actions for this lab are exposed as MCP tools. When you configure Alex, select the available MCP tools in AI Agent Studio.

---

## Lab Overview

In this lab you will perform the following tasks:

1. Import the baseline AI Agent configuration.
2. Review Alex's profile, instructions, and Knowledge Base.
3. Select MCP tools as AI Agent actions.
4. Test Alex in Preview.
5. Connect Alex to the outbound campaign call flow.
6. Run the complete outbound test.

---

## Lab 2.1 - Import the Baseline AI Agent

The fastest path for a 4-hour lab is to import a baseline agent and review the important configuration, instead of building every prompt and action from scratch.

???+ webex "Import Alex"
    1. From [Control Hub](https://admin.webex.com), navigate to **Contact Center**.
    2. Under **Quick Links**, open **Webex AI Agent**.
    3. In AI Agent Studio, select the import option [VERIFY: exact UI label].
    4. Import the baseline package: `[VERIFY: LAB-31207_Alex_baseline filename]`.
    5. Open the imported agent and confirm the name:

        | Field | Value |
        |---|---|
        | **Agent Name** | `LAB31207_Alex` |
        | **Agent Type** | `Autonomous` |
        | **Use Case** | Debt-resolution outbound assistant |

    6. Save the imported agent without publishing yet.

!!! note "If Import Is Not Available"
    If the import option is not available in your tenant, create the agent manually with **Start from scratch** and use the profile values in the next section. This fallback is expected to take longer, so the lab facilitator may provide a pre-created agent instead.

???+ webex "Review Alex's Profile"
    Confirm or populate the following values:

    | Field | Value |
    |---|---|
    | **Welcome message** | `Hello, I'm Alex from Webex Financial Group. Am I speaking with {{firstName}} {{lastName}}?` |
    | **Primary context variables** | `firstName`, `lastName`, `phoneNumber` |
    | **Tone** | Professional, concise, and helpful |
    | **Escalation behavior** | Escalate when the customer disputes a transaction, requests a human, or cannot be verified [VERIFY]. |

    Use the following compact instruction set if you are configuring manually:

    ```text
    You are Alex, a Webex Financial Group AI Agent supporting an outbound debt-resolution call.

    Confirm whether you are speaking with {{firstName}} {{lastName}}. Keep responses short and suitable for voice.

    Use MCP tools for customer lookup, authentication, balance or debt lookup, recent transactions, payment or promise-to-pay handling, and escalation support. Do not invent customer data. If a required value is missing, ask the customer or explain that you need to transfer to a specialist.

    Never disclose sensitive information before customer verification. Never ask for full PINs, full card numbers, passwords, or one-time passcodes.

    If the customer disputes a transaction, suspects fraud, asks for a human, or cannot be verified, prepare the escalation context and transfer to a specialist using the configured transfer path [VERIFY: transfer action name].
    ```

---

## Lab 2.2 - Review Knowledge Configuration

Alex should have enough knowledge to answer basic policy and product questions without turning the lab into a content-ingestion exercise.

???+ webex "Confirm Knowledge Base"
    1. Open Alex in AI Agent Studio.
    2. Select the **Knowledge** tab.
    3. Confirm the baseline Knowledge Base is attached [VERIFY: exact KB name].
    4. If the Knowledge Base is missing, create one using the provided document:

        !!! download "Knowledge Base Document"
            Use `docs/bcamp_files/Webex_Financial_Group_KB.docx` [VERIFY: keep or replace with LAB-31207-specific KB].

    5. Wait for the source to reach the **Processed** state before final testing.

!!! note
    Knowledge processing can take several minutes. Continue with MCP action selection while processing completes.

---

## Lab 2.3 - Select MCP Tools as Actions

The MCP server is already added to the Webex tenant. You only need to select the available MCP tools from the AI Agent action configuration.

???+ webex "Add MCP Tools to Alex"
    1. In AI Agent Studio, open `LAB31207_Alex`.
    2. Select the **Actions** tab.
    3. Click **Add actions**.
    4. Choose **Select Available** [VERIFY: exact UI label].
    5. Select the MCP tools provided for LAB-31207.

        | Tool | Purpose | Status |
        |---|---|---|
        | `[VERIFY: get_customer_profile]` | Retrieve customer identity and profile context. | Required |
        | `[VERIFY: verify_customer]` | Validate customer identity using the lab-safe verification method. | Required |
        | `[VERIFY: get_debt_summary]` | Retrieve balance, maturity date, and debt context. | Required |
        | `[VERIFY: get_recent_transactions]` | Retrieve recent transaction context for disputes or questions. | Recommended |
        | `[VERIFY: create_payment_or_promise]` | Record payment intent, promise-to-pay, or next step. | Recommended |
        | `[VERIFY: prepare_escalation]` | Package context for human escalation. | Required for RTA path |

    6. Review each selected action and confirm the input schema is automatically populated from the MCP tool definition.
    7. Click **Save changes**.

!!! warning "Tool Names and Schemas"
    Use the tool names and input fields shown in your tenant. If a value in this guide is marked `[VERIFY]`, confirm the exact name with the lab facilitator before continuing.

---

## Lab 2.4 - Test Alex in Preview

Before connecting Alex to the campaign, validate the agent in Preview. This lets you troubleshoot prompt or tool issues without waiting for Campaign Manager to dial.

???+ tool "Preview Test"
    1. In AI Agent Studio, open `LAB31207_Alex`.
    2. Click **Preview**.
    3. Start a conversation with a test customer identity provided by the lab facilitator [VERIFY: test customer values].
    4. Confirm Alex can:

        | Check | Expected Result |
        |---|---|
        | Name confirmation | Alex confirms the test customer's name. |
        | Customer lookup | MCP customer lookup succeeds. |
        | Verification | Alex follows the lab-safe verification process. |
        | Debt summary | Alex retrieves and explains balance/maturity context. |
        | Transaction question | Alex uses the transaction tool or explains the limitation. |
        | Escalation trigger | Alex prepares transfer context when fraud/dispute is mentioned [VERIFY]. |

    5. If a tool fails, open the session details and confirm the exact input sent to the MCP tool.

???+ failure "Troubleshooting"
    - **No MCP tools are visible**: Confirm the Agentic App is allowed and tools are enabled for the organization [VERIFY: admin path].
    - **Tool requires unknown input**: Check the MCP schema and update the prompt so Alex knows where to get the value.
    - **Preview works but voice does not**: Confirm the flow passes `phoneNumber`, `firstName`, and `lastName` to Virtual Agent V2.

---

## Lab 2.5 - Connect the AI Agent to the Outbound Call

At the end of Lab 1, the outbound call routes to `AI_Agent_DebtCollection`, which currently plays a temporary completion message. Replace that message with Alex.

???+ webex "Deliver the Outbound Call to Alex"
    1. Go to **Control Hub** > **Contact Center** > **Flows**.
    2. Open the `AI_Agent_DebtCollection` flow.
    3. Enable editing.
    4. Delete the temporary **Play Message** node from Lab 1.
    5. Drag a **Virtual Agent V2** node onto the canvas.
    6. Connect the **NewPhoneContact** or **StartFlow** node to **Virtual Agent V2**.
    7. Configure the **Virtual Agent V2** node:

        | Field | Value |
        |---|---|
        | **Activity Label** | `DebtCollectionAgent` |
        | **Contact Center AI Config** | `Webex AI Agent (Autonomous)` |
        | **Virtual Agent** | `LAB31207_Alex` |

    8. In **State Event**, set **Event Data** to:

        ```json
        {
          "phoneNumber": "{{NewPhoneContact.DNIS}}",
          "firstName": "{{firstName}}",
          "lastName": "{{lastName}}"
        }
        ```

    9. Connect the **Handled** outcome to **End Flow**.
    10. Connect **Errored** and **Escalated** to a temporary **Play Message** or to the escalation queue if you are continuing directly into Lab 3 [VERIFY: chosen path].
    11. Validate and publish the flow.

!!! important
    The values on the left side of the JSON (`phoneNumber`, `firstName`, `lastName`) must match the variables Alex expects. The values on the right side come from the Campaign Manager contact list and flow variable mapping created in Lab 1.

---

## Lab 2.6 - Test the Complete Scenario

???+ webex "Run the Outbound Test"
    1. In Campaign Manager, upload a contact list with your test customer's `firstName`, `lastName`, and `phoneNumber`.
    2. Wait for the contact list to become active.
    3. Answer the outbound call.
    4. Confirm Alex greets the customer by name.
    5. Complete the verification and debt-summary path using the MCP tools.
    6. Ask a transaction or dispute question to confirm Alex uses the relevant MCP tool or prepares escalation context [VERIFY].

!!! warning
    Campaign Manager can take 2-5 minutes to generate the call after the contact list is active. Use Preview for troubleshooting tool behavior and use the live call only for final validation.

---

## Lab Completion

At this point, you have successfully:

- [x] Imported or configured Alex.
- [x] Attached tenant-provisioned MCP tools as AI Agent actions.
- [x] Tested Alex in Preview.
- [x] Connected the outbound campaign to Alex.
- [x] Completed an outbound call into an MCP-enabled AI Agent.

[Next Lab: Lab 3 - Real-Time Assist](./lab3_human_ai_assist.md){ .md-button .md-button--primary }
