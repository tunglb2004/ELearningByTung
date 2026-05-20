/**
 * Lộ trình khóa học — trang chủ & sidebar bài học.
 */
(function (global) {
    'use strict';

    var LESSONS = [
        {
            page: 'oop1',
            href: 'part1_oop_principles.html',
            num: 'JC1',
            module: 'Java Core · Phần 1',
            title: 'OOP Principles',
            duration: '~35 phút',
            javaCore: true
        },
        {
            page: 'java2',
            href: 'java_core_phase2_collections.html',
            num: 'JC2',
            module: 'Java Core · Phần 2',
            title: 'Collections',
            duration: '~40 phút',
            javaCore: true
        },
        {
            page: 'java34',
            href: 'java_core_phase3_4_advanced.html',
            num: 'JC3',
            module: 'Java Core · Phần 3–4',
            title: 'Advanced Java',
            duration: '~45 phút',
            javaCore: true
        },
        {
            page: 'video1',
            href: 'video1_manual_vs_automation.html',
            num: '1',
            module: 'PHASE 1',
            title: 'Manual vs Automation',
            duration: '~25 phút'
        },
        {
            page: 'video2',
            href: 'video2_4_types_testing.html',
            num: '2',
            module: 'PHASE 1',
            title: '4 Loại Test',
            duration: '~30 phút'
        },
        {
            page: 'phase2',
            href: 'phase2_selenium_webdriver.html',
            num: '3',
            module: 'PHASE 2',
            title: 'Selenium WebDriver',
            duration: '~70 phút'
        },
        {
            page: 'phase3',
            href: 'phase3_testng_pom.html',
            num: '4',
            module: 'PHASE 3',
            title: 'TestNG & POM',
            duration: '~90 phút'
        },
        {
            page: 'phase4',
            href: 'phase4_advanced_cicd.html',
            num: '5',
            module: 'PHASE 4',
            title: 'Advanced & CI/CD',
            duration: '~120 phút'
        },
        {
            page: 'api1',
            href: 'api_testing_buoi1_fundamentals.html',
            num: 'API1',
            module: 'API Testing · Buổi 1',
            title: 'Fundamentals & HTTP',
            duration: '~5 giờ',
            apiTesting: true
        },
        {
            page: 'api2',
            href: 'api_testing_advanced_auth.html',
            num: 'API2',
            module: 'API Testing · Tuần 3-4',
            title: 'Auth & Security',
            duration: '~4 giờ',
            apiTesting: true
        },
        {
            page: 'api3',
            href: 'api_testing_restassured.html',
            num: 'API3',
            module: 'API Testing · RestAssured',
            title: 'RestAssured Automation',
            duration: '~4 giờ',
            apiTesting: true
        }
    ];

    function lessonBadge(lesson) {
        if (lesson.num && String(lesson.num).indexOf('JC') === 0) {
            return lesson.num + ' · ' + lesson.module;
        }
        if (lesson.apiTesting && lesson.num) {
            return lesson.num + ' · ' + lesson.module;
        }
        return 'Bài ' + lesson.num + ' · ' + lesson.module;
    }

    function renderSidebarNav(container) {
        var current = document.body.dataset.ttsPage || '';
        var html = '<h3 class="course-nav-heading">📚 Lộ trình khóa học</h3><ul class="course-nav-lessons">';
        LESSONS.forEach(function (lesson) {
            if (lesson.page === current) {
                html +=
                    '<li><span class="current-lesson" aria-current="page">' +
                    '<span class="lesson-module">' +
                    lessonBadge(lesson) +
                    '</span><span class="lesson-title">' +
                    lesson.title +
                    ' (đang học)</span></span></li>';
            } else {
                html +=
                    '<li><a href="' +
                    lesson.href +
                    '"><span class="lesson-module">' +
                    lessonBadge(lesson) +
                    '</span><span class="lesson-title">' +
                    lesson.title +
                    '</span></a></li>';
            }
        });
        html +=
            '<li><a href="index.html"><span class="lesson-title">🏠 Trang chủ khóa học</span></a></li></ul>';
        container.innerHTML = html;
        container.classList.add('sidebar-section', 'course-nav-wrap');
    }

    function renderRoadmapGroup(title, items) {
        var html =
            '<div class="course-roadmap-group"><h3 class="course-roadmap-group-title">' +
            title +
            '</h3><ol class="course-roadmap-list">';
        items.forEach(function (lesson) {
            var cls =
                'course-roadmap-item' +
                (lesson.javaCore ? ' java-core' : '') +
                (lesson.apiTesting ? ' api-testing' : '');
            html +=
                '<li><a class="' +
                cls +
                '" href="' +
                lesson.href +
                '"><span class="course-roadmap-num">' +
                lesson.num +
                '</span><span class="course-roadmap-body"><span class="course-roadmap-module">' +
                lesson.module +
                '</span><span class="course-roadmap-title">' +
                lesson.title +
                '</span><span class="course-roadmap-meta">' +
                lesson.duration +
                '</span></span><span class="course-roadmap-arrow" aria-hidden="true">→</span></a></li>';
        });
        return html + '</ol></div>';
    }

    function renderHomeRoadmap(container) {
        var javaLessons = LESSONS.filter(function (l) {
            return l.javaCore;
        });
        var autoLessons = LESSONS.filter(function (l) {
            return !l.javaCore && !l.apiTesting;
        });
        var apiLessons = LESSONS.filter(function (l) {
            return l.apiTesting;
        });
        var html =
            '<h2>📋 Lộ trình học (theo thứ tự)</h2>' +
            '<p class="roadmap-hint">Học <strong>JC1 → JC3</strong>, Automation <strong>bài 1 → 5</strong>, rồi API Testing <strong>API1 → API3</strong>.</p>';
        html += renderRoadmapGroup('☕ Java Core (3 bài)', javaLessons);
        html += renderRoadmapGroup('🔌 API Testing (3 bài)', apiLessons);
        html += renderRoadmapGroup('🤖 Automation Testing (5 bài)', autoLessons);
        container.innerHTML = html;
        container.classList.add('course-roadmap');
    }

    function setActiveSlide(index) {
        var links = document.querySelectorAll('.slide-nav-section .nav-links a');
        for (var i = 0; i < links.length; i++) {
            links[i].classList.toggle('active', i === index);
        }
    }

    function initSlideNavLinks() {
        var links = document.querySelectorAll('.slide-nav-section .nav-links a');
        for (var i = 0; i < links.length; i++) {
            (function (idx) {
                links[idx].addEventListener('click', function () {
                    setActiveSlide(idx);
                });
            })(i);
        }
        setActiveSlide(0);
    }

    function init() {
        var home = document.getElementById('courseRoadmap');
        if (home) {
            renderHomeRoadmap(home);
        }
        var slots = document.querySelectorAll('[data-course-nav]');
        for (var i = 0; i < slots.length; i++) {
            renderSidebarNav(slots[i]);
        }
        if (document.querySelector('.slide-nav-section')) {
            initSlideNavLinks();
        }
        
        // Reset audio player khi chuyển trang
        var lessonLinks = document.querySelectorAll('a[href*=".html"]');
        for (var i = 0; i < lessonLinks.length; i++) {
            lessonLinks[i].addEventListener('click', function () {
                if (typeof VietnameseTTS !== 'undefined' && VietnameseTTS.resetOnPageChange) {
                    VietnameseTTS.resetOnPageChange();
                }
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    global.CourseNav = { lessons: LESSONS, setActiveSlide: setActiveSlide };
})(typeof window !== 'undefined' ? window : global);
