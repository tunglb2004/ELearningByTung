#!/usr/bin/env python3
"""Emit generate_quiz_banks.py containing only BANKS = {...}."""
from __future__ import annotations

import pprint
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "generate_quiz_banks.py"


def q(question: str, options: list[str], answer: int, explain: str) -> dict:
    if len(options) != 4:
        raise ValueError(f"Need 4 options: {question[:50]}")
    if answer not in (0, 1, 2, 3):
        raise ValueError(f"answer must be 0-3: {question[:50]}")
    return {"q": question, "options": options, "answer": answer, "explain": explain}


def _java34() -> dict:
    return {
        "title": "Advanced Java",
        "questions": [
            q(
                "Checked exception khác unchecked exception ở điểm nào quan trọng trong thiết kế API test helper?",
                [
                    "Checked bắt buộc khai báo/handle compile-time (IOException); unchecked kế thừa RuntimeException",
                    "Checked không cần try-catch; unchecked bắt buộc throws",
                    "Chỉ unchecked mới dùng được trong interface",
                    "Checked chỉ xảy ra ở main thread",
                ],
                0,
                "IOException, SQLException là checked — caller phải xử lý. NullPointerException, IllegalArgumentException là unchecked — thường báo lỗi lập trình hoặc precondition.",
            ),
            q(
                "try-with-resources (Java 7+) giải quyết vấn đề gì khi đọc file test data hoặc properties?",
                [
                    "Tự đóng AutoCloseable (Reader, Stream) kể cả khi có exception — tránh leak handle",
                    "Tự động retry khi file không tồn tại",
                    "Chuyển checked exception thành unchecked",
                    "Bắt buộc file phải nằm trong classpath module",
                ],
                0,
                "try (BufferedReader br = ...) { } gọi close() trong finally ẩn. Quan trọng khi chạy suite lớn trên CI để không cạn file descriptor.",
            ),
            q(
                "Generics List<String> khác List raw type khi refactor framework automation?",
                [
                    "Generic giữ type safety compile-time — tránh ClassCastException khi lấy phần tử",
                    "Generic chỉ chạy nhanh hơn, không liên quan type",
                    "Raw type bắt buộc cho WebDriver",
                    "List<String> không cho phép null",
                ],
                0,
                "Type erasure runtime vẫn là List nhưng compiler kiểm tra gán/phép. Raw type mất cảnh báo khi mix kiểu.",
            ),
            q(
                "? extends T (covariant) cho phép đọc hay ghi an toàn?",
                [
                    "Đọc được T (producer); không add phần tử cụ thể (trừ null) — PECS: Producer Extends",
                    "Ghi được mọi subtype; không đọc được",
                    "Vừa đọc vừa ghi thoải mái như List<T>",
                    "Chỉ dùng với primitive",
                ],
                0,
                "List<? extends Number> nhận Integer/Double list; get() trả Number. add() bị hạn chế vì không biết subtype thực.",
            ),
            q(
                "Stream pipeline filter().map().collect() lazy evaluation nghĩa là gì?",
                [
                    "Intermediate operation chỉ chạy khi terminal operation (collect, forEach) được gọi",
                    "Mọi phần tử luôn materialize ngay khi gọi filter",
                    "Stream luôn chạy song song mặc định",
                    "collect() không phải terminal operation",
                ],
                0,
                "Tối ưu fusion — không duyệt list nhiều lần không cần thiết. Với data test lớn, chọn terminal phù hợp (toList Java 16+).",
            ),
            q(
                "Optional<T> trong Java 8+ nên dùng thế nào trong service layer (phỏng vấn)?",
                [
                    "Thể hiện giá trị có thể vắng — tránh null trả về mơ hồ; không lạm dụng cho field/mọi tham số",
                    "Thay thế hoàn toàn mọi null trong JVM",
                    "Bắt buộc cho mọi return type primitive",
                    "Optional.get() luôn an toàn không cần isPresent",
                ],
                0,
                "Optional.ofNullable/find — map/orElse/orElseThrow. Anti-pattern: Optional cho field hoặc collection element hàng loạt.",
            ),
            q(
                "Lambda (a, b) -> a + b yêu cầu interface đích loại gì?",
                [
                    "Functional interface — đúng một abstract method (ví dụ Comparator, Predicate)",
                    "Mọi class abstract",
                    "Chỉ interface có default method",
                    "Chỉ enum",
                ],
                0,
                "@FunctionalInterface — SAM. Dùng gọn cho stream filter, custom wait condition, callback listener trong test util.",
            ),
            q(
                "Method reference String::length tương đương lambda nào?",
                ["s -> s.length()", "s -> String.length(s)", "() -> s.length()", "String::new"],
                0,
                "Four kinds: static, instance bound, instance arbitrary, constructor. Giúp code ngắn khi lambda chỉ gọi một method có sẵn.",
            ),
            q(
                "synchronized block trên object intrinsic lock đảm bảo gì?",
                [
                    "Mutual exclusion — chỉ một thread vào critical section trên cùng lock tại một thời điểm",
                    "Thread pool tự scale",
                    "Thứ tự global của mọi lock trong JVM",
                    "Tự động fix race trên volatile field không cần sync",
                ],
                0,
                "Dùng khi shared mutable state (counter, cache map) giữa thread trong parallel test — cân nhắc ConcurrentHashMap thay sync toàn method.",
            ),
            q(
                "volatile đảm bảo visibility thế nào so với synchronized?",
                [
                    "Ghi volatile flush đến main memory; đọc thấy giá trị mới nhất — không đảm bảo compound atomic (i++)",
                    "volatile thay thế mọi synchronized",
                    "volatile chỉ cho static field",
                    "volatile lock toàn bộ class",
                ],
                0,
                "Happens-before giữa write/read volatile. Flag stop test worker: volatile boolean đủ; increment shared counter: cần AtomicInteger hoặc sync.",
            ),
            q(
                "ExecutorService submit(Callable) khác new Thread().start() ở lợi ích automation?",
                [
                    "Quản lý pool, tái sử dụng thread, Future lấy kết quả/exception — kiểm soát tài nguyên CI",
                    "Luôn chạy tuần tự một thread",
                    "Không bắt được exception từ task",
                    "Chỉ dùng được trên main thread",
                ],
                0,
                "Parallel run method @Test — pool size = số browser. shutdown() và awaitTermination tránh zombie thread khi suite kết thúc.",
            ),
            q(
                "enum trong Java có thể chứa gì ngoài hằng số?",
                [
                    "Field, constructor, method, implement interface — type-safe constant cho browser/env",
                    "Chỉ tên constant, không có method",
                    "Không implements interface được",
                    "Không dùng trong switch",
                ],
                0,
                "BrowserType.CHROME.getDriverPath() pattern. Enum singleton thread-safe cho config holder.",
            ),
            q(
                "Record (Java 16+) phù hợp mô hình hóa gì trong test data?",
                [
                    "Immutable data carrier — DTO response API với equals/hashCode/toString sinh sẵn",
                    "Thay thế Thread class",
                    "Class có mutable state và inheritance sâu",
                    "Chỉ dùng cho exception",
                ],
                0,
                "record User(String email, int id) gọn cho parse JSON → assert. Không thay entity JPA phức tạp.",
            ),
            q(
                "Exception trong constructor của subclass: quy tắc gọi super()?",
                [
                    "super() phải là dòng đầu (hoặc super(args)) trước logic khác nếu có constructor cha",
                    "Không cần gọi super khi có throws",
                    "Chỉ interface mới có constructor",
                    "finally chạy trước constructor",
                ],
                0,
                "Khởi tạo object: cha trước con. Nếu cha throws, con phải khai báo/handle. Page object base có thể throw khi driver null.",
            ),
            q(
                "Multi-catch catch (IOException | SQLException e) lợi ích gì?",
                [
                    "Một block xử lý nhiều checked type; e effectively final — code gọn",
                    "Bắt mọi Error và OOM",
                    "Tự động retry network",
                    "Chuyển thành unchecked",
                ],
                0,
                "Java 7+. Không đặt subclass và superclass cùng catch. Log và rethrow wrapped trong util đọc config.",
            ),
            q(
                "Assertions (assert keyword) vs TestNG Assert trong production test code?",
                [
                    "assert JVM có thể tắt (-ea); framework assert luôn chạy và tích hợp report — dùng Assert trong test",
                    "Giống hệt nhau trong CI",
                    "assert keyword sinh HTML report",
                    "TestNG Assert chỉ compile với -ea",
                ],
                0,
                "java assert cho invariant nội bộ dev. TestNG/JUnit Assert.fail, assertEquals là chuẩn automation assertion.",
            ),
            q(
                "String immutability ảnh hưởng builder pattern test log thế nào?",
                [
                    "Nối chuỗi nhiều trong loop nên dùng StringBuilder — tránh O(n²) copy",
                    "String luôn mutable qua concat",
                    "StringBuilder không thread-safe nên không dùng được",
                    "Immutable nghĩa là không so sánh được",
                ],
                0,
                "String pool và immutability an toàn key map. Log steps: StringBuilder hoặc formatted slf4j {}.",
            ),
            q(
                "Comparable vs Comparator khi sort danh sách test case theo priority?",
                [
                    "Comparable natural order trong class (compareTo); Comparator tách logic sort ngoài (lambda)",
                    "Comparator bắt buộc trong mọi class",
                    "Comparable chỉ cho primitive",
                    "TreeSet chỉ dùng Comparator, không Comparable",
                ],
                0,
                "Arrays.sort(list, Comparator.comparing(TestCase::getPriority)). TreeSet/TreeMap cần một trong hai.",
            ),
            q(
                "Module system JPMS (Java 9+) liên quan automation project thế nào?",
                [
                    "module-info exports/requires kiểm soát visibility — ảnh hưởng split package và reflective access (Selenium)",
                    "Bắt buộc mọi Maven project phải modular",
                    "Cấm classpath",
                    "Thay thế Maven",
                ],
                0,
                "Nhiều project classic vẫn classpath. Biết JPMS khi lỗi 'module not found' hoặc illegal reflective access trên JDK 17+.",
            ),
            q(
                "Garbage Collection: object không reference có chắc bị thu ngay lập tức?",
                [
                    "Không — GC non-deterministic; finalize deprecated; không dùng GC để đóng resource (dùng try-with-resources)",
                    "Có, ngay sau null gán",
                    "System.gc() đảm bảo thu hồi 100%",
                    "WebDriver quit() gọi GC thay vì native",
                ],
                0,
                "driver.quit() giải phóng process browser — không phụ thuộc GC. WeakReference hiếm dùng trong test trừ cache image.",
            ),
        ],
    }


