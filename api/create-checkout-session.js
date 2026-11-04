import Stripe from 'stripe';

const CATALOG = {
  tier_1: {
    name: 'The $1 Genesis Pass (2026 Promo Vault)',
    description: 'Verified prop discount codes, hidden rules quick-sheet, and instant starter vault access.',
    amount: 100
  },
  tier_5: {
    name: 'Prop Firm Rulebook Trap Sheet ($5)',
    description: 'Exposes hidden consistency rules, news restrictions, and payout blocks across Apex, Topstep & Lucid.',
    amount: 500
  },
  tier_7: {
    name: 'Intraday Trailing Drawdown Shield ($7)',
    description: 'Mechanical defense guide to stop blowing combines on unrealized high-water mark trailing locks.',
    amount: 700
  },
  flash_9: {
    name: '7-Day Combine Pass Blueprint ($9)',
    description: 'Exact $50K & $100K Daily Lot-Sizing Sheet, Apex Intraday Trailing Defense Rules & 90-Min NY Open Checklist.',
    amount: 900
  },
  tier_11: {
    name: 'NQ / ES Opening Bell Killzone Checklist ($11)',
    description: 'Pre-market routine and liquidity checklist for the 9:30 AM EST New York open.',
    amount: 1100
  },
  tier_17: {
    name: 'The 14-Day Evaluation Pass Blueprint ($17)',
    description: 'Step-by-step daily risk and contract-sizing schedule designed to clear a $50K or $100K combine cleanly.',
    amount: 1700
  },
  tier_19: {
    name: 'Silver Bullet & FVG Execution Guide ($19)',
    description: '10:00-11:00 AM EST NY session liquidity sweep & Fair Value Gap mechanical entry playbook.',
    amount: 1900
  },
  tier_24: {
    name: 'Funded Payout Protection Protocol ($24)',
    description: 'Build your initial buffer on a fresh PA/funded account and lock in your first withdrawal without tilting.',
    amount: 2400
  },
  tier_27: {
    name: 'First Payout Withdrawal Playbook ($27)',
    description: 'Step-by-step buffer lock and payout request schedule for funded PA & XFA accounts.',
    amount: 2700
  },
  tier_29: {
    name: 'Micro-to-Mini Scaling Matrix ($29)',
    description: 'Dynamic position-sizing calculator showing when to graduate from MNQ/MES to full NQ/ES contracts.',
    amount: 2900
  },
  risk_terminal_39: {
    name: 'The Trench Starter & C# Risk Suite ($39)',
    description: 'Unbreakable Risk Mitigation Sheet (.CSV/Excel), NinjaScript Auto-Flatten 2-Loss Daily Kill-Switch & 20-Account Copy-Trade Risk Calculator.',
    amount: 3900
  },
  tier_49: {
    name: '20-Account Copy Trading & Sync Playbook ($49)',
    description: 'Complete setup guide for syncing multiple funded accounts across NinjaTrader, Tradovate, and Rithmic.',
    amount: 4900
  },
  tier_67: {
    name: 'Prop Firm Audit & Payout Blacklist Vault ($67)',
    description: 'Data-backed breakdown of which firms pay in 15 minutes versus which deny payouts on technicalities.',
    amount: 6700
  },
  tier_79: {
    name: 'Algorithmic Execution & C# Risk Guardrails ($79)',
    description: 'Automated daily loss limit locks and scripts that shut the platform down before you revenge trade.',
    amount: 7900
  },
  tier_99: {
    name: 'The Funded Bible: Core Operator Edition ($99)',
    description: 'Every checklist, calculator, and evaluation playbook ($1-$79) bundled in one complete vault.',
    amount: 9900
  },
  standard_197: {
    name: 'Standard Scripture Master Manual ($197 Lifetime)',
    description: 'Complete Institutional Playbook, Trailing vs. EOD Drawdown Defense System, All NinjaScript Indicators & Full 12-Tier Arsenal Included.',
    amount: 19700
  },
  whale_397: {
    name: 'Whale Scale Mastermind Vault ($397 Lifetime)',
    description: '$1.2M Multi-Account Copy-Trading Blueprint (20 Accounts), Custom Bot & C# Execution Templates, VIP War Room & Every Playbook/Tax Guide Included.',
    amount: 39700
  }
};

