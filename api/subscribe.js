module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    const email = String(body.email || '').trim().toLowerCase();
    const source = String(body.source || 'website').trim();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
      return res.status(400).json({ success: false, error: 'Invalid email address' });
    }

    const leadData = {
      email,
      source,
      timestamp: new Date().toISOString(),
      lead_magnet: 'Daily Prop Firm Briefing & Evaluation Pass Cheat Sheet'
    };

    let forwarded = false;

    if (process.env.RESEND_API_KEY) {
      try {
        await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            from: process.env.FROM_EMAIL || 'The Funded Bible <briefing@thefundedbible.com>',
            to: [email],
            subject: '⚡ Your Prop Firm Evaluation Pass Cheat Sheet & Daily Briefing Access',
            html: `
              <div style="font-family: Arial, sans-serif; background-color: #08090C; color: #f8fafc; padding: 30px; border-radius: 8px;">
                <h2 style="color: #f59e0b; margin-top: 0;">Welcome to The Funded Bible Daily Briefing!</h2>
                <p style="color: #cbd5e1; font-size: 16px;">Thank you for subscribing. Here is your official <strong>Prop Firm Evaluation Pass Cheat Sheet</strong>.</p>
                <div style="background-color: #0f172a; border-left: 4px solid #10b981; padding: 15px; margin: 20px 0;">
                  <h3 style="color: #10b981; margin: 0 0 10px 0;">Evaluation Pass Rules:</h3>
                  <ul style="color: #94a3b8; padding-left: 20px; line-height: 1.6;">
                    <li>Keep risk per trade under 0.5% - 1% to prevent daily drawdown breaches.</li>
                    <li>Watch out for trailing vs static drawdown rules per firm.</li>
                    <li>Avoid news trading restrictions during major tier-1 economic releases.</li>
                  </ul>
                </div>
                <p style="color: #94a3b8;">You will receive daily prop firm rule changes and hidden drawdown alerts straight to your inbox.</p>
              </div>
            `
          })
        });
        forwarded = true;
      } catch (err) {
        console.error('Resend error:', err);
      }
    }

    if (process.env.BUTTONDOWN_API_KEY) {
      try {
        await fetch('https://api.buttondown.email/v1/subscribers', {
          method: 'POST',
          headers: {
            'Authorization': `Token ${process.env.BUTTONDOWN_API_KEY}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email: email, metadata: { source } })
        });
        forwarded = true;
      } catch (err) {
        console.error('Buttondown error:', err);
      }
    }

    if (process.env.BREVO_API_KEY) {
      try {
        await fetch('https://api.brevo.com/v3/contacts', {
          method: 'POST',
          headers: {
            'api-key': process.env.BREVO_API_KEY,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email: email, attributes: { SOURCE: source }, updateEnabled: true })
        });
        forwarded = true;
      } catch (err) {
        console.error('Brevo error:', err);
      }
    }

    if (process.env.WEBHOOK_URL) {
      try {
        await fetch(process.env.WEBHOOK_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(leadData)
        });
        forwarded = true;
      } catch (err) {
        console.error('Webhook error:', err);
      }
    }

    return res.status(200).json({
      success: true,
      message: 'Subscription successful! Check your inbox for your free evaluation pass cheat sheet.',
      forwarded
    });
  } catch (error) {
    console.error('Subscription handler error:', error);
    return res.status(500).json({ success: false, error: 'Internal server error' });
  }
};