def _video1() -> dict:
    return {
        "title": "Manual vs Automation",
        "questions": [
            q(
                "Tiêu chí nào NÊN ưu tiên trước khi quyết định automate một test case?",
                [
                    "Ổn định, lặp lại cao, ROI rõ, data deterministic — không automate exploratory một lần",
                    "Automate tất cả case manual để giảm headcount ngay",
                    "Chỉ automate UI phức tạp nhất",
                    "Chỉ automate khi không có tài liệu requirement",
                ],
                0,
                "Automation đắt bảo trì. Case flaky, UI đổi liên tục, judgment-heavy → manual/exploratory phù hợp hơn.",
            ),
            q(
                "Test pyramid khuyến nghị tỷ lệ nào (Mike Cohn) cho dự án healthy?",
                [
                    "Nhiều unit, ít integration, ít UI E2E — UI ít nhưng giá trị cao",
                    "100% UI E2E vì sát user nhất",
                    "Chỉ manual, không unit",
                    "Chỉ API, bỏ unit và UI",
                ],
                0,
                "UI chậm, brittle. Unit/API nhanh feedback. Pyramid tránh 'ice cream cone' toàn E2E chậm CI.",
            ),
            q(
                "Manual exploratory testing bổ sung automation ở điểm nào?",
                [
                    "Phát hiện risk/edge không spec — học hệ thống, charter, session-based",
                    "Thay thế regression hoàn toàn",
                    "Không cần khi đã có Selenium",
                    "Chỉ chạy một lần trước release rồi bỏ",
                ],
                0,
                "Automation kiểm tra đã biết (known). Exploratory tìm unknown. Cả hai cần trong chiến lược QA.",
            ),
            q(
                "Regression manual tốn kém nhất ở khâu nào so với automation đã ổn?",
                [
                    "Lặp lại cùng bộ case mỗi sprint/release — thời gian và sai sót con người",
                    "Thiết kế case đầu tiên",
                    "Viết bug report",
                    "Đọc requirement lần đầu",
                ],
                0,
                "Automation shine ở repeatable regression. Manual vẫn cần cho usability và case mới chưa script hóa.",
            ),
            q(
                "Flaky test trong automation thường do nguyên nhân nào (phỏng vấn senior)?",
                [
                    "Timing/async, data phụ thuộc, môi trường, locator brittle — không chỉ 'tool lỗi'",
                    "Chỉ do Selenium version cũ",
                    "Do manual tester chạy nhầm",
                    "Do unit test quá nhiều",
                ],
                0,
                "Fix: explicit wait, isolate data, stable locator, retry có kiểm soát, quarantine flake trên dashboard.",
            ),
            q(
                "ROI automation xấp xỉ tính bằng công thức nào?",
                [
                    "(Thời gian manual × số lần chạy) − (thời gian dev + bảo trì script) — breakeven khi vượt chi phí tạo",
                    "Số dòng code / số bug",
                    "Số tester / số developer",
                    "Không thể ước lượng",
                ],
                0,
                "Case chạy 1 lần/năm khó hoàn vốn. Smoke hàng ngày trên 50 case — automation rõ ràng.",
            ),
            q(
                "Automation không thay thế được hoạt động QA nào?",
                [
                    "Đánh giá UX, accessibility sâu, ethics, context business judgment",
                    "Chạy API contract test",
                    "So sánh JSON response",
                    "Load test cơ bản",
                ],
                0,
                "Tool không 'cảm' UI awkward. Human review usability, visual polish, domain rules mơ hồ.",
            ),
            q(
                "Shift-left trong manual vs automation nghĩa là gì?",
                [
                    "Tester tham gia sớm requirement/review; automate sớm ở API/unit trước UI hoàn thiện",
                    "Chỉ test sau production",
                    "Dời hết test sang UAT",
                    "Bỏ manual hoàn toàn ở design",
                ],
                0,
                "Phát hiện defect rẻ hơn khi còn spec. ATDD/BDD gắn acceptance sớm với dev.",
            ),
            q(
                "Record-and-playback tool (Katalon/Selenium IDE) hạn chế gì so code-based?",
                [
                    "Script fragile, khó refactor, version control/CI kém — học được flow nhưng scale kém",
                    "Không record được click",
                    "Không chạy trên Chrome",
                    "Luôn ổn định hơn code",
                ],
                0,
                "Tốt prototype. Production framework: code + POM + CI pipeline.",
            ),
            q(
                "Khi nào manual vẫn bắt buộc dù đã có suite automation lớn?",
                [
                    "Feature mới chưa ổn định, cần học domain, ad-hoc investigation sau incident",
                    "Không bao giờ, automation đủ",
                    "Chỉ khi mất điện",
                    "Chỉ cho performance test",
                ],
                0,
                "Sau production bug — manual reproduce và explore. Automation khóa regression sau khi hiểu root cause.",
            ),
            q(
                "Definition of Done cho story thường gắn automation level nào?",
                [
                    "Unit + integration pass CI; critical path E2E/smoke green; manual charter nếu risk cao",
                    "Chỉ demo cho PO",
                    "Chỉ code review dev",
                    "100% coverage UI mọi pixel",
                ],
                0,
                "DoD team-specific. Tránh yêu cầu automate mọi AC nếu không bền.",
            ),
            q(
                "Maintenance cost automation chiếm phần lớn vòng đời vì sao?",
                [
                    "UI/API đổi → locator/assert/data lỗi thời — cần refactor liên tục như product code",
                    "Vì JVM license",
                    "Vì tester không đọc log",
                    "Vì manual không tốn bảo trì",
                ],
                0,
                "Budget 30–50% thời gian framework cho maintenance thực tế. POM và abstraction giảm churn.",
            ),
            q(
                "Smoke test manual vs automated smoke khác nhau thế nào?",
                [
                    "Cùng mục tiêu build deployable nhanh — automated smoke trên CI gate merge nhanh hơn manual",
                    "Smoke manual luôn 2 ngày",
                    "Automated smoke phải 500 case",
                    "Không liên quan release",
                ],
                0,
                "15–30 phút automated smoke sau deploy. Manual smoke khi chưa có infra hoặc kiểm tra cảm quan nhanh.",
            ),
            q(
                "Risk-based testing ảnh hưởng chọn manual/automation ra sao?",
                [
                    "Vùng risk cao + ổn định → automate regression; risk cao + chưa rõ → manual/exploratory trước",
                    "Risk thấp automate trước",
                    "Bỏ risk matrix",
                    "Chỉ dựa severity bug cũ",
                ],
                0,
                "Ma trận likelihood × impact ưu tiên effort. Không automate low-value path trước.",
            ),
            q(
                "Automation engineer vs manual QA: vai trò overlap ở đâu?",
                [
                    "Cùng thiết kế case, phân tích risk, báo cáo chất lượng — automation thêm coding/infra",
                    "Không overlap",
                    "Manual không viết test case",
                    "Automation không đọc requirement",
                ],
                0,
                "Modern QA T-shaped: hiểu test design + có thể code. Manual deep domain vẫn quý.",
            ),
            q(
                "CI/CD pipeline automation test fail nên làm gì đầu tiên?",
                [
                    "Xem artifact (screenshot, log, video), reproduce local, phân loại flake vs real bug",
                    "Xóa test ngay",
                    "Merge anyway",
                    "Tắt pipeline",
                ],
                0,
                "Quality gate: fail có lý do. Quarantine flake có ticket, không im lặng disable vĩnh viễn.",
            ),
            q(
                "Data setup cho automated test so manual execution?",
                [
                    "Automation cần deterministic data — API/DB seed, không phụ thuộc 'tài khoản tôi test hôm qua'",
                    "Dùng chung production data không sao",
                    "Không cần cleanup",
                    "Manual cũng không cần data plan",
                ],
                0,
                "@BeforeMethod tạo user, @AfterMethod xóa. Parallel cần data isolation per thread.",
            ),
            q(
                "Accessibility testing: automation hỗ trợ được mức nào?",
                [
                    "Axe/Lighthouse bắt vi phạm WCAG kỹ thuật; manual keyboard/screen reader vẫn cần",
                    "Selenium tự đủ WCAG AAA",
                    "Không test a11y được",
                    "Chỉ manual mới hợp pháp",
                ],
                0,
                "Hybrid: auto scan + manual journey critical flow (login, checkout).",
            ),
            q(
                "Khi product pivot UI lớn, chiến lược test team nào hợp lý?",
                [
                    "Tạm tăng manual/exploratory; stabilize locator layer; refactor POM — không chase automate hết ngay",
                    "Freeze mọi test",
                    "Automate tất cả trong 1 ngày",
                    "Bỏ regression",
                ],
                0,
                "Abstraction POM che UI change. Đợt đầu chấp nhận suite đỏ có kế hoạch sửa theo priority.",
            ),
            q(
                "Metric nào KHÔNG nên dùng đơn lẻ đánh giá thành công automation?",
                [
                    "Chỉ đếm số test case automated — bỏ qua pass rate, thời gian feedback, defect escaped",
                    "Thời gian chạy suite trên CI",
                    "Tỷ lệ pass/stable",
                    "Defect tìm được trên CI",
                ],
                0,
                "Số lượng ≠ chất lượng. 500 test flake 50% pass gây hại hơn 50 test ổn định.",
            ),
        ],
    }


