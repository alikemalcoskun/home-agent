import React from "react";

interface News {
  id: number;
  newspaper: string;
  subject: string;
  preview: string;
  date: string;
}

const mockNews: News[] = [
  {
    id: 1,
    newspaper: "The Washington Post",
    subject: "Trump, visiting Capitol Hill, warns House Republicans against opposing his bill",
    preview: "President Donald Trump warned House Republicans against opposing his massive tax and immigration bill as he visited Capitol Hill on Monday in a bid to bolster support for the package.",
    date: "May 20, 2025",
  },
  {
    id: 2,
    newspaper: "The New York Times",
    subject: "New Orleans Jail Employee Is Arrested and Charged With Helping 10 Inmates Escape",
    preview: "A maintenance worker shut off water at the jail, allowing the inmates to remove a toilet and sink fixture from a cell wall, according to the Louisiana attorney general's office.",
    date: "May 20, 2025",
  },
  {
    id: 3,
    newspaper: "engadget",
    subject: "Everything announced at the Google I/O 2025 keynote",
    preview: "A tidal wave of AI updates (plus some other stuff).",
    date: "May 20, 2025",
  },
];

const Newspaper: React.FC = () => {
  return (
    <div className="dashboard-box news-widget">
      <h2>Newspaper</h2>
      <div className="news-container">
        <section className="news-list">
          {mockNews.map((news) => (
            <div
              key={news.id}
              className={`news-item`}
              title={news.preview}
            >
              <div className="news-newspaper">{news.newspaper}</div>
              <div className="news-details">
                <div className="news-subject">{news.subject}</div>
                <div className="news-preview">{news.preview}</div>
              </div>
              <div className="news-date">{news.date}</div>
            </div>
          ))}
        </section>
      </div>
    </div>
  );
};

export default Newspaper;
