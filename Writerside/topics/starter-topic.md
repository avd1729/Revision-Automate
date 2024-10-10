# About Revise Automate

<!--Writerside adds this topic when you create a new documentation project.
You can use it as a sandbox to play with Writerside features, and remove it from the TOC when you don't need it anymore.-->

## Introduction
Revise Automate is an application designed to streamline my daily DSA revision process. It fetches data from Notion, processes the list of questions, and automatically sends me an email with the specific questions I need to revise each day, also creating events in Google calendar ensuring consistency and discipline in my study routine.

![Add a heading.png](..%2Fimages%2FAdd%20a%20heading.png)

## Features
<procedure title="" id="feature">
    <step>
        <p><b>Notion Integration: </b> Fetches DSA questions directly from Notion.</p>
    </step>
    <step>
        <p><b>Daily Email Notifications: </b> Sends a summary email with the questions to be revised for the day.</p>
    </step>
    <step>
        <p><b>Google Calendar Events: </b> Automatically adds revision tasks to Google Calendar for better time management.</p>
    </step>
</procedure>

## How it Works
The application consists of several components:
<procedure>
    <step>
    <b>Config:</b> Stores configuration details like API keys and email credentials.
    </step>
    <step>
    <b>NotionClient:</b> Fetches all pages from Notion using the provided API key.
    </step>
    <step>
    <b>DataProcessor:</b> Processes the Notion data and filters it by the specific date.
    </step>
    <step>
    <b>EmailService:</b> Sends an email containing the questions to revise.
    </step>
    <step>
    <b>CalendarService:</b> Adds the selected questions as events in Google Calendar.
    </step>
    <step>
    <b>AuthManager:</b> Manages authentication for Google services.
    </step>
    <step>
    <b>LoggerManager:</b> Manages logging throughout the application.
    </step>
</procedure>

## Procedure

<procedure title="">
    <step>
        <p>Create an integration in Notion and retrieve your token.</p>
    </step>
    <step>
        <p>Preprocess the data to filter out the required data.</p>
    </step>
    <step>
        <p>Set up a Google OAuth flow for your email-id.</p>
    </step>
    <step>
        <p>Set up a Google Calendar API project and obtain your credentials.</p>
    </step>
    <step>
        <p>Automate the script to run daily.</p>
    </step>
</procedure>

