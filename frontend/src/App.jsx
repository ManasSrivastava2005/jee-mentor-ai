import { useState } from 'react';
import { BarChart3, BookOpen, History, MessageSquare } from 'lucide-react';
import ChatPage from './pages/ChatPage.jsx';
import HistoryPage from './pages/HistoryPage.jsx';
import AnalyticsPage from './pages/AnalyticsPage.jsx';

const tabs = [
  { id: 'chat', label: 'Mentor', icon: MessageSquare },
  { id: 'history', label: 'History', icon: History },
  { id: 'analytics', label: 'Analytics', icon: BarChart3 },
];

export default function App() {
  const [activeTab, setActiveTab] = useState('chat');

  return (
    <div className="appShell">
      <aside className="sidebar">
        <div className="brand">
          <BookOpen size={28} />
          <div>
            <h1>JEE Mentor AI</h1>
            <span>Reasoning Agent</span>
          </div>
        </div>
        <nav>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                className={activeTab === tab.id ? 'navButton active' : 'navButton'}
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                title={tab.label}
              >
                <Icon size={18} />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </aside>
      <main>
        {activeTab === 'chat' && <ChatPage />}
        {activeTab === 'history' && <HistoryPage />}
        {activeTab === 'analytics' && <AnalyticsPage />}
      </main>
    </div>
  );
}
