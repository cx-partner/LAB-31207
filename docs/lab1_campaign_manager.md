# Lab 1 - Native Campaign Manager

## Lab Purpose

Proactive outbound communication is a key pillar of modern customer engagement. Rather than waiting for customers to call in, organisations can leverage **Webex Contact Center Campaign Manager** to initiate timely, context-rich outbound calls — automatically, at scale, and in full compliance with regulatory requirements.

In this lab, you will configure an **end-to-end outbound IVR campaign** using Webex Campaign Management. This includes setting up the necessary WxCC infrastructure (agents, teams, queues, flows, entry points) and then configuring all Campaign Manager prerequisites before launching a live Progressive IVR campaign targeting a debt collection use case.

???+ purpose "Lab Objectives"
    By the end of this lab, you will have configured the full stack required to run an outbound IVR campaign in Webex Contact Center. Key objectives include:

    - **WxCC Infrastructure Setup:** Configure teams, outdial queues, global variables, and entry points on Collaboration Control Hub.
    - **Flow Design:** Build an outbound campaign flow with CPA-based routing and event flows, including Answer Machine Detection (AMD) and Live Voice handling.
    - **Campaign Manager Configuration:** Complete all prerequisite campaign administration settings including business days, contact modes, field mappings, suppression rules, and telephony outcomes.
    - **Campaign Activation:** Create a campaign group, configure and activate the campaign, and upload a contact list to trigger live calls.

    Note: To allow attendees to complete de labs, some of the items will be pre-configured.

???+ Challenge "Lab Outcome"
    By the end of Lab 1, you will have a fully operational outbound IVR campaign that:

    1. **Dials contacts** from an uploaded CSV contact list using Progressive IVR mode.
    2. **Detects call outcomes** (AMD, Abandoned, Live Voice) and routes them appropriately.
    3. **Plays a congratulatory message** ("Congratulations, you have completed Lab 1") to live voice contacts — confirming the end-to-end campaign flow is working.
    4. **Passes customer data** (first name, last name) as global variables to the destination flow, ready for Lab 2's AI Agent integration.

---

## Pre-requisites

In order to complete this lab, you must have:

* [x] Access to **Webex Collaboration Control Hub** with Full Admin permissions
* [x] A **Webex Contact Center** tenant provisioned and licensed
* [x] Access to the **Webex Campaign Management** portal

---

## Lab Overview 📌

!!! info "POD-specific values"
    After you complete Lab Prework, names in this guide resolve to your assigned POD, such as `POD01` or `Team01`. Select the copy icon beside a value whenever you need to enter it in Collaboration Control Hub or Campaign Manager. If a placeholder remains visible, open **Lab Prework** from this guide in the same browser and select **Get my POD**; your existing assignment is reused.

The diagram below illustrates the high-level architecture and the sequence of configuration steps you will follow throughout this lab:

<figure markdown>
![Lab 1 Architecture Overview](./assets/outbound-campaign-flow.png)
<figcaption>High-level outbound campaign configuration workflow</figcaption>
</figure>

In this lab you will perform the following tasks:

1. Configure a team and enable Contact Center users.
2. Create an Outdial Queue
3. Configure Global Variables and Wrap-up Codes (for the purpose of this lab these 2 items will be preconfigured)
4. Build the Outbound Campaign Flow (Main + Event flows)
5. Create the Outdial Entry Point (Channel) and Outdial ANI
6. Complete Campaign Manager prerequisites
7. Create, activate, and upload contacts to the Campaign

---

## Lab 1.1 - Configure a Team

### Create a Team
Even we won't use any agent to run the IVR campaign, the creation of a **team or agent** to assign to an **outdial queue** is mandatory. The **Entry Point** need to have that queue associated.

???+ webex "Create Team"


    ???+ inline vidcast "Create a team"
        <video controls width="600">
        <source src="/LAB-31207/assets/create_team.mp4" type="video/mp4">
        </video>
        <p><a href="/LAB-31207/assets/create_team.mp4" target="_blank" rel="noopener">Open video in new tab</a></p>

      1. In Collaboration Control Hub, navigate to **Contact Center** → **Teams**.
      2. Click **Create a team** and fill in the following:

        | Field | Value |
        |---|---|
        | **Name** | <copy>`Team<yourpodnumber>`</copy> |
        | **Parent site** | `Site-1` |
        | **Team type** | `Agent-based` |
        | **Multimedia profile** | `Default_Multimedia_Profile` |
        | **Desktop layout** | `Global Layout` |

     3. Click **Create**.

---

## Lab 1.2 - Enable and configure contact center agent

### Enable and configure contact center agent
After creating your team, we will enable and configure the contact center agent. Please, select the agent that contain your pod number.

???+ webex "Enable and configure contact center agent"


    ???+ inline vidcast "Enable and configure contact center agent"
        <video controls width="600">
        <source src="/LAB-31207/assets/lab1_enable_cc_user.mp4" type="video/mp4">
        </video>
        <p><a href="/LAB-31207/assets/lab1_enable_cc_user.mp4" target="_blank" rel="noopener">Open video in new tab</a></p>

      1. In Collaboration Control Hub, navigate to **Contact Center** → **Contact Center Users**.
      2. Click on the **agent** user that belong to your pod number and fill in the following:

        | Field | Value |
        |---|---|
        | **Contact Center** | `enabled (toggle ON)` |
        | **Site** | `Site-1` |
        | **Team** | `Team<yourpodnumber>` |
        | **Desktop Profile** | `Agent_profile` |

     3. Click **Save**.

