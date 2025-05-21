import React from "react";

interface Emails {
  id: number;
  sender: string;
  subject: string;
  preview: string;
  date: string;
  read: boolean;
}

const mockEmails: Emails[] = [
  {
    id: 1,
    sender: "Google Haritalar",
    subject: "Yorumlarınız Google Haritalar'da çok popüler.",
    preview: "Yarattığınız etkiyi kutlayalım.",
    date: "May 20",
    read: false,
  },
  {
    id: 2,
    sender: "LinkedIn",
    subject: "New jobs similar to Software Engineer at LinkedIn",
    preview: "Jobs similar to Software Engineer at LinkedIn",
    date: "May 19",
    read: true,
  },
  {
    id: 3,
    sender: "The Postman Team",
    subject: "New sign-in notification",
    preview: "Review new sign-in activity We recently detected a new sign-in for your Postman account. If this was you, no further action is needed.",
    date: "May 15",
    read: true,
  },
];

const Email: React.FC = () => {
  return (
    <div className="dashboard-box email-widget">
      <h2>Email</h2>
      <div className="email-container">
        
        <section className="email-list">
          {mockEmails.map((email) => (
            <div
              key={email.id}
              className={`email-item ${email.read ? "read" : "unread"}`}
            >
              <div className="email-sender">{email.sender}</div>
              <div className="email-details">
                <div className="email-subject">{email.subject}</div>
                <div className="email-preview">{email.preview}</div>
              </div>
              <div className="email-date">{email.date}</div>
            </div>
          ))}
        </section>
      </div>
    </div>
  );
};

export default Email;
