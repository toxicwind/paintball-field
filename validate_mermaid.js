
const { chromium } = require('playwright');
const fs = require('fs');

const blocks = JSON.parse(process.argv[2]);

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    // Load mermaid.js from CDN
    await page.goto('about:blank');
    await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js' });

    let results = [];

    for (let i = 0; i < blocks.length; i++) {
        const block = blocks[i];
        try {
            const result = await page.evaluate(async (diagram) => {
                try {
                    const id = 'mermaid-' + Math.random().toString(36).substr(2, 9);
                    const { svg } = await mermaid.render(id, diagram);
                    return { ok: true, error: null };
                } catch (e) {
                    return { ok: false, error: e.message || e.str || String(e) };
                }
            }, block);
            results.push({ block: i + 1, ok: result.ok, error: result.error });
            console.log(`Block ${i+1}: ${result.ok ? 'OK' : 'FAIL - ' + result.error}`);
        } catch (e) {
            results.push({ block: i + 1, ok: false, error: String(e) });
            console.log(`Block ${i+1}: FAIL - ${e}`);
        }
    }

    await browser.close();

    // Write results
    fs.writeFileSync('/mnt/agents/output/paintball-field/mermaid_lint.json', JSON.stringify(results, null, 2));

    const allOk = results.every(r => r.ok);
    process.exit(allOk ? 0 : 1);
})();
