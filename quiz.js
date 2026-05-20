/**
 * Kiểm tra kiến thức — trắc nghiệm theo bài học
 */
(function (global) {
    'use strict';

    var state = {
        step: 'lessons',
        lessonId: null,
        answers: {}
    };

    function el(id) {
        return document.getElementById(id);
    }

    function lessonClass(lesson) {
        if (lesson.javaCore) return 'java';
        if (lesson.apiTesting) return 'api';
        return '';
    }

    function renderLessons() {
        var panel = el('quizPanel');
        var lessons = global.CourseQuiz.lessons;
        var html =
            '<h2>📚 Chọn bài học</h2>' +
            '<p class="quiz-hint">Mỗi bài có <strong>20 câu</strong> trắc nghiệm (chọn 1 đáp án). ' +
            'Câu hỏi theo kiểu phỏng vấn — dựa trên nội dung slide của bài.</p>' +
            '<ul class="quiz-lesson-list">';
        lessons.forEach(function (lesson) {
            var qCount =
                global.CourseQuiz.banks[lesson.id] &&
                global.CourseQuiz.banks[lesson.id].questions
                    ? global.CourseQuiz.banks[lesson.id].questions.length
                    : 0;
            html +=
                '<li><button type="button" class="quiz-lesson-btn ' +
                lessonClass(lesson) +
                '" data-lesson="' +
                lesson.id +
                '">' +
                '<span class="quiz-lesson-num">' +
                lesson.num +
                '</span>' +
                '<span class="quiz-lesson-body">' +
                '<span class="quiz-lesson-module">' +
                lesson.module +
                '</span>' +
                '<span class="quiz-lesson-title">' +
                lesson.title +
                '</span>' +
                '<span class="quiz-lesson-meta">' +
                qCount +
                ' câu hỏi</span>' +
                '</span></button></li>';
        });
        html += '</ul>';
        panel.innerHTML = html;

        panel.querySelectorAll('.quiz-lesson-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                startQuiz(btn.getAttribute('data-lesson'));
            });
        });

        el('quizBackBtn').classList.add('quiz-hidden');
        el('quizSubmitBtn').classList.add('quiz-hidden');
    }

    function startQuiz(lessonId) {
        var bank = global.CourseQuiz.banks[lessonId];
        if (!bank || !bank.questions.length) {
            alert('Chưa có bộ câu hỏi cho bài này.');
            return;
        }
        state.step = 'quiz';
        state.lessonId = lessonId;
        state.answers = {};
        renderQuiz();
        el('quizBackBtn').classList.remove('quiz-hidden');
        el('quizSubmitBtn').classList.remove('quiz-hidden');
    }

    function renderQuiz() {
        var bank = global.CourseQuiz.banks[state.lessonId];
        var lesson = global.CourseQuiz.lessons.find(function (l) {
            return l.id === state.lessonId;
        });
        var panel = el('quizPanel');
        var answered = Object.keys(state.answers).length;
        var total = bank.questions.length;

        var html =
            '<div class="quiz-quiz-header">' +
            '<div><h2>🎯 ' +
            (lesson ? lesson.title : '') +
            '</h2>' +
            '<p class="quiz-hint">' +
            (lesson ? lesson.module : '') +
            ' — Chỉ chọn <strong>một</strong> đáp án cho mỗi câu.</p></div>' +
            '<div class="quiz-progress-text">Đã trả lời: ' +
            answered +
            ' / ' +
            total +
            '</div></div>';

        bank.questions.forEach(function (q, qi) {
            var sel = state.answers[qi];
            var cardClass = 'quiz-question-card';
            if (sel !== undefined) cardClass += ' answered';
            html += '<div class="' + cardClass + '" data-q="' + qi + '">';
            html += '<div class="quiz-q-num">Câu ' + (qi + 1) + '</div>';
            html += '<div class="quiz-q-text">' + escapeHtml(q.q) + '</div>';
            html += '<ul class="quiz-options">';
            q.options.forEach(function (opt, oi) {
                var selected = sel === oi ? ' selected' : '';
                var checked = sel === oi ? ' checked' : '';
                html +=
                    '<li><label class="quiz-option' +
                    selected +
                    '">' +
                    '<input type="radio" name="q' +
                    qi +
                    '" value="' +
                    oi +
                    '"' +
                    checked +
                    '>' +
                    '<span class="quiz-option-label">' +
                    escapeHtml(opt) +
                    '</span></label></li>';
            });
            html += '</ul></div>';
        });

        panel.innerHTML = html;

        panel.querySelectorAll('.quiz-option input').forEach(function (input) {
            input.addEventListener('change', function () {
                var card = input.closest('.quiz-question-card');
                var qi = parseInt(card.getAttribute('data-q'), 10);
                state.answers[qi] = parseInt(input.value, 10);
                card.classList.add('answered');
                card.classList.remove('unanswered-warning');
                card.querySelectorAll('.quiz-option').forEach(function (lab) {
                    lab.classList.remove('selected');
                });
                input.closest('.quiz-option').classList.add('selected');
                var bank2 = global.CourseQuiz.banks[state.lessonId];
                var prog = el('quizProgress');
                if (prog) {
                    prog.textContent =
                        'Đã trả lời: ' +
                        Object.keys(state.answers).length +
                        ' / ' +
                        bank2.questions.length;
                }
            });
        });

        var headerProg = panel.querySelector('.quiz-progress-text');
        if (headerProg) headerProg.id = 'quizProgress';
    }

    function escapeHtml(s) {
        var d = document.createElement('div');
        d.textContent = s;
        return d.innerHTML;
    }

    function submitQuiz() {
        var bank = global.CourseQuiz.banks[state.lessonId];
        var total = bank.questions.length;
        var missing = [];
        for (var i = 0; i < total; i++) {
            if (state.answers[i] === undefined) missing.push(i + 1);
        }
        if (missing.length) {
            missing.forEach(function (n) {
                var card = document.querySelector('.quiz-question-card[data-q="' + (n - 1) + '"]');
                if (card) card.classList.add('unanswered-warning');
            });
            alert('Bạn chưa trả lời câu: ' + missing.join(', ') + '. Vui lòng hoàn thành tất cả 20 câu.');
            return;
        }

        var correct = 0;
        bank.questions.forEach(function (q, qi) {
            if (state.answers[qi] === q.answer) correct++;
        });

        state.step = 'results';
        renderResults(correct, total);
        el('quizSubmitBtn').classList.add('quiz-hidden');
    }

    function renderResults(correct, total) {
        var bank = global.CourseQuiz.banks[state.lessonId];
        var lesson = global.CourseQuiz.lessons.find(function (l) {
            return l.id === state.lessonId;
        });
        var pct = Math.round((correct / total) * 100);
        var pass = pct >= 70;
        var panel = el('quizPanel');

        var html =
            '<h2>📊 Kết quả — ' +
            (lesson ? lesson.title : '') +
            '</h2>' +
            '<div class="quiz-score-box ' +
            (pass ? 'pass' : 'fail') +
            '">' +
            '<div class="score-value">' +
            correct +
            '/' +
            total +
            '</div>' +
            '<div class="score-label">Điểm: <strong>' +
            pct +
            '%</strong>' +
            (pass ? ' — Đạt yêu cầu (≥70%)' : ' — Cần ôn lại bài học') +
            '</div></div>' +
            '<p class="quiz-hint">Chi tiết từng câu (đáp án đúng + giải thích):</p>';

        bank.questions.forEach(function (q, qi) {
            var user = state.answers[qi];
            var ok = user === q.answer;
            if (!ok) {
                /* already counted */
            }
            html +=
                '<div class="quiz-result-item ' +
                (ok ? 'correct' : 'wrong') +
                '">' +
                '<div class="result-q">Câu ' +
                (qi + 1) +
                ': ' +
                escapeHtml(q.q) +
                '</div>' +
                '<div class="result-answer">Bạn chọn: <strong>' +
                escapeHtml(q.options[user]) +
                '</strong></div>';
            if (!ok) {
                html +=
                    '<div class="result-answer">Đáp án đúng: <strong>' +
                    escapeHtml(q.options[q.answer]) +
                    '</strong></div>';
            } else {
                html += '<div class="result-answer">✓ Chính xác</div>';
            }
            if (q.explain) {
                html +=
                    '<div class="result-explain">💡 ' + escapeHtml(q.explain) + '</div>';
            }
            html += '</div>';
        });

        panel.innerHTML = html;
    }

    function goBack() {
        if (state.step === 'quiz') {
            if (
                Object.keys(state.answers).length &&
                !confirm('Quay lại sẽ mất câu trả lời hiện tại. Tiếp tục?')
            ) {
                return;
            }
            state.step = 'lessons';
            state.lessonId = null;
            state.answers = {};
            renderLessons();
            el('quizSubmitBtn').classList.add('quiz-hidden');
            el('quizBackBtn').classList.remove('quiz-hidden');
            el('quizBackBtn').textContent = '← Trang chủ';
            return;
        }
        if (state.step === 'results') {
            state.step = 'lessons';
            state.lessonId = null;
            state.answers = {};
            renderLessons();
            el('quizSubmitBtn').classList.add('quiz-hidden');
            el('quizBackBtn').textContent = '← Trang chủ';
            return;
        }
        window.location.href = 'index.html';
    }

    function init() {
        if (!global.CourseQuiz) {
            el('quizPanel').innerHTML =
                '<p>Không tải được dữ liệu câu hỏi. Kiểm tra file quiz-data.js</p>';
            return;
        }

        var params = new URLSearchParams(window.location.search);
        var lesson = params.get('lesson');
        el('quizBackBtn').addEventListener('click', goBack);
        el('quizSubmitBtn').addEventListener('click', submitQuiz);

        if (lesson && global.CourseQuiz.banks[lesson]) {
            el('quizBackBtn').textContent = '← Chọn bài khác';
            startQuiz(lesson);
        } else {
            el('quizBackBtn').textContent = '← Trang chủ';
            renderLessons();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(typeof window !== 'undefined' ? window : global);