def _video2() -> dict:
    return {
        "title": "4 Loại Test",
        "questions": [
            q(
                "Unit test trong pyramid kiểm tra phạm vi nào?",
                [
                    "Một đơn vị code cô lập (method/class) — mock dependency, nhanh, không UI/DB thật",
                    "Toàn bộ hệ thống E2E",
                    "Chỉ giao diện người dùng",
                    "Chỉ contract giữa microservice",
                ],
                0,
                "JUnit/TestNG + Mockito. Fail nhanh, localize bug. QA automation engineer vẫn nên hiểu để review dev test.",
            ),
            q(
                "Integration test khác unit ở boundary nào?",
                [
                    "Nhiều module/component phối hợp thật (DB, API layer) — không mock toàn bộ stack",
                    "Chỉ test getter/setter",
                    "Luôn qua browser",
                    "Không dùng database",
                ],
                0,
                "Ví dụ: repository + DB testcontainer. Bắt lỗi wiring, SQL, transaction.",
            ),
            q(
                "System test (end-to-end hệ thống) trong ngữ cảnh QA automation thường là gì?",
                [
                    "Luồng nghiệp vụ qua UI hoặc API full stack như user — môi trường gần production",
                    "Chỉ test một hàm static",
                    "Chỉ review code",
                    "Chỉ load test",
                ],
                0,
                "Selenium/API journey: đăng ký → đặt hàng → thanh toán. Chậm hơn unit nhưng confidence cao.",
            ),
            q(
                "Acceptance test (UAT/ATDD) ai thường là stakeholder chính?",
                [
                    "PO/BA/khách hàng xác nhận behavior đúng nghiệp vụ — có thể manual hoặc BDD automated",
                    "Chỉ developer unit test",
                    "Chỉ DBA",
                    "Chỉ security team pentest",
                ],
                0,
                "Gherkin Given-When-Then gắn acceptance criteria. Pass = ready for release từ góc business.",
            ),
            q(
                "Smoke test thuộc loại nào và mục tiêu gì?",
                [
                    "Tập nhỏ critical path — xác nhận build 'có thể test sâu hơn', không exhaustive",
                    "Full regression 8 giờ",
                    "Chỉ performance",
                    "Chỉ security scan",
                ],
                0,
                "Smoke fail → dừng pipeline. Khác sanity (rất hẹp sau hotfix).",
            ),
            q(
                "Regression test đảm bảo điều gì sau thay đổi code?",
                [
                    "Chức năng cũ không bị phá (unintended side effect) — chạy lại bộ case đã biết",
                    "Chỉ test feature mới",
                    "Chỉ test performance lần đầu",
                    "Không cần sau refactor",
                ],
                0,
                "Automated regression trên CI mỗi PR. Full regression có thể nightly.",
            ),
            q(
                "Functional test tập trung vào khía cạnh nào?",
                [
                    "Hành vi đúng requirement (black-box) — input/output theo spec",
                    "Cấu trúc byte code JVM",
                    "Màu sắc CSS pixel-perfect mọi browser",
                    "Chỉ đo RAM server",
                ],
                0,
                "Khác non-functional (performance, security). Functional = 'làm đúng việc'.",
            ),
            q(
                "Non-functional testing gồm ví dụ nào?",
                [
                    "Performance, security, usability, reliability, compatibility",
                    "Chỉ CRUD API",
                    "Chỉ unit Mockito",
                    "Chỉ viết test plan",
                ],
                0,
                "Load (JMeter/Gatling), penetration, a11y — bổ sung functional, không thay thế.",
            ),
            q(
                "Sanity test so với smoke trong thực tế team?",
                [
                    "Sanity hẹp hơn — kiểm tra vùng vừa sửa sau hotfix; smoke rộng hơn critical path build",
                    "Giống hệt nhau",
                    "Sanity luôn 3 ngày",
                    "Smoke chỉ manual",
                ],
                0,
                "Sau patch login bug — sanity login + logout. Smoke toàn app core flows.",
            ),
            q(
                "Positive vs negative testing trong functional?",
                [
                    "Positive: input hợp lệ, happy path; negative: invalid, boundary, unauthorized — cả hai bắt buộc",
                    "Chỉ positive đủ cho release",
                    "Negative chỉ pentest",
                    "Positive chỉ cho unit test",
                ],
                0,
                "Automation hay bỏ sót negative edge — checklist boundary, null, SQL injection field.",
            ),
            q(
                "Component test trong microservices nghĩa là gì?",
                [
                    "Test service trong isolation với dependency giả lập (wire mock) — giữa unit và full E2E",
                    "Test từng dòng Java",
                    "Chỉ UI test",
                    "Chỉ manual",
                ],
                0,
                "Contract test consumer-driven (Pact) đảm bảo API version tương thích.",
            ),
            q(
                "Alpha vs Beta testing?",
                [
                    "Alpha nội bộ/org; Beta limited external users — trước GA",
                    "Alpha trên production users",
                    "Beta chỉ automated",
                    "Không liên quan release",
                ],
                0,
                "Feedback thật từ user. Automation regression chạy trước alpha gate.",
            ),
            q(
                "Compatibility testing ví dụ automation cần cover?",
                [
                    "Browser/OS/device matrix — Selenium Grid hoặc cloud (BrowserStack)",
                    "Chỉ Chrome latest",
                    "Chỉ JDK version",
                    "Không cần cross-browser",
                ],
                0,
                "Matrix strategy: smoke all browsers, full regression Chrome + Firefox representative.",
            ),
            q(
                "Localization (L10n) test thuộc loại gì?",
                [
                    "Functional/i18n — format ngày, currency, chuỗi UI theo locale",
                    "Chỉ load test",
                    "Chỉ API status code",
                    "Chỉ unit test",
                ],
                0,
                "Assert label không truncate, RTL layout. Data-driven locale trong test.",
            ),
            q(
                "Ad-hoc testing khác exploratory có kế hoạch thế nào?",
                [
                    "Ad-hoc không charter — exploratory có mục tiêu, ghi chú, time-box",
                    "Ad-hoc luôn có script chi tiết",
                    "Exploratory không tìm bug",
                    "Cả hai chỉ automated",
                ],
                0,
                "Session-based exploratory: charter 90 phút, findings report.",
            ),
            q(
                "Re-test vs regression sau fix bug?",
                [
                    "Re-test: chạy lại case đã fail xác nhận fix; regression: rộng hơn đảm bảo không break chỗ khác",
                    "Giống nhau",
                    "Re-test chỉ dev làm",
                    "Regression chỉ một lần",
                ],
                0,
                "Ticket JIRA: verify fix + chạy suite liên quan module.",
            ),
            q(
                "Confirmation testing trong UAT là gì?",
                [
                    "Xác nhận hệ thống đáp ứng requirement đã agree — trước khi sign-off release",
                    "Xác nhận compiler pass",
                    "Chỉ test Jenkins file",
                    "Chỉ review Git diff",
                ],
                0,
                "Checklist acceptance criteria signed. Automated acceptance chạy trên staging.",
            ),
            q(
                "API test trong phân loại 4 loại course thường đặt ở tầng nào?",
                [
                    "Integration/system tùy phạm vi — contract/integration nhanh hơn UI E2E",
                    "Luôn unit test",
                    "Không thuộc automation",
                    "Chỉ manual Postman",
                ],
                0,
                "RestAssured hit API trực tiếp — feedback nhanh, ổn định hơn UI cho logic nghiệp vụ.",
            ),
            q(
                "Test case priority P0/P1 ảnh hưởng phân loại chạy thế nào?",
                [
                    "P0 smoke/critical — chạy mỗi commit; P1 regression; P2/P3 nightly hoặc release",
                    "Tất cả chạy 8 giờ mỗi commit",
                    "Priority không ảnh hưởng CI",
                    "Chỉ dùng cho manual",
                ],
                0,
                "TestNG groups=smoke vs regression. Fail P0 block merge.",
            ),
            q(
                "Tại sao hiểu 4 loại test giúp phỏng vấn QA automation?",
                [
                    "Chọn công cụ/level phù hợp, giải thích chiến lược pyramid và trade-off thời gian CI",
                    "Chỉ để đếm số bug",
                    "Không liên quan Selenium",
                    "Chỉ dùng cho manual tester",
                ],
                0,
                "Interviewer muốn thấy bạn không automate mù — map risk → test type → tool.",
            ),
        ],
    }


