/**
 * Nút "Xem ví dụ" + popup iframe demo UI cho các khối code.
 */
(function () {
    'use strict';

    const DEMOS = {
        login: {
            title: 'Giao diện đăng nhập',
            hint: 'Điền username/password và bấm Đăng nhập — giống flow Selenium trong ví dụ.',
            url: 'demos/login.html',
        },
        ecommerce: {
            title: 'Cửa hàng E-commerce',
            hint: 'Tìm sản phẩm, chọn, đổi số lượng, thêm giỏ — flow shopping test.',
            url: 'demos/ecommerce.html',
        },
        calculator: {
            title: 'Calculator (Unit Test)',
            hint: 'Thử add() và divide() — tương ứng unit test trong slide.',
            url: 'demos/calculator.html',
        },
        bank: {
            title: 'Chuyển tiền (Integration)',
            hint: 'Chuyển giữa 2 tài khoản — mô phỏng integration test.',
            url: 'demos/bank-transfer.html',
        },
        api: {
            title: 'REST API Users',
            hint: 'GET/POST/PUT/DELETE — xem JSON response mock.',
            url: 'demos/api-users.html',
        },
        locators: {
            title: 'Locator Lab',
            hint: 'Trang có đủ id, name, class, CSS selector targets.',
            url: 'demos/locator-lab.html',
        },
        advanced: {
            title: 'Advanced UI Actions',
            hint: 'Hover menu, kéo-thả, chuột phải.',
            url: 'demos/advanced-ui.html',
        },
        frames: {
            title: 'Alert & Iframe',
            hint: 'Mở alert/confirm và iframe thanh toán.',
            url: 'demos/frames-alerts.html',
        },
        waits: {
            title: 'Explicit Wait',
            hint: 'Bấm tải — phần tử xuất hiện sau vài giây.',
            url: 'demos/waits-lab.html',
        },
    };

    const SKIP_RE =
        /jenkinsfile|pipeline\s*\{|testng\.xml|<!DOCTYPE suite|IRetryAnalyzer|RetryAnalyzer|FileUtils\.copy|onTestFailure|HtmlReporter|extentreports|maven-surefire|chromedriver\.exe|webdriver\.chrome\.driver|setProperty\(|pom\.xml|<dependency>|@BeforeSuite|@AfterSuite|listeners\s*>|Reporter\.log/i;

    const SELECTORS = '.code-block, .code-example, .locator-example';

    let overlay;

    function detectDemo(el) {
        const explicit = el.getAttribute('data-demo');
        if (explicit && DEMOS[explicit]) return explicit;

        const text = (el.textContent || '').toLowerCase();
        if (SKIP_RE.test(text) && !/findElement|sendKeys|\.click\(\)/.test(text)) {
            return null;
        }
        if (/calculator|testaddpositive|divide\(/.test(text)) return 'calculator';
        if (/restassured|given\(\)|\/users|postman|api\.example/.test(text)) return 'api';
        if (/transfer|accountservice|chuyển tiền|balance/.test(text)) return 'bank';
        if (/add-cart|cart-count|ecommerce|laptop|search-btn|product-name/.test(text)) return 'ecommerce';
        if (/switchto\(\)|\.alert\(|accept\(\)|iframe|frame\(/.test(text)) return 'frames';
        if (/webdriverwait|expectedconditions|fluentwait|implicitlywait/.test(text)) return 'waits';
        if (/actions\.|draganddrop|movetoelement|contextclick|doubleclick/.test(text)) return 'advanced';
        if (
            el.classList.contains('locator-example') ||
            (/cssselector|by\.xpath|\/\/button/.test(text) && !/findElement/.test(text))
        ) {
            return 'locators';
        }
        if (
            /findElement|sendKeys|webdriver|chromedriver|loginpage|username|password|welcome/.test(text)
        ) {
            return 'login';
        }
        return null;
    }

    function ensureModal() {
        if (overlay) return;
        overlay = document.createElement('div');
        overlay.className = 'demo-modal-overlay';

        const modal = document.createElement('div');
        modal.className = 'demo-modal';
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');

        const header = document.createElement('div');
        header.className = 'demo-modal-header';

        const titleWrap = document.createElement('div');
        const titleEl = document.createElement('h3');
        titleEl.id = 'demoModalTitle';
        const subEl = document.createElement('p');
        subEl.id = 'demoModalSub';
        titleWrap.appendChild(titleEl);
        titleWrap.appendChild(subEl);

        const closeBtn = document.createElement('button');
        closeBtn.type = 'button';
        closeBtn.className = 'demo-modal-close';
        closeBtn.setAttribute('aria-label', 'Đóng');
        closeBtn.innerHTML = '&times;';

        header.appendChild(titleWrap);
        header.appendChild(closeBtn);

        const body = document.createElement('div');
        body.className = 'demo-modal-body';
        const frame = document.createElement('iframe');
        frame.id = 'demoModalFrame';
        frame.title = 'UI demo';
        body.appendChild(frame);

        const hint = document.createElement('div');
        hint.className = 'demo-hint-bar';
        hint.id = 'demoModalHint';

        modal.appendChild(header);
        modal.appendChild(body);
        modal.appendChild(hint);
        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        closeBtn.onclick = closeModal;
        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) closeModal();
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && overlay.classList.contains('is-open')) closeModal();
        });
    }

    function openModal(demoId) {
        const demo = DEMOS[demoId];
        if (!demo) return;
        ensureModal();
        document.getElementById('demoModalTitle').textContent = demo.title;
        document.getElementById('demoModalSub').textContent = 'Mô phỏng giao diện đang được test';
        document.getElementById('demoModalHint').textContent = demo.hint;
        document.getElementById('demoModalFrame').src = demo.url;
        overlay.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        if (!overlay) return;
        overlay.classList.remove('is-open');
        document.body.style.overflow = '';
        const frame = document.getElementById('demoModalFrame');
        if (frame) frame.src = 'about:blank';
    }

    function injectButtons() {
        document.querySelectorAll(SELECTORS).forEach(function (block) {
            if (block.dataset.demoInjected) return;
            const demoId = detectDemo(block);
            if (!demoId) return;
            block.dataset.demoInjected = '1';
            block.dataset.demo = demoId;

            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn-view-demo';
            btn.textContent = '👁 Xem ví dụ';
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                openModal(demoId);
            });
            block.insertAdjacentElement('afterend', btn);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectButtons);
    } else {
        injectButtons();
    }

    window.CourseUIDemos = { open: openModal, close: closeModal, detect: detectDemo };
})();
