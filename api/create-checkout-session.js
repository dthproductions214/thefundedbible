const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const CATALOG = {
  genesis_pass: {
    name: 'The $1 Genesis Pass — 2026 Prop Promo Vault',
    description: 'Verified prop discount codes, hidden rules quick-sheet, and instant starter vault access.',
    amount: 100 // Exact $1.00
  },
  trap_sheet: {
    name: 'Prop Firm Rulebook Trap Sheet',
    description: 'Exposes hidden consistency rules, news restrictions, and payout blocks across Apex, Topstep, and Lucid.',
    amount: 500 // Exact $5.00
  },
  drawdown_survival: {
    name: 'Intraday Trailing Drawdown Survival Guide',
    description: 'Stop blowing evaluations when the equity watermark trails your unrealized intraday gains.',
    amount: 900 // Exact $9.00
  },
  killzone_checklist: {
    name: 'NQ / ES Opening Bell Killzone Checklist',
    description: 'Pre-market routine and liquidity checklist for the 9:30 AM EST New York open.',
    amount: 1100 // Exact $11.00
  },
  eval_blueprint: {
    name: 'The 14-Day Evaluation Pass Blueprint',
    description: 'Step-by-step daily risk and contract-sizing schedule designed to clear a $50K or $100K combine.',
    amount: 1700 // Exact $17.00
  },
  payout_protocol: {
    name: 'Funded Payout Protection Protocol',
    description: 'Build your initial buffer on a fresh PA/funded account and lock in your first withdrawal.',
    amount: 2400 // Exact $24.00
  },
  scaling_matrix: {
    name: 'Micro-to-Mini Scaling Matrix',
    description: 'Dynamic position-sizing calculator showing when to graduate from MNQ/MES to full NQ/ES contracts.',
    amount: 2900 // Exact $29.00
  },
  starter: {
    name: 'The Risk Terminal & Starter Scripture',
    description: 'Flagship starter bundle: live drawdown calculator, quant directory, and survival blueprint.',
    amount: 3900 // Exact $39.00
  },
  copy_sync: {
    name: '20-Account Copy Trading & Sync Playbook',
    description: 'Complete setup guide for syncing multiple funded accounts across NinjaTrader, Tradovate, and Rithmic.',
    amount: 4900 // Exact $49.00
  },
  payout_vault: {
    name: 'Prop Firm Audit & Payout Blacklist Vault',
    description: 'Data-backed breakdown of which firms pay in 15 minutes versus which deny payouts on technicalities.',
    amount: 6700 // Exact $67.00
  },
  algo_guardrails: {
    name: 'Algorithmic Execution & C# Risk Guardrails',
    description: 'Automated daily loss limit locks and scripts that shut the platform down before you revenge trade.',
    amount: 7900 // Exact $79.00
  },
  core_operator: {
    name: 'The Funded Bible: Core Operator Edition',
    description: 'All 11 checklists, calculators, and evaluation playbooks combined in one vault.',
    amount: 9900 // Exact $99.00
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

const ALIAS_MAP = {
  'genesis-pass': 'genesis_pass',
  '1': 'genesis_pass',
  'trap-sheet': 'trap_sheet',
  '5': 'trap_sheet',
  'drawdown-survival': 'drawdown_survival',
  '9': 'drawdown_survival',
  'killzone-checklist': 'killzone_checklist',
  '11': 'killzone_checklist',
  'eval-blueprint': 'eval_blueprint',
  '17': 'eval_blueprint',
  'payout-protocol': 'payout_protocol',
  '24': 'payout_protocol',
  'scaling-matrix': 'scaling_matrix',
  '29': 'scaling_matrix',
  'risk-terminal': 'starter',
  '39': 'starter',
  'copy-sync': 'copy_sync',
  '49': 'copy_sync',
  'payout-vault': 'payout_vault',
  '67': 'payout_vault',
  'algo-guardrails': 'algo_guardrails',
  '79': 'algo_guardrails',
  'core-operator': 'core_operator',
  '99': 'core_operator'
};

module.exports = async (req, res) => {
  try {
    const query = req.query || {};
    const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});

    const rawTier = (query.tier || body.tier || query.plan || body.plan || 'starter').toLowerCase().trim();
    const includeBump = (query.bump === 'true' || query.bump === '1' || body.bump === true || body.orderBump === true);

    let selectedKey = 'starter';
    if (CATALOG[rawTier]) {
      selectedKey = rawTier;
    } else if (ALIAS_MAP[rawTier]) {
      selectedKey = ALIAS_MAP[rawTier];
    } else if (rawTier.includes('whale') || rawTier.includes('mastermind') || rawTier.includes('397')) {
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

    if (includeBump) {
      lineItems.push({
        price_data: {
          currency: 'usd',
          product_data: {
            name: 'Order Bump: Prop Firm Payout & Tax Loophole Guide + 5 Cheat Sheets',
            description: 'Add-on digital bundle'
          },
          unit_amount: 1900
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
      success_url: `${origin}/vault.html?unlocked=${selectedKey}&bump=${includeBump ? '1' : '0'}&session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${origin}/vault.html`
    });

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