def _phase2() -> dict:
    return {
        "title": "Selenium WebDriver",
        "questions": [
            q(
                "WebDriver khác WebElement ở vai trò?",
                [
                    "WebDriver điều khiển browser (navigate, quit); WebElement đại diện DOM node tương tác",
                    "Cùng một interface",
                    "WebElement mở browser",
                    "WebDriver chỉ đọc attribute",
                ],
                0,
                "driver.get(url); element.click(). Một driver nhiều element. Thread-local driver trong parallel.",
            ),
            q(
                "By.id vs By.cssSelector — khi nào ưu tiên CSS?",
                [
                    "id ổn định unique thì tốt nhất; CSS linh hoạt attribute, không phụ thuộc XPath engine chậm tương đối",
                    "Luôn XPath vì ngắn",
                    "name luôn unique globally",
                    "tagName luôn đủ",
                ],
                0,
                "Ưu tiên: id > unique data-testid > CSS > XPath tương đối. Tránh index [3] brittle.",
            ),
            q(
                "Implicit wait set 10s ảnh hưởng findElement thế nào?",
                [
                    "Driver poll đến 10s trước NoSuchElementException — áp dụng mọi find sau khi set",
                    "Chỉ một lần per session",
                    "Thay thế Thread.sleep hoàn toàn cho mọi case",
                    "Chỉ cho alert",
                ],
                0,
                "Global setting. Không trộn nhiều implicit khác nhau. Explicit wait preferred cho điều kiện cụ thể.",
            ),
            q(
                "WebDriverWait + ExpectedConditions.elementToBeClickable lợi ích gì?",
                [
                    "Chờ điều kiện cụ thể với timeout — tránh flake hơn sleep cố định",
                    "Luôn chờ 30 giây mọi lúc",
                    "Bỏ qua StaleElementReferenceException",
                    "Không cần driver",
                ],
                0,
                "FluentWait polling interval, ignore exception. Pattern Page Object wrapper waitClickable(locator).",
            ),
            q(
                "StaleElementReferenceException xảy ra khi nào?",
                [
                    "DOM refresh sau khi lưu reference — element cũ không còn gắn document",
                    "Driver.quit() chưa gọi",
                    "Sai password login",
                    "ChromeDriver version mismatch",
                ],
                0,
                "Fix: re-find element, wait document ready, tránh lưu WebElement quá lâu qua AJAX re-render.",
            ),
            q(
                "driver.switchTo().frame() cần khi nào?",
                [
                    "Element nằm trong iframe — phải switch context trước interact",
                    "Mọi trang đều cần",
                    "Chỉ popup window",
                    "Chỉ shadow DOM",
                ],
                0,
                "defaultContent() quay ra. Nested frame switch tuần tự. Payment gateway hay embed iframe.",
            ),
            q(
                "Alert không phải HTML alert — xử lý bằng gì?",
                [
                    "driver.switchTo().alert() — accept/dismiss/sendKeys",
                    "findElement By.id alert",
                    "JavascriptExecutor chỉ",
                    "Không automate được",
                ],
                0,
                "Native browser dialog. Khác modal Bootstrap trong DOM (tìm button bình thường).",
            ),
            q(
                "Select class cho dropdown <select> khác click option thế nào?",
                [
                    "selectByVisibleText/Value/Index — API chuẩn HTML select; custom dropdown cần click UI",
                    "Luôn sendKeys Enter",
                    "Chỉ dùng Actions double-click",
                    "Không hỗ trợ multi-select",
                ],
                0,
                "Custom React select: không dùng org.openqa.selenium.support.ui.Select — click chain.",
            ),
            q(
                "Actions class moveToElement dùng khi nào?",
                [
                    "Hover menu, drag-drop, chord phức tạp — low-level pointer events",
                    "Thay thế get(url)",
                    "Đọc cookie",
                    "Set implicit wait",
                ],
                0,
                "moveToElement(el).click().perform(). Headless có thể khác layout — test hover cẩn thận.",
            ),
            q(
                "JavascriptExecutor executeScript click argument khi nào cần?",
                [
                    "Element bị che (overlay), visibility trick — last resort sau khi wait clickable thật",
                    "Luôn dùng thay click()",
                    "Mở browser mới",
                    "Sửa locator",
                ],
                0,
                "arguments[0].click() với element. Anti-pattern lạm dụng che bug UX thật.",
            ),
            q(
                "Headless Chrome trên CI lưu ý gì?",
                [
                    "Có thể khác viewport/rendering — set window size; một số bug chỉ hiện headed",
                    "Không cần ChromeDriver",
                    "Không chạy được Linux",
                    "Luôn nhanh hơn 10x không điều kiện",
                ],
                0,
                "--headless=new, --window-size=1920,1080. Screenshot on failure vẫn cần.",
            ),
            q(
                "driver.manage().window().maximize() quan trọng vì sao?",
                [
                    "Element responsive ẩn ở viewport nhỏ — test flake khi không maximize",
                    "Bắt buộc pháp luật Selenium",
                    "Tăng timeout mặc định",
                    "Chỉ cho Firefox",
                ],
                0,
                "Hoặc setSize cố định consistent với CI. Hamburger menu mobile breakpoint.",
            ),
            q(
                "Page Load Strategy eager vs normal?",
                [
                    "eager: DOMContentLoaded, không chờ hết resource; normal: full load — chọn theo app SPA",
                    "Không ảnh hưởng get()",
                    "Chỉ cho API test",
                    "eager chờ 60s images",
                ],
                0,
                "SPA AJAX: normal timeout dài. eager nhanh hơn nếu app sẵn sàng sớm — đo thực tế.",
            ),
            q(
                "findElements (số nhiều) trả về gì khi không có match?",
                [
                    "List rỗng — không throw; findElement throw NoSuchElementException",
                    "null",
                    "Exception luôn",
                    "Optional.empty",
                ],
                0,
                "Kiểm tra isEmpty() trước assert count. Dynamic list table rows.",
            ),
            q(
                "Cookie và localStorage trong Selenium?",
                [
                    "driver.manage().getCookies(); localStorage qua executeScript — bypass login state setup",
                    "Không đọc được",
                    "Chỉ manual browser",
                    "Tự sync cross-browser",
                ],
                0,
                "Pre-seed auth token speed up test. Security: không commit cookie prod vào repo.",
            ),
            q(
                "Screenshot khi failure best practice?",
                [
                    "TakesScreenshot OutputType.FILE trong @AfterMethod nếu test fail — attach report",
                    "Screenshot mỗi step luôn",
                    "Chỉ manual xem",
                    "Không cần vì log đủ",
                ],
                0,
                "TestNG listener ITestListener.onTestFailure. Allure attachment.",
            ),
            q(
                "ChromeDriverManager (Bonigarcia) giải quyết gì?",
                [
                    "Tự tải driver binary khớp browser version — giảm 'session not created' mismatch",
                    "Thay thế Selenium API",
                    "Chỉ chạy trên Windows",
                    "Bỏ qua cần browser cài",
                ],
                0,
                "WebDriverManager.chromedriver().setup(). Vẫn cần Chrome/Chromium cài trên agent.",
            ),
            q(
                "Multiple window handle switch flow?",
                [
                    "getWindowHandles → switchTo window handle mới — đóng rồi switch back parent",
                    "Mở tab không cần switch",
                    "Chỉ một handle mọi lúc",
                    "driver.close() đóng tất cả",
                ],
                0,
                "OAuth popup, export PDF tab. Lưu parentHandle trước click mở window.",
            ),
            q(
                "DesiredCapabilities deprecated — Selenium 4 dùng gì?",
                [
                    "Options class: ChromeOptions, FirefoxOptions — merge capabilities qua builder",
                    "Không config được",
                    "Chỉ IE",
                    "File properties duy nhất",
                ],
                0,
                "options.addArguments('--disable-gpu'). Capabilities vẫn underlying nhưng API Options ưu tiên.",
            ),
            q(
                "driver.quit() vs driver.close() trong teardown?",
                [
                    "quit() đóng mọi window và end session; close() chỉ tab hiện tại — suite dùng quit",
                    "Giống nhau",
                    "close() kill process driver",
                    "quit() chỉ minimize",
                ],
                0,
                "@AfterSuite quit tránh zombie chromedriver trên CI. close() trong flow đóng popup.",
            ),
        ],
    }


