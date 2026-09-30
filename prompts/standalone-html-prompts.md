# Prompts for Standalone, Eye-Catching HTML Websites

Use these prompts when asking an AI to create HTML pages that still look polished when opened as individual files.

## 1. Master prompt: complete standalone website

```text
Create a complete, production-quality static website made of standalone HTML files.

IMPORTANT STANDALONE REQUIREMENT:
- Every HTML file must work when opened directly by itself with file:// in a browser.
- Do not rely on /styles.css, /effects.js, /assets/*, server-side includes, build tools, npm, or a framework.
- Put all CSS inside a <style> block in each HTML file.
- Put all JavaScript inside a <script> block in each HTML file.
- Do not use root-relative paths such as /styles.css or /effects.js.
- Avoid local asset dependencies. Use CSS gradients, inline SVG, CSS shapes, and text symbols for visuals.
- External fonts and external payment widgets may be used only when clearly optional; the page must still look excellent if they fail to load.

VISUAL DIRECTION:
- Make the pages feel like a premium creative-tech product, not a plain document.
- Use a bold, original layout with a strong visual identity.
- Use a full-color animated background with gradients, glow effects, grain/noise, grid lines, floating shapes, or orbital elements.
- Use large expressive typography, high contrast, visual rhythm, and deliberate spacing.
- Use CSS animations for the background, hero visuals, floating elements, card hover states, reveal transitions, and decorative motion.
- Respect prefers-reduced-motion and provide a reduced-motion fallback.
- Use at least three accent colors and make the color system feel intentional.
- Add a light/dark theme toggle or another meaningful theme switch using localStorage.

PAGE REQUIREMENTS:
- Include a strong hero section with a memorable headline, short supporting copy, and a primary CTA.
- Include at least three visually distinct content sections.
- Include cards, panels, badges, stats, or a dashboard-style visual instead of only paragraphs.
- Include a visible support tab or support section on every page.
- Include responsive behavior for desktop, tablet, and mobile widths.
- Include hover and focus states for buttons and links.
- Make keyboard navigation and color contrast usable.
- Add a footer with navigation and support links.

CONTENT:
- Use the provided product or project information accurately.
- Do not invent technical claims, pricing, security guarantees, or integrations that were not provided.
- Keep copy concise, specific, and promotional without becoming vague marketing filler.

DELIVERABLE:
- Return each HTML file in full.
- Do not return partial snippets.
- Include all CSS and JavaScript inline inside each HTML file.
- After writing the files, open each page in a browser at desktop and mobile sizes.
- Show screenshots of the rendered pages.
- Check that the pages still look complete when each HTML file is opened alone.
```

## 2. Prompt for a single standalone `index.html`

```text
Create a single self-contained index.html promotion landing page.

The page must be completely standalone:
- It must work when I double-click index.html or open it with file://.
- Inline every style in <style> and every behavior in <script>.
- Do not reference /styles.css, /effects.js, local images, components, JSON files, or server routes.
- Do not use a build step or framework.
- If an external font fails, keep the design visually strong with system fallbacks.

Make it eye-catching and premium:
- Create an original layout, not a generic centered hero.
- Use a full-screen animated background with layered gradients, glow, noise, grid lines, or floating shapes.
- Add a large editorial-style hero headline.
- Add a visual product mockup or dashboard built with HTML/CSS/SVG.
- Add an animated ticker or marquee strip.
- Add at least three sections below the hero.
- Add a visible fixed support tab and a full support section.
- Add a theme toggle.
- Add hover states, scroll reveal animations, and a reduced-motion fallback.
- Make it responsive at 375px, 768px, and desktop widths.

Use this product information:
[PASTE PRODUCT DESCRIPTION HERE]

Use this color direction:
[PASTE COLOR / BRAND DIRECTION HERE]

Before finishing:
1. Open index.html directly as a standalone file.
2. Verify the hero text, cards, background, buttons, and animations all appear.
3. Capture and show a desktop screenshot and a mobile screenshot.
4. Return the complete index.html file.
```

## 3. Prompt for multiple HTML pages with unique themes

