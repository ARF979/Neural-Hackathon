import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    user_instruction: '',
    tone: 'Fun and Playful',
    style: 'Short caption with 3-4 hashtags',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:8000/api/generate', formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate content');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', padding: '40px 20px', fontFamily: 'Arial, sans-serif' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 style={{ fontSize: '36px', color: 'white', marginBottom: '10px' }}>🤖 AI Social Media Generator</h1>
          <p style={{ fontSize: '18px', color: 'rgba(255,255,255,0.9)' }}>Powered by Cloud AI</p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div style={{ background: 'white', borderRadius: '16px', padding: '30px' }}>
            <h2 style={{ fontSize: '24px', marginBottom: '20px' }}>✨ Create Content</h2>
            <form onSubmit={handleSubmit}>
              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>Description *</label>
                <textarea
                  style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '2px solid #ddd', fontSize: '14px' }}
                  rows="4"
                  value={formData.user_instruction}
                  onChange={(e) => setFormData({ ...formData, user_instruction: e.target.value })}
                  placeholder="E.g., Create Instagram post for eco-friendly water bottles"
                  required
                />
              </div>
              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>Tone *</label>
                <select
                  style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '2px solid #ddd', fontSize: '14px' }}
                  value={formData.tone}
                  onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
                >
                  <option>Fun and Playful</option>
                  <option>Professional and Formal</option>
                  <option>Friendly and Casual</option>
                </select>
              </div>
              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>Style *</label>
                <select
                  style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '2px solid #ddd', fontSize: '14px' }}
                  value={formData.style}
                  onChange={(e) => setFormData({ ...formData, style: e.target.value })}
                >
                  <option>Short caption with 3-4 hashtags</option>
                  <option>Long-form storytelling</option>
                  <option>Question-based engagement</option>
                </select>
              </div>
              <button
                type="submit"
                disabled={loading}
                style={{ width: '100%', padding: '14px', background: 'linear-gradient(90deg, #667eea, #764ba2)', color: 'white', border: 'none', borderRadius: '8px', fontSize: '16px', fontWeight: 'bold', cursor: loading ? 'not-allowed' : 'pointer', opacity: loading ? 0.7 : 1 }}
              >
                {loading ? '⏳ Generating...' : '🚀 Generate Content'}
              </button>
            </form>
          </div>

          <div style={{ background: 'white', borderRadius: '16px', padding: '30px' }}>
            <h2 style={{ fontSize: '24px', marginBottom: '20px' }}>📝 Results</h2>
            {loading && <div style={{ textAlign: 'center', padding: '40px', color: '#667eea' }}><p style={{ fontSize: '18px' }}>🤖 AI is working...</p></div>}
            {error && <div style={{ background: '#fee', padding: '16px', borderRadius: '8px', color: '#c00' }}>{error}</div>}
            {result && result.success && (
              <div>
                <div style={{ background: '#f5f5f5', padding: '20px', borderRadius: '12px', marginBottom: '16px' }}>
                  <h3 style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '12px' }}>Generated Content:</h3>
                  <p style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{result.content}</p>
                </div>
                {result.image_prompt && (
                  <div style={{ background: '#f5f5f5', padding: '20px', borderRadius: '12px', marginBottom: '16px' }}>
                    <h3 style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '12px' }}>🎨 Image Prompt:</h3>
                    <p style={{ lineHeight: '1.6' }}>{result.image_prompt}</p>
                  </div>
                )}
                {result.metadata && (
                  <div style={{ background: '#f0f0f0', padding: '12px', borderRadius: '8px', fontSize: '12px', color: '#666' }}>
                    <p>⏱️ Time: {result.metadata.processing_time}</p>
                    <p>☁️ Model: {result.metadata.model_type}</p>
                  </div>
                )}
              </div>
            )}
            {!loading && !error && !result && (
              <div style={{ textAlign: 'center', padding: '60px', color: '#999' }}>
                <p>💡 Fill the form and generate content!</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
