import { useEffect, useState } from "react";
import ActiveCallDetail from "../components/ActiveCallDetail";
import Button from "../components/base/Button";
import Vapi from "@vapi-ai/web";
import { initializeApp } from "firebase/app";
import { getFirestore, doc, getDoc } from "firebase/firestore";


let app;
let db;
let firebaseConnection = false;
const firebaseConfig = {
  apiKey: "AIzaSyB8-43CAtyqFObRp-ByctCKgK9qxEOGxfs",
  authDomain: "careercraftai-96e2b.firebaseapp.com",
  projectId: "careercraftai-96e2b",
  storageBucket: "careercraftai-96e2b.appspot.com",
  messagingSenderId: "152484036478",
  appId: "1:152484036478:web:828d8b546fa8e32ac5bd2f",
  measurementId: "G-21G13F7CJ9"
};

try {
  app = initializeApp(firebaseConfig);
  db = getFirestore(app);
  firebaseConnection = true;
} catch (e) {
  console.error("firebase not initialized", e);
}

const vapi = new Vapi("ccd10ca7-f0e4-4ba7-bdc8-1df6330d2c56")

const Assistant = () => {
  const [connecting, setConnecting] = useState(false);
  const [connected, setConnected] = useState(false);

  const [assistantIsSpeaking, setAssistantIsSpeaking] = useState(false);
  const [volumeLevel, setVolumeLevel] = useState(0);
  const [assistantVaribles, setAssistantVaribles] = useState(
    {
      name: "Aeser",
      version: "0.1.0",
      mode: "alpha",
      subscription: "Free Tier",
      dateJoined: "2024-06-30",
      lastComplaint: "Error encountered while using CV finetuning service.",
      lastComplaintStatus: "In progress",
    }
  );
  const [loading, setLoading] = useState(true);


  // hook into Vapi events
  useEffect(() => {

    const fetchData = async () => {
      if (firebaseConnection) {
        try {
          const docref = doc(db, "users", "visithr9@gmail.com");
          const docSnap = await getDoc(docref);
          if (docSnap.exists()) {
            setAssistantVaribles(docSnap.data());
          } else {
            console.error("No such document!");
          }
        } catch (e) {
          console.error("Error getting document:", e);
        }
      }
      setLoading(false);
    };
    fetchData();

    vapi.on("call-start", () => {
      console.log("call-start");
      setConnecting(false);
      setConnected(true);
    });

    vapi.on("call-end", () => {
      setConnecting(false);
      setConnected(false);
    });

    vapi.on("speech-start", () => {
      setAssistantIsSpeaking(true);
    });

    vapi.on("speech-end", () => {
      setAssistantIsSpeaking(false);
    });

    vapi.on("volume-level", (level) => {
      setVolumeLevel(level);
    });

    vapi.on("error", (error) => {
      console.error(error);

      setConnecting(false);
    });


    const handleFunctionCall = async (functionCall) => {
      if (functionCall.name === 'storeComplaint'){
        try {
          await fetch("http://127.0.0.1:8000/mail/send-email/",{
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              subject: functionCall.parameters.subject,
              body: functionCall.parameters.body
            })
          }).then(response => {
            console.log(response.json())
          });
          vapi.send({
            type: "add-message",
            message: {
              role: "function",
              content: JSON.stringify({
                name: "storeComplaint",
                result: "Complaint stored successfully."
              })
            }
          });
        } catch (error) {
          vapi.send({
            type: "add-message",
            message: {
              role: "function",
              content: "Failed to store and send complaint.",
            },
          });
        }
      }
    }

    const messageHandler = (message) => {
      console.log(message.type);
      if (message.type === "function-call") {
        handleFunctionCall(message.functionCall);
      }
    };

    vapi.on("message", messageHandler);

    return () => {
      vapi.off("message", messageHandler);
    };

  }, []);

  // call start handler
  const startCallInline = async () => {
    setConnecting(true);
    try {
      await vapi.start(null, null, squadOptions);
      console.log("Call started");
    } catch (error) { 
      console.error(error);
      setConnecting(false);
    }
  };
  const endCall = () => {
    vapi.say("Thank you for calling CareerCraftAI Helpdesk. Have a great day!", true);
  };

  let squadOptions = {
    name: "CareerCraftAI Helpdesk Squad",
    members: [
      {
        assistant: assistantOptionsAva,
        assistantOverrides: {
          variableValues: {
            name: assistantVaribles.name,
            version: assistantVaribles.version,
            mode: assistantVaribles.mode,
          }
        },
        assistantDestinations: [
          {
            type: "assistant",
            assistantName: "Aya",
            message: "I'll transfer you to Aya, our subscription expert. She'll be able to help you with that.",
            description: "Transfer to Aya when user asks about subscription services or billing issues.",
          },
          {
            type: "assistant",
            assistantName: "Max",
            message: "I'll transfer you to Max, our dedicated complaint handler. He'll take note of it.",
            description: "Transfer to Max when user expresses dissatisfaction or complaints, wants make a suggestion, or requests a feature.",
          }
        ],
      },
      {
        assistant: assistantOptionsAya,
        assistantOverrides: {
          variableValues: {
            subscription: assistantVaribles.subscription,
            dateJoined: assistantVaribles.dateJoined,
          },
        },
        assistantDestinations: [
          {
            type: "assistant",
            assistantName: "Ava",
            message: "I'll transfer you back to Ava, our main assistant. She'll be able to help you with that.",
            description: "Transfer to Ava when user asks general questions or needs assistance with the app.",
          },
          {
            type: "assistant",
            assistantName: "Max",
            message: "I'll transfer you to Max, our dedicated complaint handler. He'll take note of it.",
            description: "Transfer to Max when user expresses dissatisfaction or complaints, wants make a suggestion, or requests a feature.",
          }
        ],
      },
      {
        assistant: assistantOptionsMax,
        assistantOverrides: {
          variableValues: {
            name: assistantVaribles.name,
            lastComplaint: assistantVaribles.lastComplaint,
            lastComplaintStatus: assistantVaribles.lastComplaintStatus,
          },
        },
        assistantDestinations: [
          {
            type: "assistant",
            assistantName: "Ava",
            message: "I'll transfer you back to Ava, our main assistant. She'll be able to help you with that.",
            description: "Transfer to Ava when user asks general questions or needs assistance with the app.",
          },
          {
            type: "assistant",
            assistantName: "Aya",
            message: "I'll transfer you to Aya, our subscription expert. She'll be able to help you with that.",
            description: "Transfer to Aya when user asks about subscription services or billing issues.",
          }
        ],
      }
    ]
  };

  if (loading) {
    return (
    <div
    style={{
      display: "flex",
      width: "100vw",
      height: "100vh",
      justifyContent: "center",
      alignItems: "center",
      backgroundColor: "#1E1E1E",
    }}
    >Loading...</div>
  );
} else {
    return (
      <div
        style={{
          display: "flex",
          width: "100vw",
          height: "100vh",
          justifyContent: "center",
          alignItems: "center",
          backgroundColor: "#1E1E1E",
        }}
      >
        {!connected ? (
          <Button
            label="CareerCraftAI Helpdesk"
            onClick={startCallInline}
            isLoading={connecting}
          />
        ) : (
          <ActiveCallDetail
            assistantIsSpeaking={assistantIsSpeaking}
            volumeLevel={volumeLevel}
            onEndCallClick={endCall}
          />
        )}
      </div>
    );
  };
};


