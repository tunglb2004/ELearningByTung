/**
 * Phát thuyết minh từ MP3 (Edge TTS — Việt + Anh tách đoạn khi tạo file).
 * Sau khi bấm đọc: hiện thanh <audio controls> + chọn tốc độ.
 */
(function (global) {
    'use strict';

    var manifest = null;
    var manifestLoading = null;
    var currentAudio = null;
    var speaking = false;
    var onEndCallback = null;
    var ui = {
        speakBtn: null,
        stopBtn: null,
        playerSlot: null,
        audioEl: null,
        rateSelect: null
    };

    function resolveUrl(relativePath) {
        if (/^https?:\/\//i.test(relativePath)) return relativePath;
        var base = global.location.href.replace(/[^/]+$/, '');
        return base + relativePath.replace(/^\//, '');
    }

    function loadManifest() {
        if (manifest) return Promise.resolve(manifest);
        if (manifestLoading) return manifestLoading;

        manifestLoading = fetch(resolveUrl('audio/manifest.json'))
            .then(function (res) {
                if (!res.ok) throw new Error('manifest');
                return res.json();
            })
            .then(function (data) {
                manifest = data;
                return manifest;
            })
            .catch(function () {
                manifest = {};
                return manifest;
            });

        return manifestLoading;
    }

    function defaultAudioPath(page, key) {
        return 'audio/' + page + '/' + key + '.mp3';
    }

    function lookupAudioPaths(page, key) {
        var k = String(key);
        var entry = manifest && manifest[page] && manifest[page][k];
        if (entry && typeof entry === 'object' && entry.segments && entry.segments.length) {
            return entry.segments;
        }
        if (typeof entry === 'string') {
            return [entry];
        }
        return [defaultAudioPath(page, k)];
    }

    function bindPlayerUi(options) {
        options = options || {};
        ui.speakBtn =
            options.speakBtn ||
            document.getElementById('speakBtn') ||
            document.getElementById('speakIntroBtn');
        ui.stopBtn = options.stopBtn || document.getElementById('stopSpeakBtn') || document.getElementById('stopIntroBtn');
        ui.playerSlot = options.playerSlot || document.getElementById('ttsPlayerSlot');
        ui.audioEl = options.audioEl || document.getElementById('courseAudio');
        ui.rateSelect = options.rateSelect || document.getElementById('ttsRateSelect');

        if (ui.rateSelect && !ui.rateSelect.dataset.bound) {
            ui.rateSelect.dataset.bound = '1';
            ui.rateSelect.addEventListener('change', function () {
                var rate = parseFloat(ui.rateSelect.value, 10);
                if (ui.audioEl) ui.audioEl.playbackRate = rate;
                if (currentAudio) currentAudio.playbackRate = rate;
            });
        }

        if (ui.audioEl && !ui.audioEl.dataset.bound) {
            ui.audioEl.dataset.bound = '1';
            ui.audioEl.addEventListener('ended', function () {
                hidePlayer();
                finish();
            });
            ui.audioEl.addEventListener('pause', function () {
                if (ui.audioEl.ended) return;
            });
        }
    }

    function getPlaybackRate() {
        if (ui.rateSelect) return parseFloat(ui.rateSelect.value, 10) || 1;
        return 1;
    }

    function showPlayer() {
        if (ui.speakBtn) ui.speakBtn.hidden = true;
        if (ui.stopBtn) ui.stopBtn.hidden = true;
        if (ui.playerSlot) ui.playerSlot.hidden = false;
    }

    function hidePlayer() {
        if (ui.speakBtn) ui.speakBtn.hidden = false;
        if (ui.playerSlot) ui.playerSlot.hidden = true;
        if (ui.audioEl) {
            ui.audioEl.pause();
            ui.audioEl.removeAttribute('src');
            ui.audioEl.load();
        }
    }

    function stop() {
        speaking = false;
        onEndCallback = null;
        if (currentAudio) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
            currentAudio.onended = null;
            currentAudio.onerror = null;
            currentAudio = null;
        }
        if (ui.audioEl) {
            ui.audioEl.pause();
            ui.audioEl.currentTime = 0;
        }
        hidePlayer();
    }

    function finish() {
        speaking = false;
        var cb = onEndCallback;
        onEndCallback = null;
        currentAudio = null;
        if (cb) cb();
    }

    function playSegmentQueue(paths, options, index) {
        if (!paths || index >= paths.length) {
            finish();
            return;
        }
        var relativePath = paths[index];
        var url = resolveUrl(relativePath);
        var rate = getPlaybackRate();
        var audio = ui.audioEl || new Audio();

        audio.playbackRate = rate;
        audio.src = url;
        currentAudio = audio;

        audio.onerror = function () {
            if (options.onMissing) options.onMissing(relativePath);
            else alert('Chưa có file âm thanh: ' + relativePath + '\n\nChạy "Tạo lại toàn bộ audio" trên trang chủ.');
            hidePlayer();
            finish();
        };
        audio.onended = function () {
            playSegmentQueue(paths, options, index + 1);
        };

        var playPromise = audio.play();
        if (playPromise && playPromise.catch) {
            playPromise.catch(function () {
                alert('Không phát được âm thanh. Mở trang qua http://localhost:5500');
                hidePlayer();
                finish();
            });
        }
    }

    function playFile(relativePathOrList, options) {
        options = options || {};
        bindPlayerUi(options);
        stop();
        speaking = true;
        onEndCallback = options.onEnd || null;

        var paths = Array.isArray(relativePathOrList) ? relativePathOrList : [relativePathOrList];

        if (ui.audioEl && ui.playerSlot) {
            showPlayer();
            playSegmentQueue(paths, options, 0);
            return;
        }

        playSegmentQueue(paths, options, 0);
    }

    function speak(options) {
        options = options || {};
        if (!options.page && !options.audioUrl) return;

        loadManifest().then(function () {
            var paths = options.audioUrl
                ? [options.audioUrl]
                : lookupAudioPaths(options.page, String(options.key));
            playFile(paths, options);
        });
    }

    function speakSlide(page, slideIndex, callbacks) {
        var opts = {
            page: page,
            key: String(slideIndex),
            onEnd: callbacks && callbacks.onEnd,
            onMissing: callbacks && callbacks.onMissing
        };
        if (callbacks && callbacks.speakBtn) opts.speakBtn = callbacks.speakBtn;
        speak(opts);
    }

    function reloadManifest() {
        manifest = null;
        manifestLoading = null;
        return loadManifest();
    }

    global.VietnameseTTS = {
        speak: speak,
        speakSlide: speakSlide,
        stop: stop,
        bindPlayerUi: bindPlayerUi,
        isSpeaking: function () {
            return speaking;
        },
        preloadManifest: loadManifest,
        reloadManifest: reloadManifest
    };

    loadManifest();
})(typeof window !== 'undefined' ? window : this);