```text
Create these standalone HTML pages:
- index.html
- support.html
- about.html
- privacy.html
- terms.html
- accessibility.html
- 404.html

Every page must be independently openable with file://.
Each page must contain its own inline <style> and inline <script>.
Do not assume any shared CSS or JavaScript file exists.

Each page needs a different visual theme while staying within the same brand system:
- index.html: dark graphite, neon lime, electric blue, animated dashboard visual
- support.html: purple/pink grid background, colorful support cards, animated glow
- about.html: warm orange/coral editorial theme with layered shapes
- privacy.html: deep green theme with soft pulse rings
- terms.html: amber/yellow theme with sparkle and paper-like texture
- accessibility.html: blue theme with orbital rings and calm motion
- 404.html: coral/red signal-lost theme with playful motion

Every page must include:
- Animated background
- Large expressive heading
- At least one visual card or decorative CSS/SVG composition
- Page-specific animation
- Theme toggle
- Support tab linking to support.html
- Responsive mobile layout
- Keyboard-visible focus states
- prefers-reduced-motion fallback
- Footer navigation

Do not make the secondary pages plain text cards. They should feel designed and intentional, not like default legal documents.

After creating them:
- Open every page individually.
- Verify each one renders correctly without any other local file.
- Capture screenshots of all pages or at least the home, support, and one secondary page.
- Report any external resources that require internet access.
```

## 4. Prompt for adding a support page

```text
Add a standalone support.html page that feels like a premium campaign landing page, not a payment form.

STANDALONE RULE:
- Inline all CSS and JavaScript.
- The page must work when opened alone with file://.
- External payment or newsletter providers may be embedded, but the surrounding layout must remain complete if they fail to load.

DESIGN:
- Use a distinct animated background from the main landing page.
- Use a bold headline such as “Keep the signal alive.”
- Add animated decorative geometry, glow, grain, and grid elements.
- Create three large support cards with distinct accent colors.
- Include monthly support, one-time support, community sharing, and newsletter signup options.
- Add a fixed support tab, a sticky or prominent CTA, and a complete footer.
- Include a theme toggle and reduced-motion support.

INTEGRATIONS:
Use only the exact provider URLs, IDs, and public keys supplied below. Do not invent credentials. Do not auto-submit anything. Payment actions must happen only after the visitor intentionally clicks a provider button.

Provider information:
[PASTE SUPPORT PROVIDER SNIPPETS HERE]

After creating the page, render it in a browser and show a screenshot.
```

## 5. Prompt for converting an existing linked page into a standalone HTML

```text
Convert the existing page into a truly standalone HTML file.

Current file:
[PASTE OR ATTACH HTML HERE]

Current CSS:
[PASTE OR ATTACH CSS HERE]

Current JavaScript:
[PASTE OR ATTACH JAVASCRIPT HERE]

Requirements:
- Inline all relevant CSS into a <style> element inside the HTML.
- Inline all relevant JavaScript into a <script> element inside the HTML.
- Remove dependencies on /styles.css, /effects.js, /assets, components, JSON, and server-side includes.
- Preserve the existing content and functionality.
- Keep the page visually rich: animated background, colors, transitions, cards, and responsive layout.
- If the current page has reveal animations, initialize them after DOMContentLoaded.
- Do not use defer as a substitute for DOMContentLoaded on inline scripts.
- Ensure the page still works when opened by double-clicking it.

Verification checklist:
- No missing local CSS or JS files.
- No blank hero caused by opacity: 0 elements.
- All reveal elements become visible on first load.
- Buttons and links still work.
- Theme toggle works.
- Reduced-motion mode works.
- Test desktop and mobile rendering.
- Show a screenshot after the conversion.
```

## 6. Prompt for screenshot-based quality control

```text
Do not stop after writing the HTML source.

Render the actual page in a browser and inspect it visually.
Capture:
1. Desktop homepage screenshot at approximately 1280×720.
2. Mobile homepage screenshot at approximately 375×812.
3. Support page screenshot.
4. One secondary page screenshot.

Look specifically for:
- Plain white or black default backgrounds
- Missing hero content
- Invisible text caused by opacity or reveal scripts
- Broken or missing cards
- Buttons that blend into the background
- Overflow on mobile
- Support tab not visible
- Different pages accidentally sharing the exact same theme
- Local-file failures caused by absolute paths

Fix any issue you find before delivering the final files.
Return the screenshots and the final standalone HTML files.
```

## 7. Short version for quick requests

```text
Build this as a truly standalone, eye-catching HTML file.

Inline all CSS and JavaScript directly inside the HTML. It must work when opened by double-clicking the file with file://. Do not reference /styles.css, /effects.js, local assets, JSON, components, or server routes.

Make it premium and visually exciting: animated full-color background, layered gradients, glow, grain, bold typography, original layout, CSS/SVG product visual, animated cards, hover states, theme toggle, responsive mobile design, reduced-motion support, and a visible support tab or support section.

Do not make it a plain text page or generic centered card.

After creating it, render the actual HTML in a browser, verify desktop and mobile, and show screenshots.

Content:
[PASTE CONTENT HERE]
```

## The most important phrase to keep using

> **“This must work when I open the HTML file by itself with `file://`; inline all CSS and JavaScript inside the file, and show me a rendered screenshot after verifying it.”**
