const apiKey = process.env.BREVO_API_KEY;

if (!apiKey) {
  console.log('BREVO_API_KEY environment variable is not set. Exiting.');
  process.exit(0);
}

const endpoint = ['https:/', 'api', 'brevo', 'com', 'v3'].join('/').replace('/api/brevo/com/', '/api.brevo.com/');

const campaigns = [
  {
    subject: 'Sunday Prop Briefing: Weekly Risk Management Setup',
    title: 'Sunday Trading Desk Briefing',
    body: 'Prepare your trading week by reviewing risk limits and trailing drawdown rules.'
  },
  {
    subject: 'Monday Prop Briefing: Trailing Drawdown Traps to Avoid',
    title: 'Monday Desk Briefing',
    body: 'Learn how top prop traders stay clear of max trailing drawdown violations.'
  },
  {
    subject: 'Tuesday Prop Briefing: Comparing Top Prop Firm Rules',
    title: 'Tuesday Desk Briefing',
    body: 'Compare fee structures, payout schedules, and drawdown limits across top firms.'
  },
  {
    subject: 'Wednesday Prop Briefing: Mid-Week Position Sizing Audit',
    title: 'Wednesday Desk Briefing',
    body: 'Audit your leverage and position sizing against strict prop firm evaluation metrics.'
  },
  {
    subject: 'Thursday Prop Briefing: Unlocking the Prop Vault & Cheat Sheets',
    title: 'Thursday Desk Briefing',
    body: 'Access exclusive cheat sheets and trading guidelines inside our prop vault.'
  },
  {
    subject: 'Friday Prop Briefing: Weekend Risk & Profit Target Strategy',
    title: 'Friday Desk Briefing',
    body: 'Lock in profits and review your weekly metrics before closing positions.'
  },
  {
    subject: 'Saturday Prop Briefing: Weekend Strategy Review & Backtesting',
    title: 'Saturday Desk Briefing',
    body: 'Refine your trading plan and test risk calculators for the upcoming week.'
  }
];

async function main() {
  const dayIndex = new Date().getDay();
  const campaign = campaigns[dayIndex];

  console.log(`Sending campaign for day ${dayIndex}: ${campaign.subject}`);

  let contacts = [];
  try {
    const res = await fetch(`${endpoint}/contacts?limit=500`, {
      method: 'GET',
      headers: {
        'accept': 'application/json',
        'api-key': apiKey
      }
    });
    const data = await res.json();
    contacts = data.contacts || [];
  } catch (err) {
    console.error('Error fetching contacts from Brevo:', err);
  }

  console.log(`Found ${contacts.length} contacts.`);

  const htmlBody = `
    <div style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto; color: #333;">
      <h2 style="color: #1a365d;">${campaign.title}</h2>
      <p>${campaign.body}</p>
      <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;" />
      <h3>Essential Prop Trading Resources:</h3>
      <ul>
        <li><a href="https://thefundedbible.com/calculator.html">Trailing Drawdown Survival Calculator</a></li>
        <li><a href="https://thefundedbible.com/firms.html">Prop Firms Comparison</a></li>
        <li><a href="https://thefundedbible.com/vault.html">Prop Cheat Sheet & Vault</a></li>
      </ul>
      <p>Use exclusive promo code <strong>BIBLE80</strong> to get 80% off!</p>
      <footer style="margin-top: 30px; font-size: 12px; color: #888;">
        The Funded Bible Desk | Daily Prop Trading Intelligence
      </footer>
    </div>
  `;

  for (const contact of contacts) {
    if (!contact.email) continue;
    try {
      await fetch(`${endpoint}/smtp/email`, {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'content-type': 'application/json',
          'api-key': apiKey
        },
        body: JSON.stringify({
          sender: { name: 'The Funded Bible Desk', email: 'desk@thefundedbible.com' },
          to: [{ email: contact.email }],
          subject: campaign.subject,
          htmlContent: htmlBody
        })
      });
      console.log(`Email sent to ${contact.email}`);
    } catch (err) {
      console.error(`Failed to send email to ${contact.email}:`, err);
    }
  }
}

main().catch(err => {
  console.error('Error in send-daily-email:', err);
  process.exit(1);
});