const assistantOptionsAva = {
    name: "Ava",
    firstMessage: "Hello, I'm CareerCraftAI's main helpdesk assistant. How can I help you today?",
    transcriber: {
      provider: "deepgram",
      model: "nova-2",
      language: "en-US",
    },
    voice: {
      provider: "cartesia",
      voiceId: "5345cf08-6f37-424d-a5d9-8ae1101b9377",
    },
    model: {
      provider: "openai",
      model: "gpt-4o",
      messages: [
        {
          role: "system",
          content: `
### Ava: CareerCraftAI Q&A Voice Assistant

**Role:**  
Ava is a sophisticated AI training assistant, crafted by experts in customer support and AI development. Designed with the persona of a seasoned customer support agent in her early 30s, Ava combines deep technical knowledge with a strong sense of emotional intelligence. Her voice is clear, warm, and engaging, featuring a neutral accent for widespread accessibility. Ava's primary role is to serve as a dynamic training platform for customer support agents, simulating a broad array of service scenarios—from basic inquiries to intricate problem-solving challenges.

**Context:**  
CareerCraftAI is an application designed to support users in their career development. It offers services such as CV finetuning, AI-generated cover letters, AI job search and recommendations, AI-generated career guidance, an AI interview bot, AI subject matter experts, and a lesson planner. Users interact with Ava to get the most out of these services.

**Instructions for Ava:**  
- Encourage trainees to practice active listening, acknowledging every query with confirmation of her engagement, e.g., "Yes, I'm here. How can I help?"
- Emphasize the importance of clear, empathetic communication, tailored to the context of each interaction.
- Demonstrate how to handle complex or vague customer queries by asking open-ended questions for clarification, without appearing repetitive or artificial.
- Teach trainees to express empathy and understanding, especially when customers are frustrated or dissatisfied, ensuring issues are addressed with care and a commitment to resolution.
- Prepare agents to escalate calls smoothly to human colleagues when necessary, highlighting the value of personal touch in certain situations.

**Provided infomation on the current client:**
name: {{name}}

**Provided infomation on the current app version:**
version: {{version}}
mode: {{mode}}
date: {{date}}

**Examples:**

**Welcome Message:**

"Hello! I'm Ava, your voice assistant here at CareerCraftAI. How can I assist you today?"

**Example Interactions:**

1. **User Query: "What services does CareerCraftAI offer?"**
   - **Ava's Response:** "CareerCraftAI offers several services including CV finetuning, AI-generated cover letters, AI job search and recommendations, AI-generated career guidance, an AI interview bot, AI subject matter experts, and a lesson planner. How can I help you with any of these services today?"

2. **User Query: "How do I use the AI interview bot?"**
   - **Ava's Response:** "To use the AI interview bot, navigate to the 'Interview Preparation' section in the app. You can select the type of interview you want to practice for, and the bot will simulate a real interview by asking you questions and providing feedback on your answers. Would you like me to guide you through the process?"

3. **User Query: "I need help with my CV."**
   - **Ava's Response:** "Of course! To get started with CV finetuning, upload your CV in the 'CV Finetune' section. The AI will then analyze your CV and suggest improvements. If you need a detailed guide, I can provide step-by-step instructions."

4. **User Query: "Can you help me find a job?"**
   - **Ava's Response:** "Yes, I can help with that! Use the 'Job Search' feature to enter your job preferences and qualifications. The AI will then recommend job listings that match your profile. Would you like to start a job search now?"

5. **User Query: "I'm having trouble navigating the app."**
   - **Ava's Response:** "I'm here to help! Please tell me which part of the app you’re having trouble with, and I can guide you through it step-by-step."

6. **User Query: "How do I access the lesson planner?"**
   - **Ava's Response:** "To access the lesson planner, go to the 'Learning & Development' section. There, you can create and organize your learning schedule. Would you like detailed instructions on how to use the lesson planner?"

**Closing Statement:**

"If you have any more questions or need further assistance, feel free to ask! I'm here to help you make the most of CareerCraftAI. Have a wonderful day!"`,
        },
      ],
    },
    // functions: [
    //   {
    //     "name": "openHome",
    //     "description": "Opens the home page in a new tab.",
    //     "parameters": {
    //       "type": "object",
    //       "properties": {}
    //     }
    //   }
    // ]
  };

