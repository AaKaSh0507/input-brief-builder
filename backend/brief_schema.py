# GPJ Input Brief Schema Definition
# Based on assessment-brief-prompt-schema.json

BRIEF_SCHEMA = {
    "templateName": "Default Template",
    "sections": [
        {
            "sectionNumber": 1,
            "sectionName": "Project Overview",
            "inputFields": [
                {
                    "fieldsHeading": "Basic Details",
                    "fields": [
                        {
                            "inputName": "Project Name",
                            "dataType": "String",
                            "fieldType": "input",
                            "prompt": "please find only the exact project name/job name for the event '{event_name}' from the provided context"
                        },
                        {
                            "inputName": "Project Type",
                            "dataType": "String",
                            "fieldType": "dropdown",
                            "options": ["3rd party", "Proprietary", "Research/Project"]
                        },
                        {
                            "inputName": "EMB",
                            "dataType": "String",
                            "fieldType": "input",
                            "prompt": "Extract only the exact EMB number (e.g., GDDQJHMB,UACBLCMB) for the event '{event_name}' from the provided context. If no EMB number is found, respond with 'Nil' only."
                        },
                        {
                            "inputName": "Event Tier",
                            "dataType": "String",
                            "fieldType": "dropdown",
                            "options": ["1", "2", "3"]
                        },
                        {
                            "inputName": "Project Number",
                            "dataType": "String",
                            "fieldType": "input",
                            "prompt": "Extract only the exact project/job number for the event '{event_name}' from the provided context. If no project/job number is found, respond with 'Nil' only."
                        },
                        {
                            "inputName": "Event Format",
                            "dataType": "String",
                            "fieldType": "dropdown",
                            "options": ["Face-to-Face", "Virtual", "Hybrid"]
                        },
                        {
                            "inputName": "Event date",
                            "dataType": "Date",
                            "fieldType": "input",
                            "prompt": "Extract only the exact Event start Date for the event '{event_name}' from the provided context. If no Event start Date is found, respond with 'Nil' only."
                        },
                        {
                            "inputName": "Venue",
                            "dataType": "String",
                            "fieldType": "input",
                            "prompt": "Extract only the exact Event venue for the event '{event_name}' from the provided context. If no Event venue is found, respond with 'Nil' only."
                        },
                        {
                            "inputName": "City",
                            "dataType": "String",
                            "fieldType": "input",
                            "prompt": "Extract only the exact City no country were the event is conducted for the event '{event_name}' from the provided context. If no City is found, respond with 'Nil' only."
                        },
                        {
                            "inputName": "Country",
                            "dataType": "String",
                            "fieldType": "input",
                            "prompt": "Extract only the exact Country name not city were the event is conducted for the event '{event_name}' from the provided context. If no Country name is found but state code is given then using state code and find the country name,if no state code are name then respond with 'Nil' only."
                        },
                        {
                            "inputName": "Producer",
                            "dataType": "String",
                            "fieldType": "input",
                            "prompt": "Extract only the exact Producer name for the event '{event_name}' from the provided context. If no Producer name is found, respond with 'Nil' only."
                        },
                        {
                            "inputName": "Forecasted Budget",
                            "dataType": "String",
                            "fieldType": "input",
                            "prompt": "Extract only the exact total Forecasted Budget for the event '{event_name}' from the provided context. If no total Forecasted Budget is found, respond with 'Nil' only."
                        },
                        {
                            "inputName": "Sponsorship Level",
                            "dataType": "String",
                            "fieldType": "dropdown",
                            "options": ["Level-1", "Level-2", "Level-3"]
                        },
                        {
                            "inputName": "Website",
                            "dataType": "String",
                            "fieldType": "input",
                            "prompt": "Extract only the exact Event Website for the event '{event_name}' from the provided context. If no Event Website is found, respond with 'Nil' only."
                        },
                        {
                            "inputName": "Booth Size",
                            "dataType": "String",
                            "fieldType": "input",
                            "prompt": "Extract only the exact Booth Size for the event '{event_name}' from the provided context. If no Booth Size is found, respond with 'Nil' only."
                        }
                    ]
                },
                {
                    "fieldsHeading": "Sponsorship Components",
                    "fields": [
                        {
                            "inputName": "Components",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["Keynote/mainstage, Meeting rooms, Surround Branding, Sessions, Workshops, VIP Events, Roundtable, Booth, Non-traditional Tactics, Digital Tactics, Advertorial, Signage, Conference Passes, Others"],
                            "prompt": "Please compile a summary less then 50 words of all exhibitor and sponsorship benefits (such as booth specifications, pass allocations, VIP lounge access, speaking opportunities, branding options, meeting spaces, networking events, and any associated fees or requirements). Organize the answer by category (e.g., Interact, Engage, Network, Brand, etc.), and clearly highlight any unique or critical details, eligibility criteria, or costs for each benefit."
                        }
                    ]
                }
            ]
        },
        {
            "sectionNumber": 2,
            "sectionName": "Project Stakeholders",
            "inputFields": [
                {
                    "fieldsHeading": "Client Information",
                    "fields": [
                        {"inputName": "Executive Sponsor", "dataType": "Object", "fieldType": "input", "objectFields": ["Name", "Email"]},
                        {"inputName": "Event SPOC", "dataType": "Object", "fieldType": "input", "objectFields": ["Name", "Email"]},
                        {"inputName": "Content Lead", "dataType": "Object", "fieldType": "input", "objectFields": ["Name", "Email"]},
                        {"inputName": "Demand Strategist", "dataType": "Object", "fieldType": "input", "objectFields": ["Name", "Email"]},
                        {"inputName": "Field Marketer", "dataType": "Object", "fieldType": "input", "objectFields": ["Name", "Email"]},
                        {"inputName": "Sales Lead", "dataType": "Object", "fieldType": "input", "objectFields": ["Name", "Email"]},
                        {"inputName": "Commas Lead", "dataType": "Object", "fieldType": "input", "objectFields": ["Name", "Email"]}
                    ]
                },
                {
                    "fieldsHeading": "GPJ Information",
                    "fields": [
                        {"inputName": "Producer", "dataType": "Object", "fieldType": "input", "objectFields": ["Name", "Email"]},
                        {"inputName": "Account Lead", "dataType": "Object", "fieldType": "input", "objectFields": ["Name", "Email"]},
                        {"inputName": "Experience Designer", "dataType": "Object", "fieldType": "input", "objectFields": ["Name", "Email"]}
                    ]
                }
            ]
        },
        {
            "sectionNumber": 3,
            "sectionName": "Objectives & Audience",
            "inputFields": [
                {
                    "fieldsHeading": "Objective",
                    "fields": [
                        {
                            "inputName": "Primary Objectives",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["What are the primary objectives of the event? Audience, Industry & Brand Perspective"],
                            "prompt": "What are the primary objectives of the event?\n\n1. From an audience perspective:\n2. From an industry perspective:\n3. From a brand perspective:"
                        }
                    ]
                },
                {
                    "fieldsHeading": "Client Journey (Full Funnel Measurement)",
                    "fields": [
                        {
                            "inputName": "Journey Stages",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["Awareness, Consideration, Perception, Action, Qualify, Progress, Loyalty, Advocacy"],
                            "prompt": "At which stage of their journey are the clients you are intending to engage with at this event? And where do you want to move them to"
                        }
                    ]
                },
                {
                    "fieldsHeading": "Outcomes & Targets",
                    "fields": [
                        {
                            "inputName": "Outcomes",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["Which pillars would be addressed in this client journey?", "What are the desired outcomes/targets? CS, CI, SQL, SQL Revenue, Win Revenue", "Progression Revenue"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Previous Year Results",
                    "fields": [
                        {
                            "inputName": "Results",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["CS, CI, SQL Revenue, Win Revenue, Progression"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Target Audience",
                    "fields": [
                        {
                            "inputName": "Audience Details",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["Who is the audience at this event?", "Why do they attend?", "Which buying groups will be targeted?", "Is NCA an objective?", "Insights on the target audience's business challenges?"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Relationship",
                    "fields": [
                        {
                            "inputName": "Relationship Status",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["What is the current relationship of the target audience listed above?", "How do you intend to drive retention/expansion?", "How do you intend to drive progression at this event?"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Industry Context & Brand Perception",
                    "fields": [
                        {
                            "inputName": "Context",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["Current awareness of IBM", "Desired shift in audience perception", "Announcements or activations planned?"]
                        }
                    ]
                }
            ]
        },
        {
            "sectionNumber": 4,
            "sectionName": "Story & Client Experience",
            "inputFields": [
                {
                    "fieldsHeading": "Client Experience",
                    "fields": [
                        {
                            "inputName": "Experience Elements",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["What would make this experience great?", "What elements are important to you?", "What are your stakeholders asking?", "What have you seen elsewhere that you would like considered?", "Do you have any challenges that you are looking to overcome in meeting these objectives?"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Key Message & Value Proposition",
                    "fields": [
                        {
                            "inputName": "Message",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["What makes IBM stand out amongst the competition?", "What is the key message to this audience?", "What is the unique selling point?", "Leading themes, Sub-themes/pillars"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Use Cases",
                    "fields": [
                        {
                            "inputName": "Use Cases List",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["List use cases to be features"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Client Stories",
                    "fields": [
                        {
                            "inputName": "Stories",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["Mention client stories that need to be featured"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Feature Products & Demos",
                    "fields": [
                        {
                            "inputName": "Products",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["What products/solutions are relevant to this audience?", "How do they solve pain points listed above?"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Integration of the Other Parts of IBM",
                    "fields": [
                        {
                            "inputName": "Integrations",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["How do we collaborate with strategic partners?", "Is there anything new about the partnership that the audience you should know?", "Is consulting a priority at this event?", "What is the relationship between consulting & technologies?"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Other Considerations",
                    "fields": [
                        {
                            "inputName": "Additional Considerations",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["If yes, what is their objective? Other considerations"]
                        }
                    ]
                }
            ]
        },
        {
            "sectionNumber": 5,
            "sectionName": "Historical Learnings",
            "inputFields": [
                {
                    "fieldsHeading": "Previous Year Results",
                    "fields": [
                        {
                            "inputName": "Satisfaction",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["To what extent were you satisfied with the results from the event last year?"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Historical Learnings (If applicable)",
                    "fields": [
                        {
                            "inputName": "Learnings",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["What outcomes need to be considered from prior years' experiences? What worked? What didn't work?"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Additional Briefings / Meeting Space",
                    "fields": [
                        {
                            "inputName": "Meeting Space",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["Description of this space", "Which IBMers are participating?", "Who are we targeting?", "Planned outcomes", "Will there be any content in this space?"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Considerations for Efficiency Gains",
                    "fields": [
                        {
                            "inputName": "Efficiency",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["Activations to be re-used", "Demos to be re-used", "Presentation/sessions to be re-used", "Architecture/Inventory elements to be re-used", "Could it make sense to start with the booth layout from 2023"]
                        }
                    ]
                }
            ]
        },
        {
            "sectionNumber": 6,
            "sectionName": "Agency Deliverables",
            "inputFields": [
                {
                    "fieldsHeading": "Event Must Haves",
                    "fields": [
                        {
                            "inputName": "Must Haves",
                            "dataType": "Array",
                            "fieldType": "textarea"
                        }
                    ]
                },
                {
                    "fieldsHeading": "Pre-designed Floor Plan",
                    "fields": [
                        {
                            "inputName": "Floor Plan",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["Which floorplan typology will be used from the Blue Studio One IBM Design Toolkit?", "Demo-focused, Activations, Meetings, Mixed"]
                        }
                    ]
                },
                {
                    "fieldsHeading": "Blue Studio Deliverables",
                    "fields": [
                        {
                            "inputName": "Deliverables",
                            "dataType": "Array",
                            "fieldType": "textarea",
                            "helperText": ["Identify the elements that the Blue Studio Team will be providing to the project. E.g. White Models, 3D Renders, Color Scheme, etc."]
                        }
                    ]
                }
            ]
        }
    ]
}
