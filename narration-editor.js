/**
 * Chỉnh sửa script thuyết minh + lưu + tạo lại MP3 qua server.py
 */
(function (global) {
    'use strict';

    var API_BASE = '';
    var API_READY = null;
    var TAG = 'di' + 'v';

    var PAGE_LABELS = {
        index: 'Trang chủ',
        oop1: 'Java Core — OOP Principles',
        java2: 'Java Core — Collections',
        java34: 'Java Core — Advanced Java',
        video1: 'PHASE 1 — Bài 1',
        video2: 'PHASE 1 — Bài 2',
        phase2: 'PHASE 2 — Selenium',
        phase3: 'PHASE 3 — TestNG & POM',
        phase4: 'PHASE 4 — Advanced & CI/CD',
        api1: 'API Testing — Buổi 1',
        api2: 'API Testing — Tuần 3-4',
        api3: 'API Testing — RestAssured'
    };

    var PAGE_ORDER = [
        'index',
        'oop1',
        'java2',
        'java34',
        'video1',
        'video2',
        'phase2',
        'phase3',
        'phase4',
        'api1',
        'api2',
        'api3'
    ];

    var PAGE_MODULE = {
        index: 'intro',
        oop1: 'java',
        java2: 'java',
        java34: 'java',
        video1: 'auto',
        video2: 'auto',
        phase2: 'auto',
        phase3: 'auto',
        phase4: 'auto',
        api1: 'api',
        api2: 'api',
        api3: 'api'
    };

    var REGEN_MODULES = [
        { id: 'all', title: '📚 Toàn khóa học' },
        { id: 'java', title: '☕ Java Core' },
        { id: 'api', title: '🔌 API Testing' },
        { id: 'auto', title: '🤖 Automation' },
        { id: 'intro', title: '🏠 Trang chủ' }
    ];

    var regenCache = { items: [], modules: [] };

    function qs(sel, root) {
        return (root || document).querySelector(sel);
    }

    function qsa(sel, root) {
        return Array.prototype.slice.call((root || document).querySelectorAll(sel));
    }

    function el(tag, className, html) {
        var node = document.createElement(tag || TAG);
        if (className) node.className = className;
        if (html != null) node.innerHTML = html;
        return node;
    }

    function setStatus(node, message, type) {
        if (!node) return;
        node.textContent = message;
        node.className = 'narration-save-status' + (type ? ' ' + type : '');
    }

    function getSlidesDeck() {
        var deck = qs('#slidesContainer') || qs('.slides');
        if (deck) {
            var n = deck.querySelectorAll('.slide');
            if (n.length) return Array.prototype.slice.call(n);
        }
        return qsa('.slide');
    }

    function getSlideKey(box) {
        var slide = box.closest('.slide');
        if (!slide) return null;
        var slides = getSlidesDeck();
        var idx = slides.indexOf(slide);
        if (idx < 0) return null;
        return String(idx);
    }

    function getPlainText(box) {
        return box.textContent.replace(/🔊/g, '').trim().replace(/^["']|["']$/g, '');
    }

    function updateBoxDisplay(box, text) {
        box.textContent = '';
        box.appendChild(document.createTextNode('🔊 "' + text + '"'));
    }

    function parseJsonResponse(res) {
        return res.text().then(function (body) {
            try {
                return JSON.parse(body);
            } catch (e) {
                if (res.status === 404) {
                    throw new Error(
                        'API không khả dụng (404). Chạy python server.py và mở http://localhost:5500 — không dùng python -m http.server.'
                    );
                }
                throw new Error('Lỗi server (' + res.status + ')');
            }
        });
    }

    function apiUrl(path) {
        return API_BASE + path;
    }

    function tryHealthAt(base) {
        return fetch(base + '/api/health')
            .then(function (res) {
                if (!res.ok) return null;
                return res.json().then(function (data) {
                    if (data && data.ok) {
                        syncPageRegistryFromApi(data);
                        return base;
                    }
                    return null;
                });
            })
            .catch(function () {
                return null;
            });
    }

    function resolveApiBase() {
        var host = location.hostname || 'localhost';
        var protocol = location.protocol || 'http:';
        var origin = location.origin || protocol + '//' + host;
        var ports = [];
        if (location.port) ports.push(location.port);
        ['5500', '5501'].forEach(function (p) {
            if (ports.indexOf(p) === -1) ports.push(p);
        });

        var chain = Promise.resolve(null);
        ports.forEach(function (port) {
            chain = chain.then(function (found) {
                if (found !== null) return found;
                var base = protocol + '//' + host + ':' + port;
                if (port === location.port) return tryHealthAt('');
                return tryHealthAt(base);
            });
        });

        return chain.then(function (found) {
            if (found === null) {
                API_BASE = '';
                return false;
            }
            API_BASE = found;
            return true;
        });
    }

    function ensureApi() {
        if (!API_READY) API_READY = resolveApiBase();
        return API_READY;
    }

    function checkServer() {
        return ensureApi();
    }

    function saveNarration(page, key, text, options) {
        options = options || {};
        var regenerate = options.regenerate !== false;
        return ensureApi().then(function (ok) {
            if (!ok) throw new Error('Không kết nối API. Chạy python server.py (không dùng python -m http.server).');
            return fetch(
            apiUrl('/api/narration/' + encodeURIComponent(page) + '/' + encodeURIComponent(key)),
            {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json; charset=utf-8' },
                body: JSON.stringify({ text: text, regenerate: regenerate })
            }
        );
        }).then(function (res) {
            return parseJsonResponse(res).then(function (data) {
                if (!res.ok) throw new Error(data.error || 'Lưu thất bại');
                return data;
            });
        });
    }

    function saveNarrationTextOnly(page, key, text) {
        return saveNarration(page, key, text, { regenerate: false });
    }

    function regenerateOne(page, key) {
        return ensureApi().then(function (ok) {
            if (!ok) throw new Error('Không kết nối API. Chạy python server.py.');
            return fetch(
            apiUrl('/api/regenerate/' + encodeURIComponent(page) + '/' + encodeURIComponent(key)),
            { method: 'POST' }
        );
        }).then(function (res) {
            return parseJsonResponse(res).then(function (data) {
                if (!res.ok && res.status !== 207) {
                    throw new Error(data.error || 'Tạo audio thất bại');
                }
                return data;
            });
        });
    }

    function fetchNarrationList() {
        return ensureApi().then(function (ok) {
            if (!ok) throw new Error('Không kết nối API. Chạy python server.py.');
            return fetch(apiUrl('/api/narrations'));
        }).then(function (res) {
            return parseJsonResponse(res).then(function (data) {
                if (!res.ok) throw new Error(data.error || 'Không tải danh sách');
                regenCache.items = sortNarrationItems(data.items || []);
                regenCache.modules = data.modules || [];
                return regenCache;
            });
        });
    }

    function filterItemsByModule(items, moduleId) {
        if (!moduleId || moduleId === 'all') return items.slice();
        if (moduleId === 'intro') return items.filter(function (i) { return i.page === 'index'; });
        return items.filter(function (i) {
            return PAGE_MODULE[i.page] === moduleId;
        });
    }

    function filterItemsByPage(items, page) {
        return items.filter(function (i) { return i.page === page; });
    }

    function pagesInModule(moduleId) {
        if (moduleId === 'all') {
            return PAGE_ORDER.filter(function (p) { return p !== 'index'; });
        }
        if (moduleId === 'intro') return ['index'];
        return PAGE_ORDER.filter(function (p) { return PAGE_MODULE[p] === moduleId; });
    }

    function itemLabel(item) {
        if (item.label) return item.label;
        if (item.page === 'index') return 'Giới thiệu';
        return (PAGE_LABELS[item.page] || item.page) + ' — Slide ' + (parseInt(item.key, 10) + 1);
    }

    function sortNarrationItems(items) {
        var order = {};
        PAGE_ORDER.forEach(function (p, i) {
            order[p] = i;
        });
        return items.slice().sort(function (a, b) {
            var pa = order[a.page] != null ? order[a.page] : 999;
            var pb = order[b.page] != null ? order[b.page] : 999;
            if (pa !== pb) return pa - pb;
            if (a.page === 'index') return 0;
            return parseInt(a.key, 10) - parseInt(b.key, 10);
        });
    }

    function regenSubtitle(items) {
        var byPage = {};
        items.forEach(function (item) {
            byPage[item.page] = (byPage[item.page] || 0) + 1;
        });
        var parts = [];
        PAGE_ORDER.forEach(function (page) {
            if (byPage[page]) {
                parts.push((PAGE_LABELS[page] || page) + ' (' + byPage[page] + ')');
            }
        });
        return (
            'Tổng ' +
            items.length +
            ' file — intro + 11 bài (Java Core, Automation, API). ' +
            parts.join(' · ')
        );
    }

    function syncPageRegistryFromApi(data) {
        if (!data) return;
        // Không ghi đè PAGE_ORDER từ API: thứ tự dict trên server có thể thiếu bài → modal chỉ còn 6 bài.
        if (data.labels) {
            Object.keys(data.labels).forEach(function (k) {
                PAGE_LABELS[k] = data.labels[k];
            });
        }
    }

    function ensureRegenModal() {
        var overlay = qs('#regenModalOverlay');
        if (overlay) return overlay;

        overlay = el(TAG, 'regen-modal-overlay');
        overlay.id = 'regenModalOverlay';

        var modal = el(TAG, 'regen-modal regen-modal-wide');
        modal.setAttribute('role', 'dialog');

        var header = el(TAG, 'regen-modal-header');
        var h3 = document.createElement('h3');
        h3.id = 'regenModalTitle';
        h3.textContent = 'Tạo lại audio';
        var sub = document.createElement('p');
        sub.id = 'regenModalSubtitle';
        sub.textContent = 'Chọn khóa hoặc bài học';
        header.appendChild(h3);
        header.appendChild(sub);

        var body = el(TAG, 'regen-modal-body');
        body.id = 'regenModalBody';

        var summary = el(TAG, '');
        summary.id = 'regenModalSummary';

        var footer = el(TAG, 'regen-modal-footer');
        var backBtn = document.createElement('button');
        backBtn.type = 'button';
        backBtn.className = 'regen-btn-back';
        backBtn.id = 'regenModalBack';
        backBtn.textContent = '← Quay lại';
        backBtn.hidden = true;
        var closeBtn = document.createElement('button');
        closeBtn.type = 'button';
        closeBtn.className = 'regen-btn-close';
        closeBtn.id = 'regenModalClose';
        closeBtn.textContent = 'Đóng';
        footer.appendChild(backBtn);
        footer.appendChild(closeBtn);

        modal.appendChild(header);
        modal.appendChild(body);
        modal.appendChild(summary);
        modal.appendChild(footer);
        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        closeBtn.addEventListener('click', function () {
            overlay.classList.remove('visible');
        });

        return overlay;
    }

    function moduleStats(moduleId) {
        var mod = regenCache.modules.filter(function (m) { return m.id === moduleId; })[0];
        if (mod) return { lessons: mod.lessonCount, slides: mod.slideCount };
        var items = filterItemsByModule(regenCache.items, moduleId);
        var pages = {};
        items.forEach(function (i) { pages[i.page] = true; });
        return { lessons: Object.keys(pages).length, slides: items.length };
    }

    function showRegenModulePicker() {
        var body = qs('#regenModalBody');
        var subtitle = qs('#regenModalSubtitle');
        var backBtn = qs('#regenModalBack');
        var closeBtn = qs('#regenModalClose');
        var summary = qs('#regenModalSummary');
        body.textContent = '';
        summary.textContent = '';
        summary.className = '';
        backBtn.hidden = true;
        closeBtn.disabled = false;
        subtitle.textContent = 'Chọn khóa (module) hoặc tạo lại toàn bộ khóa học';

        var list = el(TAG, 'regen-module-list');
        REGEN_MODULES.forEach(function (mod) {
            var stats = moduleStats(mod.id);
            var card = el(TAG, 'regen-module-card');
            card.className += ' regen-module-' + mod.id;
            var head = el(TAG, 'regen-module-card-head');
            head.innerHTML = '<strong>' + mod.title + '</strong><span>' + stats.lessons + ' bài · ' + stats.slides + ' slide</span>';
            card.appendChild(head);
            var actions = el(TAG, 'regen-module-card-actions');
            var viewBtn = document.createElement('button');
            viewBtn.type = 'button';
            viewBtn.className = 'regen-btn-secondary';
            viewBtn.textContent = 'Danh sách bài';
            viewBtn.addEventListener('click', function () {
                showRegenLessonList(mod.id, mod.title);
            });
            var runBtn = document.createElement('button');
            runBtn.type = 'button';
            runBtn.className = 'regen-btn-primary';
            runBtn.textContent = 'Tạo lại toàn bộ khóa này';
            runBtn.addEventListener('click', function () {
                runRegeneration(filterItemsByModule(regenCache.items, mod.id), mod.title);
            });
            actions.appendChild(viewBtn);
            actions.appendChild(runBtn);
            card.appendChild(actions);
            list.appendChild(card);
        });
        body.appendChild(list);
    }

    function showRegenLessonList(moduleId, moduleTitle) {
        var body = qs('#regenModalBody');
        var subtitle = qs('#regenModalSubtitle');
        var backBtn = qs('#regenModalBack');
        var summary = qs('#regenModalSummary');
        body.textContent = '';
        summary.textContent = '';
        backBtn.hidden = false;
        backBtn.onclick = function () { showRegenModulePicker(); };
        subtitle.textContent = moduleTitle + ' — chọn bài hoặc tạo lại cả khóa';

        var topActions = el(TAG, 'regen-lesson-top-actions');
        var runAll = document.createElement('button');
        runAll.type = 'button';
        runAll.className = 'regen-btn-primary';
        runAll.textContent = '🔄 Tạo lại toàn bộ ' + moduleTitle;
        runAll.addEventListener('click', function () {
            runRegeneration(filterItemsByModule(regenCache.items, moduleId), moduleTitle);
        });
        topActions.appendChild(runAll);
        body.appendChild(topActions);

        var list = el(TAG, 'regen-lesson-list');
        pagesInModule(moduleId).forEach(function (page) {
            var pageItems = filterItemsByPage(regenCache.items, page);
            var row = el(TAG, 'regen-lesson-row');
            var info = el(TAG, 'regen-lesson-info');
            var cnt = pageItems.length;
            info.innerHTML =
                '<strong>' +
                (PAGE_LABELS[page] || page) +
                '</strong><span>' +
                (cnt ? cnt + ' slide có script' : 'Chưa có script trên server — chạy lại python server.py') +
                '</span>';
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'regen-btn-secondary';
            btn.textContent = 'Tạo lại bài này';
            if (!cnt) {
                btn.disabled = true;
                btn.title = 'Không có mục thuyết minh trong /api/narrations cho bài này.';
            } else {
                btn.addEventListener('click', function () {
                    runRegeneration(pageItems, PAGE_LABELS[page] || page);
                });
            }
            row.appendChild(info);
            row.appendChild(btn);
            list.appendChild(row);
        });
        body.appendChild(list);
    }

    function buildRegenProgressUI(items) {
        var body = qs('#regenModalBody');
        body.textContent = '';
        var byPage = {};
        items.forEach(function (item) {
            if (!byPage[item.page]) byPage[item.page] = [];
            byPage[item.page].push(item);
        });
        PAGE_ORDER.forEach(function (page) {
            if (!byPage[page]) return;
            var group = el(TAG, 'regen-phase-group');
            var title = el(TAG, 'regen-phase-title');
            title.textContent = PAGE_LABELS[page] || page;
            group.appendChild(title);
            byPage[page].forEach(function (item) {
                var row = el(TAG, 'regen-item pending');
                row.id = 'regen-' + item.page + '-' + item.key;
                var icon = el(TAG, 'regen-item-icon');
                icon.textContent = '○';
                var text = el(TAG, 'regen-item-text');
                text.textContent = itemLabel(item);
                row.appendChild(icon);
                row.appendChild(text);
                group.appendChild(row);
            });
            body.appendChild(group);
        });
    }

    function setRegenRow(page, key, state, message) {
        var row = qs('#regen-' + page + '-' + key);
        if (!row) return;
        row.className = 'regen-item ' + state;
        var icon = row.querySelector('.regen-item-icon');
        var text = row.querySelector('.regen-item-text');
        if (icon) icon.textContent = state === 'ok' ? '✓' : state === 'error' ? '✗' : state === 'running' ? '…' : '○';
        if (message && text) text.textContent = message;
    }

    function runRegeneration(items, title) {
        var overlay = ensureRegenModal();
        var subtitle = qs('#regenModalSubtitle');
        var summary = qs('#regenModalSummary');
        var closeBtn = qs('#regenModalClose');
        var backBtn = qs('#regenModalBack');
        if (!items.length) {
            summary.className = 'regen-summary warn';
            summary.textContent = 'Không có slide nào có script thuyết minh.';
            return Promise.resolve({ okCount: 0, errCount: 0, total: 0 });
        }
        backBtn.hidden = true;
        closeBtn.disabled = true;
        summary.textContent = '';
        summary.className = '';
        subtitle.textContent = title + ' — ' + items.length + ' file (xóa MP3 cũ, tạo mới)';
        buildRegenProgressUI(items);

        var okCount = 0;
        var errCount = 0;
        var idx = 0;
        var maxWorkers = 4;

        function runNext() {
            if (idx >= items.length) return Promise.resolve();
            var item = items[idx++];
            setRegenRow(item.page, item.key, 'running', itemLabel(item) + ' — đang tạo…');
            return regenerateOne(item.page, item.key)
                .then(function (result) {
                    if (result.status === 'ok') {
                        okCount += 1;
                        setRegenRow(item.page, item.key, 'ok', itemLabel(item) + ' — xong');
                    } else {
                        errCount += 1;
                        setRegenRow(item.page, item.key, 'error', itemLabel(item) + ' — ' + (result.error || 'lỗi'));
                    }
                })
                .catch(function (err) {
                    errCount += 1;
                    setRegenRow(item.page, item.key, 'error', itemLabel(item) + ' — ' + (err.message || 'lỗi'));
                })
                .then(runNext);
        }

        var workers = [];
        for (var w = 0; w < Math.min(maxWorkers, items.length); w++) {
            workers.push(runNext());
        }

        return Promise.all(workers).then(function () {
            if (global.VietnameseTTS && global.VietnameseTTS.reloadManifest) {
                global.VietnameseTTS.reloadManifest();
            }
            summary.className = 'regen-summary ' + (errCount === 0 ? 'ok' : 'warn');
            summary.textContent =
                'Hoàn tất: ' + okCount + ' thành công' + (errCount ? ', ' + errCount + ' lỗi' : '') + '.';
            subtitle.textContent = 'Đã xử lý xong — ' + title;
            closeBtn.disabled = false;
            return { okCount: okCount, errCount: errCount, total: items.length };
        });
    }

    function runRegenerateAllWithModal() {
        var overlay = ensureRegenModal();
        var subtitle = qs('#regenModalSubtitle');
        var summary = qs('#regenModalSummary');
        var closeBtn = qs('#regenModalClose');
        summary.textContent = '';
        summary.className = '';
        closeBtn.disabled = false;
        overlay.classList.add('visible');
        subtitle.textContent = 'Đang tải danh sách…';

        return fetchNarrationList()
            .then(function () {
                showRegenModulePicker();
                return { okCount: 0, errCount: 0, total: regenCache.items.length };
            })
            .catch(function (err) {
                subtitle.textContent = 'Lỗi';
                summary.className = 'regen-summary warn';
                summary.textContent = err.message || 'Không thể tải danh sách';
                closeBtn.disabled = false;
                throw err;
            });
    }

    function attachPanelToBox(box, page, key) {
        if (box.nextElementSibling && box.nextElementSibling.classList.contains('narration-edit-panel')) {
            return;
        }

        var panel = el(TAG, 'narration-edit-panel');
        var label = document.createElement('label');
        label.textContent =
            'Script thuyết minh (slide ' + (key === 'intro' ? 'giới thiệu' : parseInt(key, 10) + 1) + ')';
        var textarea = document.createElement('textarea');
        textarea.className = 'narration-script-input';
        textarea.value = getPlainText(box);

        var actions = el(TAG, 'narration-edit-actions');
        var saveTextBtn = document.createElement('button');
        saveTextBtn.type = 'button';
        saveTextBtn.className = 'btn-save-narration-text';
        saveTextBtn.textContent = '💾 Lưu';
        var saveAudioBtn = document.createElement('button');
        saveAudioBtn.type = 'button';
        saveAudioBtn.className = 'btn-save-narration';
        saveAudioBtn.textContent = '🔊 Lưu & tạo audio';
        var status = el(TAG, 'narration-save-status');

        function setButtonsDisabled(disabled) {
            saveTextBtn.disabled = disabled;
            saveAudioBtn.disabled = disabled;
        }

        saveTextBtn.addEventListener('click', function () {
            var text = textarea.value.trim();
            if (!text) {
                setStatus(status, 'Nội dung không được rỗng.', 'err');
                return;
            }
            setButtonsDisabled(true);
            setStatus(status, 'Đang lưu script…', '');

            saveNarrationTextOnly(page, key, text)
                .then(function (data) {
                    updateBoxDisplay(box, data.text);
                    textarea.value = data.text;
                    setStatus(status, 'Đã lưu script (chưa tạo lại audio).', 'ok');
                })
                .catch(function (err) {
                    setStatus(status, err.message || 'Lỗi khi lưu.', 'err');
                })
                .finally(function () {
                    setButtonsDisabled(false);
                });
        });

        saveAudioBtn.addEventListener('click', function () {
            var text = textarea.value.trim();
            if (!text) {
                setStatus(status, 'Nội dung không được rỗng.', 'err');
                return;
            }
            setButtonsDisabled(true);
            setStatus(status, 'Đang lưu và tạo audio…', '');

            saveNarration(page, key, text)
                .then(function (data) {
                    updateBoxDisplay(box, data.text);
                    textarea.value = data.text;
                    if (global.VietnameseTTS && global.VietnameseTTS.reloadManifest) {
                        global.VietnameseTTS.reloadManifest();
                    }
                    setStatus(status, 'Đã lưu script & tạo lại audio.', 'ok');
                })
                .catch(function (err) {
                    setStatus(status, err.message || 'Lỗi khi lưu.', 'err');
                })
                .finally(function () {
                    setButtonsDisabled(false);
                });
        });

        actions.appendChild(saveTextBtn);
        actions.appendChild(saveAudioBtn);
        actions.appendChild(status);
        panel.appendChild(label);
        panel.appendChild(textarea);
        panel.appendChild(actions);
        box.insertAdjacentElement('afterend', panel);
    }

    function initLessonEditors() {
        var page = document.body.dataset.ttsPage;
        if (!page) return;
        var deck = qs('#slidesContainer') || qs('.slides');
        var boxes = deck ? deck.querySelectorAll('.narration-box') : qsa('.narration-box');
        Array.prototype.forEach.call(boxes, function (box) {
            var key = getSlideKey(box);
            if (key === null || key === '-1') return;
            attachPanelToBox(box, page, key);
        });
    }

    function initIndexAdmin() {
        var panel = qs('#narrationAdminPanel');
        if (!panel) return;

        var introBox = qs('#introNarration');
        var introTextarea = qs('#introScriptEdit');
        var saveBtn = qs('#saveIntroBtn');
        var regenAllBtn = qs('#regenerateAllBtn');
        var adminStatus = qs('#adminStatus');
        var offlineBanner = qs('#serverOfflineBanner');

        if (introBox && introTextarea) {
            introTextarea.value = getPlainText(introBox);
        }

        ensureApi().then(function (ok) {
            if (!ok && offlineBanner) {
                offlineBanner.classList.add('visible');
                offlineBanner.textContent =
                    'API không tìm thấy trên cổng 5500/5501. Tắt python -m http.server, chạy python server.py, tải lại trang.';
            } else if (offlineBanner && API_BASE && API_BASE !== location.origin) {
                offlineBanner.classList.add('visible');
                offlineBanner.style.background = '#eff6ff';
                offlineBanner.style.color = '#1e40af';
                offlineBanner.textContent =
                    'Đang dùng API tại ' + API_BASE + ' (trang web và API khác cổng — nên chạy chỉ python server.py).';
            }
        });

        if (saveBtn && introTextarea && introBox) {
            saveBtn.textContent = '🔊 Lưu intro & tạo audio';

            var saveIntroTextBtn = document.createElement('button');
            saveIntroTextBtn.type = 'button';
            saveIntroTextBtn.className = 'btn-admin btn-admin-save-text';
            saveIntroTextBtn.textContent = '💾 Lưu';
            saveBtn.parentNode.insertBefore(saveIntroTextBtn, saveBtn);

            function setIntroSaveDisabled(disabled) {
                saveIntroTextBtn.disabled = disabled;
                saveBtn.disabled = disabled;
            }

            saveIntroTextBtn.addEventListener('click', function () {
                var text = introTextarea.value.trim();
                if (!text) {
                    setStatus(adminStatus, 'Nội dung không được rỗng.', 'err');
                    return;
                }
                setIntroSaveDisabled(true);
                setStatus(adminStatus, 'Đang lưu script intro…', '');

                saveNarrationTextOnly('index', 'intro', text)
                    .then(function (data) {
                        updateBoxDisplay(introBox, data.text);
                        introTextarea.value = data.text;
                        setStatus(adminStatus, 'Đã lưu script intro (chưa tạo lại audio).', 'ok');
                    })
                    .catch(function (err) {
                        setStatus(adminStatus, err.message || 'Lỗi.', 'err');
                    })
                    .finally(function () {
                        setIntroSaveDisabled(false);
                    });
            });

            saveBtn.addEventListener('click', function () {
                var text = introTextarea.value.trim();
                if (!text) {
                    setStatus(adminStatus, 'Nội dung không được rỗng.', 'err');
                    return;
                }
                setIntroSaveDisabled(true);
                setStatus(adminStatus, 'Đang lưu intro & tạo audio…', '');

                saveNarration('index', 'intro', text)
                    .then(function (data) {
                        updateBoxDisplay(introBox, data.text);
                        introTextarea.value = data.text;
                        if (global.VietnameseTTS && global.VietnameseTTS.reloadManifest) {
                            global.VietnameseTTS.reloadManifest();
                        }
                        setStatus(adminStatus, 'Đã lưu intro & tạo lại audio.', 'ok');
                    })
                    .catch(function (err) {
                        setStatus(adminStatus, err.message || 'Lỗi.', 'err');
                    })
                    .finally(function () {
                        setIntroSaveDisabled(false);
                    });
            });
        }

        if (regenAllBtn) {
            regenAllBtn.addEventListener('click', function () {
                regenAllBtn.disabled = true;
                setStatus(adminStatus, 'Đang mở tiến trình…', '');

                runRegenerateAllWithModal()
                    .then(function (result) {
                        setStatus(
                            adminStatus,
                            'Đã tải ' + result.total + ' slide từ server. Chọn khóa / bài trong cửa sổ để tạo audio.',
                            'ok'
                        );
                    })
                    .catch(function (err) {
                        setStatus(adminStatus, err.message || 'Lỗi.', 'err');
                    })
                    .finally(function () {
                        regenAllBtn.disabled = false;
                    });
            });
        }
    }

    function initToggleEdit() {
        var toggleBtn = qs('#toggleEditBtn');
        if (!toggleBtn) return;
        var deck = qs('#slidesContainer') || qs('.slides');
        var hasNarration = deck ? deck.querySelector('.narration-box') : qs('.narration-box');
        if (!hasNarration) {
            toggleBtn.style.display = 'none';
            return;
        }
        toggleBtn.addEventListener('click', function () {
            document.body.classList.toggle('narration-edit-mode');
            toggleBtn.textContent = document.body.classList.contains('narration-edit-mode')
                ? '✅ Xong sửa script'
                : '✏️ Sửa script';
        });
    }

    function init() {
        ensureApi().then(function () {
            initLessonEditors();
            initIndexAdmin();
            initToggleEdit();
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    global.NarrationEditor = {
        saveNarration: saveNarration,
        saveNarrationTextOnly: saveNarrationTextOnly,
        regenerateAll: runRegenerateAllWithModal,
        checkServer: checkServer
    };
})(typeof window !== 'undefined' ? window : this);