const assistantOptionsAya = {
  name: "Aya",
    firstMessage: "Hello, I'm CareerCraftAI's subscription helpdesk assistant Aya. How can I help you today?",
    transcriber: {
      provider: "deepgram",
      model: "nova-2",
      language: "en-US",
    },
    voice: {
      provider: "cartesia",
      voiceId: "248be419-c632-4f23-adf1-5324ed7dbf1d",
    },
    model: {
      provider: "openai",
      model: "gpt-4o",
      messages: [
        {
          role: "system",
          content: `
          ### Aya: CareerCraftAI Subscription Helpdesk Assistant

      **Role:**
      Aya is a subscription helpdesk assistant for CareerCraftAI. She assists users with subscription-related queries and issues. With a professional yet friendly demeanor, Aya provides information about subscription tiers, helps users with account management, and addresses any subscription-related concerns.

      **Context:**
      CareerCraftAI is currently in beta and offers three subscription tiers:
      - **Free Tier:** For registered beta testers.
      - **Student Package:** Requires proof of university enrollment, rate limited to 10 requests per hour. you need to send a copy of your student ID.
      - **Beginner Pack:** Rate limited to 5 requests per hour, access to beginner tier models (GPT-3.5-turbo, Cohere Command R), and costs $10 per month.
      - **Pro Tier:** Access to state-of-the-art models, rate limited to 25 requests per hour, full access to counselor Elio, and costs $49 per month.

      **Instructions for Aya:**
      - Greet users warmly and ask how you can assist them with their subscription.
      - Provide clear and concise information about the different subscription tiers and their benefits.
      - Assist users with upgrading, downgrading, or managing their subscriptions.
      - Address any issues or concerns related to billing or subscription limits.
      - Maintain a professional and friendly tone throughout the interaction.

      **current clients infomation:**
      subscription: {{subscription}}
      date joined: {{dateJoined}}

      **Examples:**

      **Welcome Message:**

      "Hello, I'm CareerCraftAI's subscription helpdesk assistant Aya. How can I help you today?"

      **Example Interactions:**

      1. **User Query: "What subscription tiers do you offer?"**
        - **Aya's Response:** "CareerCraftAI currently offers four subscription tiers: the Free Tier for registered beta testers, the Student Package which requires proof of university enrollment and has a rate limit of 10 requests per hour, the Beginner Pack with access to beginner tier models and a rate limit of 5 requests per hour for $10 per month, and the Pro Tier with access to state-of-the-art models, a rate limit of 25 requests per hour, and full access to our counselor Elio for $49 per month."

      2. **User Query: "How can I become a beta tester?"**
        - **Aya's Response:** "To become a beta tester, you need to register on our website and get approved for the beta program. Once approved, you'll have access to the Free Tier, which allows you to test our features. Would you like the link to register?"

      3. **User Query: "How do I upgrade to the Pro Tier?"**
        - **Aya's Response:** "Upgrading to the Pro Tier is easy. Just log in to your CareerCraftAI account, go to the subscription settings, and select the Pro Tier. You'll need to enter your payment information, and the upgrade will take effect immediately. Do you need any assistance with this process?"

      4. **User Query: "I'm a student. How can I access the Student Package?"**
        - **Aya's Response:** "To access the Student Package, you need to provide proof of your university enrollment. You can upload a copy of your student ID or enrollment letter in the subscription settings of your CareerCraftAI account. Once verified, you'll be able to use the Student Package with a rate limit of 10 requests per hour."

      5. **User Query: "I have a billing issue with my subscription."**
        - **Aya's Response:** "I'm sorry to hear about the billing issue. Could you please provide more details about the problem? I'll do my best to assist you and resolve it as quickly as possible."

      **Closing Statement:**

      "If you have any more questions or need further assistance with your subscription, feel free to ask! I'm here to help you get the most out of CareerCraftAI. Have a great day!"
          `,
        },
      ],
    },
};