function resolveTierKey(raw, rawAmount) {
  const s = String(raw || '').toLowerCase().trim();
  const amt = parseInt(rawAmount, 10);

  if (CATALOG[s]) return s;

  // Match by explicit slug aliases
  if (s.includes('397') || s.includes('whale') || s.includes('mastermind') || s === 'tier_3') return 'whale_397';
  if (s.includes('197') || s.includes('standard') || s.includes('scripture') || s === 'tier_2') return 'standard_197';
  if (s.includes('99') || s.includes('core-operator') || s.includes('core_operator')) return 'tier_99';
  if (s.includes('79') || s.includes('algo-guardrails') || s.includes('guardrail')) return 'tier_79';
  if (s.includes('67') || s.includes('payout-vault') || s.includes('blacklist')) return 'tier_67';
  if (s.includes('49') || s.includes('copy-sync') || s.includes('copier')) return 'tier_49';
  if (s.includes('39') || s.includes('starter') || s.includes('terminal') || s === 'tier_1_anchor') return 'risk_terminal_39';
  if (s.includes('29') || s.includes('scaling-matrix')) return 'tier_29';
  if (s.includes('27')) return 'tier_27';
  if (s.includes('24') || s.includes('payout-protocol')) return 'tier_24';
  if (s.includes('19') || s.includes('silver')) return 'tier_19';
  if (s.includes('17') || s.includes('eval-blueprint')) return 'tier_17';
  if (s.includes('11') || s.includes('killzone')) return 'tier_11';
  if (s.includes('9') || s.includes('flash') || s.includes('drawdown-survival') || s.includes('blueprint')) return 'flash_9';
  if (s.includes('7') || s.includes('shield')) return 'tier_7';
  if (s.includes('5') || s.includes('trap-sheet')) return 'tier_5';
  if (s.includes('1') || s.includes('genesis')) return 'tier_1';

  // Fallback match by dollar amount if passed
  const byAmount = {
    1: 'tier_1', 5: 'tier_5', 7: 'tier_7', 9: 'flash_9', 11: 'tier_11',
    17: 'tier_17', 19: 'tier_19', 24: 'tier_24', 27: 'tier_27', 29: 'tier_29',
    39: 'risk_terminal_39', 49: 'tier_49', 67: 'tier_67', 79: 'tier_79',
    99: 'tier_99', 197: 'standard_197', 397: 'whale_397'
  };
  if (byAmount[amt]) return byAmount[amt];

  return 'risk_terminal_39';
}

export default async function handler(req, res) {
  let fallbackUrl = 'https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03';
  try {
    const query = req.query || {};
    let body = {};
    try {
      body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    } catch (_) {}

    const rawTier = query.tier || body.tier || query.plan || body.plan || '';
    const rawAmount = query.amount || body.amount || '';
    const includeBump = (
      query.bump === 'true' ||
      query.bump === '1' ||
      body.bump === true ||
      body.orderBump === true
    );

    const selectedKey = resolveTierKey(rawTier, rawAmount);
    const item = CATALOG[selectedKey] || CATALOG.risk_terminal_39;

    const secretKey = (process.env.STRIPE_SECRET_KEY || process.env.STRIPE_API_KEY || '').trim();
    const proto = (req.headers && req.headers['x-forwarded-proto']) || 'https';
    const host = (req.headers && (req.headers['x-forwarded-host'] || req.headers.host)) || 'www.thefundedbible.com';
    const origin = `${proto}://${host}`;

    if (secretKey) {
      const stripe = new Stripe(secretKey);
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

      if (includeBump) {
        lineItems.push({
          price_data: {
            currency: 'usd',
            product_data: {
              name: 'Order Bump: Prop Firm LLC Payout & 1099 Tax Shield + 5 Drawdown Cheat Sheets',
              description: 'Instant Add-On Bundle: LLC/S-Corp tax deduction blueprint + 5 rapid prop desk rule cheat sheets.'
            },
            unit_amount: 1900
          },
          quantity: 1
        });
      }

      const session = await stripe.checkout.sessions.create({
        payment_method_types: ['card'],
        mode: 'payment',
        line_items: lineItems,
        success_url: `${origin}/vault.html?unlocked=${selectedKey}&bump=${includeBump ? '1' : '0'}&session_id={CHECKOUT_SESSION_ID}`,
        cancel_url: `${origin}/#pricing`
      });

      if (session && session.url) {
        if (req.method === 'GET') {
          res.writeHead(303, { Location: session.url, 'Cache-Control': 'no-store' });
          return res.end();
        }
        return res.status(200).json({ id: session.id, url: session.url });
      }
    }

    if (req.method === 'GET') {
      res.writeHead(303, { Location: fallbackUrl, 'Cache-Control': 'no-store' });
      return res.end();
    }
    return res.status(200).json({ id: 'fallback_link', url: fallbackUrl });
  } catch (err) {
    if (req.method === 'GET') {
      res.writeHead(303, { Location: fallbackUrl, 'Cache-Control': 'no-store' });
      return res.end();
    }
    return res.status(200).json({ id: 'fallback_link', url: fallbackUrl });
  }
}
