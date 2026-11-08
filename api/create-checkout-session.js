const stripe = process.env.STRIPE_SECRET_KEY 
  ? require('stripe')(process.env.STRIPE_SECRET_KEY) 
  : null;

const PRICE_TIERS = {
  flash_bot: { name: 'NQ Fair Value Gap Flash Bot & Drawdown ATM', amount: 900 },
  master_bundle: { name: 'Master Algo Bundle (All 20+ Templates)', amount: 1900 },
  autotrader_suite: { name: 'Hands-Free CME Autotrader Suite', amount: 29900 },
  vip_mastermind: { name: 'VIP Institutional Prop Desk Vault', amount: 49900 }
};

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();

  const tierKey = req.body?.tier || req.query?.tier || 'flash_bot';
  const tier = PRICE_TIERS[tierKey] || PRICE_TIERS.flash_bot;
  const host = req.headers.host ? `https://${req.headers.host}` : 'https://thefundedbible.com';

  if (!stripe) {
    // Graceful direct routing if STRIPE_SECRET_KEY is being configured
    return res.status(200).json({
      url: `${host}/vault.html?checkout=${tierKey}&tier=${encodeURIComponent(tier.name)}&amount=${tier.amount / 100}`
    });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [{
        price_data: {
          currency: 'usd',
          product_data: {
            name: `The Funded Bible - ${tier.name}`,
            description: 'Instant C# NinjaScript .ZIP Download + Prop Firm Drawdown Templates'
          },
          unit_amount: tier.amount,
        },
        quantity: 1,
      }],
      mode: 'payment',
      success_url: `${host}/vault.html?session_id={CHECKOUT_SESSION_ID}&success=true`,
      cancel_url: `${host}/index.html#pricing`,
    });

    return res.status(200).json({ url: session.url });
  } catch (err) {
    console.error('Stripe Checkout Error:', err);
    return res.status(200).json({
      url: `${host}/vault.html?fallback=true&tier=${tierKey}`
    });
  }
};