def _phase3() -> dict:
    return {
        "title": "TestNG & POM",
        "questions": [
            q(
                "@Test trong TestNG khác @Test JUnit ở feature hay dùng automation?",
                [
                    "TestNG: dependsOnMethods, groups, priority, dataProvider mạnh — phổ biến Selenium stack",
                    "Giống hệt không khác",
                    "JUnit không có parameterized",
                    "TestNG không có BeforeMethod",
                ],
                0,
                "Maven surefire chọn provider. Project course dùng TestNG + RestAssured.",
            ),
            q(
                "@BeforeClass vs @BeforeMethod lifecycle?",
                [
                    "BeforeClass một lần/class (mở DB connection); BeforeMethod mỗi test (reset state, fresh driver)",
                    "BeforeMethod một lần suite",
                    "BeforeClass mỗi test",
                    "Không thứ tự đảm bảo",
                ],
                0,
                "Parallel methods: BeforeMethod thread-safe. Expensive setup → BeforeClass + careful shared state.",
            ),
            q(
                "dependsOnMethods = {\"login\"} ý nghĩa?",
                [
                    "Test chỉ chạy nếu login pass — order phụ thuộc (dùng cẩn thận, dễ brittle)",
                    "Chạy song song bắt buộc",
                    "Bỏ qua assertion",
                    "Thay DataProvider",
                ],
                0,
                "Ưu tiên independent test + setup method. dependsOn khó debug khi login flake.",
            ),
            q(
                "TestNG groups smoke, regression dùng trên CI thế nào?",
                [
                    "mvn test -Dgroups=smoke — chạy subset nhanh trên PR; full regression nightly",
                    "Không filter được",
                    "Chỉ trong IDE",
                    "Groups thay thế priority",
                ],
                0,
                "testng.xml <groups><run><include name='smoke'/>. Matrix job parallel group.",
            ),
            q(
                "@DataProvider(name='users') trả về Object[][] — test nhận tham số thế nào?",
                [
                    "@Test(dataProvider='users') — mỗi row chạy một invocation test riêng",
                    "Chỉ một lần row đầu",
                    "DataProvider chỉ String",
                    "Không report từng row",
                ],
                0,
                "Parallel dataProvider thread count. Excel/CSV đọc vào Object[][] trong provider method.",
            ),
            q(
                "SoftAssert (TestNG) khác hard assert?",
                [
                    "Thu thập lỗi, assertAll() cuối — một test kiểm nhiều field form",
                    "Không fail test",
                    "Chỉ cho unit test",
                    "Tự retry",
                ],
                0,
                "Validation trang profile: soft assert email, phone, name — một report đủ failure.",
            ),
            q(
                "testng.xml suite file điều khiển gì?",
                [
                    "Chọn class, groups, parallel mode, thread count, listeners — CI không cần click IDE",
                    "Chỉ format HTML report",
                    "Thay pom.xml",
                    "Compile Java",
                ],
                0,
                "<suite parallel='tests' thread-count='4'>. Cross-browser suite định nghĩa tập.",
            ),
            q(
                "ITestListener onTestFailure dùng để?",
                [
                    "Hook screenshot, log URL, custom report khi fail — không sửa mọi test class",
                    "Thay @Test",
                    "Chỉ chạy BeforeSuite",
                    "Tăng timeout",
                ],
                0,
                "Listener @Listeners hoặc testng.xml. Allure TestNG listener tương tự.",
            ),
            q(
                "Page Object Model (POM) mục tiêu chính?",
                [
                    "Tách locator + hành vi trang khỏi test — một nơi sửa khi UI đổi",
                    "Một class chứa 500 test method",
                    "Thay thế assertion",
                    "Chỉ cho API",
                ],
                0,
                "LoginPage.login(user, pass) — test đọc như scenario. Giảm duplicate findElement.",
            ),
            q(
                "Page Factory @FindBy lazy init khác khởi tạo By trong constructor?",
                [
                    "FindBy proxy element — init khi dùng; cần PageFactory.initElements(driver, this)",
                    "FindBy không cần driver",
                    "Luôn nhanh hơn không POM",
                    "Không hỗ trợ List",
                ],
                0,
                "Một số team prefer explicit By field + constructor injection driver — rõ ràng hơn magic.",
            ),
            q(
                "BasePage pattern thường chứa gì?",
                [
                    "Driver, wait helper, clickSafe, load wait — các page extend/share",
                    "Mọi test assertion",
                    "pom.xml dependencies",
                    "Test data CSV",
                ],
                0,
                "protected WebDriver driver; protected WebDriverWait wait. DRY explicit wait.",
            ),
            q(
                "Test không nên assert chi tiết UI trong test class mà nên ở đâu?",
                [
                    "Page method return state hoặc assert trong page method có tên nghiệp vụ (isDashboardDisplayed)",
                    "XPath trong @Test",
                    "main method",
                    "pom.xml",
                ],
                0,
                "Test: loginPage.login(); assert dashboard visible. Locator ẩn trong page.",
            ),
            q(
                "@Parameters từ testng.xml đọc browser param — ví dụ?",
                [
                    "<parameter name='browser' value='firefox'/> — @Parameters({'browser'}) void setup(String b)",
                    "Chỉ System.getenv",
                    "Không type safe",
                    "Thay DataProvider luôn tốt hơn",
                ],
                0,
                "Factory @Parameters browser hoặc @Optional('chrome') default. Cross-browser matrix.",
            ),
            q(
                "RetryAnalyzer trong TestNG dùng khi nào hợp lý?",
                [
                    "Flake known infrastructure — giới hạn retry (1-2), log quarantine; không che bug thật",
                    "Retry vô hạn",
                    "Mọi test fail",
                    "Thay fix locator",
                ],
                0,
                "ITestAnalyzer retry. CI policy: flake rate metric, không retry mù.",
            ),
            q(
                "Assert.assertEquals(actual, expected, message) message giúp gì?",
                [
                    "Log/report rõ context khi fail — 'Order total after discount'",
                    "Tăng timeout",
                    "Skip test",
                    "Chỉ hiện IDE",
                ],
                0,
                "Message mô tả business. Hamcrest assertThat readable hơn một số team.",
            ),
            q(
                "InvocationCount = 3 trên @Test nghĩa là gì?",
                [
                    "Chạy cùng test method 3 lần — stress nhỏ hoặc flake detection (hiếm production)",
                    "3 thread parallel",
                    "3 browser",
                    "3 DataProvider row",
                ],
                0,
                "Khác invocation per data row. Dùng có chủ đích, tránh suite phình.",
            ),
            q(
                "timeOut = 5000 trên @Test fail khi nào?",
                [
                    "Method chạy quá 5s — kill test (vòng lặp vô hạn, wait sai)",
                    "Chờ element 5s",
                    "CI cancel job",
                    "Network timeout HTTP",
                ],
                0,
                "Khác implicit wait. Bảo vệ suite không treo cả giờ một test.",
            ),
            q(
                "Page object không nên chứa gì?",
                [
                    "Assertion framework logic lẫn test data business scenario khác trang — tránh God class",
                    "Locator private",
                    "Method navigate",
                    "Constructor nhận driver",
                ],
                0,
                "CheckoutPage không assert LoginPage element. Composition nhiều page trong flow test.",
            ),
            q(
                "LoadableComponent isLoaded() pattern trong POM?",
                [
                    "Trang định nghĩa điều kiện loaded — get() wait đến ready trước interact",
                    "Thay WebDriver",
                    "Chỉ RestAssured",
                    "Không cần wait",
                ],
                0,
                "Template: load() → isLoaded() check key element. Giảm flake ngay sau navigation.",
            ),
            q(
                "Maven Surefire + TestNG chạy test: cấu hình thường ở đâu?",
                [
                    "pom.xml surefire plugin suiteXmlFiles hoặc includes **/*Test.java",
                    "Chỉ build.gradle",
                    "web.xml",
                    "testng.xml tự chạy không cần Maven",
                ],
                0,
                "mvn clean test -Dsuite=smoke.xml. CI gọi Maven, không IDE runner.",
            ),
        ],
    }


