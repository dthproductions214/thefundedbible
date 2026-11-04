const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const CATALOG = {
  starter: {
    name: 'The Trench Starter — Risk & Drawdown Terminal',
    description: 'Automated Prop Firm Risk Mitigation Sheet, Trailing Stop Freeze Calculator & 2-Loss Kill-Switch Tracker',
    amount: 3900 // Exact $39.00
  },
  starter_bailout: {
    name: 'The Trench Starter — 30% Off Bailout Ticket (BAILOUT30)',
    description: 'Instant download: Unbreakable Risk Mitigation Sheet + NY Session Kill-Switch Tracker',
    amount: 2700 // Exact $27.00
  },
  standard: {
    name: 'Standard Scripture — Lifetime Master Manual & Risk Suite',
    description: 'Complete 28-Page Funded Bible Playbook, Multi-Account Pod Blueprint + $39 Risk Terminal Included',
    amount: 19700 // Exact $197.00
  },
  standard_bailout: {
    name: 'Standard Scripture — 30% Off Bailout Ticket (BAILOUT30)',
    description: 'Lifetime Standard Scripture Manual + Risk Terminal Suite (30% Off Special)',
    amount: 13700 // Exact $137.00
  },
  standard_monthly: {
    name: 'Standard Scripture — Pro Desk Access',
    description: 'Complete Funded Bible Playbook, Drawdown Defense & Discord Community Access',
    amount: 9700 // Exact $97.00
  },
  whale: {
    name: 'Scale Mastermind Whale Suite — Lifetime Dossier',
    description: 'Complete 50-Page Fleet Operations Dossier, 20-Account Copy-Trading Blueprint & Direct 1-on-1 Audit',
    amount: 39700 // Exact $397.00
  }
};

module.exports = async (req, res) => {
  try {
    const query = req.query || {};
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    
    const rawTier = (query.tier || body.tier || query.plan || body.plan || 'starter').toLowerCase();
    const includeBump = (query.bump === 'true' || query.bump === '1' || body.bump === true || body.orderBump === true);

    let selectedKey = 'starter';
    if (rawTier.includes('whale') || rawTier.includes('mastermind') || rawTier.includes('397')) {
      selectedKey = 'whale';
    } else if (rawTier.includes('137') || (rawTier.includes('standard') && rawTier.includes('bailout'))) {
      selectedKey = 'standard_bailout';
    } else if (rawTier.includes('97') && !rawTier.includes('197') && !rawTier.includes('397')) {
      selectedKey = 'standard_monthly';
    } else if (rawTier.includes('standard') || rawTier.includes('scripture') || rawTier.includes('197')) {
      selectedKey = 'standard';
    } else if (rawTier.includes('27') || rawTier.includes('bailout')) {
      selectedKey = 'starter_bailout';
    } else {
      selectedKey = 'starter';
    }

    const item = CATALOG[selectedKey];
    const lineItems = [
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
    ];

    // Only add the $19 Order Bump if explicitly requested
    if (includeBump) {
      lineItems.push({
        price_data: {
          currency: 'usd',
          product_data: {
            name: 'Order Bump: Prop Firm Payout & Tax Loophole Guide + 5 Cheat Sheets',
            description: 'Add-on digital bundle'
          },
          unit_amount: 1900 // Exact $19.00
        },
        quantity: 1
      });
    }

    const proto = req.headers['x-forwarded-proto'] || 'https';
    const host = req.headers['x-forwarded-host'] || req.headers.host || 'www.thefundedbible.com';
    const origin = `${proto}://${host}`;

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      line_items: lineItems,
      success_url: `${origin}/success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${origin}/cancel.html`
    });

    // If navigated via a direct GET link (<a href="/api/create-checkout-session?tier=starter">), redirect 303 straight to Stripe Checkout
    if (req.method === 'GET') {
      res.writeHead(303, { Location: session.url });
      return res.end();
    }

    return res.status(200).json({ id: session.id, url: session.url });
  } catch (err) {
    console.error('Stripe Checkout Error:', err);
    return res.status(500).json({ error: err.message });
  }
};
