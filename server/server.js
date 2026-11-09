require('dotenv').config();
const express = require('express');
const cors = require('cors');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const app = express();
app.use(express.json());
app.use(cors());

const PRICE_MAP = {
  'flash_bot': 'price_YOUR_9_DOLLAR_ID',
  'master_bundle': 'price_YOUR_19_DOLLAR_ID',
  'autotrader_suite': 'price_YOUR_299_DOLLAR_ID',
  'vip_mastermind': 'price_YOUR_499_DOLLAR_ID'
};

app.post('/create-checkout-session', async (req, res) => {
  try {
    const { productKey, addonKeys = [] } = req.body;
    
    const selectedPriceId = PRICE_MAP[productKey];
    if (!selectedPriceId) {
      return res.status(400).json({ error: 'Invalid product selection.' });
    }

    const lineItems = [{ price: selectedPriceId, quantity: 1 }];

    addonKeys.forEach(key => {
      if (PRICE_MAP[key]) {
        lineItems.push({ price: PRICE_MAP[key], quantity: 1 });
      }
    });

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: lineItems,
      mode: 'payment',
      success_url: 'https://thefundedbible.com/success.html?session_id={CHECKOUT_SESSION_ID}',
      cancel_url: 'https://thefundedbible.com/index.html',
    });

    res.json({ url: session.url });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 4242;
if (process.env.NODE_ENV !== 'production') {
  app.listen(PORT, () => console.log(Stripe checkout backend running on port \));
}
module.exports = app;
