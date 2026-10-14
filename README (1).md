<div align="center">

# ❤️ Love Heart

### *"I love you" in 20 languages, writing itself into a heart.*

![Python](https://img.shields.io/badge/python-3.8+-ff4d6d?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/vanilla-JS-98001a?style=for-the-badge&logo=javascript&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-zero-e60d24?style=for-the-badge)
![Made with](https://img.shields.io/badge/made%20with-love-fa1a29?style=for-the-badge)

*A tiny romantic web gift: tap, music starts, and hundreds of words of love fall into place to form a glowing heart.*

</div>

---

## ✨ What is this?

You open the link. A heart beats on a dark screen. You tap it.

The music starts, and word by word, in 20 languages, the words *"I love you"* drift into place until they fill a heart shape in wine, crimson and blood-red. When it's done, the heart keeps shimmering.

No frameworks. No build step. No server. Just a Python script, a JavaScript file, a page and a song.

---

## 🗂️ The files, and what each one does

```
love/
├── 🐍 heart.py      →  the brain: does the geometry
├── 📜 layout.js     →  the blueprint: where every word goes
├── 🌐 index.html    →  the stage: draws and animates it all
└── 🎵 music.mp3     →  the soundtrack
```

| File | Job | Edit it when… |
|---|---|---|
| **`heart.py`** | Builds the heart curve, slices it into rows, and fits phrases into each row. Picks every word's position, size and color, and decides the order they appear in. Writes the result to `layout.js`. | You want different words, colors, or heart size. |
| **`layout.js`** | Auto-generated data file holding two ready-made layouts: `wide` for desktop and `narrow` for phones. | Never by hand. Re-run `heart.py` instead. |
| **`index.html`** | Loads the layout and the music. Shows the "TAP TO OPEN" screen, starts the audio, then animates each word floating up, fading in and flashing. Adds the shimmer afterwards. | You want to change the look or animation timing. |
| **`music.mp3`** | The song that plays (and loops) when she taps. | You want a different song. Keep the same filename. |

---

## ⚙️ How it works

```
 heart.py                    layout.js                   index.html
┌──────────────┐  writes   ┌─────────────┐   loaded by  ┌──────────────────┐
│ heart curve  │ ───────▶  │ word        │ ───────────▶ │ canvas animation │
│ + row slicing│           │ positions,  │              │ + music.mp3      │
│ + word fitting│          │ sizes,      │              │ + tap-to-start   │
│ + colors     │           │ colors      │              └──────────────────┘
└──────────────┘           └─────────────┘
```

**1. The heart.** `heart.py` uses the classic parametric heart curve:

```
x = 16·sin³(t)
y = 13·cos(t) − 5·cos(2t) − 2·cos(3t) − cos(4t)
```

**2. The rows.** The heart is cut into horizontal strips. For each strip, the script finds the left and right edges of the shape, which is where words may go.

**3. The words.** Phrases are shuffled and packed left to right into each strip, then spaced out evenly so every line is flush with the heart's edge. Words on the outline are tinted brighter, and words near the center are deeper wine red.

**4. The order.** The outline is "drawn" first, going around the heart. Then the inside fills from the center outward.

**5. The stage.** `index.html` takes that blueprint and animates each word: it lifts up from below, fades in with a soft glow and shadow, and gives a brief pink flash as it lands. When everything has landed, random words sparkle forever.

**6. Why the tap?** Browsers block audio that starts by itself. The "TAP TO OPEN" screen is the one tap that lets the music play with sound.

---

## 🚀 Run it

**Just see it:** double-click `index.html`. That's it. No server needed.

**Change the words or colors:**

```bash
# 1. edit PHRASES (or colors) in heart.py
# 2. regenerate the blueprint
python heart.py
# 3. refresh index.html
```

**Send it to someone** (a link they can open on their phone):

1. Keep all four files together in the folder.
2. Drag the folder onto [Netlify Drop](https://app.netlify.com/drop), or push it to GitHub and turn on **GitHub Pages**.
3. Send the link. 💌

> ⚠️ All four files must be uploaded together. `index.html` loads `layout.js` and `music.mp3` by name.

---

## 🎛️ Make it yours

| Want to change… | Where |
|---|---|
| The languages / words (add her name!) | `PHRASES` list in `heart.py` |
| Heart size | `SC` in `heart.py` |
| Word colors | `wine`, `crimson`, `blood` in `heart.py` |
| Text size on phones | the `make_layout(1.4)` call at the bottom of `heart.py` |
| How long the build-up takes | `DURATION` in `index.html` |
| The song | replace `music.mp3` |

---

## 🌍 Languages inside the heart

English · Turkish · Spanish · French · German · Italian · Portuguese · Russian · Korean · Japanese · Chinese · Hindi · Greek · Dutch · Swedish · Polish · Thai · Vietnamese · Indonesian · Ukrainian

---

## 📝 Notes

- `heart.py` measures text with Tkinter fonts when available, so words fit tightly. Without Tkinter it falls back to an estimate, which still looks good.
- The layout is seeded (`seed=11`), so the heart looks the same every time you generate it. Change the seed for a different arrangement.
- Works on modern desktop and mobile browsers, and no internet is needed once the files are loaded.

---

<div align="center">

*Made with ❤️ for someone who deserves every language.*

</div>