---

## Lab 1.3 - Create an Outdial Queue

The outdial queue is what connects your outbound campaign to the agent pool. It must be set to **Outbound queue** type and have the **Outbound campaign** toggle enabled.

???+ webex "Create Outdial Queue"

    ???+ inline vidcast "Enable and configure contact center agent"
        <video controls width="600">
        <source src="/LAB-31207/assets/lab1_outdial_queue.mp4" type="video/mp4">
        </video>
        <p><a href="/LAB-31207/assets/lab1_outdial_queue.mp4" target="_blank" rel="noopener">Open video in new tab</a></p>

    1. In Collaboration Control Hub, navigate to **Contact Center** → **Queues**.
    2. Click **Create a queue** and configure:

        | Field | Value |
        |---|---|
        | **Name** | <copy>`OutdialQ<yourpodnumber>`</copy> |
        | **Contact direction** | `Outbound queue` |
        | **Channel type** | `Telephony` |
        | **Outbound campaign** | Enabled (toggle ON) |
        | **Agent assignment** | `Teams` → select `Team<yourpodnumber>` |

    3. Under **Call distribution**, click **Create a group**, expand it, and select your Team.
    4. Fill in the mandatory **Advanced settings**:

        - **Service level threshold**: *120*
        - **Maximum time in queue**: *30*
        - **Default music in queue**: *defaultmusic_on_hold.wav*

    4. Click **Create**.

    !!! note
        The **Contact direction** and **Channel type** fields cannot be changed after the queue is created. Double-check these values before clicking Create.


---

## Lab 1.4 -  Global Variables and Wrap-up Codes (Pre-Configured)

### Global Variables

Global Variables are used to carry customer data (from the contact list) through the campaign flow and display it on the Agent Desktop. You must create two variables: `firstName` and `lastName`.
All PODs will use the same global variables which are already pre-configured. If you want to check the configuration (OPTIONAL) you can follow the instructions below and check their values.

???+ webex "Check Global Variables"

    1. In Collaboration Control Hub, navigate to **Contact Center** → **Flows** → **Global Variables**.
    2. Click on the **firstName** variable and you must see the following information:

        | Field | Value |
        |---|---|
        | **Name** | `firstName` |
        | **Description** | `firstName` |
        | **Variable type** | `String` |
        | **Make reportable** | Enabled |
        | **Make agent viewable** | Enabled |
        | **Desktop label** | `First Name` |
        | **Edit on desktop** | Disabled |

    3. Click on the top left to go back to **Global Variables**.
    4. Repeat the process to check the **lastName** variable.

    <figure markdown>
    ![Create firstName global variable](./assets/lab1_p5_img2.png)
    <figcaption>Creating the firstName global variable with agent viewable and reportable settings enabled</figcaption>
    </figure>

    !!! important
        Both `firstName` and `lastName` must be added to all flows in this lab — both the dummy test flow and the outbound campaign flow — under **Global Flow Properties** → **Global Variables**. This is will be done in Lab 1.5

### Check Wrap-up Code

A wrap-up code is required by Campaign Manager when configuring the contact attempt strategy. Similar to Global Variables, the wrap-up codes are pre-configured and all the PODs must use the same. You can check the configuration as optional following the next steps.

???+ webex " Wrap-up Code"

    1. In Collaboration Control Hub, navigate to **Contact Center** → **Idle/wrap-up codes**.
    2. Click **debt** wrap-ip code and check the following:

        | Field | Value |
        |---|---|
        | **Name** | `debt` |
        | **Description** | `Debt Collection` |
        | **Make it default** | Enabled |
        | **Code type** | `Default Wrapup Work Type` |

   

    <figure markdown>
    ![Debt wrap-up code](./assets/lab1_p6_img1.png)
    <figcaption>The debt wrap-up code configured in Collaboration Control Hub</figcaption>
    </figure>

---

## Lab 1.5 - Build the Flows

### Create the "Lab2" Dummy Test Flow

Before building the full outbound campaign flow, create a simple **dummy flow** to validate the end-to-end campaign configuration. This same flow will be used as the starting point for **Lab 2**. Name it **PODXX_AI_Agent_DebtCollection**.

The flow plays a congratulatory TTS message when a live voice contact is detected, confirming Lab 1 is fully operational.

???+ webex "Create Lab2 dummy flow"

    1. In Collaboration Control Hub, navigate to **Contact Center** → **Flows**.
    2. Click **Manage Flows -> Create Flows** 
    3. Select **Flow** and **Start from scratch** and click **Next**
    4. Name the flow <copy>`PODXX_AI_Agent_DebtCollection`</copy> and select **Voice** as the channel type.
    3. In the **Global Flow Properties** panel on the right:
        - Under **Global Variables**, click **Add global variables** and add both `firstName` and `lastName`.
    4. From the **Activities Library**, drag a **Play Message** node onto the canvas and connect it to the **NewPhoneContact** Start node.



    5. Configure the **Play Message** node:
        - **Activity Label**: <copy>`EndOfLab1`</copy>
        - Enable **Text-to-Speech**
        - **Connector**: `Cisco Cloud Text-to-Speech`
        - Add **Text-to-Speech Message**: <copy>`Congratulations, You have completed lab 1`</copy>
        - Remove the **Audio file** field.
    6. Drag and drop an **End Flow** node and connect the **Play Message** node to it.
    7. Enable the **Validation** slider at the bottom-right of the editor to validate the flow and then click **Publish Flow** (select **Latest** as the version label).

    <figure markdown>
    ![Lab1_completed flow with TTS message](./assets/lab1_p6_img2.png)
    <figcaption>Lab1_completed flow showing the Play Message node with the congratulatory TTS message and Global Variables added</figcaption>
    </figure>

    <figure markdown>
    ![Play Message TTS configuration](./assets/lab1_p7_img1.png)
    <figcaption>Play Message node configured with Cisco Cloud Text-to-Speech playing "Congratulations, You have completed lab 1"</figcaption>
    </figure>

