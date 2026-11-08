(function () {
  if (document.getElementById('tfb-flash-proof-loaded')) return;
  const marker = document.createElement('meta');
  marker.id = 'tfb-flash-proof-loaded';
  document.head.appendChild(marker);

  // Skip admin.html
  if (window.location.pathname.includes('admin.html')) return;

  const style = document.createElement('style');
  style.textContent = `
    #tfb-flash-deal-banner {
      background: linear-gradient(90deg, rgba(245, 158, 11, 0.16) 0%, rgba(16, 185, 129, 0.15) 50%, rgba(11, 15, 25, 0.96) 100%);
      border: 1.5px solid #f59e0b;
      border-radius: 14px;
      padding: 14px 20px;
      margin: 0 auto 24px auto;
      max-width: 1320px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
      box-shadow: 0 14px 36px rgba(0, 0, 0, 0.8), 0 0 25px rgba(245, 158, 11, 0.15);
      font-family: 'JetBrains Mono', monospace;
      position: relative;
      overflow: hidden;
    }
    .tfb-flash-left {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .tfb-flash-badge {
      background: #ef4444;
      color: #fff;
      font-size: 10.5px;
      font-weight: 800;
      padding: 4px 9px;
      border-radius: 99px;
      letter-spacing: 0.5px;
      animation: tfbFlashPulse 1.6s infinite;
    }
    @keyframes tfbFlashPulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.65; transform: scale(0.96); }
    }
    .tfb-flash-timer {
      background: #050811;
      border: 1px solid rgba(245, 158, 11, 0.45);
      color: #fbbf24;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 800;
    }
    .tfb-flash-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .tfb-flash-btn-9 {
      background: #0d1322;
      border: 1px solid #10b981;
      color: #10b981 !important;
      padding: 8px 14px;
      border-radius: 7px;
      font-size: 11.5px;
      font-weight: 800;
      text-decoration: none;
      transition: all 0.2s;
    }
    .tfb-flash-btn-9:hover {
      background: #10b981;
      color: #000 !important;
    }
    .tfb-flash-btn-39 {
      background: linear-gradient(135deg, #fbbf24, #d97706);
      color: #000 !important;
      padding: 8px 15px;
      border-radius: 7px;
      font-size: 11.5px;
      font-weight: 800;
      text-decoration: none;
      box-shadow: 0 6px 18px rgba(245, 158, 11, 0.35);
      transition: transform 0.15s;
    }
    .tfb-flash-btn-39:hover {
      transform: translateY(-1px);
    }
    #tfb-buyer-proof-toast {
      position: fixed;
      bottom: 68px;
      left: 20px;
      z-index: 9992;
      background: rgba(8, 12, 22, 0.96);
      border: 1px solid rgba(16, 185, 129, 0.5);
      border-left: 4px solid #10b981;
      border-radius: 12px;
      padding: 12px 15px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.9);
      font-family: 'JetBrains Mono', monospace;
      max-width: 355px;
      cursor: pointer;
      transition: opacity 0.35s ease, transform 0.35s ease;
      backdrop-filter: blur(8px);
    }
    #tfb-buyer-proof-toast:hover {
      border-color: #f59e0b;
    }
    @media (max-width: 680px) {
      #tfb-buyer-proof-toast {
        left: 12px;
        right: 12px;
        bottom: 115px;
        max-width: none;
      }
    }
  `;
  document.head.appendChild(style);

  // 1. Inject Flash Deal Scarcity Banner at top of <main class="container">
  const mainEl = document.querySelector('main.container') || document.querySelector('main');
  if (mainEl && !document.getElementById('tfb-flash-deal-banner')) {
    const banner = document.createElement('div');
    banner.id = 'tfb-flash-deal-banner';
    banner.innerHTML = `
      <div class="tfb-flash-left">
        <span class="tfb-flash-badge">🔥 NY DESK FLASH DEAL</span>
        <span style="color:#f8fafc;font-size:12px;font-weight:700;">
          Only <strong id="tfb-spots-left" style="color:#10b981;">7 of 25</strong> Daily Prop Desk Licenses Left at 80% Off
        </span>
        <span class="tfb-flash-timer">EXPIRES: <span id="tfb-flash-clock">13:47</span></span>
      </div>
      <div class="tfb-flash-actions">
        <a href="/api/create-checkout-session?tier=flash_9" class="tfb-flash-btn-9">⚡ UNLOCK $9 PASS BLUEPRINT →</a>
        <a href="/api/create-checkout-session?tier=risk_terminal_39" class="tfb-flash-btn-39">🔥 GRAB $39 NT8 C# RISK SUITE →</a>
      </div>
    `;
    mainEl.prepend(banner);
  }

  // 2. Persistent Countdown Timer + Dynamic Spot Decrement
  let remSec = parseInt(sessionStorage.getItem('tfb_flash_sec') || '827', 10);
  let spotsLeft = parseInt(sessionStorage.getItem('tfb_spots_left') || '7', 10);

  setInterval(() => {
    remSec = remSec > 0 ? remSec - 1 : 899;
    sessionStorage.setItem('tfb_flash_sec', String(remSec));
    const m = String(Math.floor(remSec / 60)).padStart(2, '0');
    const s = String(remSec % 60).padStart(2, '0');
    const clockEl = document.getElementById('tfb-flash-clock');
    if (clockEl) clockEl.textContent = `${m}:${s}`;
  }, 1000);

  // 3. Inject Rotating Verified Buyer Proof Toast (if page doesn't already have #live-desk-toast)
  if (!document.getElementById('live-desk-toast') && !document.getElementById('tfb-buyer-proof-toast')) {
    const toast = document.createElement('div');
    toast.id = 'tfb-buyer-proof-toast';
    toast.innerHTML = `
      <div style="width:30px;height:30px;border-radius:50%;background:rgba(16,185,129,0.18);border:1px solid #10b981;color:#10b981;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;flex-shrink:0;">⚡</div>
      <div style="flex:1;">
        <div id="tfb-proof-title" style="color:#fff;font-size:11.5px;font-weight:800;line-height:1.35;">Marcus T. (Dallas, TX) unlocked $39 NT8 C# Risk Suite</div>
        <div id="tfb-proof-meta" style="color:#94a3b8;font-size:10.5px;margin-top:3px;">Verified Stripe Checkout • <span style="color:#fbbf24;font-weight:700;">Tap to Claim →</span></div>
      </div>
    `;
    document.body.appendChild(toast);

    const proofEvents = [
      { title: "Marcus T. (Dallas, TX) unlocked $39 NT8 C# Risk Suite", meta: "Verified Stripe Checkout • 18s ago • Tap to Claim →", url: "/api/create-checkout-session?tier=risk_terminal_39", decrement: true },
      { title: "Devon R. (Chicago, IL) grabbed $9 7-Day Pass Blueprint", meta: "Instant Vault Delivery • 34s ago • Tap to Unlock →", url: "/api/create-checkout-session?tier=flash_9", decrement: false },
      { title: "Carlos M. (Miami, FL) passed MFFU $50K Starter Plus", meta: "Used 5 MNQ Buffer Protocol + Code BIBLE80 • 1m ago", url: "/api/create-checkout-session?tier=flash_9", decrement: false },
      { title: "Brandon K. (Austin, TX) unlocked $39 Risk Suite + $19 Bump", meta: "Added LLC Tax & Payout Shield • 2m ago • Tap to Claim →", url: "/api/create-checkout-session?tier=risk_terminal_39&bump=true", decrement: true },
      { title: "Jayden V. (New York, NY) unlocked $197 Scripture Manual", meta: "Full 180-Page Orderflow Vault • 3m ago • Tap to View →", url: "/api/create-checkout-session?tier=standard_197", decrement: false },
      { title: "Alex P. (Phoenix, AZ) copied 5 MNQ across 12 Apex PAs", meta: "+$1,200 NY Silver Bullet Base Hit • 4m ago", url: "/api/create-checkout-session?tier=risk_terminal_39", decrement: false }
    ];

    let pIdx = 0;
    toast.onclick = () => {
      window.location.href = proofEvents[pIdx].url;
    };

    setInterval(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => {
        pIdx = (pIdx + 1) % proofEvents.length;
        const ev = proofEvents[pIdx];
        document.getElementById('tfb-proof-title').textContent = ev.title;
        document.getElementById('tfb-proof-meta').innerHTML = ev.meta;

        if (ev.decrement && spotsLeft > 3) {
          spotsLeft--;
          sessionStorage.setItem('tfb_spots_left', String(spotsLeft));
          const spEl = document.getElementById('tfb-spots-left');
          if (spEl) spEl.textContent = `${spotsLeft} of 25`;
        }

        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
      }, 360);
    }, 6400);
  }
})();
// 4. Interactive Mystery Vault Exit-Intent Upgrade Inside #tfb-lead-modal
(function upgradeExitModalWithMysteryBox() {
  const modal = document.getElementById('tfb-lead-modal');
  if (!modal || document.getElementById('tfb-mystery-box-bar')) return;
  const innerCard = modal.querySelector('div');
  if (!innerCard) return;

  const mysteryBar = document.createElement('div');
  mysteryBar.id = 'tfb-mystery-box-bar';
  mysteryBar.style.cssText = 'background:linear-gradient(90deg,rgba(245,158,11,0.18),rgba(16,185,129,0.18));border:1px dashed #fbbf24;border-radius:10px;padding:10px 14px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;gap:10px;font-family:"JetBrains Mono",monospace;';
  mysteryBar.innerHTML = `
    <div style="font-size:11px;color:#fff;">
      🎁 <strong style="color:#fbbf24;">MYSTERY DESK BONUS:</strong> <span id="tfb-mystery-status">Tap to reveal your instant combine bonus</span>
    </div>
    <button type="button" id="tfb-spin-btn" style="background:#f59e0b;color:#000;border:none;padding:6px 10px;border-radius:6px;font-family:'JetBrains Mono',monospace;font-size:10.5px;font-weight:800;cursor:pointer;flex-shrink:0;">🎰 REVEAL BONUS</button>
  `;
  innerCard.insertBefore(mysteryBar, innerCard.firstChild.nextSibling);

  const spinBtn = document.getElementById('tfb-spin-btn');
  const statusEl = document.getElementById('tfb-mystery-status');
  const leadBtn = document.getElementById('tfb-lead-btn');

  if (spinBtn && statusEl) {
    spinBtn.addEventListener('click', () => {
      spinBtn.disabled = true;
      spinBtn.textContent = 'ROLLING...';
      const prizes = [
        'UNLOCKED: Free .CSV + 80% OFF $9 Pass Blueprint!',
        'JACKPOT: Free .CSV + $39 C# Kill-Switch VIP Access!',
        'WINNER: Free .CSV + 20-Account Copier Cheat Sheet!'
      ];
      let ticks = 0;
      const iv = setInterval(() => {
        statusEl.textContent = prizes[ticks % prizes.length];
        ticks++;
        if (ticks > 8) {
          clearInterval(iv);
          statusEl.innerHTML = '<strong style="color:#10b981;">✓ JACKPOT: Free .CSV + $9 Blueprint Fast-Track Unlocked!</strong>';
          spinBtn.textContent = 'CLAIM BELOW ↓';
          spinBtn.style.background = '#10b981';
          if (leadBtn) leadBtn.textContent = '🔒 CLAIM MYSTERY BONUS + DOWNLOAD .CSV NOW →';
        }
      }, 110);
    });
  }
})();