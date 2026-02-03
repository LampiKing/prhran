
const https = require('https');

const expectedScript = "entry-eb4f29c57a3656ef267d0737d10df6e7.js";
const urls = [
    "https://www.prhran.com",
    "https://6981ebefb2302c7b88f29e99--prhrannn.netlify.app"
];

console.log(`EXPECTED SCRIPT: ${expectedScript}`);

urls.forEach(url => {
    https.get(url, (res) => {
        let data = '';

        res.on('data', (chunk) => {
            data += chunk;
        });

        res.on('end', () => {
            console.log(`\n--- Checking ${url} ---`);

            const scriptMatch = data.match(/src="\/_expo\/static\/js\/web\/(entry-[a-z0-9]+\.js)"/i);
            if (scriptMatch) {
                const foundScript = scriptMatch[1];
                console.log(`Found Script: ${foundScript}`);

                if (foundScript === expectedScript) {
                    console.log("✅ MATCH! Final Polish is LIVE.");
                } else {
                    console.log(`❌ MISMATCH! Expected ${expectedScript}, found ${foundScript}`);
                }
            } else {
                console.log("❌ Script tag not found in HTML");
            }
        });

    }).on("error", (err) => {
        console.log(`Error checking ${url}: ` + err.message);
    });
});
