import socket
import gradio as gr
import websocket
import yaml
import requests
import base64
import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import email
from email.mime.text import MIMEText
from vapi_python import Vapi

# Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
VAPI_PUBLIC_KEY = os.getenv('VAPI_PUBLIC_KEY', '')
VAPI_PRIVATE_KEY = os.getenv('VAPI_PRIVATE_KEY', '')
VAPI_ASSISTANT_ID = os.getenv('VAPI_ASSISTANT_ID', '')

def authenticate_gmail():
    """Authenticate and return Gmail service object"""
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "credentials.json not found. Please download it from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def get_gmail_emails(service, max_results=5, query='is:unread'):
    """Fetch emails from Gmail"""
    try:
        # Get list of messages
        results = service.users().messages().list(
            userId='me', 
            q=query,
            maxResults=max_results
        ).execute()
        messages = results.get('messages', [])
        
        emails = []
        for message in messages:
            # Get full message details
            msg = service.users().messages().get(
                userId='me', 
                id=message['id'],
                format='full'
            ).execute()
            
            # Extract headers
            headers = msg['payload'].get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            
            # Extract body
            body = extract_email_body(msg['payload'])
            
            emails.append({
                'subject': subject,
                'body': body[:500] + ('...' if len(body) > 500 else ''),  # Truncate long emails
                'sender': sender,
                'id': message['id']
            })
            
        return emails
        
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def extract_email_body(payload):
    """Extract email body from Gmail API payload"""
    body = ""
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
            elif part['mimeType'] == 'text/html' and not body:
                if 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    else:
        if payload['mimeType'] == 'text/plain':
            if 'data' in payload['body']:
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    
    # Clean up HTML tags if present
    import re
    body = re.sub(r'<[^>]+>', '', body)
    return body.strip()

# Load dummy emails from YAML (fallback)
def load_emails():
    with open("emails.yaml", "r") as f:
        return yaml.safe_load(f)

# Load emails from Gmail or fallback to YAML
def load_emails_source(use_gmail=True, max_emails=5):
    """Load emails from Gmail or fallback to YAML file"""
    if use_gmail:
        try:
            service = authenticate_gmail()
            gmail_emails = get_gmail_emails(service, max_results=max_emails)
            if gmail_emails:
                return gmail_emails, "Gmail"
            else:
                print("No emails found in Gmail, falling back to YAML")
                return load_emails(), "YAML (Fallback)"
        except Exception as e:
            print(f"Gmail authentication failed: {e}")
            print("Falling back to YAML file")
            return load_emails(), "YAML (Fallback)"
    else:
        return load_emails(), "YAML"

# Prompt the local Ollama model (e.g., llama3, phi3)
def classify_email_with_ollama(email, model="phi3"):
    prompt = f"""
Classify this email using the Eisenhower Matrix. Respond with EXACTLY one of these categories:

DO_NOW - Urgent and Important (Quadrant 1)
SCHEDULE - Important but Not Urgent (Quadrant 2)  
DELEGATE - Urgent but Not Important (Quadrant 3)
IGNORE - Not Urgent and Not Important (Quadrant 4)

Email:
Subject: "{email['subject']}"
Body: "{email['body']}"

Consider:
- Urgency: Does this need immediate attention (within hours/today)?
- Importance: Does this directly impact business goals, customer satisfaction, or critical operations?

Respond with only the category (DO_NOW, SCHEDULE, DELEGATE, or IGNORE) followed by a brief reason.

Category: """
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model, 
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Lower temperature for more consistent responses
                    "top_p": 0.9
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', '').strip()
        else:
            return "IGNORE - Error in classification"
            
    except Exception as e:
        print(f"Error classifying email: {e}")
        return "IGNORE - Error in classification"

