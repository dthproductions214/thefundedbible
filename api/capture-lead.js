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

    if (!email || !email.includes('@')) {
      return res.status(400).json({ ok: false, error: 'Valid email required' });
    }

    const welcomeSubject = 'Your 2-Trade Prop Saver (.CSV) + Why $50K Combines Are A Trap';
    const welcomeText = `Here is your direct link to re-download the "2-Trade Prop Saver" Mechanical Risk Sheet (.CSV) anytime:
https://www.thefundedbible.com/vault.html

Before you fire your next NQ or ES trade today, read this carefully:

You do NOT have a $50,000 account. You have a $2,500 drawdown buffer.

When you fire 2 NQ Minis with a 20-point stop loss, you are risking $800 on a single candle—that is 32% of your entire evaluation life gone in 45 seconds.

Here is the mechanical fix inside your sheet:
1. Drop your size to 5 MNQ Micros ($10/point total).
2. Lock a strict 15-point structural stop ($150 max risk per trade = 6% of your buffer).
3. Arm a hard 2-loss daily kill-switch (-$300 max daily drawdown).

At $150 risk per trade, a $50K evaluation survives 16.6 consecutive losing trades without blowing up.

⚡ STEP 1 — UNLOCK THE $9 7-DAY COMBINE PASS BLUEPRINT:
Want the exact 90-minute NY Open Silver Bullet checklist to clear $3,000 profit targets in 7 sessions using this exact 5 MNQ schedule?
https://www.thefundedbible.com/api/create-checkout-session?tier=flash_9

🔥 STEP 2 — DEPLOY THE $39 NINJATRADER 8 C# RISK LOCKOUT SUITE:
Auto-flatten your platform the second you hit +2R or -2 losses so you never tilt an evaluation again:
https://www.thefundedbible.com/api/create-checkout-session?tier=risk_terminal_39

💰 STEP 3 — CLAIM 80% OFF + $0 ACTIVATION FEE EOD EVALUATIONS (CODE: BIBLE80):
https://www.thefundedbible.com/firms.html

Trade mechanical buffer math,
Danny Hoang
The Funded Bible™ Desk
https://www.thefundedbible.com`;

    const welcomeHtml = `
    <div style="background:#04060a;color:#f8fafc;font-family:Arial,sans-serif;padding:28px;max-width:600px;margin:0 auto;border:1px solid #f59e0b;border-radius:12px;">
      <div style="color:#10b981;font-family:monospace;font-size:12px;font-weight:bold;margin-bottom:8px;">● THE FUNDED BIBLE™ EXECUTION DESK</div>
      <h2 style="color:#ffffff;margin:0 0 14px;">Your 2-Trade Prop Saver (.CSV) Is Unlocked</h2>
      <p style="color:#cbd5e1;font-size:14px;line-height:1.6;">You can re-download your mechanical risk sheet anytime inside the Member Vault: <a href="https://www.thefundedbible.com/vault.html" style="color:#fbbf24;font-weight:bold;">Open Member Vault →</a></p>
      <div style="background:#0b101b;border-left:4px solid #f59e0b;padding:14px;margin:18px 0;font-size:13px;color:#e2e8f0;line-height:1.6;">
        <strong>Remember the #1 Combine Survival Rule:</strong><br/>
        You do NOT have a $50,000 account—you have a <strong>$2,500 drawdown buffer</strong>. Size at <strong>5 MNQ Micros</strong> with a 15-point stop ($150 risk = 6% of buffer) so your combine survives <strong>16.6 consecutive losses</strong>.
      </div>
      <p style="margin:20px 0;">
        <a href="https://www.thefundedbible.com/api/create-checkout-session?tier=flash_9" style="display:block;background:#f59e0b;color:#000000;text-align:center;padding:14px;border-radius:8px;font-weight:bold;text-decoration:none;margin-bottom:12px;">⚡ UNLOCK THE $9 7-DAY PASS BLUEPRINT →</a>
        <a href="https://www.thefundedbible.com/api/create-checkout-session?tier=risk_terminal_39" style="display:block;background:#10b981;color:#000000;text-align:center;padding:14px;border-radius:8px;font-weight:bold;text-decoration:none;">🔥 DEPLOY THE $39 NT8 C# RISK LOCKOUT SUITE →</a>
      </p>
      <p style="color:#94a3b8;font-size:12px;text-align:center;margin-top:18px;">
        Need a fresh evaluation? Use code <strong style="color:#fbbf24;">BIBLE80</strong> for 80% off + $0 activation fees at <a href="https://www.thefundedbible.com/firms.html" style="color:#10b981;">TheFundedBible.com/firms.html</a>
      </p>
    </div>`;

    console.log(JSON.stringify({
      event: 'TFB_LEAD_AND_AUTORESPONDER_FIRED',
      email,
      source,
      timestamp,
      ip
    }));

    const tasks = [];

    // 1. Save Lead to Stripe Customers with Email #1 Status Logged
    if (process.env.STRIPE_SECRET_KEY) {
      const params = new URLSearchParams();
      params.append('email', email);
      params.append('description', `Funded Bible Lead (.CSV Downloaded + Welcome Pitch Sent) — Source: ${source}`);
      params.append('metadata[lead_source]', source);
      params.append('metadata[captured_at]', timestamp);
      params.append('metadata[welcome_email_sent]', 'true');
      params.append('metadata[pitched_tiers]', 'flash_9,risk_terminal_39');

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

    // 2. Fire FormSubmit with _autoresponse + email field so the trader receives the instant welcome email
    tasks.push(
      fetch('https://formsubmit.co/ajax/dannydth87@gmail.com', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          email: email,
          _replyto: email,
          _subject: `🔥 NEW FUNDED BIBLE LEAD: ${email} (Auto-Welcome Sent)`,
          _autoresponse: welcomeText,
          _template: 'table',
          _captcha: 'false',
          Trader_Email: email,
          Auto_Welcome_Pitch: 'SENT ($9 Blueprint + $39 Risk Suite + BIBLE80)',
          Captured_On_Page: `https://www.thefundedbible.com${source}`,
          Timestamp_UTC: timestamp
        })
      }).catch(err => console.error('FormSubmit Autoresponse Error:', err))
    );

    // 3. If RESEND_API_KEY is present in Vercel, send full HTML dark-mode email directly to the trader
    if (process.env.RESEND_API_KEY) {
      tasks.push(
        fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            from: process.env.RESEND_FROM_EMAIL || 'The Funded Bible Desk <onboarding@resend.dev>',
            to: [email],
            bcc: ['dannydth87@gmail.com'],
            subject: welcomeSubject,
            html: welcomeHtml,
            text: welcomeText
          })
        }).catch(err => console.error('Resend Trader Welcome Error:', err))
      );
    }

    await Promise.allSettled(tasks);

    return res.status(200).json({
      ok: true,
      autoresponder: 'sent',
      offers: {
        blueprint_9: '/api/create-checkout-session?tier=flash_9',
        risk_suite_39: '/api/create-checkout-session?tier=risk_terminal_39'
      }
    });
  } catch (error) {
    console.error('Lead Capture Error:', error);
    return res.status(200).json({ ok: true, fallback: true });
  }
}