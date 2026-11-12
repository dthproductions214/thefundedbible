// THE FUNDED BIBLE — Master Stripe Checkout Router
const TFB_STRIPE = {
  flash9: "https://buy.stripe.com/00waEZgpXgIYgjC7BU9k400",     // $9 Flash Bot / Entry Indicator
  bump19: "https://buy.stripe.com/6oUaEZehPakA8Ra1dw9k401",     // $19 Master Bundle / Fast-Track Add-on
  starter39: "https://buy.stripe.com/3cI4gz0Ep2wE3XxaZB3gk05",  // $39 NT8 C# Risk Suite / Starter Sheet
  starterBundle: "https://buy.stripe.com/bJedR9cn7c7egKjaZB3gk06", // $39 + $19 Order Bump Bundle ($58)
  standard197: "https://buy.stripe.com/bJefZh2Mx3AI79J9Vx3gk02", // $197 Standard Scripture (Lifetime)
  scale397: "https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03",   // $397 Scale Mastermind / Whale Suite
  support: "https://buy.stripe.com/bJe8wP5YJgnu51B1p13gk00"     // Tip / Desk Support
};

function syncTFBButtons() {
  const bumpChecked = document.getElementById("tfb-bump")?.checked;

  // 1. Wire every button tagged with data-tier="..."
  document.querySelectorAll("[data-tier]").forEach((el) => {
    const tier = el.getAttribute("data-tier");
    const targetUrl = (tier === "starter39" && bumpChecked)
      ? TFB_STRIPE.starterBundle
      : TFB_STRIPE[tier];

    if (targetUrl) {
      el.setAttribute("href", targetUrl);
      el.removeAttribute("target"); // Prevents iOS Safari popup blocking
    }
  });

  // 2. Catch any dead href="#" buy buttons left over on subpages
  document.querySelectorAll('a[href="#"], a[href=""]').forEach((el) => {
    const txt = el.textContent.toLowerCase();
    if (txt.includes("397") || txt.includes("whale") || txt.includes("scale")) {
      el.href = TFB_STRIPE.scale397;
    } else if (txt.includes("197") || txt.includes("standard") || txt.includes("scripture")) {
      el.href = TFB_STRIPE.standard197;
    } else if (txt.includes("39") || txt.includes("risk suite") || txt.includes("claim")) {
      el.href = TFB_STRIPE.starter39;
    } else if (txt.includes("$19") || txt.includes("bundle")) {
      el.href = TFB_STRIPE.bump19;
    } else if (txt.includes("$9") || txt.includes("flash")) {
      el.href = TFB_STRIPE.flash9;
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  syncTFBButtons();
  document.getElementById("tfb-bump")?.addEventListener("change", syncTFBButtons);
});
