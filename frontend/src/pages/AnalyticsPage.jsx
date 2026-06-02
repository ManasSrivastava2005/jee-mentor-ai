import { useEffect, useState } from 'react';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { getAnalytics } from '../services/api.js';

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState({
    most_attempted_topics: [],
    weak_topics: [],
    recommended_revision_areas: [],
  });

  useEffect(() => {
    getAnalytics().then(setAnalytics).catch(() => {});
  }, []);

  return (
    <section className="workspace">
      <div className="toolbar">
        <div>
          <h2>Analytics Dashboard</h2>
          <p>Topic performance, weak areas, and revision recommendations.</p>
        </div>
      </div>

      <div className="chartBand">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={analytics.most_attempted_topics}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="topic" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="attempts" fill="#2d6cdf" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="metricGrid">
        {analytics.weak_topics.map((topic) => (
          <article className="metricCard" key={`${topic.subject}-${topic.topic}`}>
            <span>{topic.subject}</span>
            <h3>{topic.topic}</h3>
            <p>Accuracy {Math.round(topic.accuracy * 100)}%</p>
            <p>{topic.attempts} attempts</p>
          </article>
        ))}
      </div>

      <div className="panel">
        <h3>Recommended Revision Areas</h3>
        {analytics.recommended_revision_areas.map((item) => (
          <p key={item}>{item}</p>
        ))}
      </div>
    </section>
  );
}