def _phase4() -> dict:
    return {
        "title": "Advanced & CI/CD",
        "questions": [
            q(
                "Selenium Grid 4 architecture thành phần chính?",
                [
                    "Router → Distributor → Node (browser slots) — scale parallel cross-machine",
                    "Chỉ một chromedriver local",
                    "Thay thế TestNG",
                    "Chỉ chạy API",
                ],
                0,
                "RemoteWebDriver hub URL. Docker Selenium chrome standalone cho CI.",
            ),
            q(
                "Docker container cho Selenium test lợi ích CI?",
                [
                    "Môi trường reproducible, isolate browser version, scale agent",
                    "Không cần chromedriver",
                    "Thay assertion",
                    "Chỉ Windows host",
                ],
                0,
                "selenium/standalone-chrome image. Mount test jar hoặc pipeline artifact.",
            ),
            q(
                "Jenkins pipeline stage 'test' thường làm gì?",
                [
                    "Checkout → build → mvn test → publish JUnit/Allure report — fail stage fail pipeline",
                    "Chỉ send email",
                    "Deploy production trước test",
                    "Không artifact",
                ],
                0,
                "Declarative pipeline post always archive screenshot. Quality gate merge PR.",
            ),
            q(
                "Parallel test execution risk chính?",
                [
                    "Shared data collision, static driver, file lock — cần thread-local driver và data isolation",
                    "Luôn an toàn",
                    "Chỉ chậm hơn",
                    "Không chạy được TestNG",
                ],
                0,
                "ThreadLocal<WebDriver>. Unique user per thread. Avoid static mutable counters.",
            ),
            q(
                "Allure report khác surefire HTML?",
                [
                    "Timeline, severity, attachment screenshot/log, history trend — stakeholder friendly",
                    "Không attach file",
                    "Chỉ console",
                    "Thay TestNG",
                ],
                0,
                "allure-maven plugin. @Step annotation trong page method.",
            ),
            q(
                "GitHub Actions workflow trigger on pull_request dùng để?",
                [
                    "Chạy CI mỗi PR — feedback trước merge",
                    "Chỉ deploy",
                    "Chỉ schedule nightly",
                    "Không cache dependency",
                ],
                0,
                "jobs: test runs-on ubuntu-latest, services postgres optional.",
            ),
            q(
                "Environment variable trên CI cho base URL?",
                [
                    "BASE_URL staging vs prod — test đọc System.getenv không hardcode",
                    "Phải sửa code mỗi môi trường",
                    "Chỉ testng.xml",
                    "Không đổi được",
                ],
                0,
                "@BeforeSuite đọc env. Jenkins credentials cho secret.",
            ),
            q(
                "Artifact lưu screenshot/video khi fail — retention policy?",
                [
                    "Giữ 7–30 ngày debug — không lưu vô hạn (storage cost)",
                    "Không cần artifact",
                    "Commit screenshot vào git",
                    "Chỉ local IDE",
                ],
                0,
                "Jenkins archiveArtifacts, GitHub Actions upload-artifact.",
            ),
            q(
                "Flaky test quarantine strategy trên CI?",
                [
                    "Tách group quarantine, không block merge nhưng ticket bắt buộc fix SLA — không im lặng disable",
                    "Xóa vĩnh viễn",
                    "Retry 100 lần",
                    "Ignore mọi fail",
                ],
                0,
                "Track flake rate dashboard. Root cause: wait, data, env.",
            ),
            q(
                "Blue-green deploy và automation smoke?",
                [
                    "Smoke trên green trước switch traffic — automation gate go-live",
                    "Không test staging",
                    "Chỉ manual sau switch",
                    "Smoke sau khi user báo lỗi",
                ],
                0,
                "API health + critical UI path 5 phút trước cutover.",
            ),
            q(
                "Infrastructure as Code (Terraform) liên quan QA CI?",
                [
                    "Spin ephemeral env giống prod cho test — reproducible stack",
                    "Thay Selenium",
                    "Chỉ devops không QA",
                    "Không dùng Jenkins",
                ],
                0,
                "QA request staging namespace per PR preview environment.",
            ),
            q(
                "Visual regression (Percy, Applitools) bổ sung Selenium thế nào?",
                [
                    "So sánh screenshot baseline — bắt CSS/layout break functional assert miss",
                    "Thay locator",
                    "Không cần WebDriver",
                    "Chỉ unit test",
                ],
                0,
                "Ignore dynamic banner region. Review diff human approve baseline update.",
            ),
            q(
                "API mock (WireMock) trong CI khi UI phụ thuộc backend unstable?",
                [
                    "Stub response predictable — UI test không block team backend chậm",
                    "Thay hết integration test",
                    "Chỉ production",
                    "Không dùng được Docker",
                ],
                0,
                "Contract + UI against mock; periodic test against real integration env.",
            ),
            q(
                "Maven profile dev vs ci trong pom?",
                [
                    "Profile ci: headless, parallel, skip slow tests — mvn test -Pci",
                    "Profile thay Java version",
                    "Không thể skip test",
                    "Chỉ IDE",
                ],
                0,
                "<profiles><profile><id>ci</id> properties skipTests false groups smoke</profile>",
            ),
            q(
                "Secrets trong CI (password, API key) best practice?",
                [
                    "Credentials binding Jenkins/GitHub Secrets — không plaintext trong repo",
                    "Commit .env prod",
                    "Log password debug",
                    "Hardcode test class",
                ],
                0,
                "Mask console log. Rotate key. Test account riêng staging.",
            ),
            q(
                "Test coverage Jacoco có nghĩa thay QA automation UI?",
                [
                    "Không — code coverage đo dev unit test; UI automation đo user journey khác layer",
                    "100% Jacoco thay Selenium",
                    "Jacoco chỉ manual",
                    "Không liên quan Java",
                ],
                0,
                "Cả hai metric bổ sung. Coverage cao vẫn có thể miss integration bug.",
            ),
            q(
                "Scheduled cron nightly regression lợi ích?",
                [
                    "Bắt flake/env drift khi PR ít — full suite dài không chặn dev ban ngày",
                    "Thay smoke PR",
                    "Chỉ chạy một lần",
                    "Không report",
                ],
                0,
                "Jenkins cron H 2 * * *. Alert Slack on failure.",
            ),
            q(
                "Container resource limit OOMKilled khi parallel Chrome?",
                [
                    "Giảm thread-count hoặc tăng memory limit node — mỗi Chrome ~200-500MB+",
                    "Thêm assert",
                    "Đổi TestNG sang JUnit",
                    "Không liên quan RAM",
                ],
                0,
                "Monitor CI agent. Sharding suite across nodes.",
            ),
            q(
                "Shift-right (production monitoring) bổ sung CI automation?",
                [
                    "Synthetic check prod, real user monitoring — phát hiện sau deploy",
                    "Thay hết test pre-merge",
                    "Chỉ log4j",
                    "Không cần alert",
                ],
                0,
                "Datadog synthetics ping checkout. Canary release + metric gate.",
            ),
            q(
                "Definition pipeline 'quality gate' SonarQube block merge khi?",
                [
                    "Coverage/threshold, blocker bug, security hotspot vượt ngưỡng policy",
                    "Mọi warning style",
                    "Không có API",
                    "Chỉ đếm dòng code",
                ],
                0,
                "Sonar quality gate kết hợp automated test pass — không thay functional scenario.",
            ),
        ],
    }


def _api1() -> dict:
    return {
        "title": "Fundamentals & HTTP",
        "questions": [
            q(
                "REST architectural constraint nào nhấn mạnh stateless server?",
                [
                    "Mỗi request chứa đủ context — server không lưu session client giữa request (auth qua token/header)",
                    "Server phải lưu session file",
                    "Chỉ dùng TCP socket",
                    "Bắt buộc SOAP XML",
                ],
                0,
                "Stateless scale horizontal. Session state → client cookie/JWT hoặc server DB với token id.",
            ),
            q(
                "HTTP GET idempotent và safe nghĩa là gì?",
                [
                    "Safe: không đổi resource; idempotent: gọi nhiều lần như một — GET đọc dữ liệu",
                    "GET luôn tạo record mới",
                    "GET gửi body bắt buộc",
                    "GET không cache được",
                ],
                0,
                "Test GET assert 200 và body. Không dùng GET xóa/tạo side effect (anti-pattern).",
            ),
            q(
                "POST vs PUT trong thiết kế API test?",
                [
                    "POST thường tạo resource (server chọn id); PUT thường replace theo URI xác định — idempotent PUT",
                    "Giống nhau",
                    "POST idempotent mặc định",
                    "PUT chỉ cho file upload",
                ],
                0,
                "POST /users → 201 Location. PUT /users/1 update toàn bộ. PATCH partial.",
            ),
            q(
                "HTTP status 201 vs 200 khi automate assertion?",
                [
                    "201 Created — resource mới (kèm Location header); 200 OK — thành công chung đọc/update",
                    "201 chỉ lỗi",
                    "200 luôn là create",
                    "Không assert status",
                ],
                0,
                "rest-assured statusCode(201). body path id không null.",
            ),
            q(
                "404 vs 400 trong debugging API fail?",
                [
                    "404 resource không tồn tại URL/id; 400 request syntax/validation sai — đọc body error message",
                    "404 luôn auth",
                    "400 server crash",
                    "Giống nhau",
                ],
                0,
                "Test negative: invalid id → 404. Missing field → 400 problem+json.",
            ),
            q(
                "Header Content-Type application/json ý nghĩa?",
                [
                    "Body gửi/nhận là JSON — server parse đúng format",
                    "Chỉ cho GET",
                    "Thay Authorization",
                    "Bắt buộc multipart",
                ],
                0,
                "Accept: application/json yêu cầu response JSON. form-urlencoded khác schema.",
            ),
            q(
                "Query parameter vs path parameter ví dụ /users/1?active=true?",
                [
                    "Path /users/1 định danh resource; query ?active=true filter/option",
                    "Query bắt buộc trong mọi REST",
                    "Path chỉ cho POST",
                    "Không test được",
                ],
                0,
                "Automation: given().pathParam('id',1).queryParam('active',true).",
            ),
            q(
                "HTTP header Authorization: Bearer <token> dùng khi nào?",
                [
                    "OAuth2/JWT access token — stateless auth sau login",
                    "Chỉ Basic auth",
                    "Thay Content-Type",
                    "Chỉ SOAP",
                ],
                0,
                "given().header('Authorization', 'Bearer ' + token). Refresh token flow test riêng.",
            ),
            q(
                "Idempotent DELETE /users/1 gọi 2 lần kết quả mong đợi?",
                [
                    "Lần 1: 204/200 xóa; lần 2 thường 404 — resource đã mất, không duplicate delete side effect",
                    "Tạo 2 user",
                    "500 luôn",
                    "201 Created",
                ],
                0,
                "Assert lần hai 404 hoặc 204 tùy API contract document.",
            ),
            q(
                "HTTPS so HTTP trong test environment?",
                [
                    "TLS mã hóa — CI trust store, certificate pinning, ignore cert chỉ dev có kiểm soát",
                    "Giống port 80",
                    "Không test được Postman",
                    "HTTP đủ production",
                ],
                0,
                "rest-assured relaxedHTTPSValidation() chỉ test lab. Prod validate cert.",
            ),
            q(
                "JSON object vs array trong assert response?",
                [
                    "Object {} key-value; array [] list — jsonPath size(), [0].id",
                    "Không phân biệt",
                    "Chỉ XML",
                    "Array không có index",
                ],
                0,
                "body('items.size()', greaterThan(0)). Hamcrest matchers.",
            ),
            q(
                "HTTP 401 vs 403 authentication vs authorization?",
                [
                    "401 chưa auth / sai credential; 403 đã auth nhưng không đủ quyền",
                    "403 luôn là network",
                    "401 not found",
                    "Giống nhau",
                ],
                0,
                "Test role user vs admin: cùng endpoint khác permission → 403.",
            ),
            q(
                "Rate limiting 429 Too Many Requests — test strategy?",
                [
                    "Assert header Retry-After; không hammer prod — dùng mock hoặc limit cao staging",
                    "Ignore",
                    "Fail suite",
                    "Chỉ manual",
                ],
                0,
                "Load test environment riêng. Contract document rate policy.",
            ),
            q(
                "Header Accept-Language vi-VN dùng để test gì?",
                [
                    "Localization response message/format — i18n API",
                    "Encryption",
                    "CORS",
                    "Cache only",
                ],
                0,
                "Assert error message tiếng Việt khi product yêu cầu.",
            ),
            q(
                "CORS preflight OPTIONS request là gì?",
                [
                    "Browser gửi OPTIONS trước cross-origin POST có custom header — server trả Access-Control-*",
                    "Thay GET",
                    "Chỉ Selenium",
                    "Unit test JVM",
                ],
                0,
                "API test RestAssured không qua browser CORS như frontend — E2E UI mới gặp CORS thật.",
            ),
            q(
                "OpenAPI (Swagger) spec giúp QA automation?",
                [
                    "Contract document path, schema, example — sinh test case và validation",
                    "Thay assertion",
                    "Chỉ cho manual",
                    "Không có schema",
                ],
                0,
                "Schema validation rest-assured against openapi.json. Contract drift fail CI.",
            ),
            q(
                "Multipart form-data upload file field HTTP?",
                [
                    "Content-Type multipart/form-data; boundary — POST file avatar",
                    "application/json chứa binary",
                    "GET upload",
                    "Chỉ FTP",
                ],
                0,
                "given().multiPart('file', file). Khác raw JSON base64 tùy API.",
            ),
            q(
                "HTTP caching header ETag dùng test optimistic locking?",
                [
                    "If-Match ETag khi PUT — 412 Precondition Failed nếu resource đổi",
                    "Chỉ CSS cache",
                    "Thay JWT",
                    "Không liên quan API",
                ],
                0,
                "Concurrency scenario: hai client update cùng resource.",
            ),
            q(
                "HATEOAS trong REST response ví dụ?",
                [
                    "Link rel next/prev trong body — client discover action động",
                    "Bắt buộc mọi API",
                    "Chỉ GraphQL",
                    "Thay status code",
                ],
                0,
                "Assert _links.self.href tồn tại. Ít API pure HATEOAS nhưng hay hỏi concept.",
            ),
            q(
                "GraphQL khác REST một endpoint nhiều resource — test implication?",
                [
                    "POST một URL query/mutation — assert partial data shape; over-fetch under-fetch khác REST nhiều call",
                    "Giống GET /users",
                    "Không assert được",
                    "Chỉ manual",
                ],
                0,
                "RestAssured có thể POST GraphQL body { query: '{ user(id:1){ name } }' }.",
            ),
        ],
    }