# Parse the LLM response to extract category
def parse_classification(output):
    """Parse the LLM output to determine the category"""
    output_upper = output.upper()
    
    # Look for exact category matches first
    if "DO_NOW" in output_upper or "DO NOW" in output_upper:
        return "Do Now"
    elif "SCHEDULE" in output_upper:
        return "Schedule"  
    elif "DELEGATE" in output_upper:
        return "Delegate"
    elif "IGNORE" in output_upper:
        return "Ignore"
    
    # Fallback: look for keywords that might indicate category
    urgent_keywords = ["urgent", "asap", "immediate", "emergency", "critical"]
    important_keywords = ["important", "strategic", "goal", "revenue", "customer"]
    
    has_urgent = any(keyword in output.lower() for keyword in urgent_keywords)
    has_important = any(keyword in output.lower() for keyword in important_keywords)
    
    if has_urgent and has_important:
        return "Do Now"
    elif has_important and not has_urgent:
        return "Schedule"
    elif has_urgent and not has_important:
        return "Delegate"
    else:
        return "Ignore"

# UI logic
def classify_all_emails(use_gmail=True, max_emails=5, gmail_query="is:unread"):
    emails, source = load_emails_source(use_gmail, max_emails)
    results = {"Do Now": [], "Schedule": [], "Delegate": [], "Ignore": []}
    total_emails = len(emails)

    print(f"Loaded {total_emails} emails from {source}")
    if gmail_query and use_gmail:
        print(f"Gmail query: {gmail_query}")

    for i, email in enumerate(emails, 1):
        print(f"Classifying email {i}/{total_emails}: {email['subject']}")
        output = classify_email_with_ollama(email)
        category = parse_classification(output)
        
        # Add debugging info
        print(f"  LLM Output: {output[:100]}...")
        print(f"  Classified as: {category}")
        
        results[category].append({
            "subject": email['subject'], 
            "body": email['body'], 
            "result": output.strip(),
            "category": category,
            "sender": email.get('sender', 'Unknown')
        })
        
    return results, source


