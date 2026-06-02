import { useState } from 'react';
import { ImagePlus, Send, Sparkles } from 'lucide-react';
import { generateSimilar, solveQuestion, uploadQuestionImage } from '../services/api.js';

const starterQuestion =
  'A point charge q is placed at the center of a cube. Find the electric flux through one face of the cube.';

export default function ChatPage() {
  const [question, setQuestion] = useState(starterQuestion);
  const [result, setResult] = useState(null);
  const [similar, setSimilar] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSolve(event) {
    event.preventDefault();
    setLoading(true);
    setError('');
    setSimilar([]);
    try {
      const solved = await solveQuestion(question);
      setResult(solved);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleSimilar() {
    if (!result) return;
    const response = await generateSimilar(question, result.detection.subject, result.detection.topic);
    setSimilar(response.questions);
  }

  async function handleImageUpload(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    setLoading(true);
    setError('');
    try {
      const response = await uploadQuestionImage(file);
      setQuestion(response.text || question);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="workspace">
      <div className="toolbar">
        <div>
          <h2>Question Solver</h2>
          <p>Physics, Chemistry, and Mathematics reasoning grounded in your JEE knowledge base.</p>
        </div>
        <label className="iconButton" title="Upload question image">
          <ImagePlus size={19} />
          <input type="file" accept="image/*" onChange={handleImageUpload} />
        </label>
      </div>

      <form className="questionComposer" onSubmit={handleSolve}>
        <textarea value={question} onChange={(event) => setQuestion(event.target.value)} />
        <button className="primaryButton" disabled={loading || question.length < 5}>
          <Send size={18} />
          {loading ? 'Solving' : 'Solve'}
        </button>
      </form>

      {error && <div className="errorBox">{error}</div>}

      {result && (
        <div className="answerGrid">
          <article className="panel mainAnswer">
            <div className="answerHeader">
              <span>{result.subject}</span>
              <span>{result.topic}</span>
              <span>{Math.round(result.confidence * 100)}% confidence</span>
            </div>
            <div className="finalAnswer">
              <strong>Final Answer</strong>
              <code>{result.final_answer}</code>
            </div>
            <h3>Derivation</h3>
            <ol className="reasoningList">
              {result.reasoning_steps.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ol>
          </article>

          <aside className="panel detailPanel">
            <h3>Formulas Used</h3>
            {result.formulas_used.map((formula) => (
              <code key={formula}>{formula}</code>
            ))}
            <h3>Concepts</h3>
            {result.concepts.map((concept) => (
              <p key={concept}>{concept}</p>
            ))}
            <h3>Citations</h3>
            {result.citations.map((citation) => (
              <blockquote key={`${citation.title}-${citation.source}`}>
                <strong>{citation.title}</strong>
                <span>{citation.snippet}</span>
              </blockquote>
            ))}
          </aside>
        </div>
      )}

      {result && (
        <div className="similarSection">
          <button className="secondaryButton" onClick={handleSimilar}>
            <Sparkles size={18} />
            Generate Similar Questions
          </button>
          <div className="similarGrid">
            {similar.map((item) => (
              <article className="questionCard" key={item.difficulty}>
                <span>{item.difficulty}</span>
                <p>{item.question}</p>
                <small>{item.hint}</small>
              </article>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