def _api2() -> dict:
    return {
        "title": "Auth & Security",
        "questions": [
            q(
                "Basic Authentication encode credential thế nào trên wire?",
                [
                    "Base64(username:password) trong header Authorization: Basic — không mã hóa, cần HTTPS",
                    "MD5 hash password",
                    "JWT trong cookie only",
                    "Không gửi header",
                ],
                0,
                "given().auth().basic(user, pass). Dễ sniff nếu HTTP plaintext — chỉ lab hoặc TLS.",
            ),
            q(
                "JWT gồm ba phần nào?",
                [
                    "Header.Payload.Signature — base64url; signature verify integrity với secret/public key",
                    "Chỉ payload JSON",
                    "Session id database",
                    "XML token",
                ],
                0,
                "Decode payload assert exp, sub, role. Không tin client decode không verify signature.",
            ),
            q(
                "OAuth2 Authorization Code flow bước chính cho web app?",
                [
                    "Redirect login → authorization code → exchange access token server-side — refresh token optional",
                    "Client secret trong mobile app plaintext",
                    "Chỉ password grant production",
                    "Không cần redirect URI",
                ],
                0,
                "Test: mock IdP hoặc staging Keycloak. Không embed client secret frontend.",
            ),
            q(
                "API key trong header X-API-Key vs query string risk?",
                [
                    "Header an toàn hơn — query log trong server/proxy history, browser referrer leak",
                    "Query luôn encrypt",
                    "Header không dùng được",
                    "Giống nhau",
                ],
                0,
                "Rotate key. Scope permission read-only khi có thể.",
            ),
            q(
                "SQL injection test API field search q=' OR 1=1 -- mong đợi gì từ API secure?",
                [
                    "400/422 validation hoặc sanitized — không lộ stack trace / không trả full DB",
                    "200 với mọi record",
                    "500 với SQL syntax trong body",
                    "Không test được API",
                ],
                0,
                "Parameterized query phía server. Fuzz negative security suite.",
            ),
            q(
                "OWASP API Security Top 10 Broken Object Level Authorization (BOLA) ví dụ?",
                [
                    "User A đổi id URL /orders/99 của user B — phải 403",
                    "Chỉ XSS",
                    "Chỉ DDoS",
                    "Chỉ log4j",
                ],
                0,
                "Automate: token user A access resource B id → assert forbidden.",
            ),
            q(
                "HTTPS TLS certificate expired test kỳ vọng client?",
                [
                    "Handshake fail — RestAssured exception; monitor cert expiry alert",
                    "200 OK",
                    "401",
                    "Redirect HTTP",
                ],
                0,
                "Không relaxed validation prod. CI check cert trước deploy.",
            ),
            q(
                "refresh_token dùng để?",
                [
                    "Lấy access_token mới khi hết hạn mà không bắt user login lại — lưu trữ an toàn",
                    "Thay password hash DB",
                    "Public trong JS",
                    "Không expire",
                ],
                0,
                "Test expire access: call refresh endpoint → new token works.",
            ),
            q(
                "Scope OAuth 'read:orders' ý nghĩa?",
                [
                    "Giới hạn quyền token — chỉ action trong scope",
                    "Chỉ UI label",
                    "Encryption algorithm",
                    "Content-Type",
                ],
                0,
                "Token scope read only → POST create order 403.",
            ),
            q(
                "CSRF primarily concern cho?",
                [
                    "Browser cookie session based — attacker site gửi request dùng cookie victim",
                    "RestAssured direct API không browser",
                    "Chỉ database",
                    "JWT header",
                ],
                0,
                "API JWT header ít CSRF hơn cookie session. UI form cần CSRF token.",
            ),
            q(
                "Sensitive data in API response test nên assert?",
                [
                    "Không trả password hash, full PAN card, internal id không cần — mask field",
                    "Trả đủ mọi field DB",
                    "200 là đủ",
                    "Chỉ check status",
                ],
                0,
                "Schema + negative: field password absent in GET user.",
            ),
            q(
                "Brute force login protection kỳ vọng?",
                [
                    "429 lockout / captcha sau N fail — test không lock staging shared account vĩnh viễn",
                    "200 forever",
                    "500",
                    "201",
                ],
                0,
                "Dedicated test user. Assert lockout policy documented.",
            ),
            q(
                "mTLS client certificate authentication scenario?",
                [
                    "Mutual TLS — client cert + server cert; common microservice internal",
                    "Chỉ Basic auth",
                    "Chỉ API key query",
                    "Không dùng HTTPS",
                ],
                0,
                "RestAssured certificate trust store config. Service mesh Istio.",
            ),
            q(
                "PII GDPR trong test data automation?",
                [
                    "Synthetic data, anonymize, không copy prod DB raw — env staging masked",
                    "Prod data luôn OK test",
                    "Commit CSV customer thật",
                    "Không liên quan QA",
                ],
                0,
                "Compliance audit. Delete test user after suite.",
            ),
            q(
                "Security header Strict-Transport-Security (HSTS)?",
                [
                    "Browser chỉ HTTPS — giảm downgrade attack",
                    "CORS allow *",
                    "JWT secret",
                    "SQL escape",
                ],
                0,
                "Assert header present response prod. API tool có thể bỏ qua browser enforce.",
            ),
            q(
                "Penetration test khác automated security scan?",
                [
                    "Human creative attack chain; scan (ZAP) pattern known — bổ sung nhau",
                    "Giống nhau",
                    "Scan thay pentest compliance",
                    "Chỉ manual QA functional",
                ],
                0,
                "CI OWASP ZAP baseline. Pentest annual release.",
            ),
            q(
                "Log redaction — token không xuất hiện log CI?",
                [
                    "Mask Authorization header trong report; fail nếu log full JWT",
                    "Log full cho debug luôn",
                    "Không cần",
                    "Chỉ dev local",
                ],
                0,
                "Allure filter attachment. Secret scanner git pre-commit.",
            ),
            q(
                "Role-based access control (RBAC) test matrix?",
                [
                    "Table role × endpoint × expected status — automate data-driven",
                    "Chỉ test admin",
                    "Một test đủ",
                    "Không cần negative",
                ],
                0,
                "DataProvider roles guest,user,admin.",
            ),
            q(
                "Insecure direct object reference (IDOR) fix phía server?",
                [
                    "Authorize mọi request — check ownership resource thuộc subject token",
                    "Security through obscurity UUID only",
                    "Hide button frontend",
                    "200 always",
                ],
                0,
                "UUID không thay authorize. Test đổi id sequential.",
            ),
            q(
                "Secret rotation automation test consideration?",
                [
                    "Dual key period — test cả old và new secret trong window",
                    "Stop all test",
                    "Hardcode forever",
                    "Chỉ rotate prod không báo",
                ],
                0,
                "Pipeline env inject VERSION_2_API_KEY. Coordinate devops.",
            ),
        ],
    }


