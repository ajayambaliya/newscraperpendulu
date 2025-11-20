/**
 * Beautiful PDF Generator using Playwright
 * Perfect for Gujarati typography with browser rendering
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function generatePDF(htmlPath, outputPath) {
    console.log('🚀 Starting PDF generation with Playwright...');
    
    try {
        // Read HTML file
        const htmlContent = fs.readFileSync(htmlPath, 'utf-8');
        console.log('✓ HTML file loaded');
        
        // Launch browser
        const browser = await chromium.launch({
            headless: true
        });
        console.log('✓ Browser launched');
        
        // Create page
        const page = await browser.newPage();
        
        // Set content
        await page.setContent(htmlContent, {
            waitUntil: 'networkidle'
        });
        console.log('✓ HTML content loaded');
        
        // Wait for fonts to load
        await page.evaluate(() => document.fonts.ready);
        console.log('✓ Fonts loaded');
        
        // Generate PDF
        await page.pdf({
            path: outputPath,
            format: 'A4',
            printBackground: true,
            margin: {
                top: 0,
                right: 0,
                bottom: 0,
                left: 0
            },
            preferCSSPageSize: false
        });
        console.log('✓ PDF generated');
        
        await browser.close();
        console.log('✓ Browser closed');
        
        // Get file size
        const stats = fs.statSync(outputPath);
        const fileSizeKB = (stats.size / 1024).toFixed(2);
        
        console.log(`\n✅ SUCCESS!`);
        console.log(`📄 PDF: ${outputPath}`);
        console.log(`📊 Size: ${fileSizeKB} KB`);
        
        return outputPath;
        
    } catch (error) {
        console.error('❌ Error generating PDF:', error);
        throw error;
    }
}

// Main execution
const htmlPath = process.argv[2] || path.join(__dirname, 'output', 'quiz.html');
const outputPath = process.argv[3] || path.join(__dirname, 'pdfs', `quiz_${Date.now()}.pdf`);

// Ensure output directory exists
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

generatePDF(htmlPath, outputPath)
    .then(() => {
        console.log('\n🎉 PDF generation complete!');
        process.exit(0);
    })
    .catch((error) => {
        console.error('\n💥 PDF generation failed:', error.message);
        process.exit(1);
    });
