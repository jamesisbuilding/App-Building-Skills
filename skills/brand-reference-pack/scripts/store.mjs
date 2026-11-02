// App Store listing + customer reviews for the reference pack — the brand's official positioning and raw
// voice-of-customer material (not a VOC synthesis; that's upstream).
//   node .claude/skills/brand-reference-pack/scripts/store.mjs <app-store-id> <out-dir> [country=gb]
// Writes listing.json, screenshots/NN.png, reviews.json and reviews.md. Uses Apple's public lookup API and reviews RSS.
// shortcut: App Store only — Google Play has no public API; capture its listing in the browser if it matters.
import fs from 'node:fs';

const [id, out, country = 'gb'] = process.argv.slice(2);
if (!id || !out) { console.error('usage: node store.mjs <app-store-id> <out-dir> [country]'); process.exit(2); }
fs.mkdirSync(`${out}/screenshots`, { recursive: true });
const get = async url => { const r = await fetch(url); if (!r.ok) throw new Error(`${r.status} ${url}`); return r; };

const app = (await (await get(`https://itunes.apple.com/lookup?id=${id}&country=${country}`)).json()).results?.[0];
if (!app) throw new Error(`no App Store app ${id} in ${country}`);
const keep = ['trackName', 'sellerName', 'primaryGenreName', 'genres', 'description', 'releaseNotes', 'version',
  'averageUserRating', 'userRatingCount', 'contentAdvisoryRating', 'price', 'formattedPrice', 'trackViewUrl', 'artworkUrl512'];
fs.writeFileSync(`${out}/listing.json`, JSON.stringify(Object.fromEntries(keep.map(k => [k, app[k]])), null, 1));
for (const [i, url] of (app.screenshotUrls ?? []).entries())
  fs.writeFileSync(`${out}/screenshots/${String(i + 1).padStart(2, '0')}.png`, Buffer.from(await (await get(url)).arrayBuffer()));

// Reviews RSS: up to 10 pages × 50, most recent first; stops at the first empty page.
const reviews = [];
for (let page = 1; page <= 10; page++) {
  const feed = (await (await get(`https://itunes.apple.com/${country}/rss/customerreviews/page=${page}/id=${id}/sortby=mostrecent/json`)).json()).feed;
  const entries = [].concat(feed?.entry ?? []).filter(e => e['im:rating']);
  if (!entries.length) break;
  reviews.push(...entries.map(e => ({ date: e.updated?.label?.slice(0, 10), rating: +e['im:rating'].label, title: e.title?.label,
    text: e.content?.label, version: e['im:version']?.label })));
}
fs.writeFileSync(`${out}/reviews.json`, JSON.stringify(reviews, null, 1));
fs.writeFileSync(`${out}/reviews.md`, `# ${app.trackName} — App Store reviews (${country}, ${reviews.length}, captured ${new Date().toISOString().slice(0, 10)})\n\n`
  + reviews.map(r => `- **${'★'.repeat(r.rating)}${'☆'.repeat(5 - r.rating)} ${r.title}** (${r.date}, v${r.version})  \n  ${r.text?.replace(/\s+/g, ' ')}`).join('\n') + '\n');
console.log(`${app.trackName}: ${app.userRatingCount ?? 0} ratings (avg ${app.averageUserRating ?? '–'}), ${app.screenshotUrls?.length ?? 0} screenshots, ${reviews.length} reviews → ${out}`);