### Create the Outbound Campaign Flow

Now create the main outbound campaign flow. This flow handles the outbound dialling logic and routes calls based on the CPA (Call Progress Analysis) result.

???+ webex "Create Outbound_DebtCollection Flow"

    1. In Collaboration Control Hub, navigate to **Contact Center** → **Flows**.
    2. Click **Manage Flows -> Create Flows** and select **Flow** and **Start from scratch** in the next window. Click **Next**
    3. Name it <copy>`Outbound_DebtCollection<yourPodNumber>`</copy> and select **Voice** as the channel type.
    3. In the **Global Flow Properties** panel:
        - Under **Global Variables**, add both `firstName` and `lastName`.
    4. The Main flow canvas starts with a **NewContact** Start Flow node.
    

        Connect it to an **End Flow** node as a placeholder — the actual logic is handled in Event flows.

    <figure markdown>
    ![Outbound_DebtCollection flow global variables](./assets/lab1_flow1_1.png)
    <figcaption>Outbound_DebtCollection flow showing firstName and lastName Global Variables added to the flow configuration</figcaption>
    </figure>

#### Configure Event Flows

The campaign logic is driven by **Event flows**. Click on **Event flows** at the top of the flow builder to switch to the event flow canvas. You will configure one key event:

**OutboundCampaignCallResult**

This event triggers when the dialler receives a CPA result for an outbound call attempt. It determines whether the call reached an answering machine, was abandoned, or reached a live conversation.

???+ webex "Configure OutboundCampaignCallResult Event"

    1. On the Event flows canvas, locate the **OutboundCampaignCallResult** event handler node.
    2. Drag a **Case** node onto the canvas and connect the **OutboundCampaignCallResult** event handler to it.
    3. Configure the **Case** node:
        - **Activity Label**: <copy>`Campaign_Results`</copy>
        - **Case variable**: `OutboundCampaignCallResult.CPAResult`
        - Add the following case outputs:

            | Case | Value |
            |---|---|
            | **AMD** | <copy>`AMD`</copy> |
            | **ABANDONED** | <copy>`ABANDONED`</copy> |
            | **LIVE_VOICE** | <copy>`LIVE_VOICE`</copy> |
            | **Default** | (default fallthrough) |

    <figure markdown style="width: 70%;">
    ![Event flows overview](./assets/lab1_flow_case.png)
    <figcaption>Case node configured with CPAResult variable showing AMD, ABANDONED, and LIVE_VOICE outputs</figcaption>
    </figure>


**Handling AMD and Abandoned outcomes:**

???+ webex "Configure AMD and Abandoned Routing"

    1. Drag a **Play Message** node onto the canvas.
    2. Connect both the **AMD** and **ABANDONED** outputs of the Case node to this Play Message node.
    3. Configure the Play Message node:
        - Enable **Text-to-Speech**
        - **Connector**: `Cisco Cloud Text-to-Speech`
        - **Text-to-Speech Message**: `Goodbye`
        - Remove the **Audio file** field.
    4. Drag and **End Flow** message to the canvas and connect the **Play Message** node to an **End Flow** node.

    <figure markdown>
    ![Play Message Goodbye configuration](./assets/lab1_p9_img2.png)
    <figcaption>Play Message node configured with TTS "Goodbye" for AMD and Abandoned call outcomes</figcaption>
    </figure>

**Handling Live Voice outcome:**

???+ webex "Configure Live Voice Routing"

    1. Drag a **Go To** node onto the canvas.
    2. Connect the **LIVE_VOICE** output of the **Case** node to the **Go To** node.
    3. Connect also the **Default** output of the **Case** node to the **Go To** node.
    3. Configure the **Go To** node:
        - **Activity Label**: `GoTo_AIAgent`
        - **Destination type**: `Flow`
        - **Flow type**: `Static Flow`
        - **Flow**: <copy>`PODXX_AI_Agent_DebtCollection`</copy> *(this will be used in Lab 2)*
        - **Version Label**: `Latest`
    4. Under **Flow Variable Mapping**, map the global variables from the current flow to the destination flow:

        | Current variable | Destination variable |
        |---|---|
        | `firstName` | `firstName` |
        | `lastName` | `lastName` |

    5. Connect the **Undefined Errors** outlet of the **GoTo** node to the **End Flow** node.

        !!! important
            The **Flow Variable Mapping** is critical for Lab 2. This ensures that the customer's first and last name (loaded from the campaign contact list) are passed to the destination flow where the AI Agent will use them.

        <figure markdown>
            <figure markdown style="width: 80%;" >
            ![GoTo AIAgent node configuration](./assets/lab1_flow_Goto.png)
            <figure markdown style="width: 30%;" >
            ![GoTo AIAgent flow variable mapping](./assets/lab1_p10_img2.png)
            <figcaption>Go To node pointing to the POD-specific AI Agent flow with firstName and lastName mapped across flows</figcaption>
        </figure>


    6. Connect the **Undefined Errors** output of the **Case** node to the **End Flow** node.

    7. Enable the **Validation** slider to validate the flow and once validated, click **Publish Flow** to publish it. 

    Your **Outbound DebtCollection** flow is ready.  

