import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score
import pickle

# Large dataset for maximum accuracy
spam_texts = [
    "Buy now and get free stuff", "Limited time offer only today", "Cheap meds available now", "Win a free iPhone",
    "Act fast! Limited offer", "Congratulations! You've won", "Click here to claim your prize", "Free vacation package",
    "Subscribe now", "Final reminder for payment", "Earn money easily", "Don't miss this deal", "Lowest prices guaranteed",
    "URGENT: Your account will be closed", "You have won $1000000", "Free money waiting for you", "Claim your reward now",
    "Hot singles in your area", "Lose weight fast with this pill", "Make money from home", "Casino bonus available",
    "Credit card debt relief", "Work from home opportunity", "Nigerian prince needs your help", "Miracle cure discovered",
    "Get rich quick scheme", "No credit check required", "Congratulations winner", "Free gift with purchase",
    "Amazing deal expires today", "50% off everything", "Call now operators waiting", "As seen on TV",
    "Guaranteed weight loss", "Investment opportunity", "Cash advance available", "Refinance your home",
    "Viagra discount", "Free trial offer", "Pre-approved loan", "Debt consolidation", "Instant cash now",
    "Make $5000 weekly", "Risk-free investment", "100% satisfaction guaranteed", "Order now limited supply",
    "Winner selected congratulations", "Claim cash prize today", "Exclusive VIP offer", "Double your income",
    "Free iPhone waiting", "Click to claim prize", "Urgent action required", "Last chance offer",
    "Act now or lose forever", "Guaranteed approval", "No strings attached", "Free membership",
    "Million dollar opportunity", "Secret to wealth", "Lose 30 pounds fast", "Miracle weight loss",
    "Get paid to work from home", "Earn while you sleep", "Financial freedom now", "Investment returns guaranteed",
    "Free credit report", "Consolidate your debt", "Lower your payments", "Eliminate debt forever",
    "Free government money", "Unclaimed inheritance", "Tax refund available", "Lottery winner notification",
    "Casino jackpot winner", "Sweepstakes winner", "Contest winner selected", "Prize claim notification",
    "Urgent payment required", "Account verification needed", "Suspend account warning", "Security alert message",
    "Phishing attempt detected", "Verify identity now", "Update payment method", "Expired card notification",
    "Free pills online", "Discount pharmacy", "Cheap medication", "No prescription needed",
    "Adult content warning", "Meet singles tonight", "Dating site invitation", "Romantic encounter",
    "Work from home scam", "Pyramid scheme invitation", "Multi-level marketing", "Business opportunity",
    "Fake degree offer", "Diploma mill advertisement", "Certificate for sale", "Instant qualification"
]

non_spam_texts = [
    "Meeting at 5pm", "This is not spam", "Let's catch up tomorrow", "Let's schedule a meeting",
    "See you at dinner", "I will call you later", "Got the documents, thanks", "Reminder: team sync at 9am",
    "Lunch at 12?", "Join our webinar", "Re: your application", "Looking forward to your reply",
    "Your invoice is attached", "How was your weekend?", "Thanks for the update", "Can you send the report?",
    "Project deadline is Friday", "Conference call at 2pm", "Happy birthday!", "Good morning team",
    "Please review the document", "Meeting minutes attached", "Travel arrangements confirmed", "Budget approved",
    "System maintenance tonight", "New policy update", "Training session tomorrow", "Quarterly results published",
    "Office closed on Monday", "Welcome to the team", "Vacation request approved", "Performance review scheduled",
    "Client meeting moved to 3pm", "Server backup completed", "New employee orientation", "Holiday schedule updated",
    "Expense report due", "Conference registration open", "Team building event", "Software update available",
    "Monthly newsletter", "Annual report ready", "Please confirm your attendance", "Thanks for your help",
    "Document shared with you", "Deadline extended to next week", "Meeting room booked", "Flight tickets confirmed",
    "Hotel reservation complete", "Task completed successfully", "Project status update", "Weekly team meeting",
    "Department budget review", "Employee handbook update", "Training materials attached", "Conference agenda",
    "Quarterly planning session", "Annual performance review", "Benefits enrollment open", "Health insurance update",
    "Parking permit renewal", "Office supplies order", "IT support ticket", "Software license renewal",
    "Security badge update", "Emergency contact form", "Time sheet reminder", "Payroll processing notice",
    "Company policy change", "Employee survey invitation", "Lunch and learn session", "Professional development",
    "Client presentation scheduled", "Sales report attached", "Marketing campaign update", "Product launch meeting",
    "Customer feedback summary", "Quality assurance report", "Compliance training required", "Audit preparation meeting",
    "Board meeting minutes", "Shareholder update", "Financial statement review", "Tax preparation documents",
    "Legal contract review", "Insurance policy update", "Vendor payment processed", "Purchase order approved"
]

# Create balanced dataset
data = pd.DataFrame({
    "text": spam_texts + non_spam_texts,
    "label": [1] * len(spam_texts) + [0] * len(non_spam_texts)
})

X_train, X_test, y_train, y_test = train_test_split(
    data["text"], data["label"], 
    test_size=0.2, random_state=42, stratify=data["label"]
)

# Optimized pipeline for maximum accuracy
model = Pipeline([
    ("vectorizer", TfidfVectorizer(max_features=2000, ngram_range=(1, 2), stop_words='english')),
    ("classifier", LogisticRegression(C=10, max_iter=1000, random_state=42))
])

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

with open("spam_model.pkl", "wb") as f:
    pickle.dump(model, f)