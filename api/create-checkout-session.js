const CATALOG = {
  genesis_pass: {
    name: 'The $1 Genesis Pass — 2026 Prop Promo Vault',
    description: 'Verified prop discount codes, hidden rules quick-sheet, and instant starter vault access.',
    amount: 100,
    fallback: 'https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03'
  },
  trap_sheet: {
    name: 'Prop Firm Rulebook Trap Sheet',
    description: 'Exposes hidden consistency rules, news restrictions, and payout blocks across Apex, Topstep, and Lucid.',
    amount: 500,
    fallback: 'https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03'
  },
  drawdown_survival: {
    name: 'Intraday Trailing Drawdown Survival Guide',
    description: 'Stop blowing evaluations when the equity watermark trails your unrealized intraday gains.',
    amount: 900,
    fallback: 'https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03'
  },
  killzone_checklist: {
    name: 'NQ / ES Opening Bell Killzone Checklist',
    description: 'Pre-market routine and liquidity checklist for the 9:30 AM EST New York open.',
    amount: 1100,
    fallback: 'https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03'
  },
  eval_blueprint: {
    name: 'The 14-Day Evaluation Pass Blueprint',
    description: 'Step-by-step daily risk and contract-sizing schedule designed to clear a $50K or $100K combine.',
    amount: 1700,
    fallback: 'https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03'
  },
  payout_protocol: {
    name: 'Funded Payout Protection Protocol',
    description: 'Build your initial buffer on a fresh PA/funded account and lock in your first withdrawal.',
    amount: 2400,
    fallback: 'https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03'
  },
  scaling_matrix: {
    name: 'Micro-to-Mini Scaling Matrix',
    description: 'Dynamic position-sizing calculator showing when to graduate from MNQ/MES to full NQ/ES contracts.',
    amount: 2900,
    fallback: 'https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03'
  },
  starter: {
    name: 'The Risk Terminal & Starter Scripture',
    description: 'Flagship starter bundle: live drawdown calculator, quant directory, and survival blueprint.',
    amount: 3900,
    fallback: 'https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03'
  },
  copy_sync: {
    name: '20-Account Copy Trading & Sync Playbook',
    description: 'Complete setup guide for syncing multiple funded accounts across NinjaTrader, Tradovate, and Rithmic.',
    amount: 4900,
    fallback: 'https://buy.stripe.com/3cI4gz0Ep2wE3XxaZB3gk05'
  },
  payout_vault: {
    name: 'Prop Firm Audit & Payout Blacklist Vault',
    description: 'Data-backed breakdown of which firms pay in 15 minutes versus which deny payouts on technicalities.',
    amount: 6700,
    fallback: 'https://buy.stripe.com/3cI4gz0Ep2wE3XxaZB3gk05'
  },
  algo_guardrails: {
    name: 'Algorithmic Execution & C# Risk Guardrails',
    description: 'Automated daily loss limit locks and scripts that shut the platform down before you revenge trade.',
    amount: 7900,
    fallback: 'https://buy.stripe.com/3cI4gz0Ep2wE3XxaZB3gk05'
  },
  core_operator: {
    name: 'The Funded Bible: Core Operator Edition',
    description: 'All 11 checklists, calculators, and evaluation playbooks combined in one vault.',
    amount: 9900,
    fallback: 'https://buy.stripe.com/3cI4gz0Ep2wE3XxaZB3gk05'
  },
  starter_bailout: {
    name: 'The Trench Starter — 30% Off Bailout Ticket (BAILOUT30)',
    description: 'Instant download: Unbreakable Risk Mitigation Sheet + NY Session Kill-Switch Tracker',
    amount: 2700,
    fallback: 'https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03'
  },
  standard: {
    name: 'Standard Scripture — Lifetime Master Manual & Risk Suite',
    description: 'Complete 28-Page Funded Bible Playbook, Multi-Account Pod Blueprint + $39 Risk Terminal Included',
    amount: 19700,
    fallback: 'https://buy.stripe.com/3cI4gz0Ep2wE3XxaZB3gk05'
  },
  standard_bailout: {
    name: 'Standard Scripture — 30% Off Bailout Ticket (BAILOUT30)',
    description: 'Lifetime Standard Scripture Manual + Risk Terminal Suite (30% Off Special)',
    amount: 13700,
    fallback: 'https://buy.stripe.com/3cI4gz0Ep2wE3XxaZB3gk05'
  },
  standard_monthly: {
    name: 'Standard Scripture — Pro Desk Access',
    description: 'Complete Funded Bible Playbook, Drawdown Defense & Discord Community Access',
    amount: 9700,
    fallback: 'https://buy.stripe.com/3cI4gz0Ep2wE3XxaZB3gk05'
  },
  whale: {
    name: 'Scale Mastermind Whale Suite — Lifetime Dossier',
    description: 'Complete 50-Page Fleet Operations Dossier, 20-Account Copy-Trading Blueprint & Direct 1-on-1 Audit',
    amount: 39700,
    fallback: 'https://buy.stripe.com/bJedR9cn7c7egKjaZB3gk06'
  }
};

