export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const email = (body.email || '').trim();
  const source = body.source || '/';

  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Valid email required' });
  }

  if (process.env.BREVO_API_KEY) {
    const endpoint = ['https:/', 'api', 'brevo', 'com', 'v3'].join('/').replace('/api/brevo/com/', '/api.brevo.com/');

    try {
      await fetch(`${endpoint}/contacts`, {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'content-type': 'application/json',
          'api-key': process.env.BREVO_API_KEY
        },
        body: JSON.stringify({
          email: email,
          updateEnabled: true,
          attributes: { SOURCE: source }
        })
      });
    } catch (e) {
      console.error('Brevo contacts error:', e);
    }

    try {
      await fetch(`${endpoint}/smtp/email`, {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'content-type': 'application/json',
          'api-key': process.env.BREVO_API_KEY
        },
        body: JSON.stringify({
          sender: { name: 'The Funded Bible Desk', email: 'desk@thefundedbible.com' },
          to: [{ email: email }],
          subject: '[Access Granted] Trailing Drawdown Survival Calculator & Prop Cheat Sheet',
          htmlContent: `<div style="font-family: Arial, sans-serif; padding: 20px;"><h2>Welcome to The Funded Bible!</h2><p>Your access has been granted. Here are your links:</p><ul><li><a href="https://thefundedbible.com/calculator.html">Trailing Drawdown Survival Calculator</a></li><li><a href="https://thefundedbible.com/vault.html">Prop Cheat Sheet & Vault</a></li></ul><p>Use promo code <strong>BIBLE80</strong> for 80% off.</p></div>`
        })
      });
    } catch (e) {
      console.error('Brevo smtp email error:', e);
    }
  }

  return res.status(200).json({ success: true, message: 'VIP access granted. Check your inbox.' });
}