def build_gradio_interface():
    
    with gr.Blocks(title="Quadrant AI") as demo:

        gr.Markdown("# 📧 Quadrant AI")
        gr.Markdown("Classify your emails using the Quadrant AI")

        # Gmail Configuration Section
        with gr.Accordion("📬 Email Source", open=True):
            with gr.Row():
                use_gmail = gr.Checkbox(label="Gmail", value=True, scale=1)
                max_emails = gr.Slider(minimum=5, maximum=50, value=5, step=1, label="Max emails to fetch", scale=1)
                gmail_query = gr.Textbox(
                    label="Gmail Query", 
                    value="is:unread", 
                    placeholder="e.g., is:unread, from:boss@company.com, subject:urgent",
                    info="Gmail search query (leave empty for all recent emails)"
                )

        with gr.Row():
            btn = gr.Button("🔍 Classify Emails", variant="primary", interactive=True)

        # Loading indicator and source info
        with gr.Row():
            loading_status = gr.Markdown(visible=False)
        with gr.Row():
            source_info = gr.Markdown("", visible=False)

        with gr.Row(variant='panel'):
            with gr.Column(variant='panel'):
                gr.Markdown("### 🔥 Do Now (Urgent + Important)")
                do_now = gr.Markdown()
            with gr.Column(variant='panel'):
                gr.Markdown("### 📅 Schedule (Important, Not Urgent)")
                schedule = gr.Markdown()
        with gr.Row(variant='panel'):
            with gr.Column(variant='panel'):
                gr.Markdown("### 👥 Delegate (Urgent, Not Important)")
                delegate = gr.Markdown()
            with gr.Column(variant='panel'):
                gr.Markdown("### 🗑️ Ignore (Not Urgent, Not Important)")
                ignore = gr.Markdown()

        def format_gradio_block(items):
            if not items:
                return "📭 _No emails in this category._"
            lines = []
            for idx, item in enumerate(items):
                # Get classification reason
                try:
                    result_preview = item.get('result', '').split('\n')[0].split('-')[1].strip()[:80]
                except (IndexError, AttributeError):
                    result_preview = item.get('result', '')[:80]
                
                # Format sender with emoji
                sender_info = item.get('sender', '')
                if '@' in sender_info:
                    sender_emoji = "👨‍💼"  # Default business person
                    sender_lower = sender_info.lower()
                    # Try to match sender type
                    if any(term in sender_lower for term in ['team', 'support', 'help', 'service']):
                        sender_emoji = "👥"
                    elif any(term in sender_lower for term in ['noreply', 'no-reply', 'donotreply']):
                        sender_emoji = "🤖"
                    elif any(term in sender_lower for term in ['sales', 'marketing', 'offer']):
                        sender_emoji = "🛍️"
                    elif any(term in sender_lower for term in ['news', 'newsletter', 'update']):
                        sender_emoji = "📰"
                    elif any(term in sender_lower for term in ['alert', 'security', 'warning']):
                        sender_emoji = "🚨"
                else:
                    sender_emoji = "📧"
                
                if sender_info and len(sender_info) > 30:
                    sender_info = sender_info[:30] + "..."
                
                # Format body text, escape any markdown characters and limit length
                body_preview = item["body"][:150]
                if len(item["body"]) > 150:
                    body_preview += "..."
                # Escape any characters that could be interpreted as markdown
                body_preview = body_preview.replace("*", "\\*").replace("_", "\\_").replace("#", "\\#")
                # Replace newlines with spaces to prevent markdown formatting issues
                body_preview = body_preview.replace("\n", " ")
                
                # Format subject
                subject = item.get('subject', 'No Subject')
                if len(subject) > 50:
                    subject += "..."

                # Build the formatted card with consistent formatting
                email_card = (
                    f"### {idx+1}. {subject}\n\n"
                    f"{sender_emoji} **From:** {sender_info}\n\n"
                    f"📝 **Preview:**  \n`{body_preview}`\n\n"
                    f"💡 **Reason:** _{result_preview}_"
                )
                lines.append(email_card)
            
            return '\n\n---\n\n'.join(lines)
        
        def toggle_interactive(interactive):
            return gr.Button(
                value="🔍 Classify Emails", 
                variant="primary", 
                interactive=interactive
            )

        def update_results(use_gmail, max_emails, gmail_query):
            result, source = classify_all_emails(use_gmail, max_emails, gmail_query if gmail_query.strip() else "")
            source_text = f"📊 **Source:** {source} | **Total emails:** {sum(len(v) for v in result.values())}"

            vapi = Vapi(api_key=VAPI_PUBLIC_KEY)
            call_id, web_call_url = vapi.start(assistant_id=VAPI_ASSISTANT_ID)
            print(f"Joining call... {call_id}")

            data = requests.get(f"{vapi.api_url}/call/{call_id}", headers={
                'Authorization': f'Bearer {VAPI_PRIVATE_KEY}'
            })

            control_url = data.json().get("monitor", {}).get("controlUrl")

            if len(result["Do Now"]) > 0:
                print("Sending Do Now message to VAPI...")
                top_email = result["Do Now"][0]
                email_subject = top_email['subject']
                email_body = top_email['body']
                email_sender = top_email.get('sender', 'Unknown Sender')
                
                requests.post(
                    control_url,
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {VAPI_PRIVATE_KEY}'
                    },
                    json={
                        "type": "add-message",
                        "message": {
                            "role": "user",
                            "content": f"Please summarize the following email. Read out the summary Sender: {email_sender}, Subject: {email_subject}, Body: {email_body}."
                        },
                        "triggerResponseEnabled": True
                    }
                )


            return (
                format_gradio_block(result["Do Now"]),
                format_gradio_block(result["Schedule"]),
                format_gradio_block(result["Delegate"]),
                format_gradio_block(result["Ignore"]),
                gr.Markdown("", visible=False),
                gr.Markdown(source_text, visible=True),
                gr.Button("🔍 Classify Emails", variant="primary", interactive=True)
            )

        btn.click(fn=lambda: toggle_interactive(False),
            inputs=None,
            outputs=btn
        ).then(
            update_results, 
            show_progress=True,
            inputs=[use_gmail, max_emails, gmail_query],
            outputs=[
                do_now,
                schedule,
                delegate,
                ignore,
                loading_status, source_info, btn
            ]
        ).then(fn=lambda: toggle_interactive(True),
            inputs=None,
            outputs=btn
        )

    return demo

if __name__ == "__main__":
    demo = build_gradio_interface()
    demo.launch(debug=True, show_error=True)
