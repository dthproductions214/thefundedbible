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

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    const email = (body.email || '').trim().toLowerCase();
    const source = body.source || '/';
    const timestamp = body.timestamp || new Date().toISOString();
    const ip = req.headers['x-forwarded-for'] || req.socket?.remoteAddress || 'unknown';
    const userAgent = req.headers['user-agent'] || 'unknown';

    if (!email || !email.includes('@')) {
      return res.status(400).json({ ok: false, error: 'Valid email required' });
    }

    // 1. Permanent structured log in Vercel Function Logs
    console.log(JSON.stringify({
      event: 'TFB_LEAD_CAPTURED',
      email,
      source,
      timestamp,
      ip
    }));

    const tasks = [];

    // 2. Auto-save lead into your Stripe Customers database (uses your existing STRIPE_SECRET_KEY)
    if (process.env.STRIPE_SECRET_KEY) {
      const params = new URLSearchParams();
      params.append('email', email);
      params.append('description', `The Funded Bible Lead Magnet (.CSV Risk Sheet) — Source: ${source}`);
      params.append('metadata[lead_source]', source);
      params.append('metadata[captured_at]', timestamp);
      params.append('metadata[funnel]', '2_Trade_Prop_Saver_CSV');

      tasks.push(
        fetch('https://api.stripe.com/v1/customers', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${process.env.STRIPE_SECRET_KEY}`,
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: params.toString()
        }).catch(err => console.error('Stripe Customer Save Error:', err))
      );
    }

    // 3. Forward instant notification email to dannydth87@gmail.com via FormSubmit AJAX
    tasks.push(
      fetch('https://formsubmit.co/ajax/dannydth87@gmail.com', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          _subject: `🔥 NEW FUNDED BIBLE LEAD: ${email}`,
          _template: 'table',
          _captcha: 'false',
          Trader_Email: email,
          Captured_On_Page: `https://www.thefundedbible.com${source}`,
          Lead_Magnet: '2-Trade Prop Saver Risk Sheet (.CSV)',
          Next_Funnel_Step: '$9 7-Day Pass Blueprint / $39 NT8 Risk Suite',
          Timestamp_UTC: timestamp,
          Trader_IP: ip,
          Device: userAgent
        })
      }).catch(err => console.error('Email Forward Error:', err))
    );

    // 4. Optional Resend API support if RESEND_API_KEY is ever added to Vercel
    if (process.env.RESEND_API_KEY) {
      tasks.push(
        fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            from: 'The Funded Bible Desk <onboarding@resend.dev>',
            to: ['dannydth87@gmail.com'],
            subject: `🔥 New Funded Bible Lead: ${email}`,
            html: `<h3>New Trader Lead Captured on TheFundedBible.com</h3>
                   <p><strong>Email:</strong> ${email}</p>
                   <p><strong>Source Page:</strong> ${source}</p>
                   <p><strong>Time:</strong> ${timestamp}</p>
                   <p><strong>Saved to Stripe Customers:</strong> Yes</p>`
          })
        }).catch(err => console.error('Resend Error:', err))
      );
    }

    await Promise.allSettled(tasks);

    return res.status(200).json({
      ok: true,
      message: 'Lead captured, stored in Stripe Customers, and forwarded to dannydth87@gmail.com'
    });
  } catch (error) {
    console.error('Lead Capture Handler Error:', error);
    return res.status(200).json({ ok: true, fallback: true });
  }
}