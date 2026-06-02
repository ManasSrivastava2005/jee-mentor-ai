import { useEffect, useState } from 'react';
import { getHistory } from '../services/api.js';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    getHistory().then(setHistory).catch(() => setHistory([]));
  }, []);

  return (
    <section className="workspace">
      <div className="toolbar">
        <div>
          <h2>Question History</h2>
          <p>Every solved question is stored for performance tracking.</p>
        </div>
      </div>
      <div className="tablePanel">
        <table>
          <thead>
            <tr>
              <th>Question</th>
              <th>Subject</th>
              <th>Topic</th>
              <th>Confidence</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item) => (
              <tr key={item.id}>
                <td>{item.prompt}</td>
                <td>{item.subject}</td>
                <td>{item.topic}</td>
                <td>{Math.round(item.confidence_score * 100)}%</td>
                <td>{new Date(item.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
