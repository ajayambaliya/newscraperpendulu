/**
 * Modern PDF Generator using Puppeteer
 * Converts HTML to beautiful PDF with perfect Gujarati rendering
 */

import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function generatePDF(htmlPath, outputPath) {
    console.log('🚀 Starting PDF generation with Puppeteer...');
    
    try {
        // Read HTML file
        const html = fs.readFileSync(htmlPath, 'utf-8');
        console.log('✓ HTML file loaded');
        
        // Launch browser with optimized settings
        const browser = await puppeteer.launch({
            headless: 'new',
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--disable-extensions',
                '--disable-background-networking',
                '--disable-sync',
                '--metrics-recording-only',
                '--mute-audio',
                '--no-first-run',
                '--disable-default-apps',
                '--disable-breakpad',
                '--disable-component-extensions-with-background-pages'
            ]
        });
        console.log('✓ Browser launched');
        
        // Create new page with optimal viewport for A4
        const page = await browser.newPage();
        
        // Set viewport to A4 dimensions at 96 DPI (standard screen DPI)
        // A4 at 96 DPI: 794 x 1123 pixels
        await page.setViewport({
            width: 794,
            height: 1123,
            deviceScaleFactor: 1
        });
        
        // Set content with optimized timeout
        await page.setContent(html, {
            waitUntil: 'domcontentloaded', // Faster than networkidle0
            timeout: 15000 // Reduced from 30s to 15s
        });
        console.log('✓ HTML content loaded in browser');
        
        // Wait for fonts to load (critical for Gujarati rendering)
        await page.evaluateHandle('document.fonts.ready');
        console.log('✓ Fonts loaded');
        
        // Generate PDF with optimized settings
        await page.pdf({
            path: outputPath,
            format: 'A4',
            printBackground: true,
            margin: {
                top: '15mm',
                right: '15mm',
                bottom: '15mm',
                left: '15mm'
            },
            preferCSSPageSize: true,
            // Optimize PDF compression
            tagged: false, // Disable PDF tagging for smaller file size
            displayHeaderFooter: false,
            // Use screen media type for better rendering
            mediaType: 'screen'
        });
        console.log('✓ PDF generated successfully');
        
        await browser.close();
        console.log('✓ Browser closed');
        
        // Get file size
        const stats = fs.statSync(outputPath);
        const fileSizeInBytes = stats.size;
        const fileSizeInKB = (fileSizeInBytes / 1024).toFixed(2);
        
        console.log(`\n✅ SUCCESS!`);
        console.log(`📄 PDF: ${outputPath}`);
        console.log(`📊 Size: ${fileSizeInKB} KB`);
        
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