const ALIAS_MAP = {
  'genesis-pass': 'genesis_pass', '1': 'genesis_pass',
  'trap-sheet': 'trap_sheet', '5': 'trap_sheet',
  'drawdown-survival': 'drawdown_survival', '9': 'drawdown_survival',
  'killzone-checklist': 'killzone_checklist', '11': 'killzone_checklist',
  'eval-blueprint': 'eval_blueprint', '17': 'eval_blueprint',
  'payout-protocol': 'payout_protocol', '24': 'payout_protocol',
  'scaling-matrix': 'scaling_matrix', '29': 'scaling_matrix',
  'risk-terminal': 'starter', '39': 'starter',
  'copy-sync': 'copy_sync', '49': 'copy_sync',
  'payout-vault': 'payout_vault', '67': 'payout_vault',
  'algo-guardrails': 'algo_guardrails', '79': 'algo_guardrails',
  'core-operator': 'core_operator', '99': 'core_operator'
};

function resolveTierKey(rawTier) {
  const t = String(rawTier || 'starter').toLowerCase().trim();
  if (CATALOG[t]) return t;
  if (ALIAS_MAP[t]) return ALIAS_MAP[t];
  if (t.includes('whale') || t.includes('mastermind') || t.includes('397')) return 'whale';
  if (t.includes('137') || (t.includes('standard') && t.includes('bailout'))) return 'standard_bailout';
  if (t.includes('97') && !t.includes('197') && !t.includes('397')) return 'standard_monthly';
  if (t.includes('standard') || t.includes('scripture') || t.includes('197')) return 'standard';
  if (t.includes('27') || t.includes('bailout')) return 'starter_bailout';
  return 'starter';
}

export default async function handler(req, res) {
  let fallbackUrl = 'https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03';
  try {
    const query = req.query || {};
    let body = {};
    try {
      body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
    } catch (_) {}

    const rawTier = query.tier || body.tier || query.plan || body.plan || 'starter';
    const includeBump = (query.bump === 'true' || query.bump === '1' || body.bump === true || body.orderBump === true);

    const selectedKey = resolveTierKey(rawTier);
    const item = CATALOG[selectedKey] || CATALOG.starter;
    fallbackUrl = item.fallback || fallbackUrl;

    const secretKey = (process.env.STRIPE_SECRET_KEY || process.env.STRIPE_API_KEY || '').trim();
    const proto = (req.headers && req.headers['x-forwarded-proto']) || 'https';
    const host = (req.headers && (req.headers['x-forwarded-host'] || req.headers.host)) || 'www.thefundedbible.com';
    const origin = `${proto}://${host}`;

    if (secretKey && secretKey.startsWith('sk_')) {
      const form = new URLSearchParams();
      form.append('mode', 'payment');
      form.append('payment_method_types[0]', 'card');
      form.append('allow_promotion_codes', 'true');
      form.append('success_url', `${origin}/vault.html?unlocked=${selectedKey}&bump=${includeBump ? '1' : '0'}&session_id={CHECKOUT_SESSION_ID}`);
      form.append('cancel_url', `${origin}/vault.html`);

      form.append('line_items[0][price_data][currency]', 'usd');
      form.append('line_items[0][price_data][product_data][name]', item.name);
      form.append('line_items[0][price_data][product_data][description]', item.description);
      form.append('line_items[0][price_data][unit_amount]', String(item.amount));
      form.append('line_items[0][quantity]', '1');

      if (includeBump) {
        form.append('line_items[1][price_data][currency]', 'usd');
        form.append('line_items[1][price_data][product_data][name]', 'Order Bump: Prop Firm Payout & Tax Loophole Guide + 5 Cheat Sheets');
        form.append('line_items[1][price_data][product_data][description]', 'Add-on digital bundle');
        form.append('line_items[1][price_data][unit_amount]', '1900');
        form.append('line_items[1][quantity]', '1');
      }

      const resp = await fetch('https://api.stripe.com/v1/checkout/sessions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${secretKey}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: form.toString()
      });

      const data = await resp.json();
      if (resp.ok && data && data.url) {
        if (req.method === 'GET') {
          res.writeHead(303, { Location: data.url, 'Cache-Control': 'no-store' });
          return res.end();
        }
        return res.status(200).json({ id: data.id, url: data.url });
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