---

## Lab 1.6 - Create the Outdial Entry Point (Channel) and Outdial ANI

### Create the Outdial Entry Point

The Entry Point (Channel) is the outbound telephony channel that ties together the flow, the outdial queue, and the dialling configuration.

???+ webex "Create Outdial Entry Point (aka Channel)"

    ???+ inline vidcast "Create Outdial Entry Point (aka channel)"
        <video controls width="600">
        <source src="/LAB-31207/assets/lab1_EP_Creation.mp4" type="video/mp4">
        </video>
        <p><a href="/LAB-31207/assets/lab1_EP_Creation.mp4" target="_blank" rel="noopener">Open video in new tab</a></p>

    1. In Collaboration Control Hub, navigate to **Contact Center** → **Channels**.
    2. Click **Create a channel** and configure:

        | Field | Value |
        |---|---|
        | **Name** | `Campaign_EP_<yourPodNumber>` |
        | **Channel type** | `Outbound telephony` |
        | **Service level threshold** | `30` seconds |
        | **Timezone** | `Europe/London` *(use your local timezone)* |
        | **Routing flow** | `Outbound_Debt_Collection<youtPodNumber>` the one you create on the previous step |
        | **Music on hold** | `defaultmusic_on_hold.wav` |
        | **Version label** | `Latest` |
        | **Outdial queue** | `OutdialQ<yourPodNumber>` the one you create in the previous step|

    3. Click **Create**.


###  Outdial ANI (Pre-Configured)

The Outdial ANI is the caller ID displayed to customers when they receive the outbound call. You can configure multiple ANIs for different regions. For the purpose of this lab, all attendes will use the same Outdial ANI which will be preconfigured. If you want to check the configuration (OPIONAL) you can follow this steps.

???+ webex "Outdial ANI"

    1. In Collaboration Control Hub, navigate to **Contact Center** → **Outdial ANI**.
    2. Click on **OutdialANI_All** and you will see:
        - **Name**: `OudialANI_All`
    3. Under **Configured ANIs**, you should see the following:
        - **Name**: `Campaign`
        - **Contact Number**: `+17382033500`
        - **Default ANI**: `Campaign(+17382033500)`
  

    <figure markdown style="width: 70%;">
    ![LAB31207_outANI configuration](./assets/Lab1_OutdialANI.png)
    <figcaption>OutdialANI configured for outdial caller ID</figcaption>
    </figure>

    !!! Important
        In order to configure the **Outdial ANI**, a PSTN number must a assigned to an **Inboud Telephony Entry Point** (aka **Channel**) first.
---


## Lab 1.7 - Campaign Manager Configuration

