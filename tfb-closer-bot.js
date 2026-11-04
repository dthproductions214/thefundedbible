(function () {
  if (document.getElementById('tfb-ai-closer-root')) return;

  const style = document.createElement('style');
  style.textContent = `
    #tfb-ai-closer-root {
      position: fixed;
      bottom: 68px;
      right: 20px;
      z-index: 9998;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    #tfb-bot-launcher {
      background: linear-gradient(135deg, #0d1322, #060911);
      border: 1.5px solid #f59e0b;
      color: #fff;
      padding: 12px 18px;
      border-radius: 999px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.9), 0 0 20px rgba(245, 158, 11, 0.28);
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 800;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }
    #tfb-bot-launcher:hover {
      transform: translateY(-2px);
      border-color: #10b981;
    }
    .tfb-bot-pulse {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 10px #10b981;
      display: inline-block;
    }
    .tfb-bot-badge {
      background: #ef4444;
      color: #fff;
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 99px;
      font-weight: 800;
    }
    #tfb-bot-window {
      display: none;
      width: 370px;
      max-width: calc(100vw - 32px);
      height: 520px;
      max-height: calc(100vh - 150px);
      background: #060911;
      border: 1.5px solid #f59e0b;
      border-radius: 16px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.95);
      flex-direction: column;
      overflow: hidden;
      margin-bottom: 12px;
    }
    .tfb-bot-header {
      background: linear-gradient(90deg, #0b111e, #070a12);
      border-bottom: 1px solid rgba(245, 158, 11, 0.3);
      padding: 14px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .tfb-bot-messages {
      flex: 1;
      padding: 14px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: #04060b;
    }
    .tfb-msg-bot {
      background: #0d1322;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-left: 3px solid #10b981;
      color: #e2e8f0;
      padding: 11px 13px;
      border-radius: 10px;
      font-size: 12.5px;
      line-height: 1.55;
      max-width: 92%;
    }
    .tfb-msg-user {
      background: rgba(245, 158, 11, 0.16);
      border: 1px solid #f59e0b;
      color: #fff;
      padding: 9px 12px;
      border-radius: 10px;
      font-size: 12px;
      align-self: flex-end;
      max-width: 85%;
      font-family: 'JetBrains Mono', monospace;
    }
    .tfb-quick-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding: 10px 12px;
      background: #070b14;
      border-top: 1px solid rgba(255, 255, 255, 0.07);
    }
    .tfb-chip {
      background: #111827;
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: #fbbf24;
      padding: 5px 9px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10.5px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s;
    }
    .tfb-chip:hover {
      background: #f59e0b;
      color: #000;
    }
    .tfb-bot-input-row {
      display: flex;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      background: #050811;
    }
    .tfb-bot-input-row input {
      flex: 1;
      background: transparent;
      border: none;
      color: #fff;
      padding: 12px;
      font-size: 12px;
      font-family: 'JetBrains Mono', monospace;
      outline: none;
    }
    .tfb-bot-input-row button {
      background: #f59e0b;
      color: #000;
      border: none;
      padding: 0 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
    }
    .tfb-bot-cta {
      display: block;
      margin-top: 9px;
      padding: 9px 12px;
      border-radius: 6px;
      background: linear-gradient(135deg, #fbbf24, #d97706);
      color: #000 !important;
      text-decoration: none;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 800;
      text-align: center;
    }
    .tfb-bot-cta-sec {
      display: block;
      margin-top: 6px;
      padding: 8px 12px;
      border-radius: 6px;
      background: #111827;
      border: 1px solid #10b981;
      color: #10b981 !important;
      text-decoration: none;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 800;
      text-align: center;
    }
  `;
  document.head.appendChild(style);

  const root = document.createElement('div');
  root.id = 'tfb-ai-closer-root';
  root.innerHTML = `
    <div id="tfb-bot-window">
      <div class="tfb-bot-header">
        <div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#10b981;font-weight:800;">● 24/7 AI PROP DESK CLOSER</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:15px;font-weight:800;color:#fff;">The Funded Bible™ Risk AI</div>
        </div>
        <button id="tfb-bot-close" style="background:transparent;border:none;color:#94a3b8;font-family:'JetBrains Mono',monospace;font-size:16px;cursor:pointer;">[X]</button>
      </div>

      <div class="tfb-bot-messages" id="tfb-bot-messages">
        <div class="tfb-msg-bot">
          <strong>Welcome to the Institutional Futures Desk.</strong><br/>
          94% of traders fail combines because they size against nominal balance instead of the drawdown buffer. Tap a question below or type yours:
          <a href="/api/create-checkout-session?tier=flash_9" class="tfb-bot-cta">⚡ GET $9 7-DAY PASS BLUEPRINT →</a>
          <a href="/api/create-checkout-session?tier=risk_terminal_39" class="tfb-bot-cta-sec">🔥 DEPLOY $39 NT8 C# RISK SUITE →</a>
        </div>
      </div>

      <div class="tfb-quick-chips">
        <button class="tfb-chip" data-q="What is the safe MNQ lot size on a $50K account?">$50K Safe MNQ Size?</button>
        <button class="tfb-chip" data-q="Which prop firms have $0 activation fee and EOD drawdown?">$0 Fee EOD Firms?</button>
        <button class="tfb-chip" data-q="How do I beat Apex intraday trailing drawdown?">Beat Trailing Lock?</button>
        <button class="tfb-chip" data-q="What is inside the $9 vs $39 Risk Suite?">$9 vs $39 Suite?</button>
        <button class="tfb-chip" data-q="Send me the free 2-Trade Prop Saver .CSV">Free .CSV Sheet</button>
      </div>

      <form class="tfb-bot-input-row" id="tfb-bot-form">
        <input type="text" id="tfb-bot-input" placeholder="Ask about MNQ sizing, EOD firms, or C# bot..." />
        <button type="submit">SEND</button>
      </form>
    </div>

    <button id="tfb-bot-launcher">
      <span class="tfb-bot-pulse"></span>
      <span>ASK AI PROP DESK</span>
      <span class="tfb-bot-badge" id="tfb-bot-unread">1</span>
    </button>
  `;
  document.body.appendChild(root);

  const win = document.getElementById('tfb-bot-window');
  const launcher = document.getElementById('tfb-bot-launcher');
  const closeBtn = document.getElementById('tfb-bot-close');
  const unread = document.getElementById('tfb-bot-unread');
  const msgBox = document.getElementById('tfb-bot-messages');
  const form = document.getElementById('tfb-bot-form');
  const input = document.getElementById('tfb-bot-input');

  function toggleBot(open) {
    const isOpen = open !== undefined ? open : win.style.display !== 'flex';
    win.style.display = isOpen ? 'flex' : 'none';
    if (isOpen && unread) unread.style.display = 'none';
  }

  launcher.addEventListener('click', () => toggleBot());
  closeBtn.addEventListener('click', () => toggleBot(false));

  function getAiReply(q) {
    const s = q.toLowerCase();
    if (s.includes('csv') || s.includes('free') || s.includes('sheet')) {
      if (typeof openLeadModal === 'function') setTimeout(openLeadModal, 400);
      return `I just triggered our <strong>Free "2-Trade Prop Saver" (.CSV)</strong> modal for you! If you also want the step-by-step 7-session schedule to pass your $50K combine, grab the $9 Blueprint below:
      <a href="/api/create-checkout-session?tier=flash_9" class="tfb-bot-cta">⚡ UNLOCK $9 PASS BLUEPRINT →</a>`;
    }
    if (s.includes('50k') || s.includes('lot') || s.includes('mnq') || s.includes('size')) {
      return `On a <strong>$50,000 combine ($2,500 drawdown buffer)</strong>, never risk more than 6% of your buffer ($150) per trade.<br/><br/>• <strong>Exact Size:</strong> 5 MNQ Micros ($10/pt)<br/>• <strong>Stop Loss:</strong> 15 Points (-$150)<br/>• <strong>Survival Buffer:</strong> 16.6 straight losses.<br/><br/>Get the full $50K–$300K scaling schedule inside the $9 Blueprint or automate your 2-loss lockout with the $39 C# Suite:
      <a href="/api/create-checkout-session?tier=flash_9" class="tfb-bot-cta">⚡ GET $9 7-DAY PASS BLUEPRINT →</a>
      <a href="/api/create-checkout-session?tier=risk_terminal_39" class="tfb-bot-cta-sec">🔥 GET $39 NT8 C# KILL-SWITCH →</a>`;
    }
    if (s.includes('activation') || s.includes('eod') || s.includes('firm') || s.includes('mffu') || s.includes('topstep')) {
      return `Top <strong>$0 Activation Fee + EOD Static Drawdown</strong> firms for November 2026:<br/>1. <strong>MyFundedFutures (MFFU)</strong> ($0 Activation + EOD)<br/>2. <strong>Tradeify Select</strong> ($0 Activation + EOD)<br/>3. <strong>TopstepX</strong> ($0 No-Fee Path + EOD)<br/><br/>Use code <strong style="color:#fbbf24;">BIBLE80</strong> for up to 80% off on our <a href="firms.html" style="color:#10b981;">12-Firm Matrix</a>, and arm our $39 Risk Suite before trading:
      <a href="/api/create-checkout-session?tier=risk_terminal_39" class="tfb-bot-cta">🔥 DEPLOY $39 RISK SUITE FIRST →</a>`;
    }
    if (s.includes('trailing') || s.includes('apex') || s.includes('intraday')) {
      return `<strong>Intraday High-Water Trailing Drawdown</strong> trails your highest unrealized open equity tick-by-tick. If an NQ runner goes up +40pts and pulls back to entry, you lose 40pts of buffer!<br/><br/><strong>The Fix:</strong> Dump 80% (4 of 5 MNQ) at +20 points ($160 banked) and let our <strong>$39 NinjaTrader 8 C# Risk Suite</strong> auto-flatten your account at +2R or -2 losses:
      <a href="/api/create-checkout-session?tier=risk_terminal_39" class="tfb-bot-cta">⚡ DEPLOY $39 NT8 C# RISK SUITE →</a>`;
    }
    if (s.includes('$9') || s.includes('$39') || s.includes('suite') || s.includes('difference') || s.includes('vs')) {
      return `Here is the breakdown:<br/>• <strong>$9 Pass Blueprint:</strong> 7-Day $50K Combine Pass Schedule (+$450/day), 09:50 EST Silver Bullet FVG checklist &amp; .CSV Risk Sheet.<br/>• <strong>$39 Trench Starter (Most Popular):</strong> Includes the $9 Blueprint PLUS the working <strong>NinjaTrader 8 C# Auto-Flatten Daily Kill-Switch (TFBDailyKillSwitch.cs)</strong> so you never tilt an account again:
      <a href="/api/create-checkout-session?tier=risk_terminal_39" class="tfb-bot-cta">🔥 GRAB $39 TRENCH STARTER SUITE →</a>
      <a href="/api/create-checkout-session?tier=flash_9" class="tfb-bot-cta-sec">⚡ START WITH $9 PASS BLUEPRINT →</a>`;
    }
    return `To pass any $50K–$150K combine without blowing your trailing buffer, trade <strong>5 MNQ Micros (15pt SL = $150 risk)</strong> during the 09:50–10:10 EST NY Silver Bullet window, and hard-lock your platform after 2 stops.<br/><br/>Pick your execution tier below for instant vault delivery:
    <a href="/api/create-checkout-session?tier=flash_9" class="tfb-bot-cta">⚡ UNLOCK $9 7-DAY PASS BLUEPRINT →</a>
    <a href="/api/create-checkout-session?tier=risk_terminal_39" class="tfb-bot-cta-sec">🔥 DEPLOY $39 NT8 C# RISK SUITE →</a>`;
  }

  function handleUserQuestion(text) {
    if (!text.trim()) return;
    const uDiv = document.createElement('div');
    uDiv.className = 'tfb-msg-user';
    uDiv.textContent = text;
    msgBox.appendChild(uDiv);
    msgBox.scrollTop = msgBox.scrollHeight;

    setTimeout(() => {
      const bDiv = document.createElement('div');
      bDiv.className = 'tfb-msg-bot';
      bDiv.innerHTML = getAiReply(text);
      msgBox.appendChild(bDiv);
      msgBox.scrollTop = msgBox.scrollHeight;
    }, 320);
  }

  document.querySelectorAll('.tfb-chip').forEach(btn => {
    btn.addEventListener('click', () => {
      handleUserQuestion(btn.getAttribute('data-q'));
    });
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const val = input.value;
    input.value = '';
    handleUserQuestion(val);
  });
})();