/**
 * Sago Pitch Deck Analyzer - Gmail Monitor
 * Monitors Gmail for PDFs and sends analysis results
 */

// Configuration
const BACKEND_URL = 'https://nine-rabbits-grin.loca.lt'; // UPDATE THIS after deployment!
const LABEL_NAME = 'Sago/Analyzed';

function monitorGmailForPitchDecks() {
  Logger.log('🔍 Checking for new pitch deck emails...');

  const processedLabel = getOrCreateLabel(LABEL_NAME);

  // Search for unprocessed emails with PDF attachments
  const threads = GmailApp.search(
    'has:attachment filename:pdf -label:' + LABEL_NAME + ' newer_than:1h',
    0,
    10
  );

  Logger.log('Found ' + threads.length + ' unprocessed emails with PDFs');

  threads.forEach(function(thread) {
    try {
      processThread(thread, processedLabel);
    } catch (error) {
      Logger.log('❌ Error: ' + error);
    }
  });
}

function processThread(thread, processedLabel) {
  const messages = thread.getMessages();
  const latestMessage = messages[messages.length - 1];
  const sender = latestMessage.getFrom();
  const subject = latestMessage.getSubject();
  const bodyPlain = latestMessage.getPlainBody().toLowerCase();

  Logger.log('📧 Processing: ' + subject);

  // Check if email contains trigger phrase
  const triggerPhrases = [
    'hey sago',
    'sago analyze',
    'analyze this pitch deck',
    'analyze pitch deck',
    'sago please analyze'
  ];

  let hasTrigger = false;
  for (let i = 0; i < triggerPhrases.length; i++) {
    if (bodyPlain.indexOf(triggerPhrases[i]) !== -1) {
      hasTrigger = true;
      break;
    }
  }

  if (!hasTrigger) {
    Logger.log('⏭️ Skipped: No trigger phrase found (need "hey sago", "sago analyze", etc.)');
    return;
  }

  Logger.log('✅ Trigger phrase detected!');

  // Find PDF attachments
  const attachments = latestMessage.getAttachments();
  let pdfAttachment = null;

  for (var i = 0; i < attachments.length; i++) {
    if (attachments[i].getContentType() === 'application/pdf') {
      pdfAttachment = attachments[i];
      break;
    }
  }

  if (!pdfAttachment) {
    Logger.log('No PDF found');
    return;
  }

  Logger.log('📄 Found PDF: ' + pdfAttachment.getName());

  // Analyze pitch deck
  const result = analyzePitchDeck(pdfAttachment);

  if (result) {
    sendAnalysisReply(thread, result);
    thread.addLabel(processedLabel);
    Logger.log('✅ Complete');
  }
}

function analyzePitchDeck(pdfAttachment) {
  try {
    // Step 1: Upload PDF
    const formData = {
      file: pdfAttachment.copyBlob()
    };

    const uploadOptions = {
      method: 'post',
      payload: formData,
      muteHttpExceptions: true
    };

    const uploadResponse = UrlFetchApp.fetch(BACKEND_URL + '/api/pitch-deck/upload', uploadOptions);
    const uploadData = JSON.parse(uploadResponse.getContentText());
    const fileId = uploadData.file_id;

    Logger.log('✅ Uploaded: ' + fileId);

    // Step 2: Analyze
    const analyzeUrl = BACKEND_URL + '/api/pitch-deck/analyze-with-agents/' + fileId;
    const analyzeResponse = UrlFetchApp.fetch(analyzeUrl, {
      method: 'post',
      muteHttpExceptions: true
    });

    if (analyzeResponse.getResponseCode() === 200) {
      return JSON.parse(analyzeResponse.getContentText());
    } else {
      Logger.log('❌ Analysis failed');
      return null;
    }

  } catch (error) {
    Logger.log('❌ API Error: ' + error);
    return null;
  }
}

