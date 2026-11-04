const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const CATALOG = {
  starter: {
    name: 'The Trench Starter — Risk & Drawdown Terminal ($39)',
    description: 'Automated Prop Firm Risk Mitigation Sheet, Trailing Stop Freeze Calculator & 2-Loss Kill-Switch Tracker',
    amount: 3900
  },
  standard: {
    name: 'Standard Scripture — Lifetime Master Manual & Risk Suite ($197)',
    description: 'Complete 28-Page Funded Bible Playbook, Multi-Account Pod Blueprint + $39 Risk Terminal Included',
    amount: 19700
  },
  whale: {
    name: 'Whale Scale Mastermind — 20-Account Fleet Dossier ($397)',
    description: 'Complete 50-Page Fleet Operations Dossier, 20-Account Copy-Trading Blueprint & Direct 1-on-1 Audit',
    amount: 39700
  }
};

module.exports = async (req, res) => {
  try {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
    const urlObj = new URL(req.url, `https://${req.headers.host || 'www.thefundedbible.com'}`);
    const queryTier = urlObj.searchParams.get('tier') || (req.query && req.query.tier) || '';
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    const rawTier = String(queryTier || body.tier || body.plan || 'starter').toLowerCase().trim();

    let selectedKey = 'starter';
    if (rawTier.includes('whale') || rawTier.includes('mastermind') || rawTier.includes('397')) {
      selectedKey = 'whale';
    } else if (rawTier.includes('standard') || rawTier.includes('scripture') || rawTier.includes('197')) {
      selectedKey = 'standard';
    } else {
      selectedKey = 'starter';
    }

    const item = CATALOG[selectedKey];
    const proto = req.headers['x-forwarded-proto'] || 'https';
    const host = req.headers['x-forwarded-host'] || req.headers.host || 'www.thefundedbible.com';
    const origin = `${proto}://${host}`;

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      line_items: [
        {
          price_data: {
            currency: 'usd',
            product_data: {
              name: item.name,
              description: item.description
            },
            unit_amount: item.amount
          },
          quantity: 1
        }
      ],
      success_url: `${origin}/success.html?session_id={CHECKOUT_SESSION_ID}&tier=${selectedKey}`,
      cancel_url: `${origin}/cancel.html`
    });

    if (req.method === 'GET') {
      res.writeHead(303, { Location: session.url });
      return res.end();
    }

    return res.status(200).json({ id: session.id, url: session.url, tier: selectedKey, amount: item.amount });
  } catch (err) {
    console.error('Stripe Checkout Error:', err);
    return res.status(500).json({ error: err.message });
  }
};
