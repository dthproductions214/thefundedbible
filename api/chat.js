export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    const userMsg = (body.message || '').trim();
    const history = Array.isArray(body.history) ? body.history.slice(-8) : [];

    if (!userMsg) {
      return res.status(200).json({ reply: "Yo, you didn't type anything—what's on your mind?" });
    }

    const systemPrompt = `You are Danny's lead prop desk operator and head closer at The Funded Bible (thefundedbible.com).
Talk 100% like a real, sharp human futures trader (NQ/ES/MNQ) in a private Discord DM—casual, direct, street-smart, zero corporate robot fluff.
NEVER say "As an AI", "I understand", "Certainly!", "Great question!", or use bulleted essays.
Keep replies natural, punchy (1 to 3 sentences max), and human. React directly to whatever they say—even if they joke, vent about blowing an account, curse, ask random questions, or test if you're real.
Know the exact offer inside out when relevant:
- $9 Blueprint (/api/create-checkout-session?tier=flash_9): 7-Day Combine Pass Blueprint, $50K/$100K lot sizing & 90-min NY Open rules.
- $39 Trench Starter & C# Suite (/api/create-checkout-session?tier=risk_terminal_39): Unbreakable Risk Sheet (.CSV) + NinjaTrader 8 C# Auto-Flatten 2-Loss Kill Switch + 20-Account Copy Calculator.
- $197 Standard Scripture (/api/create-checkout-session?tier=standard_197): Full Institutional Playbook, Trailing vs EOD Drawdown Defense (Apex, Topstep, TPT, MFFU), and all indicators.
- $397 Whale Scale Mastermind (/api/create-checkout-session?tier=whale_397): 20-Account Replikanto Copy-Trading Blueprint ($300K-$1M+), VIP War Room, and custom bots.
- Optional $19 Order Bump: LLC Payout & 1099 Tax Loophole Guide + 5 Firm Cheat Sheets.
Answer their specific question first like a real trader, then naturally point them to the best tier link using clean HTML like <a href="/api/create-checkout-session?tier=risk_terminal_39" style="color:#10b981;font-weight:800;text-decoration:underline;">Grab the $39 C# Risk Suite here →</a> only when it fits.`;

    const openAiKey = (process.env.OPENAI_API_KEY || '').trim();
    const geminiKey = (process.env.GEMINI_API_KEY || '').trim();
    const groqKey   = (process.env.GROQ_API_KEY || '').trim();

    // Option A: OpenAI / Groq compatible call
    if (openAiKey || groqKey) {
      const isGroq = !openAiKey && !!groqKey;
      const endpoint = isGroq
        ? 'https://api.groq.com/openai/v1/chat/completions'
        : 'https://api.openai.com/v1/chat/completions';
      const model = isGroq ? 'llama-3.3-70b-versatile' : 'gpt-4o-mini';
      const key = isGroq ? groqKey : openAiKey;

      const messages = [
        { role: 'system', content: systemPrompt },
        ...history.map(m => ({ role: m.role === 'user' ? 'user' : 'assistant', content: String(m.content || '') })),
        { role: 'user', content: userMsg }
      ];

      const r = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${key}` }, body: JSON.stringify({ model, messages, temperature: 0.8, max_tokens: 220 }) });  const data = await r.json(); const reply = data?.choices?.[0]?.message?.content; if (reply) return res.status(200).json({ reply }); }  // Option B: Google Gemini API if (geminiKey) { const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${geminiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          systemInstruction: { parts: [{ text: systemPrompt }] },
          contents: [
            ...history.map(m => ({
              role: m.role === 'user' ? 'user' : 'model',
              parts: [{ text: String(m.content || '') }]
            })),
            { role: 'user', parts: [{ text: userMsg }] }
          ]
        })
      });
      const data = await r.json();
      const reply = data?.candidates?.[0]?.content?.parts?.[0]?.text;
      if (reply) return res.status(200).json({ reply });
    }

    // Option C: Free live LLM fallback (Pollinations OpenAI-compatible text endpoint - works with zero API keys!)
    const pollRes = await fetch('https://text.pollinations.ai/openai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'openai',
        messages: [
          { role: 'system', content: systemPrompt },
          ...history.map(m => ({ role: m.role === 'user' ? 'user' : 'assistant', content: String(m.content || '') })),
          { role: 'user', content: userMsg }
        ],
        temperature: 0.8
      })
    });

    if (pollRes.ok) {
      const pollData = await pollRes.json();
      const reply = pollData?.choices?.[0]?.message?.content;
      if (reply) return res.status(200).json({ reply });
    }

    return res.status(200).json({ reply: null });
  } catch (e) {
    return res.status(200).json({ reply: null });
  }
}
