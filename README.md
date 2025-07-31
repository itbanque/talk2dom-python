# talk2dom — Locate Web Elements with One Sentence

> 📚 [English](./README.md) | [中文](./README.zh.md)

![PyPI](https://img.shields.io/pypi/v/talk2dom)
[![PyPI Downloads](https://static.pepy.tech/badge/talk2dom)](https://pepy.tech/projects/talk2dom)
![Stars](https://img.shields.io/github/stars/itbanque/talk2dom?style=social)
![License](https://img.shields.io/github/license/itbanque/talk2dom)
![CI](https://github.com/itbanque/talk2dom/actions/workflows/test.yaml/badge.svg)

**talk2dom** is a focused utility that solves one of the hardest problems in browser automation and UI testing:

> ✅ **Finding the correct UI element on a page.**

---

[![Watch the demo on YouTube](https://img.youtube.com/vi/6S3dOdWj5Gg/0.jpg)](https://youtu.be/6S3dOdWj5Gg)


## 🧠 Why `talk2dom`

In most automated testing or LLM-driven web navigation tasks, the real challenge is not how to click or type — it's how to **locate the right element**.

Think about it:

- Clicking a button is easy — *if* you know its selector.
- Typing into a field is trivial — *if* you've already located the right input.
- But finding the correct element among hundreds of `<div>`, `<span>`, or deeply nested Shadow DOM trees? That's the hard part.

**`talk2dom` is built to solve exactly that.**

---

## 🎯 What it does

`talk2dom` helps you locate elements by:

- Understands natural language instructions and turns them into browser actions  
- Supports single-command execution or persistent interactive sessions  
- Uses LLMs (like GPT-4 or Claude) to analyze live HTML and intent  
- Returns flexible output: actions, selectors, or both — providing flexible outputs: actions, selectors, or both — depending on the instruction and model response  
- Compatible with both desktop and mobile browsers via Selenium

---

## 🤔 Why Selenium?

While there are many modern tools for controlling browsers (like Playwright or Puppeteer), **Selenium remains the most robust and cross-platform solution**, especially when dealing with:

- ✅ Safari (WebKit)
- ✅ Firefox
- ✅ Mobile browsers
- ✅ Cross-browser testing grids

These tools often have limited support for anything beyond Chrome-based browsers. Selenium, by contrast, has battle-tested support across all major platforms and continues to be the industry standard in enterprise and CI/CD environments.

That’s why `talk2dom` is designed to integrate directly with Selenium — it works where the real-world complexity lives.

---

## 📦 Installation

```bash
pip install talk2dom
```

---

## 🧩 Code-Based ActionChain Mode

For developers and testers who prefer structured Python control, `ActionChain` lets you drive the browser step-by-step.

#### Sample Code

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from talk2dom import ActionChain

driver = webdriver.Chrome()

ActionChain(driver) \
    .open("http://www.python.org") \
    .find("Find the Search box") \
    .type("pycon") \
    .wait(2) \
    .type(Keys.RETURN) \
    .assert_page_not_contains("No results found.") \
    .close()
```

### Free Tier Access

You can use `talk2dom` for free — just [register for an API key](https://talk2dom.itbanque.com) to receive a generous quota, or self-host it with your own model and server.

No credit card required.

---


## ✨ Philosophy

> Our goal is not to control the browser — you still control your browser. 
> Our goal is to **find the right DOM element**, so you can tell the browser what to do.

---

## ✅ Key Features

- 💬 Natural language interface to control the browser  
- 🔁 Persistent session for multi-step interactions  
- 🧠 LLM-powered understanding of high-level intent  
- 🧩 Outputs: actionable XPath/CSS selectors or ready-to-run browser steps  
- 🧪 Built-in assertions and step validations  
- 💡 Works with both CLI scripts and interactive chat

---