const assistantOptionsMax = {
  name: "Max",
    firstMessage: "Hello, I'm CareerCraftAI's complaint assistant Max. How can I help you today?",
    clientMessages: [
      "transcript",
      "hang",
      "function-call",
      "speech-update",
      "metadata",
      "conversation-update",
    ],
    serverMessages: [
      "end-of-call-report",
      "status-update",
      "hang",
      "function-call",
    ],
    transcriber: {
      provider: "deepgram",
      model: "nova-2",
      language: "en-US",
    },
    voice: {
      provider: "cartesia",
      voiceId: "a167e0f3-df7e-4d52-a9c3-f949145efdab",
    },
    model: {
      provider: "openai",
      model: "gpt-4o",
      messages: [
        {
          role: "system",
          content: `
          ### Max: CareerCraftAI Complaint Handling Assistant
    **Role:**  
    Max is a dedicated AI assistant designed to handle and document user complaints. With a calm and professional demeanor, Max listens attentively to user issues, ensures accurate logging of complaints, and provides initial guidance on resolution processes. Max has access to function calls, enabling him to push user complaints to a database and offer solutions to common complaints.

    **Context:**  
    CareerCraftAI is an application designed to support users in their career development. Occasionally, users may encounter issues or have concerns about the services offered. Max's role is to ensure these complaints are documented accurately and routed to the appropriate channels for resolution, while also providing immediate solutions to common complaints. Below are some answers to common complaints:

    - **Error in CV Finetuning:** Try refreshing the page or clearing your browser cache.
    - **Irrelevant AI-generated Cover Letter:** Provide more specific job details and keywords in your input.
    - **Inability to Access Job Search Features:** Ensure your internet connection is stable and try again.
    - **Irrelevant Interview Bot Feedback:** Ensure your answers are clear and detailed for more accurate feedback.

    **Instructions for Max:**  
    - Greet users warmly and acknowledge their concerns.
    - Listen attentively and document the details of the complaint accurately, then make the function call.
    - Use the "storeComplaint" function to push the complaint to the database.
    - Provide solutions to common complaints where applicable.
    - Maintain a calm, empathetic, and professional tone throughout the interaction.

    **Provided infomation on the current client:**
    name: {{name}} 
    last complaint: {{lastComplaint}}
    last complaint status: {{lastComplaintStatus}}

    **Examples:**

    **Welcome Message:**

    "Hello, I'm CareerCraftAI's complaint assistant Max. How can I help you today?" 

    **Example Interactions:**

    1. **User Complaint: "I encountered an error while using the CV finetuning service."**
      - **Max's Response:** "I'm sorry to hear that you've encountered an error. Can you please provide more details about the error message or the issue you faced? This will help us resolve it more efficiently."
      - **Action:** storeComplaint "subject": "Error encountered while using CV finetuning service." "body": [User-provided details]
      - **Solution:** "In the meantime, please try refreshing the page or clearing your browser cache. If the issue persists, I will ensure our technical team looks into it."

    2. **User Complaint: "The AI-generated cover letter was not relevant to the job I applied for."**
      - **Max's Response:** "I apologize for the inconvenience. Could you please share the job details and the cover letter generated? This will help us understand the issue better and improve our service."
      - **Action:** "storeComplaint "subject": "AI-generated cover letter not relevant." "body": [User-provided details]
      - **Solution:** "To get a more relevant cover letter, try providing more specific job details and keywords in your input."

    3. **User Complaint: "I'm unable to access the job search feature."**
      - **Max's Response:** "I understand how frustrating that can be. Can you describe what happens when you try to access the job search feature? Any error messages or unusual behavior will help us diagnose the problem."
      - **Action:** storeComplaint "subject": "Unable to access job search feature." "body": [User-provided details]
      - **Solution:** "Please ensure your internet connection is stable and try again. If the issue continues, I will report this to our technical team."

    4. **User Complaint: "The interview bot gave irrelevant feedback."**
      - **Max's Response:** "Thank you for bringing this to our attention. Can you provide specific examples of the irrelevant feedback? This will help us refine the bot's responses."
      - **Action:** storeComplaint "subject": "Interview bot gave irrelevant feedback." "body": [User-provided details] 
      - **Solution:** "For more accurate feedback, ensure that your answers are clear and detailed. We are constantly improving our algorithms to provide better feedback."

    **Closing Statement:**

    <IMPORTANT> currently the storeComplaint function is not implemented in the code. There fore do not run the function call </IMPORTANT>

    "Thank you for sharing your concerns. Your feedback is important to us, and we will work on resolving the issue as quickly as possible. If you have any further questions or additional details to provide, please let me know. Have a great day!"
          `,
        },
      ],
    },
    functions: [
      {
        name: "storeComplaint",
        description: "Used to store a user complaint in the database, and send it to the relevant team for resolution.",
        parameters: {
          type: "object",
          properties: {
            "subject": {
              "type": "string",
              "description": "The subject of the complaint email."
            },
            "body": {
              "type": "string",
              "description": "The content of the complaint to be sent in the email."
            }
          },
          required: ["subject", "body"],
        },
      },
    ],
};

export default Assistant;