Open the [Webex Campaign Management portal](https://campaignmanager.wxcc-us1.cisco.com/nextgen/login?orgId=36db6df3-4ec3-4eb9-905b-d90660c2c2ea). On first login, you will see the welcome screen outlining all the administration areas to configure before launching campaigns.

<figure markdown style="width: 70%;">
![Campaign Manager welcome screen](./assets/lab1_p13_img1.png)
<figcaption>Welcome to Webex Campaign Management — administration checklist</figcaption>
</figure>

Once in the Campaign Manager configuration portal, you can click on the different options from the left navigation panel, and will go through each item as described in the sections below. 

<figure markdown style="width: 30%;">
![Campaign Manager Administration](./assets/lab1_CM_options.png)
<figcaption>Welcome to Webex Campaign Management — Configuration Options</figcaption>
</figure>

### Business Days (Only Informational, no configuration is required)

Business days are used solely for the purpose of contact list expiry calculation. They have no association with 'Business hours' on Collaboration Control Hub. We won't use this option as part of this lab.

### Contact Modes (Pre-configured)

Contact modes define the type of phone number in your contact list (e.g. Home, Office, Mobile). For this lab, we use a single contact mode mapped to the `phoneNumber` column in the CSV. All the PODs will use the same pre-configured contact mode called **phone**

???+ webex "Verify Contact Mode"

    1. Navigate to **Campaign data config** → **Contact modes**.
    2. Click **phone** contact mode and the following details should be displayed:

        | Field | Value |
        |---|---|
        | **Contact mode name** | `phone` |
        | **Contact mode type** | `Voice` |
        | **Description** | *(optional)* |
        | **Minimum length** | `7` |
        | **Maximum length** | `15` |


    <figure markdown style="width: 60%;">
    ![Create contact mode](./assets/lab1_p15_img1.png)
    <figcaption>Creating the phone contact mode with Voice type and default length constraints</figcaption>
    </figure>

### DNC Lists (Only Informational, No configuration is required)

Do Not Contact (DNC) lists prevent the campaign from calling restricted numbers. For this lab, **no DNC list will be configured**.

!!! info
    In production environments, you would upload DNC lists here to comply with regulatory requirements (e.g., national DNC registries). The campaign engine automatically suppresses any contacts matched against active DNC lists.

### Global Variables (Pre-loaded by the sync between WxCC and Campaign Manager)

Global variables are synced from Collaboration Control Hub. They appear here for informational purposes — you cannot create or modify them in Campaign Manager.

???+ webex "Verify Global Variables"

    1. Navigate to **Organization config** → **Global variables**.
    2. Verify that `firstName` and `lastName` are listed with **Status: Active** and **Agent view: Yes**.

        If you don´t see the variables, click *Refresh from Collaboration Control Hub* at the top-right of the page

    ???+ note
        Campaign Manager is case-insensitive. If variables in Collaboration Control Hub differ only by character case, Campaign Manager will treat them as duplicates and only import one of them. E.g. if *lastname* and *Lastname* are global variables in Collaboration Control Hub, Campaign Manager will ignore one of them.

    !!! important
        Before you can use Global Variables in Campaign Manager, you must designate a **customer-unique-identifier** and **account-unique-identifier** for compliance with call attempt regulations. For this lab, since we are not configuring unique identifiers, this step is skipped.

    <figure markdown>
    ![Global variables in Campaign Manager](./assets/lab1_p16_img1.png)
    <figcaption>Global variables list showing firstName and lastName as Active, agent-viewable, and reportable</figcaption>
    </figure>

### Field Mappings

Field mappings define how the columns in your CSV contact list map to the Campaign Manager's dialler system, including which column contains the phone number, which global variables carry the customer name, and the data types.

#### Prepare the Contact List CSV

Before creating the field mapping, create your contact list file.

???+ webex "Create Contact List CSV"

    Create or [download](./bcamp_files/contact_list_lab31207.csv) a CSV file named `contact_list_lab31207.csv` with the following header structure:

    ```csv
    firstName,lastName,phoneNumber
    John,Smith,+14085052211
    ```

    Populate your own customer `firstName`, `lastName`, and `phoneNumber`. Use the test customer details provided for LAB-31207.

    !!! note
        - All phone numbers must use the E.164 format with the `+` prefix and country code (e.g. `+14085052211`).
        - All rows within a single file must use numbers from the **same country**.
        - Spaces, hyphens, or other special characters in phone numbers are not permitted.

    <figure markdown>
    ![Contact list CSV structure](./assets/lab1_p16_img2.png)
    <figcaption>contact_list_lab31207.csv showing the three-column header: firstName, lastName, phoneNumber</figcaption>
    </figure>

#### Create the Field Mapping

???+ webex "Create Field Mapping"

    1. Navigate to **Campaign data config** → **Field mappings**.
    2. Click **Create field mapping**.
    3. Enter a **Field mapping name**: `field_mapping_<yourPodNumber>`

    **Step 1 — Upload sample file:**

    Click **Choose file** and select your `contact_list_lab31207.csv`. Once uploaded, the system displays the detected headers: `firstName`, `lastName`, `phoneNumber`.

    <figure markdown>
    ![Field mapping upload](./assets/lab1_CM_FM1.png)
    <figcaption>Field mapping showing field_mapping<yourPodNumber> with the uploaded CSV and 3 detected headers</figcaption>
    </figure>

    **Step 2 — Map contact modes:**

    In the **Map contact modes** section, map the `phoneNumber` column to the `Phone` contact mode you created earlier. Leave `firstName` and `lastName` as **Unmapped** at this stage.

    <figure markdown style="width: 60%;">
    ![Map contact modes](./assets/lab1_CM_FM2.png)
    <figcaption>Contact mode mapping showing phoneNumber mapped to the Phone contact mode</figcaption>
    </figure>

    **Step 3 — Specify country of all phone numbers:**

    Select the appropriate country code for your numbers and set the format to:
    *`Prefixed with + sign and country code i.e. '+<country code><phone number>'`*

    <figure markdown style="width: 80%;">
    ![Country and phone number format](./assets/lab1_CM_FM3.png)
    <figcaption>Phone number format set to E.164 with + prefix and country code</figcaption>
    </figure>

    **Step 4 — Map source of timezones:**

    Keep the default configuration.

    **Step 5 — Map global variables:**

    Map each column in the CSV file to the corresponding Global Variable:

    | File header | Global variable | Data type |
    |---|---|---|
    | `firstName` | `firstName` | String |
    | `lastName` | `lastName` | String |
    | `phoneNumber` | Unmapped | N/A |

    <figure markdown>
    ![Global variable mapping](./assets/lab1_p18_img2.png)
    <figcaption>Global variable mapping</figcaption>
    </figure>

    **Step 6 — Specify file header data types:**

    Leave all columns as **String** data type. Enable **PII protection** for `phoneNumber` if required by your organisation's data handling policies.

    <figure markdown>
    ![File header data types](./assets/lab1_p18_img3.png)
    <figcaption>File header data types: all set to String. PII protection enabled for phoneNumber</figcaption>
    </figure>

    Click **Save** to finalise the field mapping. You might get a pop up message like *Some global variables are unmapped in step# 5*. This is due to the fact the phonenumber is not being mapped to any global variable. That is fine, just click on **Save field mapping as is** to continue. 

### Holidays for All Campaigns (Pre-Configured)

**Holidays for All Campaigns** prevent campaigns from running on specific dates (e.g. national holidays). These exclusions apply to **all campaigns** in the organisation.

???+ webex "Holidays for All Campaigns"

    1. Navigate to **Organization config** → **Holidays for All Campaigns**.
    2. Verify the existing holiday:

        | Exclusion date | Comment |
        |---|---|
        | `Dec 31, 2026` | `End of the Year` |


    <figure markdown>
    ![Org exclusion dates](./assets/lab1_CM-H1.png)
    <figcaption>Exclusion date set for 31 December 2026</figcaption>
    </figure>

    !!! info
        When a campaign is running and an exclusion date is reached, the campaign status automatically changes to **Pending** and calling stops. Once the exclusion date passes, the campaign automatically resumes with **Running** status.

### Purpose Meta-tags (Pre-configured)

Purpose meta-tags allow you to categorise campaigns by business function. They are **mandatory for campaign activation** (though not required to save a campaign in draft). All PODs will use the same pre-configured meta-tag.

???+ webex "Verify Purpose Meta-tag"

    1. Navigate to **Organization config** → **Purpose meta-tags**.
    2. Click on the existing **purpose meta-tag** and verify:
        - **Purpose meta-tag**: `debt`
        - **Purpose meta-tag group**: `DEFAULT`

    <figure markdown style="width: 70%;">
    ![Purpose meta-tag creation](./assets/lab1_CM_PMT.gif)
    <figcaption>Verify the "debt" purpose meta-tag under the DEFAULT group</figcaption>
    </figure>

### P&L Meta-tags (Pre-configured)

P&L (Profit and Loss) meta-tags allow campaigns to be assigned to different business divisions or cost centres. Like purpose meta-tags, they are **mandatory for campaign activation**. All PODs will use the same pre-configured P&L meta-tag.

???+ webex "Verify P&L Meta-tag"

    1. Navigate to **Organization config* → **P&L meta-tags**.
    2. Click on the existing **P&L meta-tag** and verify:
        - **P&L meta-tag name**: `debt`
        - **P&L meta-tag description**: `Debt Department`

    <figure markdown>
    ![P&L meta-tags list](./assets/lab1_cm-plmt.gif)
    <figcaption>P&L meta-tags list showing the debt tag created alongside the system Default tag</figcaption>
    </figure>

### Suppression Rules (Pre-configured)

Suppression rules prevent calls from being made to contacts during restricted time windows or under other compliance conditions. They are evaluated before each call attempt. For this lab, All the PODs will use the same supression rule set named **sr_hours**

???+ webex "Verify Suppression Rule Set and Rule"

    **Step 1 — Very the rule set and supression rule:**

    1. Navigate to **Compliance** → **Suppression rule sets**.
    2. Click **sr_hours**.
    3. Then click on supression rule **sr_after_hours**  
    4. Verifiy the configuration, you will find that the rule has been set to avoid calls between 23rhs to 7hrs.

 

    <figure markdown>
    ![Suppression rule conditions](./assets/lab1_CM_SR.png)
    <figcaption>Suppression rule configured to prevent calls before 07:00 and after 23:00 in the recipient's timezone</figcaption>
    </figure>

    !!! tip
        This rule ensures the campaign never dials contacts during overnight hours, protecting both customer experience and regulatory compliance.

### Telephony Outcomes (Pre-Configured)

A telephony outcome set defines how each possible call result (Busy, No Answer, AMD, etc.) is treated by the campaign — including whether it counts as a contact attempt and how long to wait before retrying.

The system provides a **primary (read-only) outcome set**. We have **duplicated** it to create a configurable version for your campaign. All PODs will use the same telephony outcomes named **Copy_Telephony_Outcome** and we will keep the configuration as it is.

???+ webex "Verify Telephony Outcome Set"

    1. Navigate to **Voice outcome sets** → **Telephony outcome sets**.
    2. Click On the `Copy_Telephony_Outcomes` 
    3. Explore the different outcomes and options.
   

    <figure markdown>

    ![Telephony outcomes list](./assets/lab1_CM_TO.gif)
    <figcaption>Copy_telephony_outcome showing all 20 telephony outcomes including AMD, ABANDONED, LIVE_VOICE, BUSY, INVALID_NUMBER, and others</figcaption>
    </figure>

### UI Users (Only Informational, no configuration is required)

Webex Campaign Management uses **just-in-time (JIT) provisioning** — user accounts are created automatically the first time a user logs in, based on their role in Collaboration Control Hub. No manual user creation is required in Campaign Manager.

<figure markdown>
![UI Users](./assets/lab1_p23_img2.png)
<figcaption>UI Users list showing the admin account provisioned via JIT sync from Collaboration Control Hub</figcaption>
</figure>

For more information, refer to the [Campaign Management UI Users documentation](https://docs-campaign-for-contact-centers.webexcampaign.com/docs/ui-users).

### Wrap-up Code Sets (Pre-Configured)

Wrap-up codes defined in Collaboration Control Hub are synced to Campaign Manager. You can configure how each code affects future campaign contact attempts (e.g. whether a contact with a given wrap-up code should be retried). For this lab, we have created a set called **Finance** which will include the **debt** wrap-up code. All the PODs will use this one to configure the campaign.

???+ webex "Verify Wrap-up Code Set"

    1. Navigate to **Voice outcome sets** → **Wrap-up code sets**.
    2. Click on **Finance**
    3. Verify it coints **debt** wrap-up code.
    
        <figure markdown>
        ![Wrap-up code - sets](./assets/lab1_CM_WUC.gif)

        </figure>


    For more information, refer to the [Wrap-up code sets documentation](https://docs-campaign-for-contact-centers.webexcampaign.com/docs/wrap-up-code-sets).

---

## Lab 1.8 - Campaign Management

With all prerequisites in place, you are ready to create the campaign group, configure the campaign, and activate it.

### Create a Campaign Group

A campaign group is a container (wrapper) for one or more campaigns. You must create the group first before creating any campaigns inside it.

???+ webex "Create Campaign Group"

    1. In Campaign Manager's left navigation panel, navigate to **Campaign management** → **Campaign groups**.
    2. Click **Create campaign group** and enter:
        - **Campaign group name**: `cgroup_<yourPodNumber>`
        - *(All other fields are optional)*
    3. Click **Save & proceed**.


    <figure markdown>
        ![Campaign groups list](./assets/lab1_CM_CG.png)
        <figcaption>Campaign groups list</figcaption>
    </figure>

    <figure markdown style="width: 80%;">
        ![Campaign group detail view](./assets/lab1_p25_img2.png)
    </figure>

### Create and Configure the Campaign

???+ webex "Create Campaign"

    1. Click on the **cgroup_yourPodNumber** campaign group.
    2. Click **Create campaign** in the top-right corner.

        <figure markdown>
        ![Campaign group detail view](./assets/lab1_p26_img1.png)
        </figure>

    3. An untitled campaign opens with a visual node-based configuration canvas. Work through each node from left to right.

    <figure markdown style="width: 80%;">
        ![Campaign flow](./assets/lab1_CM_flow.png)
    </figure>

**Node 1 — Dialer configuration:**

???+ webex "Configure Dialer"

    In the **Dialer configuration** panel on the right side:

    | Field | Value |
    |---|---|
    | **Collaboration Control Hub channel** | `Campaign_EP_<yourPodNumber>` |
    | **Outdial ANI** | `+17382033500` *(select the common Outdial ANI)* |
    | **Dialing mode** | `Progressive IVR` |
    | **CPA parameters** | Enabled (leave defaults) |
    | **# of contacts to be sent to the dialer in each push** | `100` |

    Click **Save changes** at the right-bottom of the page.

    <figure markdown>
    ![Dialer configuration](./assets/lab1_CM_FlowDC.png)
    </figure>

**Node 2 — Contact list configuration:**

???+ webex "Configure Contact List configuration"

    1. Click the **Contact list configuration** node.
    2. The **Select contact list source** is by default set to the options *File* and *API*. We will use manual file upload.
    3. Set **Select field mapping** to the field mapping you created before: `field_mapping_<yourPodNumber>`.
    4. Set the contact expiration to 10 days.
    4. Click **Save changes**.

    !!! note
        The actual contact list file will be uploaded after the campaign is activated. For now, just associate the field mapping.

    !!! Warning
        
        The field mapping can only be changed while the campaign is in **Draft** status.


    <figure markdown>
    ![Contact list source configuration](./assets/lab1_CM_FlowCL.png)
    </figure>

**Node 3 — Daily schedule:**

???+ webex "Configure Daily Schedule"

    1. Click the **Daily schedule** node.
    2. Configure the **start date**
    3. Configure the calling window using your local timezone.
    4. A typical lab schedule runs:
        - **Start time**: `08:00`
        - **End time**: `23:00`
    5. Click **Save changes**.

    <figure markdown>
    ![Campaign daily schedule](./assets/lab1_CM_flowDS.png)
    </figure>

**Node 4 — Campaign Holidays:**

???+ webex "Configure Campaign Holidays"

    1. Click the **Campaign Holidays** node.
    2. Under **Holidays for all campaigns**, the `End of the Year (Dec 31, 2026)` date previously created  should appear automatically.
    3. Leave it checked (enabled).
    4. Click **Save changes**.

    !!! Note
        Note you can define specific campaign holidays dates that would only apply for the current campaign. We will not use it in this lab.


    <figure markdown>
    ![Schedule exclusion dates](./assets/lab1_CM_flowCH.png)
    </figure>

**Node 5 — Contact attempts strategy:**

???+ webex "Configure Contact Attempt Strategy"

    1. Click the **Contact attempts strategy** node, then click **Configure**.

        <figure markdown>
        ![Contact attempts strategy](./assets/lab1_CM_flowCAS1.png)
        </figure>

    2. Configure the following sections:

    **Section 1 — Call outcome sets:**

    | Field | Value |
    |---|---|
    | **Wrap-up code set** | `Finance` (with 1 wrap-up code) |
    | **Telephony outcome set** | `Copy_telephony_outcome` |


    **Section 2 — Contact mode priority:**

    **Safe calling window** will be `8:00 to 23:00`
    The `Phone` contact mode should be pre-populated from your field mapping. Leave priority at `1`.

    **Section 3 — Max call attempts:**

    | Timeframe | Max call attempts |
    |---|---|
    | Until the contact list expires | `40` |
    | In 1 day (from 00:01 to 23:59) | `4` |

    **Section 4 — Sequential dialling:**

    Disable sequential dialling and set the amount of contact to `10`.


    Click **Save**.

    <figure markdown style="width: 60%;">
    ![Contact attempts strategy full view - part 1](./assets/lab1_CM_flowCAS2.png)
    </figure>
    <figure markdown style="width: 60%;">
    ![Contact attempts strategy full view- part 2](./assets/lab1_CM_flowCAS3.png)
    </figure>

    Back to the campaign flow canvas, click **Save changes** in the right panel. 

**Node 6 — Suppression rule sets:**

???+ webex "Configure Suppression Rules"

    1. Click the **Suppression rule sets** node.
    2. Under **Suppression rule sets**, select `sr_hours` (which includes `sr_after_hours`).
    3. Click **Save changes**.

    <figure markdown>
    ![Suppression rule sets in campaign](./assets/lab1_CM_flowSR.png)
    </figure>

### Save and Activate the Campaign

???+ webex "Save Campaign"

    1. Click **Save & exit** (top right of the campaign flow canvas).
    2. In the **Save campaign** dialog, fill in:
        - **Campaign name**: `wxone_camp_<yourPodNumber>`
        - **P&L meta-tag**: `debt`
        - **Purpose meta-tag**: `debt`
        - **Applicable DNC lists**: `None`
    3. Click **Save**.

    <figure markdown>
    ![Save campaign dialog](./assets/lab1_CM_SaveC.png)
    </figure>



???+ webex "Activate Campaign"

    !!! Warning
        Once a campaign is active, field mappings in the Contact List Source node cannot be modified. To change them, you must create a new campaign —or duplicate the existing one— and update the field mappings before activation.

        The field mapping can be changed while the campaign is in **Draft** status.
    
    1. Back in the Campaign group list, locate **wxone_camp_<yourPodNumber>** (status: **Draft**).
    2. Click the **⋮ Actions** menu and select **Activate**.
    3. In the confirmation dialog, click **Confirm**.

    The campaign status will change to **Pending** and then **Running**.

    <figure markdown>
    ![Activate campaign](./assets/lab1_CM_Activate.png)
    </figure>

    ???+ tip 
        Campaign status is not refreshed in real time, so make sure you click on the **Refresh** button to get the updated status of the campaign.

---

## Lab 1.9 - Upload Contact List and Test

### Upload the Contact List

Now that the campaign is active, upload your contact list CSV to trigger the outbound calls.

???+ webex "Upload Contact List"

    1. In the campaign list, click the **⋮ Actions** menu on **wxone_camp_<youPodNumber>** and select **Manage contact lists**.
        
        <figure markdown>
        ![Manage contact lists panel](./assets/lab1_CM_CL1.png)
        </figure>

    2. Click **Upload file to create contact list**.

         <figure markdown>
        ![Contact list upload dialog](./assets/lab1_CM_CL2.png)
        </figure>

    3. In the **Contact list from file upload** dialog:
        - **Supported channels**: Voice (pre-selected)
        - **Contact list type**: Static
        - **Field mapping**: `field_mapping_<yourPodNumber>` (pre-selected)
        - Click **Browse** and select your `contact_list_lab31207.csv` The one you edit with your details.
        - **Automatically activate**: Immediately after upload
        - **In case of record issues**: Skip the particular record
    4. Click **Save and proceed**.


        <figure markdown style="width: 70%;">
        ![Contact list file upload form](./assets/lab1_CM_CL3.png)
        <figcaption>Contact list upload form showing field mapping, file selection, and activation settings</figcaption>
        </figure>




### Monitor Upload Status

After uploading, the contact list will show a status of **Uploading**, then it will transition to **Active** once processed. You can see the processing going through different status: *Processed, Valid, Eligible...*. Make sure you click **Refresh** to see the latest status.



<figure markdown>
![Contact list uploading status](./assets/lab1_p32_img1.png)
</figure>

<figure markdown>
![Contact list Active status](./assets/lab1_p33_img1.png)
</figure>

!!! warning
    If your contact list fails to upload, the most likely cause is a **formatting issue** with the CSV file. Check that:

    - The column headers match **exactly** what was defined in the field mapping (`firstName`, `lastName`, `phoneNumber`)
    - Phone numbers use E.164 format with the `+` prefix (e.g. `+14085052211`)
    - All phone numbers in the file are from the **same country**
    - No spaces, hyphens, or special characters appear in the phone number field
    - The file is saved as a proper comma-separated CSV (not semicolon or tab-separated)

### Verify the Campaign is Running

Once the contact list is active, the Campaign Manager will begin pushing contacts to the dialler. **Allow 2–5 minutes** for the first calls to be generated.

<figure markdown>
![Campaign running with contact list active](./assets/lab1_p33_img1.png)
<figcaption>Campaign in Running status with the contact list showing as Active and ready for dialling</figcaption>
</figure>

If everything is configured correctly, **you will receive a call** on the phone number specified in your contact list. When you answer, you will hear:

> *"Congratulations, You have completed lab 1"*

This confirms that the full end-to-end flow is working — from Campaign Manager initiating the call, through the CPA detection identifying a live voice, routing through the Go To node, and arriving at the `AI_Agent_DebtCollection` flow which plays the TTS message.

???+ Note
    Note that the **End Flow** node does not disconnect the call, so you must hang up manually after testing. We have chosen **End Flow** over **Disconnect Contact** because the call will eventually be routed to a queue in future exercises.

---

## Lab Completion ✅

At this point, you have successfully:

- [x] Configured an agent, team, and outdial queue in Webex Contact Center
- [x] Created `firstName` and `lastName` Global Variables for customer data propagation
- [x] Built the `PODXX_AI_Agent_DebtCollection` test flow with a congratulatory TTS message
- [x] Built the `Outbound_DebtCollection` campaign flow with CPA-based routing (AMD, Abandoned, Live Voice)
- [x] Configured the outdial Entry Point (Channel) and Outdial ANI
- [x] Completed all Campaign Manager prerequisites (contact modes, field mappings, suppression rules, telephony outcomes, wrap-up codes, meta-tags)
- [x] Created, configured, and activated the `wxone_camp_<yourPodName>` Progressive IVR campaign
- [x] Uploaded a contact list and received a live test call

**Congratulations!** You have completed Lab 1. The outbound campaign infrastructure is fully operational and ready to connect to the AI Agent in Lab 2.

[Next Lab: Lab 2 - Automating Debt Collection](./lab2_debt_ai_agent.md){ .md-button .md-button--primary }