function sendAnalysisReply(thread, result) {
  const companyName = result.company_name || 'Unknown';
  const summary = result.summary || {};
  const verifications = result.verification_results || [];
  const questions = result.questions || [];

  // Build verification results HTML
  let verificationsHtml = '';
  for (let i = 0; i < verifications.length; i++) {
    verificationsHtml += `
      <div style="margin-bottom: 20px; padding: 15px; background: #f9fafb; border-left: 4px solid #4f46e5; border-radius: 4px;">
        <h3 style="margin-top: 0; color: #1f2937; font-size: 16px;">
          ${i + 1}. ${verifications[i].claim}
        </h3>
        <div style="color: #4b5563; font-size: 14px; white-space: pre-wrap;">
          ${verifications[i].verification_result}
        </div>
      </div>
    `;
  }

  // Build questions HTML
  let questionsHtml = '';
  for (let i = 0; i < questions.length; i++) {
    questionsHtml += `
      <li style="margin-bottom: 10px; color: #374151; font-size: 14px;">
        ${questions[i]}
      </li>
    `;
  }

  // Complete HTML email
  const htmlBody = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">

      <!-- Header -->
      <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px 20px; border-radius: 8px; margin-bottom: 30px; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 28px;">🚀 Sago Analysis</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">
          Pitch Deck Verification Report
        </p>
      </div>

      <!-- Summary Cards -->
      <table style="width: 100%; margin-bottom: 30px;" cellpadding="0" cellspacing="0">
        <tr>
          <td style="width: 33%; padding: 5px;">
            <div style="background: #dbeafe; padding: 15px; border-radius: 8px; text-align: center;">
              <div style="font-size: 24px; font-weight: bold; color: #1e40af;">
                ${summary.total_claims || 0}
              </div>
              <div style="font-size: 12px; color: #1e3a8a; margin-top: 5px;">
                Claims Extracted
              </div>
            </div>
          </td>
          <td style="width: 33%; padding: 5px;">
            <div style="background: #d1fae5; padding: 15px; border-radius: 8px; text-align: center;">
              <div style="font-size: 24px; font-weight: bold; color: #047857;">
                ${summary.verified_claims || 0}
              </div>
              <div style="font-size: 12px; color: #065f46; margin-top: 5px;">
                Verified Claims
              </div>
            </div>
          </td>
          <td style="width: 33%; padding: 5px;">
            <div style="background: #e9d5ff; padding: 15px; border-radius: 8px; text-align: center;">
              <div style="font-size: 24px; font-weight: bold; color: #7c3aed;">
                ${summary.questions_generated || 0}
              </div>
              <div style="font-size: 12px; color: #6b21a8; margin-top: 5px;">
                Questions
              </div>
            </div>
          </td>
        </tr>
      </table>

      <!-- Company Name -->
      <h2 style="color: #1f2937; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px;">
        Company: ${companyName}
      </h2>

      <!-- Verification Results -->
      <div style="margin-bottom: 30px;">
        <h2 style="color: #1f2937; margin-bottom: 20px;">
          ✓ Verification Results
        </h2>
        ${verificationsHtml}
      </div>

      <!-- Questions -->
      <div style="margin-bottom: 30px;">
        <h2 style="color: #1f2937; margin-bottom: 20px;">
          ❓ Questions for the Founder
        </h2>
        <ol style="padding-left: 20px;">
          ${questionsHtml}
        </ol>
      </div>

      <!-- Footer -->
      <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280; font-size: 12px;">
        <p>🤖 Generated by Sago - AI-Powered Pitch Deck Analyzer</p>
        <p style="margin-top: 10px;">
          <a href="https://github.com/varunmehta14/sago" style="color: #4f46e5; text-decoration: none;">
            View on GitHub
          </a>
        </p>
      </div>

    </body>
    </html>
  `;

  thread.reply('', {
    htmlBody: htmlBody,
    name: 'Sago Analysis'
  });
}

function getOrCreateLabel(labelName) {
  let label = GmailApp.getUserLabelByName(labelName);
  if (!label) {
    label = GmailApp.createLabel(labelName);
  }
  return label;
}