def _api3() -> dict:
    return {
        "title": "RestAssured Automation",
        "questions": [
            q(
                "RestAssured Given-When-Then mapping?",
                [
                    "given() setup (headers, auth, body) — when() request — then() assert response",
                    "Chỉ when",
                    "then trước when",
                    "Không fluent",
                ],
                0,
                "BDD readable. given().header().body().when().get().then().statusCode().",
            ),
            q(
                "RestAssured.baseURI vs basePath?",
                [
                    "baseURI https://api.com + basePath /v1 + get /users → full URL",
                    "Giống nhau",
                    "Chỉ path",
                    "Thay port",
                ],
                0,
                "RestAssured.baseURI = ... trong @BeforeClass. Per-request path.",
            ),
            q(
                "JsonPath body('data[0].name') dùng khi nào?",
                [
                    "Extract nested field assert — hoặc lưu biến cho request sau",
                    "Chỉ XML",
                    "Thay status code",
                    "Không hỗ trợ array",
                ],
                0,
                "String name = response.path('data[0].name'). Hamcrest body matcher.",
            ),
            q(
                "given().contentType(JSON) với object POJO?",
                [
                    "Serialize POJO Jackson — server nhận JSON",
                    "Chỉ form",
                    "Chỉ XML",
                    "Không cần mapper",
                ],
                0,
                "ObjectMapper config date format. @JsonProperty field name.",
            ),
            q(
                "Response time assertion rest-assured?",
                [
                    "then().time(lessThan(2000L)) — SLA API performance smoke",
                    "Không đo được",
                    "Chỉ JMeter",
                    "Chỉ manual stopwatch",
                ],
                0,
                "Không thay load test. Catch regression slow query.",
            ),
            q(
                "Schema validation json-schema trong RestAssured?",
                [
                    "matchesJsonSchemaInClasspath('user-schema.json') — contract response structure",
                    "Chỉ status 200",
                    "Chỉ string contains",
                    "Không cần OpenAPI",
                ],
                0,
                "Fail khi API thêm field required missing hoặc type đổi.",
            ),
            q(
                "RequestSpec reuse Builder pattern?",
                [
                    "given().spec(commonSpec) — DRY auth header base URI",
                    "Copy paste mỗi test",
                    "Chỉ UI POM",
                    "Không support",
                ],
                0,
                "RequestSpecBuilder addHeader Authorization. ResponseSpec common expect.",
            ),
            q(
                "Logging RestAssured log().all() khi debug?",
                [
                    "In request/response full — tắt CI hoặc on failure only (log if validation fails)",
                    "Luôn bật prod",
                    "Không log được",
                    "Chỉ error",
                ],
                0,
                "RestAssured.filters. Sensitive data mask.",
            ),
            q(
                "Extract response cookie cho session flow?",
                [
                    "Response.getDetailedCookie('JSESSIONID') — given().cookie() request tiếp",
                    "Không dùng cookie API",
                    "Chỉ Selenium",
                    "Chỉ JWT",
                ],
                0,
                "Session-based API chain login → action. Prefer token stateless khi có.",
            ),
            q(
                "RestAssured + TestNG @Test integration?",
                [
                    "Mỗi @Test method gọi given-when-then — suite Maven surefire",
                    "Chỉ main()",
                    "Chỉ JUnit 5",
                    "Không parallel",
                ],
                0,
                "BaseAPITest @BeforeClass setup baseURI. Groups smoke regression.",
            ),
            q(
                "Hamcrest hasItems matcher array response?",
                [
                    "body('tags', hasItems('a','b')) — JSON array contains",
                    "Chỉ equalTo",
                    "Chỉ notNull",
                    "Không array",
                ],
                0,
                "contains, hasSize, everyItem matchers expressive assert.",
            ),
            q(
                "File upload RestAssured multiPart?",
                [
                    "given().multiPart('file', new File('a.pdf')) — POST multipart",
                    "body raw JSON file",
                    "GET only",
                    "Không test upload",
                ],
                0,
                "Content-Type boundary auto. Assert 201 storage url response.",
            ),
            q(
                "OAuth2 rest-assured built-in?",
                [
                    "given().auth().oauth2(token) — hoặc oauth2 service get token setup",
                    "Không hỗ trợ",
                    "Chỉ Basic",
                    "Chỉ manual header",
                ],
                0,
                "AuthScheme config. Pre-request token endpoint RestAssured OAuth2.",
            ),
            q(
                "relaxedHTTPSValidation() cảnh báo?",
                [
                    "Bỏ qua cert check — CHỈ test/dev; production dùng trust store đúng",
                    "Bắt buộc mọi env",
                    "Tăng security",
                    "Thay TLS 1.3",
                ],
                0,
                "Man-in-the-middle risk nếu lạm dụng prod.",
            ),
            q(
                "API Object Model (giống POM) cho RestAssured?",
                [
                    "Class UsersApi.getUser(id) wrap endpoint — test gọi API layer không raw path",
                    "Không cần abstraction",
                    "Chỉ Page Object UI",
                    "Chỉ record",
                ],
                0,
                "UsersApi + UserTests separation. Maintain path một chỗ.",
            ),
            q(
                "Data-driven RestAssured TestNG DataProvider CSV?",
                [
                    "Đọc row CSV → Object[][] — mỗi row một POST case",
                    "Chỉ một data hardcode",
                    "Không kết hợp được",
                    "Chỉ Excel manual",
                ],
                0,
                "@DataProvider đọc resources/testdata/login.csv.",
            ),
            q(
                "Chaining call: create user → get id → delete cleanup?",
                [
                    "Extract id path → given().delete('/users/'+id) trong @AfterMethod",
                    "Không cleanup",
                    "Để rác staging",
                    "Chỉ @BeforeSuite",
                ],
                0,
                "Test isolation. Teardown dù fail vẫn chạy @AfterMethod.",
            ),
            q(
                "Soft assertion RestAssured?",
                [
                    "Collect multiple then() hoặc dùng ValidatableResponse — TestNG SoftAssert field",
                    "Chỉ một assert",
                    "Không fail",
                    "Chỉ UI",
                ],
                0,
                "Validate nhiều field response một lần report đủ.",
            ),
            q(
                "RestAssured filter RequestLoggingFilter CI?",
                [
                    "Custom Filter log on fail attach Allure — balance noise vs debug",
                    "Log all pass",
                    "Không filter",
                    "Thay TestNG",
                ],
                0,
                "FilterBuilder implement Filter interface.",
            ),
            q(
                "So sánh Postman collection vs RestAssured framework scale?",
                [
                    "RestAssured: version control, CI parallel, refactor OOP — Postman tốt explore/manual",
                    "Postman luôn scale hơn 1000 test",
                    "RestAssured không CI",
                    "Giống nhau hoàn toàn",
                ],
                0,
                "Course narrative: 500+ case → code framework. Newman CI middle ground.",
            ),
        ],
    }


def build_banks() -> dict:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _build_quiz_banks_content import BANKS as partial  # noqa: PLC0415

    banks = {
        "oop1": partial["oop1"],
        "java2": partial["java2"],
        "java34": _java34(),
        "video1": _video1(),
        "video2": _video2(),
        "phase2": _phase2(),
        "phase3": _phase3(),
        "phase4": _phase4(),
        "api1": _api1(),
        "api2": _api2(),
        "api3": _api3(),
    }
    expected = [
        "oop1",
        "java2",
        "java34",
        "video1",
        "video2",
        "phase2",
        "phase3",
        "phase4",
        "api1",
        "api2",
        "api3",
    ]
    if list(banks.keys()) != expected:
        raise ValueError(f"Key order mismatch: {list(banks.keys())}")
    for key, bank in banks.items():
        if len(bank["questions"]) != 20:
            raise ValueError(f"{key}: expected 20 questions, got {len(bank['questions'])}")
        for i, item in enumerate(bank["questions"]):
            if set(item.keys()) != {"q", "options", "answer", "explain"}:
                raise ValueError(f"{key} q{i}: bad keys {item.keys()}")
            if len(item["options"]) != 4:
                raise ValueError(f"{key} q{i}: need 4 options")
            if item["answer"] not in (0, 1, 2, 3):
                raise ValueError(f"{key} q{i}: answer must be 0-3")
    return banks


def emit() -> None:
    banks = build_banks()
    body = pprint.pformat(banks, width=100, sort_dicts=False)
    OUT.write_text(f"BANKS = {body}\n", encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    emit()
